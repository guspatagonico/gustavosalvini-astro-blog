# Diagramas del blog

Generadores de las figuras que no son portadas. Cada uno escribe su artefacto en
`public/assets/`, que es lo que el post referencia.

## El gráfico del AUROC

`auroc-roc-curve.py` genera `public/assets/auroc-roc-curve.svg`, que usa el post
`modelos-de-decision-harness-coding`.

El pipeline son tres pasos, **siempre desde la raíz del repo** (los scripts usan rutas
relativas), más un render para verificar:

```bash
# 1. generar el SVG. Verifica que el área dibujada de cada curva sea el AUC reportado.
/usr/bin/python3 scripts/diagramas/auroc-roc-curve.py

# 2. embeber Inter en subset woff2 dentro del SVG. Obligatorio después de cada
#    regeneración, porque el paso 1 reescribe el archivo. Necesita fontTools + brotli:
#    están en ~/.venv, no en el python del sistema.
~/.venv/bin/python3 scripts/diagramas/embeber-fuente.py

# 3. armar el HTML del render con el SVG INLINE y sacarle la captura.
/usr/bin/python3 - <<'PY'
from pathlib import Path
svg = Path('public/assets/auroc-roc-curve.svg').read_text(encoding='utf-8')
Path('.hermes/diagramas/wrap.html').write_text(
    '<!doctype html><meta charset="utf-8">\n'
    '<style>html,body{margin:0;padding:0;background:#f8fafc}'
    'svg{display:block;width:1100px;height:740px}</style>\n' + svg, encoding='utf-8')
PY
/usr/bin/chromium-browser --headless --disable-gpu --no-sandbox \
  --screenshot="$PWD/.hermes/diagramas/auroc-full.png" --window-size=1100,740 \
  --force-device-scale-factor=1.4 --virtual-time-budget=5000 \
  file://$PWD/.hermes/diagramas/wrap.html

# 4. verificar: cajas de texto dentro del panel, sin solapes, y recortes para mirar
/usr/bin/python3 scripts/diagramas/check.py
```

## Dos trampas de esta máquina

- **El chromium es snap y `/tmp` es su tmp privado.** Escribí la captura dentro del
  repo: si la mandás a `/tmp`, chromium dice "N bytes written" y después el archivo no
  existe en ninguna parte.
- **El SVG va INLINE en el HTML del render.** Un `<img src="file://...">` no carga en el
  snap y la captura sale siendo una página `ERR_FILE_NOT_FOUND`.

## Por qué el gráfico es esquemático

La evaluación no publica los puntos de las curvas ROC, solo los valores de AUC.
Dibujar la forma exacta sería inventar la medición, así que cada curva sigue el modelo
`TPR = FPR**k` con el `k` elegido para que **su área sea exactamente el AUC que reporta
el informe**, y el generador lo verifica contra ese valor. La forma es un modelo; el
área es el dato. Por eso el gráfico y su epígrafe lo dicen.
