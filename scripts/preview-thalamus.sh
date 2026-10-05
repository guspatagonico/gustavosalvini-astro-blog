#!/usr/bin/env bash
#
# Refresca el espejo del blog en
#   https://thalamus.tail789282.ts.net/gustavosalvini-blog/
#
# Compila con base no vacia y sincroniza el resultado a /var/www.
# El base se pasa por PUBLIC_BASE_PATH (src/config.ts) y por --base, asi
# quedan apuntadas al subpath tanto las rutas absolutas que emite Astro
# (/_astro/...) como las portadas que los posts arman con SITE.base.
#
# Si el build falla, NO sincroniza: el espejo se queda con el ultimo estado
# bueno en vez de publicar un sitio a medio compilar.
#
# Uso:  bash scripts/preview-thalamus.sh      (o pnpm preview:thalamus)

set -euo pipefail

REPO="/home/gustavo/dev/gustavosalvini-astro-blog"
BASE_PATH="/gustavosalvini-blog"
OUT_DIR="dist-gustavosalvini-blog"
DEST="/var/www/gustavosalvini-blog"

# systemd no hereda el PATH del shell interactivo.
export PATH="/home/gustavo/.local/share/pnpm/bin:/home/gustavo/.local/bin:/usr/local/bin:/usr/bin:/bin"

cd "$REPO"

PUBLIC_BASE_PATH="$BASE_PATH" pnpm exec astro build --outDir "$OUT_DIR"

# Indice de busqueda del build de preview (el de produccion usa dist/).
pnpm exec pagefind --site "$OUT_DIR" >/dev/null

sudo -n rsync -a --delete "$OUT_DIR"/ "$DEST"/
sudo -n chown -R caddy:caddy "$DEST"

echo "[$(date -Is)] espejo actualizado ($(du -sh "$DEST" | cut -f1))"
