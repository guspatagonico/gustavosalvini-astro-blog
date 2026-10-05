#!/usr/bin/env python3
"""Genera el gráfico de la curva ROC / AUROC para el post de modelos de decisión.

Diseño: un cuadrado de 100x100 (ambos ejes en porcentaje, para que la diagonal del
azar quede a 45 grados), dos curvas esquemáticas del tipo TPR = FPR**k elegidas para
que su área sea EXACTAMENTE el AUC que reporta la evaluación (0,734 Jev y 0,816 el
LLM), la diagonal del azar, y el área bajo la curva más alta sombreada.

La forma de cada curva es un modelo, no la medición: lo que se afirma es el área.
Por eso el epígrafe del post lo dice y el gráfico rotula cada curva por su valor.
"""

from pathlib import Path

W, H = 1100, 740
PL, PT, PS = 150, 70, 540          # izquierda, arriba y lado del cuadrado del gráfico
PB, PR = PT + PS, PL + PS          # 610, 690
AUC_A, AUC_B = 0.816, 0.734        # el LLM (confianza verbalizada) y Jev

BG1, BG2 = "#070d19", "#0e1c31"
GRID, AXIS, TXT, MUT = "#1e293b", "#334155", "#e2e8f0", "#94a3b8"
BLUE, TURQ = "#2f6bff", "#2fd0c5"

K_A, K_B = 1 / AUC_A - 1, 1 / AUC_B - 1     # TPR = FPR**k  =>  área = 1/(k+1)

COM = lambda v: f"{v*100:.1f}".replace(".", ",")   # 0.816 -> "81,6"


def x(f):
    return PL + f * PS


def y(t):
    return PB - t * PS


def puntos(k, n=90):
    """Muestreo denso cerca de 0, donde la curva es casi vertical: con puntos
    uniformes el polígono subestima el área (la curva arranca con pendiente alta)."""
    return [(x(t), y(t ** k)) for t in ((i / n) ** 2 for i in range(n + 1))]


def area_dibujada(pts):
    """Área del polígono cerrado por la curva y el eje de abajo (fórmula del cordón)."""
    poli = [(PL, PB)] + pts + [(PR, PB)]
    a = 0.0
    for (x1, y1), (x2, y2) in zip(poli, poli[1:] + poli[:1]):
        a += x1 * y2 - x2 * y1
    return abs(a) / 2 / (PS * PS)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


pA, pB = puntos(K_A), puntos(K_B)
aA, aB = area_dibujada(pA), area_dibujada(pB)
assert abs(aA - AUC_A) < 0.002, f"área curva A {aA} != {AUC_A}"
assert abs(aB - AUC_B) < 0.002, f"área curva B {aB} != {AUC_B}"
print(f"área dibujada -> A: {aA:.4f} (esperado {AUC_A}) | B: {aB:.4f} (esperado {AUC_B})")

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'role="img" aria-label="Curva ROC de dos clasificadores y el área que mide el AUROC">',
    '<defs>',
    f'<linearGradient id="fondo" x1="0" y1="0" x2="0.6" y2="1">'
    f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>',
    '</defs>',
    f'<style>text{{font-family:Inter, ui-sans-serif, system-ui, sans-serif}}'
    f'.eje{{fill:{TXT};font-size:22px;font-weight:600}}'
    f'.tick{{fill:{MUT};font-size:17px}}'
    f'.ley{{fill:{TXT};font-size:18px}}'
    f'.nota{{fill:#b3bed1;font-size:18px}}'
    f'.dentro{{fill:{TXT};font-size:18px;font-weight:600}}'
    f'.azar{{fill:{MUT};font-size:17px;font-style:italic}}</style>',
    f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="url(#fondo)" stroke="{GRID}" stroke-width="2"/>',
]

# grilla y graduaciones
for i in range(1, 4):
    f = i / 4
    svg.append(f'<line x1="{x(f):.1f}" y1="{PT}" x2="{x(f):.1f}" y2="{PB}" stroke="{GRID}" stroke-width="1"/>')
    svg.append(f'<line x1="{PL}" y1="{y(f):.1f}" x2="{PR}" y2="{y(f):.1f}" stroke="{GRID}" stroke-width="1"/>')
