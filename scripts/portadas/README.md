# Portadas de post

Generadores de las portadas que se dibujan a mano (un HTML de 1200x750) en lugar de
generarse con IA. El JPEG final vive en `public/assets/` y es lo que el post referencia;
el HTML es la fuente de verdad para ajustar la composición.

```bash
mkdir -p /tmp/hero
# Render al doble y bajada a 1200x750: el texto chico queda limpio en retina.
CH=$(ls -d ~/.cache/ms-playwright/chromium-*/chrome-linux/chrome | tail -1)
"$CH" --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size=1200,750 --force-device-scale-factor=2 --virtual-time-budget=6000 \
  --screenshot=/tmp/hero/cover.png "file://$PWD/scripts/portadas/<archivo>.html"
/usr/bin/python3 -c "
from PIL import Image
Image.open('/tmp/hero/cover.png').convert('RGB').resize((1200,750), Image.LANCZOS) \
  .save('/tmp/hero/portada.jpg', 'JPEG', quality=88, subsampling=0, optimize=True, progressive=True)"
```

Usá el chromium de Playwright, no el `chromium-browser` del sistema: ese es snap y no
puede escribir en `/tmp`. Composición, recorte de capturas e iteración con visión:
skill `gustavosalvini-blog`, `references/portadas-de-post.md`.

Las portadas de este directorio son las de la cartelera de Pívot. Las portadas
generadas con IA no tienen generador y no viven acá.
