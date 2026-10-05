#!/usr/bin/env python3
"""Embebe Inter (subset woff2, data URI) dentro del SVG del AUROC.

Motivo: un SVG dentro de <img> no puede cargar @font-face desde el HTML padre ni
fuentes externas; resuelve contra las fuentes del sistema del cliente. Embebiendo el
subset, el gráfico se ve con Inter en cualquier dispositivo.

Se corre con ~/.venv/bin/python3 (único intérprete con fontTools + brotli).
Es idempotente: saca una inyección previa antes de volver a inyectar.
"""
import base64
import os
import pathlib
import re
import subprocess
import sys
import tempfile

SVG = pathlib.Path('public/assets/auroc-roc-curve.svg')
FAMILIA = 'Inter'
FUENTES = [(400, '/usr/share/fonts/opentype/inter/Inter-Regular.otf'),
           (700, '/usr/share/fonts/opentype/inter/Inter-Bold.otf')]
UNICODES = 'U+0020-00FF,U+2013-2014,U+2018-201D,U+2022,U+2026,U+2192,U+2212'


def woff2_b64(src):
    with tempfile.NamedTemporaryFile(suffix='.woff2', delete=False) as f:
        out = f.name
    try:
        subprocess.run([sys.executable, '-m', 'fontTools.subset', src,
                        '--unicodes=' + UNICODES, '--flavor=woff2',
                        '--output-file=' + out], check=True, capture_output=True)
        return base64.b64encode(pathlib.Path(out).read_bytes()).decode()
    finally:
        os.unlink(out)


s = SVG.read_text(encoding='utf-8')
# idempotencia: fuera la inyección anterior si existe
s = re.sub(r'\n<style id="fuentes">.*?</style>', '', s, flags=re.S)

css = ['<style id="fuentes">']
for peso, ruta in FUENTES:
    if not pathlib.Path(ruta).exists():
        raise SystemExit(f'FALTA la fuente {ruta}')
    b64 = woff2_b64(ruta)
    print(f'  {pathlib.Path(ruta).name}: subset woff2 {len(b64) * 3 // 4 // 1024} KB aprox')
    css.append(f'@font-face {{ font-family: "{FAMILIA}"; font-style: normal; font-weight: {peso}; '
               f'src: url(data:font/woff2;base64,{b64}) format("woff2"); font-display: swap; }}')
css.append('</style>')

m = re.search(r'<svg[^>]*>', s)
if not m:
    raise SystemExit('FALLO: no encuentro el tag <svg>')
antes = len(s)
s = s[:m.end()] + '\n' + ''.join(css) + s[m.end():]
SVG.write_text(s, encoding='utf-8')
print(f'injectado: {antes} -> {len(s)} bytes | data URIs: {s.count("data:font/woff2;base64")}')
