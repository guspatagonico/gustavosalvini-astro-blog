---
author: Gustavo Salvini
pubDatetime: 2025-04-09T16:45:39.660Z
modDatetime: 2025-04-09T16:45:39.660Z
title: Testing LaTeX equations
featured: false
hideEditPost: true
draft: false
tags:
  - LaTeX
  - math
description: Testing LaTeX equations in Astro with remark/rehype plugins.
---

This document demonstrates how to use LaTeX equations in your Markdown files for AstroPaper. LaTeX is a powerful typesetting system often used for mathematical and scientific documents.

## Inline Equations

Inline equations are written between single dollar signs `$...$`. Here are some examples:

1. The famous mass-energy equivalence formula: `$E = mc^2$` $E = mc^2$
2. The quadratic formula: `$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$` $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$
3. Euler's identity: `$e^{i\pi} + 1 = 0$` $e^{i\pi} + 1 = 0$

---

## Block Equations

For more complex equations or when you want the equation to be displayed on its own line, use double dollar signs `$$...$$`:

### The Gaussian integral

```latex
$$ \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi} $$
```

$$ \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi} $$

### The definition of the Riemann zeta function

```latex
$$ \zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} $$
```

$$ \zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} $$

### Maxwell's equations in differential form

```latex
$$
\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0\left(\mathbf{J} + \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}\right)
\end{aligned}
$$
```

$$
\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0\left(\mathbf{J} + \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}\right)
\end{aligned}
$$

---

## Using Mathematical Symbols

LaTeX provides a wide range of mathematical symbols:

- Greek letters: `$\alpha$`, `$\beta$`, `$\gamma$`, `$\delta$`, `$\epsilon$`, `$\pi$`
- Operators: `$\sum$`, `$\prod$`, `$\int$`, `$\partial$`, `$\nabla$`
- Relations: `$\leq$`, `$\geq$`, `$\approx$`, `$\sim$`, `$\propto$`
- Logical symbols: `$\forall$`, `$\exists$`, `$\neg$`, `$\wedge$`, `$\vee$`


---

## Testing specific characters:

```latex
$H_a: \theta>\theta_0$
```

### Results:

$H_a: \theta>\theta_0$

```latex
$\not\in$
$\neq$
$\neg$
$\sim$
$\nexists$
$\lambda$
$\lmoustache\0\2pi$
```

### Results

$\not\in$
$\neq$
$\neg$
$\sim$
$\nexists$
$\lambda$
$\lmoustache\pi$


```latex
$$
\begin{equation*}
\begin{aligned}
\iiint_{\mathcal{Q}} f(w,x,y,z) \,dw \,dx \,dy \,dz
&\leq 
\oint_{\partial Q} f'
  \left(
    \max \left\{ \frac{|w|}{|{w^2 + x^2}|} ; 
    \frac{|z|}{|{y^2 + z^2}|} ;
    \frac{|{w \oplus z}|}{|{x \oplus y}|} \right\}
  \right)
\\
&\precapprox
\biguplus_{\mathbb{Q} \Subset \bar{Q}}
  \left[ f^* \left(
    \frac{\lmoustache \mathbb{Q}(t)\rmoustache}{\sqrt{1 - t^2}}
  \right) \right]^{t=9}_{t=\alpha}
\end{aligned}
\end{equation*}
$$
```

$$
\begin{equation*}
\begin{aligned}
\iiint_{\mathcal{Q}} f(w,x,y,z) \,dw \,dx \,dy \,dz
&\leq 
\oint_{\partial Q} f'
  \left(
    \max \left\{ \frac{|w|}{|{w^2 + x^2}|} ; 
    \frac{|z|}{|{y^2 + z^2}|} ;
    \frac{|{w \oplus z}|}{|{x \oplus y}|} \right\}
  \right)
\\
&\precapprox
\biguplus_{\mathbb{Q} \Subset \bar{Q}}
  \left[ f^* \left(
    \frac{\lmoustache \mathbb{Q}(t)\rmoustache}{\sqrt{1 - t^2}}
  \right) \right]^{t=9}_{t=\alpha}
\end{aligned}
\end{equation*}
$$


$$
\oint_V f(s) \,ds
\iiint_V f(x,y,z) \,dx \,dy \,dz
$$
