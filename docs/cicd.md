# CI/CD del blog

## Modelo de ramas

| Rama | Qué dispara | Destino | URL |
| --- | --- | --- | --- |
| `main` | push o merge | `/home/gsalvini/public_html` en `ecim.tech:2222` | https://gustavosalvini.com.ar |
| `staging` | push | `/home/gsalvini/staging_html` en `ecim.tech:2222` | https://staging.gustavosalvini.com.ar (ver pendientes) |
| cualquier otra | nada | nada | — |

Un PR no despliega: solo corre CI. El merge a `main` es el único camino a producción.

`workflow_dispatch` permite disparar a mano desde la pestaña Actions, eligiendo `staging` o `production`.

## Workflows

- `.github/workflows/ci.yml` — en PR y en push a `main`/`staging`. Bloquea por `astro check` y `pnpm build`; lint y formato corren como informativos (hay deuda vieja, ver más abajo).
- `.github/workflows/deploy.yml` — buildea una vez, sube `dist` como artefacto, y lo despliega según la rama.
- `.github/scripts/deploy-sftp.sh` — el deploy en sí: preflight, backup, rsync con guardas y verificación.

## Cómo viaja el sitio

```
GitHub Actions (runner)
   └─ rsync por SSH :2222 (clave dedicada de CI)
        └─ ecim.tech
             ├─ /home/gsalvini/public_html   <- producción
             └─ /home/gsalvini/staging_html  <- staging
                   nginx (443, certbot) -> proxy_pass -> Apache :8080 (www-data)
```

Producción la sirve Apache detrás de nginx (`/etc/apache2/sites-enabled/gustavosalvini.com.ar.conf`, DocumentRoot `public_html`, Apache escuchando en `:8080`). nginx solo hace de front con el certificado.

## Secrets

Están por **environment**, no a nivel repo, así que revocar un ambiente no toca el otro:

| Secret | staging | production |
| --- | --- | --- |
| `SFTP_HOST` | `ecim.tech` | `ecim.tech` |
| `SFTP_PORT` | `2222` | `2222` |
| `SFTP_USER` | `gsalvini` | `gsalvini` |
| `SFTP_PATH` | `/home/gsalvini/staging_html` | `/home/gsalvini/public_html` |
| `SFTP_SSH_KEY` | clave `gsblog-ci-staging` | clave `gsblog-ci-prod` |
| `SSH_KNOWN_HOSTS` | host key de `[ecim.tech]:2222` | idem |

Las claves son ed25519 dedicadas al CI, sin passphrase, con `restrict` en el `authorized_keys` del server (sin pty, sin forwarding, sin X11). La host key está pineada: si el server cambia de clave, el deploy falla en vez de confiar en la nueva.

Para rotar una clave:

```bash
ssh-keygen -t ed25519 -N "" -C "gsblog-ci-staging@github-actions" -f ~/.ssh/id_ed25519_gsblog_ci_staging
# agregar la pública al authorized_keys del server con el prefijo restrict
gh secret set SFTP_SSH_KEY --env staging --repo guspatagonico/gustavosalvini-astro-blog < ~/.ssh/id_ed25519_gsblog_ci_staging
```

## Guardas del deploy

1. **Preflight**: el destino existe y es escribible; si no, corta antes de tocar nada.
2. **Backup**: en producción, tarball del docroot actual en `/home/gsalvini/backups/gustavosalvini.com.ar/`. Se conservan los últimos 5.
3. **Dry-run del `--delete`**: si rsync borraría rutas fuera de `_astro/`, `pagefind/`, `posts/`, `tags/`, `assets/` y `embeds/`, el deploy falla con la lista. Todo lo que vive en el server sin salir del build se declara en `.deployignore`.
4. **Verificación**: se compara el `sha256` de `index.html` local contra el remoto, y en producción además se pide la home por HTTPS y se chequea que sirva un asset `/_astro/...` del build nuevo.

## Rollback

Opción rápida (restaurar el deploy anterior en caliente):