for i in range(5):
    f = i / 4
    svg.append(f'<text class="tick" x="{x(f):.1f}" y="{PB+28}" text-anchor="middle">{int(f*100)}%</text>')
    svg.append(f'<text class="tick" x="{PL-16}" y="{y(f)+6:.1f}" text-anchor="end">{int(f*100)}%</text>')

# ejes
svg.append(f'<line x1="{PL}" y1="{PB}" x2="{PR}" y2="{PB}" stroke="{AXIS}" stroke-width="2"/>')
svg.append(f'<line x1="{PL}" y1="{PT}" x2="{PL}" y2="{PB}" stroke="{AXIS}" stroke-width="2"/>')

# área bajo la curva más alta (la del clasificador de 81,6%)
svg.append('<path d="M ' + f'{PL} {PB} ' + ' '.join(f'L {px:.1f} {py:.1f}' for px, py in pA)
           + f' L {PR} {PB} Z" fill="{BLUE}" fill-opacity="0.42"/>')

# diagonal del azar
svg.append(f'<line x1="{x(0)}" y1="{y(0)}" x2="{x(1)}" y2="{y(1)}" stroke="{MUT}" '
           f'stroke-width="1.6" stroke-dasharray="7 6"/>')

# curvas
for pts, color, wd in ((pA, BLUE, 3.6), (pB, TURQ, 3.0)):
    d = 'M ' + ' '.join(f'{px:.1f} {py:.1f}' for px, py in pts)
    svg.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{wd}" stroke-linecap="round"/>')

# rótulos dentro del gráfico
svg.append(f'<text class="azar" x="{x(0.56):.0f}" y="{PB-186:.0f}" text-anchor="middle">azar</text>')
svg.append(f'<text class="dentro" x="{x(0.70):.0f}" y="{PB-26:.0f}" text-anchor="middle">área = {COM(AUC_A)}%</text>')

# títulos de los ejes
svg.append(f'<text class="eje" x="{(PL+PR)/2:.0f}" y="{H-30}" text-anchor="middle">Tasa de falsos positivos</text>')
ym = (PT + PB) / 2
svg.append(f'<text class="eje" x="46" y="{ym:.0f}" text-anchor="middle" '
           f'transform="rotate(-90 46 {ym:.0f})">Tasa de verdaderos positivos</text>')

# leyenda y nota, en la columna de la derecha
CX, YY = PR + 40, PT + 16
svg.append(f'<text class="ley" x="{CX}" y="{YY}" font-weight="600">Cómo se lee</text>')
YY += 40
for color, txt in ((BLUE, f'El LLM: {COM(AUC_A)}% de área'),
                   (TURQ, f'Jev: {COM(AUC_B)}% de área'),
                   (MUT, 'Azar: 50%')):
    svg.append(f'<line x1="{CX}" y1="{YY-6}" x2="{CX+34}" y2="{YY-6}" stroke="{color}" stroke-width="4" '
               f'stroke-linecap="round"' + (' stroke-dasharray="7 6"' if color == MUT else '') + '/>')
    svg.append(f'<text class="ley" x="{CX+46}" y="{YY}">{esc(txt)}</text>')
    YY += 34
YY += 14
for linea in ('La zona sombreada es el área',
              'bajo la curva de arriba:',
              'el AUROC es eso, un área.',
              '',
              'La forma de cada curva es',
              'esquemática. Lo que el informe',
              'mide y reporta es su área.'):
    svg.append(f'<text class="nota" x="{CX}" y="{YY}">{esc(linea)}</text>')
    YY += 23

svg.append('</svg>')
out = Path('public/assets/auroc-roc-curve.svg')
out.write_text('\n'.join(svg) + '\n', encoding='utf-8')
print('escrito:', out, out.stat().st_size, 'bytes')
