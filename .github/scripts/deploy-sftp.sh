#!/usr/bin/env bash
#
# Deploy de un build estático a un destino SFTP, con preflight, backup,
# sincronización por rsync y verificación post-deploy.
#
# Uso: se ejecuta desde GitHub Actions con las variables en el entorno.
# Todas las variables sensibles llegan por secrets, nunca por argumentos.
#
set -euo pipefail

# Nunca activar xtrace: expondría la clave privada en los logs del runner.

: "${SFTP_HOST:?falta SFTP_HOST}"
: "${SFTP_PORT:?falta SFTP_PORT}"
: "${SFTP_USER:?falta SFTP_USER}"
: "${SFTP_PATH:?falta SFTP_PATH}"
: "${SFTP_SSH_KEY:?falta SFTP_SSH_KEY}"
: "${SSH_KNOWN_HOSTS:?falta SSH_KNOWN_HOSTS}"

DIST_DIR="${DIST_DIR:-dist}"
BACKUP_DIR="${BACKUP_DIR:-}"           # vacío = sin backup
BACKUP_KEEP="${BACKUP_KEEP:-5}"
SITE_URL="${SITE_URL:-}"               # vacío = sin verificación HTTP
NOINDEX="${NOINDEX:-0}"                # 1 = agrega robots.txt de bloqueo
LABEL="${LABEL:-deploy}"

KEY_FILE="$HOME/.ssh/deploy_key"
KNOWN_HOSTS_FILE="$HOME/.ssh/known_hosts"
TARGET="${SFTP_USER}@${SFTP_HOST}"

SSH_OPTS=(
  -i "$KEY_FILE"
  -p "$SFTP_PORT"
  -o IdentitiesOnly=yes
  -o UserKnownHostsFile="$KNOWN_HOSTS_FILE"
  -o StrictHostKeyChecking=yes
  -o ConnectTimeout=20
  -o BatchMode=yes
)

# Ejecuta un script en el remoto sin pelear con el quoting de la shell local.
remote_run() {
  ssh "${SSH_OPTS[@]}" "$TARGET" 'bash -s'
}

# --- Credenciales -----------------------------------------------------------
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
printf '%s\n' "$SFTP_SSH_KEY" > "$KEY_FILE"
chmod 600 "$KEY_FILE"
printf '%s\n' "$SSH_KNOWN_HOSTS" > "$KNOWN_HOSTS_FILE"
chmod 644 "$KNOWN_HOSTS_FILE"

# --- Preflight --------------------------------------------------------------
echo "::group::Preflight ($LABEL)"
remote_run <<REMS
set -euo pipefail
if [ ! -d "$SFTP_PATH" ]; then
  echo "ERROR: el destino $SFTP_PATH no existe" >&2
  exit 1
fi
if [ ! -w "$SFTP_PATH" ]; then
  echo "ERROR: el destino $SFTP_PATH no es escribible por $SFTP_USER" >&2
  exit 1
fi
echo "destino ok: $SFTP_PATH"
echo "archivos actuales: \$(find "$SFTP_PATH" -type f | wc -l)"
REMS
echo "::endgroup::"

# --- Aviso de no indexación (staging) ---------------------------------------
if [ "$NOINDEX" = "1" ]; then
  printf 'User-agent: *\nDisallow: /\n' > "$DIST_DIR/robots.txt"
  echo "robots.txt de bloqueo agregado al build"
fi

# --- Backup del deploy anterior --------------------------------------------
if [ -n "$BACKUP_DIR" ]; then
  echo "::group::Backup ($LABEL)"
  remote_run <<REMS
