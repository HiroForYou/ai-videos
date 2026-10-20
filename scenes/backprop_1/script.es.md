# Retropropagación, parte 1: guion (ES)

Generado desde script.yaml con scripts/export_scripts.py. El tiempo de narración asume 150 palabras por minuto.

| # | Sección | Palabras | Narración (s) | Escena (s) |
|---|---|---|---|---|
| 1 | `intro` | 41 | 16.4 | sin render |
| 2 | `next_token` | 38 | 15.2 | sin render |
| 3 | `loss` | 48 | 19.2 | sin render |
| 4 | `two_weights` | 42 | 16.8 | sin render |
| 5 | `gradient` | 40 | 16.0 | sin render |
| 6 | `slices` | 53 | 21.2 | sin render |
| 7 | `landscape` | 45 | 18.0 | sin render |
| 8 | `hidden_valley` | 41 | 16.4 | sin render |
| 9 | `fit` | 43 | 17.2 | sin render |
| 10 | `summary` | 34 | 13.6 | sin render |

Palabras: 425 · Narración: 170 s

## 1. `intro`

**Narración.** Entrenar una red neuronal es ajustar más de mil millones de números hasta que sus predicciones mejoren. La retropropagación indica hacia dónde mover cada uno. En esta primera parte vemos el paisaje de la pérdida de un modelo de lenguaje real.

| Texto en pantalla | |
|---|---|
| `title` | Retropropagación |
| `part` | Parte 1 |
| `subtitle` | Encontrar el camino cuesta abajo |
| `credit` | Llama 3.2 1B · 1.235.814.400 parámetros |

## 2. `next_token`

**Narración.** Le damos a Llama 3.2 el texto: the capital of France is. El modelo devuelve una probabilidad para cada uno de sus 128.256 tokens. Paris recibe un 39 por ciento; a, the, one y also quedan muy atrás.

| Texto en pantalla | |
|---|---|
| `section` | 1 · Predecir el siguiente token |
| `prompt` | The capital of France is |
| `vocab` | probabilidad sobre 128.256 tokens |

## 3. `loss`

**Narración.** La predicción se evalúa con la pérdida, menos el logaritmo de la probabilidad de la respuesta correcta. Con 39 por ciento la pérdida es 0,94. Si la probabilidad de Paris se acerca a uno, la pérdida baja a cero; si se acerca a cero, la pérdida se dispara.

| Texto en pantalla | |
|---|---|
| `section` | 2 · Medir el error |
| `probability` | probabilidad de Paris |
| `loss_label` | pérdida |

## 4. `two_weights`

**Narración.** Ahora elegimos dos de los 1.200 millones de parámetros, ambos en la última capa, y los llamamos theta uno y theta dos. Recorrer ambos en un rango y recalcular la pérdida en cada punto dibuja una superficie, el paisaje de la pérdida.

| Texto en pantalla | |
|---|---|
| `section` | 3 · Dos pesos, una superficie |
| `layer` | dos pesos de la última capa |
| `surface` | pérdida sobre dos pesos |

## 5. `gradient`

**Narración.** En cada punto, el gradiente apunta hacia donde la pérdida sube más rápido. Dar pasos en contra, una y otra vez, lleva los dos pesos cuesta abajo hasta el fondo del cuenco, y la pérdida baja de 1,7 a 0,3.

| Texto en pantalla | |
|---|---|
| `section` | 4 · Seguir el gradiente |
| `overhead` | vista desde arriba |
| `descent` | descenso de gradiente |

## 6. `slices`

**Narración.** Un modelo real tiene muchas más de dos direcciones. Una vista habitual elige una dirección aleatoria a través de todos los parámetros y grafica la pérdida a lo largo de ella. Con pesos aleatorios la curva es alta y dentada; tras el entrenamiento tiene un valle profundo y suave en los pesos entrenados.

| Texto en pantalla | |
|---|---|
| `section` | 5 · Cortes en mil millones de dimensiones |
| `random` | pesos aleatorios |
| `trained` | pesos entrenados |

## 7. `landscape`

**Narración.** Dos direcciones aleatorias a través de las primeras ocho capas dan una vista en dos dimensiones. Mientras el modelo entrena con esta frase, el propio paisaje cambia. Se abre un valle bajo los pesos actuales y la pérdida baja de 14 a cerca de 1.

| Texto en pantalla | |
|---|---|
| `section` | 6 · Un paisaje que se mueve |
| `step` | paso de entrenamiento |
| `current` | pesos actuales |

## 8. `hidden_valley`

**Narración.** El descenso de gradiente solo ve la pendiente local. En esta superficie el punto más profundo es un valle estrecho a un costado. Desde lejos, la pendiente apunta al centro del cuenco; solo cerca del centro el valle atrae la trayectoria.

| Texto en pantalla | |
|---|---|
| `section` | 7 · Valles ocultos |
| `valley` | valle oculto |

## 9. `fit`

**Narración.** La misma imagen vale para el modelo más pequeño, una recta con pendiente e intercepto ajustada a veinte puntos. Cada punto de la superficie de pérdida es una recta, y el descenso de gradiente la mueve hasta que se ajusta a los datos.

| Texto en pantalla | |
|---|---|
| `section` | 8 · La misma idea, en pequeño |
| `data_fit` | ajuste de datos |
| `loss_surface` | superficie de pérdida |
| `slope` | pendiente |
| `intercept` | intercepto |

## 10. `summary`

**Narración.** Cada paso necesita la pendiente de la pérdida para cada parámetro, 1.235.814.400 en este modelo. La retropropagación las calcula todas en una sola pasada hacia atrás por la red; la parte dos muestra cómo.

| Texto en pantalla | |
|---|---|
| `summary` | Una pérdida, 1.235.814.400 parámetros · Una pendiente por parámetro · Retropropagación: todas las pendientes en una pasada hacia atrás |
| `next_part` | Parte 2: cómo la retropropagación calcula las pendientes |
