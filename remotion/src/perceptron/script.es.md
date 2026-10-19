# El perceptrón: guion (ES)

Generado desde script.json con scripts/export_scripts.py. El tiempo de narración asume 150 palabras por minuto.

| # | Sección | Palabras | Narración (s) | Escena (s) |
|---|---|---|---|---|
| 1 | `intro` | 18 | 7.2 | 8.0 |
| 2 | `neuron` | 32 | 12.8 | 13.6 |
| 3 | `boundary` | 31 | 12.4 | 13.2 |
| 4 | `learning` | 31 | 12.4 | 13.2 |
| 5 | `landscape` | 36 | 14.4 | 15.2 |
| 6 | `limits` | 32 | 12.8 | 13.6 |
| 7 | `summary` | 19 | 7.6 | 8.4 |

Palabras: 199 · Narración: 80 s

## 1. `intro`

**Narración.** En 1958, Frank Rosenblatt presentó el perceptrón, la primera neurona artificial capaz de aprender a partir de ejemplos.

| Texto en pantalla | |
|---|---|
| `title` | El perceptrón |
| `subtitle` | La primera neurona que aprende |
| `credit` | Frank Rosenblatt · 1958 |

## 2. `neuron`

**Narración.** Toma unas pocas entradas, multiplica cada una por un peso, suma un sesgo y pasa el resultado por una función escalón. La salida es una sola decisión: más uno o menos uno.

| Texto en pantalla | |
|---|---|
| `header` | 1 · Una neurona |
| `inputs` | entradas |
| `sum` | suma ponderada |
| `step` | escalón |
| `output` | decisión |

## 3. `boundary`

**Narración.** Geométricamente, los pesos y el sesgo definen una recta. Los puntos de un lado se clasifican como más y los del otro lado como menos. Cambiar los pesos mueve la recta.

| Texto en pantalla | |
|---|---|
| `header` | 2 · Una recta que decide |
| `boundary` | frontera de decisión |
| `positive` | clasificado +1 |
| `negative` | clasificado −1 |

## 4. `learning`

**Narración.** Aprender significa girar estos diales. Cuando el perceptrón se equivoca con un ejemplo, mueve cada peso hacia la respuesta correcta y la recta se desplaza. Luego repite con el siguiente error.

| Texto en pantalla | |
|---|---|
| `header` | 3 · Aprender girando diales |
| `example` | ejemplo $x = (-1, -1)$, etiqueta $y = -1$ |
| `wrong` | predicción $\hat{y} = +1$: incorrecta |
| `rule` | regla de aprendizaje del perceptrón, $\eta = 0.25$ |
| `fixed` | ahora $\hat{y} = -1$: correcta |
| `next` | repetir con el siguiente error hasta que no quede ninguno |

## 5. `landscape`

**Narración.** Si medimos el error cuadrático de la suma ponderada para cada valor de los pesos, obtenemos un paisaje. Con dos pesos se convierte en un cuenco, y los mejores pesos están en su punto más bajo.

| Texto en pantalla | |
|---|---|
| `header` | 4 · El paisaje del error |
| `curve` | un peso: $w_0$ (con $w_1 = b = 1$) |
| `surface` | dos pesos: $w_0$ y $w_1$ |
| `minimum` | menor error = mejores pesos |

## 6. `limits`

**Narración.** Pero un solo perceptrón solo puede trazar una recta. En 1969, Minsky y Papert mostraron que no resuelve XOR, donde ninguna recta separa las clases. La respuesta fue apilar neuronas en capas.

| Texto en pantalla | |
|---|---|
| `header` | 5 · El límite: XOR |
| `no_line` | ninguna recta separa + y − |
| `credit` | Minsky y Papert, 1969 |
| `fix` | solución: redes multicapa |

## 7. `summary`

**Narración.** Suma ponderada, escalón y una regla para corregir errores: el perceptrón es la semilla de toda red neuronal moderna.

| Texto en pantalla | |
|---|---|
| `summary` | Suma ponderada + escalón = una decisión · Aprender es mover los pesos tras cada error · Una recta no basta: apilar capas |