set -euo pipefail
mkdir -p "$BACKUP_DIR"
ts=\$(date +%Y%m%d-%H%M%S)
tar czf "$BACKUP_DIR/\$ts.tar.gz" -C "$SFTP_PATH" .
echo "backup creado: $BACKUP_DIR/\$ts.tar.gz (\$(du -h "$BACKUP_DIR/\$ts.tar.gz" | cut -f1))"
ls -1t "$BACKUP_DIR"/*.tar.gz | tail -n +$((BACKUP_KEEP + 1)) | xargs -r rm -f
echo "backups conservados: \$(ls -1 "$BACKUP_DIR"/*.tar.gz | wc -l)"
REMS
  echo "::endgroup::"
fi

# --- Sincronización ---------------------------------------------------------
echo "::group::Rsync ($LABEL)"
if [ ! -f "$DIST_DIR/index.html" ]; then
  echo "ERROR: no hay $DIST_DIR/index.html, el build no se descargó" >&2
  exit 1
fi

# Basura del sistema operativo que no debe llegar al docroot.
find "$DIST_DIR" -name '.DS_Store' -delete

EXCLUDE_OPTS=()
if [ -f .deployignore ]; then
  EXCLUDE_OPTS=(--exclude-from=.deployignore)
fi

RSYNC_SSH="ssh -i $KEY_FILE -p $SFTP_PORT -o IdentitiesOnly=yes -o UserKnownHostsFile=$KNOWN_HOSTS_FILE -o StrictHostKeyChecking=yes"

# Ojo con los flags: el docroot de producción es de www-data y gsalvini solo
# tiene escritura por grupo. Por eso NO se usa -p (chmod sobre archivos ajenos
# falla con "Operation not permitted") ni se preservan tiempos de directorio
# (-O): los archivos nuevos heredan el umask 022 del runner, que es lo que
# Apache necesita para leerlos.
#
# Dry-run primero: si el --delete se llevaría algo que el build no gestiona,
# se corta acá y no se toca el servidor.
rsync -rltzO --delete --itemize-changes --dry-run "${EXCLUDE_OPTS[@]}" \
  -e "$RSYNC_SSH" "$DIST_DIR"/ "$TARGET:$SFTP_PATH"/ > /tmp/rsync-dry.log 2>&1 || {
    echo "ERROR: falló el dry-run de rsync" >&2
    cat /tmp/rsync-dry.log >&2
    exit 1
  }

borrados="$(grep -c '^\*deleting' /tmp/rsync-dry.log || true)"
sospechosos="$(grep '^\*deleting' /tmp/rsync-dry.log | awk '{print $2}' | grep -vE '^(_astro|pagefind|posts|tags|assets|embeds)/' || true)"
echo "archivos a subir o actualizar: $(grep -c '^[<>]' /tmp/rsync-dry.log || true)"
echo "archivos a borrar del servidor: $borrados"
if [ -n "$sospechosos" ]; then
  {
    echo "ERROR: el --delete borraría rutas que el build no gestiona."
    echo "Revisá si hay que preservarlas en .deployignore:"
    echo "$sospechosos"
  } >&2
  exit 1
fi

rsync -rltzO --delete --delay-updates --human-readable --stats "${EXCLUDE_OPTS[@]}" \
  -e "$RSYNC_SSH" "$DIST_DIR"/ "$TARGET:$SFTP_PATH"/
echo "::endgroup::"

# --- Verificación -----------------------------------------------------------
echo "::group::Verificación ($LABEL)"
local_hash="$(sha256sum "$DIST_DIR/index.html" | cut -d' ' -f1)"
remote_hash="$(remote_run <<REMS
set -euo pipefail
sha256sum "$SFTP_PATH/index.html" | cut -d' ' -f1
REMS
)"
if [ "$local_hash" != "$remote_hash" ]; then
  echo "ERROR: el index.html remoto no coincide con el build" >&2
  echo "local:  $local_hash" >&2
  echo "remoto: $remote_hash" >&2
  exit 1
fi
echo "hash de index.html coincide: $local_hash"

# Chequeo exacto: si después de sincronizar un dry-run no tiene nada pendiente,
# el servidor es idéntico al build. Contar archivos a mano no sirve porque el
# server puede tener archivos protegidos por .deployignore.
post_dry="$(mktemp)"
rsync -rltzO --delete --itemize-changes --dry-run "${EXCLUDE_OPTS[@]}" \
  -e "$RSYNC_SSH" "$DIST_DIR"/ "$TARGET:$SFTP_PATH"/ > "$post_dry" 2>&1
pendientes="$(grep -cE '^([<>*]|cd)' "$post_dry" || true)"
remote_files="$(remote_run <<REMS
set -euo pipefail
find "$SFTP_PATH" -type f | wc -l
REMS
)"
echo "archivos: locales=$(find "$DIST_DIR" -type f | wc -l) remotos=$remote_files"
if [ "$pendientes" -ne 0 ]; then
  echo "ERROR: quedaron $pendientes diferencias entre el build y el servidor" >&2
  grep -E '^([<>*]|cd)' "$post_dry" | head -20 >&2
  exit 1
fi
echo "servidor idéntico al build (dry-run posterior sin diferencias)"

if [ -n "$SITE_URL" ]; then
  marker="$(grep -oE '/_astro/[A-Za-z0-9._-]+\.(css|js)' "$DIST_DIR/index.html" | head -1 || true)"
  if [ -z "$marker" ]; then
    echo "ERROR: no se encontró un asset /_astro/ en el build para verificar" >&2
    exit 1
  fi
  live_file="$(mktemp)"
  if ! curl -fsS -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' \
      "$SITE_URL/?deploy=${GITHUB_SHA:-local}" -o "$live_file"; then
    echo "ERROR: no se pudo descargar $SITE_URL" >&2
    exit 1
  fi
  # grep sobre archivo y no por pipe: grep -q cierra el pipe antes de que el
  # escritor termine y con pipefail el pipeline muere por SIGPIPE (141).
  if ! grep -qF "$marker" "$live_file"; then
    echo "ERROR: $SITE_URL no está sirviendo el build nuevo (falta $marker)" >&2
    exit 1
  fi
  echo "HTTP ok: $SITE_URL sirve el asset $marker"
fi
echo "::endgroup::"

{
  echo "### Deploy $LABEL"
  echo ""
  echo "| dato | valor |"
  echo "| --- | --- |"
  echo "| destino | \`$TARGET:$SFTP_PATH\` |"
  echo "| archivos | $remote_files |"
  echo "| borrados por --delete | ${borrados:-0} |"
  echo "| sha256 index.html | \`$local_hash\` |"
  if [ -n "$SITE_URL" ]; then
    echo "| verificación HTTP | $SITE_URL ok |"
  fi
  if [ -n "$BACKUP_DIR" ]; then
    echo "| backup | \`$BACKUP_DIR\` (se conservan $BACKUP_KEEP) |"
  fi
} >> "$GITHUB_STEP_SUMMARY"
