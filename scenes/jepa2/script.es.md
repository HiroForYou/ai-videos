# JEPA 2: guion (ES)

Generado desde script.yaml con scripts/export_scripts.py. El tiempo de narración asume 150 palabras por minuto.

| # | Sección | Palabras | Narración (s) | Escena (s) |
|---|---|---|---|---|
| 1 | `intro` | 20 | 8.0 | 8.0 |
| 2 | `masked_prediction` | 60 | 24.0 | 24.0 |
| 3 | `planning` | 68 | 27.2 | 26.2 |
| 4 | `summary` | 18 | 7.2 | 7.2 |

Palabras: 166 · Narración: 66 s

## 1. `intro`

**Narración.** JEPA 2 es un world model de Meta. Su idea central es simple: en lugar de predecir píxeles, predice representaciones.

| Texto en pantalla | |
|---|---|
| `subtitle` | Predecir en el espacio de representaciones, no en píxeles |

## 2. `masked_prediction`

**Narración.** V-JEPA 2 se pre-entrena con más de un millón de horas de video. Se enmascara un tubo de parches en todos los cuadros. El encoder de contexto solo ve los parches visibles y un predictor estima los embeddings de los ocultos. Los objetivos salen de una media móvil exponencial del encoder y la pérdida es una distancia L1 entre embeddings.

| Texto en pantalla | |
|---|---|
| `section1` | 1 · Pre-entrenamiento con video (V-JEPA 2) |
| `video` | video |
| `mask` | tubo enmascarado |
| `predicted` | (predicho) |
| `target` | (objetivo) |
| `no_pixels` | Sin reconstruir píxeles: la pérdida compara embeddings |

## 3. `planning`

**Narración.** V-JEPA 2-AC agrega un predictor condicionado a acciones, entrenado con menos de 62 horas de video de robots. Para planificar, el robot codifica su observación actual y una imagen meta. El método de entropía cruzada muestrea secuencias de acciones, las simula en el espacio latente, conserva las que terminan más cerca de la meta y reajusta la distribución. El robot ejecuta la primera acción y vuelve a planificar.

| Texto en pantalla | |
|---|---|
| `section2` | 2 · Planificación con el world model (V-JEPA 2-AC) |
| `latent` | espacio latente |
| `cem_title` | Método de entropía cruzada |
| `cem` | muestrear secuencias de acciones · simular con el predictor · conservar las k de menor energía · reajustar la gaussiana |
| `iteration` | iteración {} |
| `mpc` | ejecutar la primera acción y re-planificar |

## 4. `summary`

**Narración.** Aprender a predecir representaciones a partir de video y luego usar ese predictor como world model para planificar.

| Texto en pantalla | |
|---|---|
| `summary` | V-JEPA 2 aprende a predecir representaciones de video · V-JEPA 2-AC usa ese predictor como world model · La planificación busca acciones que acerquen z a la meta |