```bash
ssh -p 2222 -i ~/.ssh/id_ed25519_gsblog_ci_prod gsalvini@ecim.tech \
  'ls -1t ~/backups/gustavosalvini.com.ar/ | head'
ssh -p 2222 -i ~/.ssh/id_ed25519_gsblog_ci_prod gsalvini@ecim.tech \
  'tar xzf ~/backups/gustavosalvini.com.ar/<tarball>.tar.gz -C ~/public_html'
```

Opción limpia (el historial queda coherente): `git revert` del commit roto, push a `main`, y el pipeline vuelve a desplegar.

## Pendiente para que staging tenga URL pública

`staging.gustavosalvini.com.ar` todavía no existe en DNS ni tiene vhost. Los archivos ya llegan al server; falta publicarlos. Son tres pasos, todos con root en el server (el deploy desde Actions no los necesita):

1. **DNS**: en el panel de DigitalOcean, registro `A` para `staging` apuntando a `143.198.173.62`.
2. **vhost de nginx**: copiar `docs/nginx/staging.gustavosalvini.com.ar.conf` a `/etc/nginx/sites-available/`, symlink en `sites-enabled`, `nginx -t && systemctl reload nginx`. Sirve estático directo, sin pasar por Apache, que para un sitio estático no aporta nada.
3. **Certificado**: `certbot --nginx -d staging.gustavosalvini.com.ar --redirect`.

El deploy de staging ya escribe un `robots.txt` con `Disallow: /` y el vhost agrega `X-Robots-Tag: noindex`, así que aunque quede indexable por error, no se indexa.

## Deuda conocida

- `pnpm lint` tiene 19 errores viejos (3 archivos): `src/components/CookieConsentConfig.ts`, `src/layouts/Layout.astro`, `tests-examples/demo-todo-app.spec.ts`. Por eso no bloquea el pipeline.
- `pnpm format:check` falla en 24 archivos de contenido viejos. Tampoco bloquea.
- La rama `github-pages` y su workflow quedaron obsoletos: el dominio hace años que no apunta a GitHub Pages. Cuando el deploy por SFTP esté probado, conviene archivarla.
- `posts/el-perceptron/` quedó en el server de una versión vieja del sitio (el slug actual es `posts/perceptron-es/`). El próximo deploy con `--delete` lo limpia. **Ya limpiado** en el primer deploy real (13/09/2026).

## Pitfalls ya pagados

- **No usar `-p` en rsync ni preservar tiempos de directorio.** El docroot de producción es de `www-data` y `gsalvini` solo escribe por grupo: `chmod` y `utimes` sobre archivos ajenos fallan con `Operation not permitted`, y rsync termina en exit 23 **con el contenido ya sincronizado**, que es la peor combinación porque el sitio queda actualizado y el job en rojo. Por eso el script usa `-rltzO` y los archivos nuevos heredan el umask 022 del runner.
- **Nunca comparar con `printf | grep -q`.** `grep -q` cierra el pipe antes de que el escritor termine, el escritor muere por SIGPIPE y con `pipefail` el pipeline queda en 141 aunque el contenido esté perfecto. Descargar a archivo y grepear el archivo.
- **No verificar contando archivos.** El server puede tener archivos legítimos que el build no conoce (los de `.deployignore`), así que el conteo da falso positivo. La verificación correcta es un dry-run posterior: si no queda nada pendiente, el server es idéntico al build.
- **La guarda del `--delete` salva de verdad.** Corre un dry-run antes del sync y aborta si el borrado tocaría rutas fuera de los prefijos que gestiona el build (`_astro/`, `pagefind/`, `posts/`, `tags/`, `assets/`, `embeds/`). Ya evitó borrar `embeds/images/iso-logotipo.png`, que está subido a mano y no existe en el repo.
- **El bucket de la guarda tiene un agujero conocido**: cualquier archivo ajeno dentro de esos prefijos se borra sin avisar. Si aparece algo importante, listarlo en `.deployignore`.

