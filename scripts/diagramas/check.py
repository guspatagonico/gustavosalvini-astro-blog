#!/usr/bin/env python3
"""Verifica la geometría del SVG del AUROC: cajas de texto dentro del panel y sin solapes."""
import re
import pathlib
from PIL import Image

SVG = pathlib.Path('public/assets/auroc-roc-curve.svg')
W, H = 1100, 740
svg = SVG.read_text(encoding='utf-8')
style = re.search(r'<style>(.*?)</style>', svg, re.S).group(1)
size = {c: float(re.search(rf'\.{c}\{{[^}}]*font-size:(\d+)px', style).group(1))
        for c in ['eje', 'tick', 'ley', 'nota', 'dentro', 'azar']}

cajas = []
for m in re.finditer(r'<text class="(\w+)"([^>]*)>(.*?)</text>', svg):
    cls, attrs, txt = m.group(1), m.group(2), m.group(3)
    x = float(re.search(r'\bx="([\d.]+)"', attrs).group(1))
    y = float(re.search(r'\by="([\d.]+)"', attrs).group(1))
    anc = (re.search(r'text-anchor="(\w+)"', attrs) or [None, 'start'])[1]
    rot = 'rotate(' in attrs
    ancho = len(txt) * 0.55 * size[cls]
    if rot:
        # rotado -90: el ancho del texto pasa a ser alto
        x0, x1 = x - size[cls] * 0.8, x + size[cls] * 0.2
        y0, y1 = y - ancho / 2, y + ancho / 2
    else:
        x0 = x - ancho if anc == 'end' else (x - ancho / 2 if anc == 'middle' else x)
        x1 = x0 + ancho
        y0, y1 = y - size[cls], y + size[cls] * 0.25
    cajas.append((cls, txt, x0, y0, x1, y1))

print(f'textos: {len(cajas)} | clases: {sorted(size)}')

print('\n=== dentro del panel? ===')
problemas = []
for cls, txt, x0, y0, x1, y1 in cajas:
    if x0 < 6 or x1 > W - 6:
        problemas.append(f'ancho: "{txt}" [{x0:.0f}, {x1:.0f}]')
    if y0 < 6 or y1 > H - 6:
        problemas.append(f'alto: "{txt}" [{y0:.0f}, {y1:.0f}]')
print('  ' + ('\n  '.join(problemas) if problemas else 'ninguno'))

print('\n=== solapes entre textos ===')
n = 0
for i in range(len(cajas)):
    for j in range(i + 1, len(cajas)):
        a, b = cajas[i], cajas[j]
        if a[2] < b[4] and b[2] < a[4] and a[3] < b[5] and b[3] < a[5]:
            print(f'  SOLAPAN: "{a[1]}" con "{b[1]}"')
            n += 1
print(f'  total: {n}')

print('\n=== textos clave en el SVG ===')
for t in ['Tasa de falsos positivos', 'Tasa de verdaderos positivos', 'área = 81,6%',
          'Cómo se lee', 'El LLM: 81,6% de área', 'Jev: 73,4% de área',
          'Azar: 50% de área', 'esquemática', '>azar<']:
    print(f'  {"OK   " if t in svg else "FALTA"}  {t}')
print('  sin tilde (deberia ser 0):', len(re.findall(r'\b(area|eschematica)\b', svg, re.I)))

im = Image.open('.hermes/diagramas/auroc-full.png')
s = 1.4
im.crop((int(715 * s), int(55 * s), int(1105 * s), int(700 * s))).save('.hermes/diagramas/crop-leyenda.png')
im.crop((int(290 * s), int(330 * s), int(720 * s), int(645 * s))).save('.hermes/diagramas/crop-rotulos.png')
print('\nrecortes listos: crop-leyenda.png, crop-rotulos.png')
