---
title: "De Boltzmann a ChatGPT — Cómic educativo"
url: "https://gustavosalvini.com.ar/comics/boltzmann-chatgpt/"
author: "Gustavo Adrián Salvini"
lang: "es-AR"
published: "2026-06-09"
pages: 9
tags:
  - física estadística
  - inteligencia artificial
  - softmax
  - Boltzmann
  - ChatGPT
  - entropía
  - cómic educativo
  - machine learning
  - transformers
  - divulgación científica
---

# De Boltzmann a ChatGPT — Cómic educativo

## Resumen

Cómic educativo en estilo **ligne-claire** (línea clara, tradición del cómic europeo) que revela la identidad matemática exacta entre la **distribución de Boltzmann** (1877) y la **función softmax** utilizada en ChatGPT y los modelos transformer.

El recorrido abarca 150 años de ciencia: desde la física estadística del siglo XIX (Boltzmann, Gibbs) pasando por la teoría de la información (Shannon, 1948), las redes neuronales (Hopfield, Hinton), hasta la arquitectura transformer (Vaswani et al., 2017) y los LLMs actuales.

## Hechos clave

| Hecho | Detalle |
|-------|---------|
| **Identidad matemática** | `softmax(z_i) = exp(z_i/τ) / Σ exp(z_j/τ)` ≡ `P(E_i) = exp(-E_i/kT) / Σ exp(-E_j/kT)` |
| **Principio unificador** | Ambas ecuaciones maximizan entropía sujeta a restricciones |
| **Temperatura (τ/T)** | τ→0 = determinista (frío), τ→∞ = creativo (caliente) — misma perilla en física y ML |
| **Entropía cruzada** | `H(p,q) = -Σ p(x) log q(x)` — minimizarla equivale a maximizar verosimilitud |
| **Nobel de Física 2024** | Otorgado a John Hopfield y Geoffrey Hinton por redes neuronales |
| **Redes de Hopfield** | Adaptación del modelo de Ising de la física estadística (1982) |
| **Lema** | "What I cannot create, I do not understand" — Richard P. Feynman, 1988 |

## Personajes y entidades

- **Ludwig Boltzmann** (1844-1906): Físico austriaco. Formuló la distribución de Boltzmann y `S = k ln W`. Aparece en las páginas 1 (portada), 4, 7 y 8.
- **Claude Shannon** (1916-2001): Padre de la teoría de la información. `H = -Σ p log p`. Aparece en páginas 2 y 8.
- **John Hopfield** (n. 1933): Físico, creó las redes de Hopfield. Premio Nobel de Física 2024. Aparece en páginas 4 y 7.
- **Geoffrey Hinton** (n. 1947): "Padrino de la IA". Premio Nobel de Física 2024. Aparece en páginas 4 y 7.
- **Richard Feynman** (1918-1988): Físico estadounidense, premio Nobel. Su cita cierra el cómic (página 8) y aparece diciendo "¡EXCELENTE!" en la página 4.
- **Josiah Willard Gibbs** (1839-1903): Extendió la termodinámica estadística. Aparece en páginas 4 y 7.
- **Carl Friedrich Gauss** (1777-1855): Matemático y estadístico. Base de la máxima verosimilitud. Aparece en página 2.
- **Gus**: Narrador del cómic. Rubio, ojos celestes, sin lentes, ~45 años, camisa celeste y suéter azul V-neck. Basado en el autor. Guía al lector a través de todos los conceptos.

## Estructura del cómic (9 viñetas)

| # | Viñeta | Concepto principal |
|---|--------|-------------------|
| 1 | Portada — De Boltzmann a ChatGPT | La ecuación que une el gas de Boltzmann con ChatGPT |
| 2 | Álgebra Lineal | Embeddings, matrices Q/K/V, mecanismo de atención, "Attention Is All You Need" |
| 3 | Probabilidad y entropía | Shannon, entropía cruzada H(p,q), máxima verosimilitud L(θ) |
| 4 | LA MISMA ECUACIÓN | Identidad Boltzmann = softmax, splash page dramática |
| 5 | De Hopfield a los Transformers | Modelo de Ising, paisaje de energía, Nobel 2024, Feynman "¡EXCELENTE!" |
| 6 | Entrenamiento y fine-tuning | GPUs, SGD, física como lenguaje unificador del ML |
| 7 | La perilla termodinámica | Temperatura τ, frío→determinista, caliente→creativo |
| 8 | La unidad profunda de las matemáticas | Línea de tiempo 1877→2024, conexión dorada entre todas las ecuaciones |
| 9 | Cierre | Feynman quote, enlace a visualización 3D interactiva |

## Ecuaciones clave

1. **Distribución de Boltzmann** (1877): `P(E_i) = exp(-E_i/kT) / Σ_j exp(-E_j/kT)`
2. **Función softmax** (2017): `softmax(z_i) = exp(z_i/τ) / Σ_j exp(z_j/τ)`
3. **Entropía de Boltzmann**: `S = k ln W`
4. **Entropía de Shannon** (1948): `H = -Σ p_i log p_i`
5. **Entropía cruzada**: `H(p,q) = -Σ p(x) log q(x)`
6. **Máxima verosimilitud**: `L(θ) = Π P_θ(x_i | x_<i)`
7. **Red de Hopfield — energía**: `E = -½ Σ_i,j w_ij s_i s_j`

## Recursos relacionados

- [Artículo completo](https://gustavosalvini.com.ar/posts/de-boltzmann-a-chatgpt/)
- [Sitio del autor](https://gustavosalvini.com.ar)
- [Visualización 3D interactiva](https://learn.harness.ar/webapps/boltzmann-chatgpt/)
