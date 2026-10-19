# VLA: guion (ES)

Generado desde script.yaml con scripts/export_scripts.py. El tiempo de narración asume 150 palabras por minuto.

| # | Sección | Palabras | Narración (s) | Escena (s) |
|---|---|---|---|---|
| 1 | `intro` | 20 | 8.0 | 8.0 |
| 2 | `inputs` | 51 | 20.4 | 20.4 |
| 3 | `flow_matching` | 42 | 16.8 | 15.9 |
| 4 | `execution` | 14 | 5.6 | 9.8 |
| 5 | `summary` | 15 | 6.0 | 6.7 |

Palabras: 142 · Narración: 57 s

## 1. `intro`

**Narración.** Los modelos de visión, lenguaje y acción convierten imágenes de cámara y una instrucción de texto en movimientos del robot.

| Texto en pantalla | |
|---|---|
| `tagline` | de píxeles e instrucciones a movimientos del robot |

## 2. `inputs`

**Narración.** Un modelo como π0 lee tres cámaras, la instrucción y el estado de las articulaciones del robot. SigLIP convierte cada imagen en tokens y la instrucción se tokeniza. La secuencia completa pasa por el modelo de visión y lenguaje PaliGemma, y un action expert más pequeño atiende a todos sus tokens.

| Texto en pantalla | |
|---|---|
| `section1` | 1 · Entradas y tokens |
| `cams` | cámara base · muñeca izq. · muñeca der. |
| `sequence` | secuencia de tokens |
| `attends` | atiende a todos los tokens del VLM |

## 3. `flow_matching`

**Narración.** El action expert no produce una sola acción. Genera un chunk de 50 acciones futuras con flow matching. En entrenamiento aprende un campo de velocidades que lleva el ruido hacia acciones reales. En inferencia integra ese campo en diez pasos de Euler.

| Texto en pantalla | |
|---|---|
| `section2` | 2 · Action expert con flow matching |
| `context` | contexto |
| `x_axis` | paso del chunk |
| `y_axis` | acción por articulación |
| `train` | entrenamiento |
| `infer` | inferencia: 10 pasos de Euler |
| `noise` | ruido |
| `chunk` | chunk de acciones |

## 4. `execution`

**Narración.** El robot ejecuta el chunk, vuelve a observar la escena y genera el siguiente.

| Texto en pantalla | |
|---|---|
| `section3` | 3 · Ejecución del chunk |
| `replan` | Cada chunk se ejecuta en lazo abierto; luego el robot observa y predice de nuevo |

## 5. `summary`

**Narración.** Entran tokens, sale un chunk de acciones y hay un plan nuevo en cada paso.

| Texto en pantalla | |
|---|---|
| `summary` | Visión, lenguaje y estado entran al VLM como tokens · El action expert genera un chunk de acciones con flow matching · El robot ejecuta el chunk y vuelve a planificar |
