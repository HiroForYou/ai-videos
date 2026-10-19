# El perceptrón: guion (ES)

Generado desde script.yaml con scripts/export_scripts.py. El tiempo de narración asume 150 palabras por minuto.

| # | Sección | Palabras | Narración (s) | Escena (s) |
|---|---|---|---|---|
| 1 | `intro` | 26 | 10.4 | 10.4 |
| 2 | `neuron` | 47 | 18.8 | 18.8 |
| 3 | `dials` | 50 | 20.0 | 20.0 |
| 4 | `landscape` | 35 | 14.0 | 14.0 |
| 5 | `xor` | 34 | 13.6 | 13.6 |
| 6 | `step_surface` | 48 | 19.2 | 19.2 |
| 7 | `scale` | 26 | 10.4 | 10.4 |
| 8 | `summary` | 18 | 7.2 | 7.2 |

Palabras: 284 · Narración: 114 s

## 1. `intro`

**Narración.** En 1958, Frank Rosenblatt construyó el perceptrón: una sola neurona artificial que aprende a partir de ejemplos. Toda red neuronal moderna sigue usando su idea central.

| Texto en pantalla | |
|---|---|
| `title` | El perceptrón |
| `subtitle` | La primera neurona que aprende |
| `credit` | Frank Rosenblatt · 1958 |

## 2. `neuron`

**Narración.** Tomemos cuatro puntos con dos entradas cada uno. El perceptrón multiplica cada entrada por un peso, suma un sesgo y compara el resultado con la etiqueta. Para este punto la predicción es uno, pero la etiqueta es menos uno, así que el error al cuadrado es cuatro.

| Texto en pantalla | |
|---|---|
| `section` | 1 · Una neurona, cuatro puntos |
| `example` | ejemplo |

## 3. `dials`

**Narración.** Los pesos son diales que podemos girar. Mover el primer peso de menos uno a menos cero coma nueve baja el error de cuatro a tres coma sesenta y uno. Recorrer ese dial dibuja el error como una curva, con su punto más bajo donde el primer peso vale uno.

| Texto en pantalla | |
|---|---|
| `section` | 2 · Los pesos son diales |
| `sweep` | recorriendo el primer peso |
| `minimum` | menor error |

## 4. `landscape`

**Narración.** Con dos pesos, el error se convierte en una superficie sobre el plano: un cuenco suave al sumar los cuatro puntos. Aprender es bajar por la pendiente, paso a paso, hasta su punto más bajo.

| Texto en pantalla | |
|---|---|
| `section` | 3 · El paisaje del error |
| `surface` | error sobre dos pesos, los cuatro puntos |
| `descent` | descenso de gradiente |

## 5. `xor`

**Narración.** Ahora cambiemos las etiquetas a XOR. Ninguna recta separa los puntos más de los puntos menos. Dos neuronas ocultas lo resuelven: cada una traza una recta y la salida conserva la franja entre ambas.

| Texto en pantalla | |
|---|---|
| `section` | 4 · El problema XOR |
| `no_line` | ninguna recta separa + y − |
| `two_neurons` | dos neuronas ocultas, dos rectas |

## 6. `step_surface`

**Narración.** Pero con activaciones escalón, el paisaje del error está hecho de terrazas planas. La pendiente es cero casi en todas partes, así que no hay una dirección que seguir. Activaciones suaves como la sigmoide convierten las terrazas en pendientes por las que el descenso de gradiente puede bajar.

| Texto en pantalla | |
|---|---|
| `section` | 5 · Por qué activaciones suaves |
| `step` | activación escalón |
| `sigmoid` | activación sigmoide |
| `flat` | pendiente = 0 casi en todas partes |
| `smooth` | una pendiente que seguir |

## 7. `scale`

**Narración.** Activaciones suaves, muchas capas y muchos datos: si apilamos suficientes de estas neuronas y añadimos atención, obtenemos los bloques transformer de los modelos de lenguaje actuales.

| Texto en pantalla | |
|---|---|
| `section` | 6 · De una neurona a los transformers |
| `mlp` | perceptrón multicapa |
| `attention` | Atención |
| `block_mlp` | MLP |
| `blocks` | un bloque, repetido decenas de veces |

## 8. `summary`

**Narración.** Sumas ponderadas, un error que minimizar y un camino suave cuesta abajo. Ese es el legado del perceptrón.

| Texto en pantalla | |
|---|---|
| `summary` | Suma ponderada + sesgo, comparada con una etiqueta · Aprender = bajar por el error · Activaciones suaves y muchas capas lo escalan |
