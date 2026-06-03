# EL PERCEPTRÓN

**Fundamentos, historia y matemática de la neurona artificial más simple**

*Basado en fuentes académicas: Rosenblatt (1958), Minsky & Papert (1969), y literatura contemporánea de arxiv.org*

Junio 2026

---

## 1. ¿Qué es un perceptrón?

El perceptrón es la forma más simple de red neuronal artificial. Es un **clasificador binario lineal**: toma un vector de entradas, las pondera mediante pesos, les suma un sesgo (*bias*) y produce una salida binaria (típicamente $0$ o $1$, o bien $-1$ o $+1$). Geométricamente, traza una línea —un hiperplano en dimensiones superiores— que separa dos clases de datos.

Constituye el **ladrillo fundamental del deep learning moderno**. Cada «neurona» en arquitecturas como *transformers*, *CNNs* o *GPTs* es, conceptualmente, un perceptrón con una función de activación diferenciable.

### 1.1 Origen histórico

El concepto de neurona artificial fue propuesto por **Warren McCulloch y Walter Pitts** en 1943 como un modelo matemático simplificado de la neurona biológica. Sin embargo, fue **Frank Rosenblatt** quien, en 1958, desarrolló el perceptrón como una máquina real —el *Mark I Perceptron*— y publicó el artículo fundacional del campo:

> *"The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain"*
> — Frank Rosenblatt, *Psychological Review*, 65(6), 386–408, 1958

Rosenblatt no solo describió la arquitectura, sino también un **algoritmo de aprendizaje** que permitía al perceptrón aprender de sus propios errores ajustando los pesos de las conexiones. Fue un hito: por primera vez, una máquina podía «aprender» de la experiencia sin ser programada explícitamente.

### 1.2 Arquitectura visual

El perceptrón opera en tres etapas claramente diferenciadas:

```
Entradas         Pesos           Suma + Sesgo       Activación     Salida

   x₁ ─────────── w₁
                  │
   x₂ ─────────── w₂ ────→  z = Σ(wᵢ·xᵢ) + b  ────→ step(z) ────→  ŷ
                  │
   …              │
                  │
   xₙ ─────────── wₙ
                       │
                    sesgo b
```

---

## 2. Formulación matemática

### 2.1 Suma ponderada

El corazón del perceptrón es una combinación lineal de las entradas. Cada entrada $x_i$ se multiplica por un peso $w_i$ que representa su importancia relativa, y se suma un término de sesgo $b$ (*bias*):

$$
z = w_1 x_1 + w_2 x_2 + \dots + w_n x_n + b = \sum_{i=1}^{n} w_i x_i + b
$$

Los **pesos** controlan cuánto influye cada entrada en la decisión final. El **sesgo** permite desplazar la frontera de decisión lejos del origen, lo cual es esencial cuando los datos no están centrados en cero.

### 2.2 Función de activación

La suma ponderada $z$ se pasa por una **función escalón** (*step function*), también conocida como función de Heaviside:

$$
\hat{y} = \begin{cases}
1 & \text{si } z \geq 0 \\
0 & \text{si } z < 0
\end{cases}
$$

Esta función introduce la **no linealidad mínima** necesaria para la clasificación binaria. Si $z$ cruza el umbral (cero), la neurona «dispara» (salida $1$); en caso contrario, permanece en reposo (salida $0$).

### 2.3 Regla de aprendizaje

El algoritmo de aprendizaje del perceptrón es sorprendentemente simple. Cuando la predicción $\hat{y}$ difiere de la etiqueta real $y$, se actualizan los pesos en la dirección que corrige el error:

$$
w_i \leftarrow w_i + \eta \cdot (y - \hat{y}) \cdot x_i
$$

$$
b \leftarrow b + \eta \cdot (y - \hat{y})
$$

Donde $\eta$ (*eta*, **tasa de aprendizaje**) controla la magnitud de los ajustes. Valores típicos: $0.01$, $0.1$ o $1.0$.

La regla tiene una interpretación intuitiva:

- Si la predicción fue $0$ pero debía ser $1$: aumentamos los pesos de las entradas positivas.
- Si fue $1$ pero debía ser $0$: reducimos los pesos de las entradas positivas.

### 2.4 Teorema de convergencia

El **teorema de convergencia del perceptrón**, demostrado por **Novikoff (1962)**, garantiza que:

> Si los datos de entrenamiento son **linealmente separables**, el algoritmo encontrará un hiperplano que los clasifique perfectamente en un **número finito de iteraciones**.

Este resultado fue fundamental para establecer las bases teóricas del aprendizaje automático.

---

## 3. Limitaciones y el invierno de la IA

### 3.1 El problema XOR

En 1969, **Marvin Minsky y Seymour Papert** publicaron el influyente libro *«Perceptrons»*, donde demostraron matemáticamente que un perceptrón de una sola capa **no puede resolver problemas no linealmente separables**. El ejemplo canónico es la función lógica XOR (OR exclusivo):

| $X_1$ | $X_2$ | XOR |
|:-----:|:-----:|:---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

No existe una sola línea recta en el plano que separe los puntos $(0,0)$ y $(1,1)$ —que deben dar $0$— de los puntos $(0,1)$ y $(1,0)$ —que deben dar $1$—. Se necesita al menos una frontera curva o, equivalentemente, **más de una capa**.

```
     X₂
      ↑
    1 ┊   ○(0,1)        ●(1,1)
      ┊      salida=1      salida=0
      ┊
    0 ┊   ●(0,0)        ○(1,0)
      ┊      salida=0      salida=1
      └──────────────────────→ X₁
         0                 1

   ● = salida 0    ○ = salida 1
   Ninguna línea recta separa ● de ○
```

### 3.2 Consecuencias históricas

La crítica de Minsky y Papert, combinada con las expectativas exageradas que el propio Rosenblatt había alimentado, provocó el **primer «invierno de la IA»**. La financiación para la investigación en redes neuronales se desplomó y el campo permaneció estancado durante más de una década. No fue hasta los años 80 —con el desarrollo del algoritmo de **retropropagación** (*backpropagation*) por Rumelhart, Hinton y Williams (1986)— que las redes neuronales resurgieron con fuerza.

> *"Although the perceptron initially seemed promising, it was quickly proved that perceptrons could not be trained to recognise many classes of patterns."*
> — Wikipedia: Perceptron

---

## 4. Del perceptrón al deep learning

### 4.1 El perceptrón multicapa (MLP)

La solución al problema XOR y a las limitaciones del perceptrón simple fue **apilar múltiples capas** de neuronas, usando funciones de activación no lineales y diferenciables ($\sigma$, $\tanh$, $\text{ReLU}$) en lugar del escalón. Así nació el **perceptrón multicapa (MLP)**, capaz de aproximar cualquier función continua (**teorema de aproximación universal**, Cybenko 1989).

Como señala un artículo reciente de arxiv.org ([2409.13854](https://arxiv.org/abs/2409.13854), *«More Consideration for the Perceptron»*):

> «El desarrollo de perceptrones multicapa y algoritmos de entrenamiento como la retropropagación permitió el procesamiento de problemas no lineales. Usar una sola neurona en una red de una capa para clasificación binaria es equivalente a un clasificador lineal simple.»

### 4.2 Comparativa

| Característica | Perceptrón simple | Perceptrón multicapa (MLP) |
|---|---|---|
| **Capas** | 1 | 2 o más capas ocultas |
| **Activación** | Escalón (*step*) | Sigmoide, ReLU, tanh |
| **Frontera de decisión** | Lineal | No lineal |
| **Resuelve XOR** | ❌ No | ✅ Sí |
| **Algoritmo** | Regla del perceptrón | Backpropagation + gradiente descendente |
| **Garantía de convergencia** | ✅ Para datos separables | ❌ No hay garantía de óptimo global |

### 4.3 Relevancia actual

Hoy, el perceptrón es mucho más que una pieza de museo. Es la **unidad fundamental** sobre la que se construyen arquitecturas como:

- **Redes convolucionales (CNNs):** cada filtro es un perceptrón aplicado localmente.
- **Transformers:** el mecanismo de atención se combina con capas *feedforward* que son esencialmente MLPs.
- **Modelos de lenguaje (GPT, LLaMA, Claude):** cada bloque transformer contiene miles de «neuronas» que son, en esencia, perceptrones modernos.
- **Autoencoders y GANs:** construidos sobre capas densas de perceptrones.

> **Entender el perceptrón es entender el alfabeto del deep learning.** Toda la complejidad de los modelos actuales emerge de la combinación de estas unidades simples.

---

## 5. Referencias

1. **Rosenblatt, F. (1958)** — *The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain.* Psychological Review, 65(6), 386–408.

2. **Minsky, M. & Papert, S. (1969)** — *Perceptrons: An Introduction to Computational Geometry.* MIT Press.

3. **Novikoff, A. B. (1962)** — *On convergence proofs for perceptrons.* Symposium on the Mathematical Theory of Automata, 12, 615–622.

4. **Rumelhart, D., Hinton, G. & Williams, R. (1986)** — *Learning representations by back-propagating errors.* Nature, 323, 533–536.

5. **Cybenko, G. (1989)** — *Approximation by superpositions of a sigmoidal function.* Mathematics of Control, Signals, and Systems, 2(4), 303–314.

6. **arXiv:2409.13854 (2024)** — *More Consideration for the Perceptron.*

7. **arXiv:2510.18862 (2025)** — Trabajo sobre perceptrones y clasificación binaria.

8. **arXiv:2012.03642 (2020)** — *Generalised perceptron and feed-forward networks.*

---

*Documento generado a partir del PDF original — Junio 2026*
