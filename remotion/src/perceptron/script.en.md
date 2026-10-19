# The Perceptron: script (EN)

Generated from script.json by scripts/export_scripts.py. Narration time assumes 150 words per minute.

| # | Section | Words | Narration (s) | Scene (s) |
|---|---|---|---|---|
| 1 | `intro` | 16 | 6.4 | 7.2 |
| 2 | `neuron` | 33 | 13.2 | 14.0 |
| 3 | `boundary` | 30 | 12.0 | 12.8 |
| 4 | `learning` | 31 | 12.4 | 13.2 |
| 5 | `landscape` | 36 | 14.4 | 15.2 |
| 6 | `limits` | 35 | 14.0 | 14.8 |
| 7 | `summary` | 19 | 7.6 | 8.4 |

Words: 200 · Narration: 80 s

## 1. `intro`

**Narration.** In 1958 Frank Rosenblatt introduced the perceptron, the first artificial neuron that could learn from examples.

| On-screen text | |
|---|---|
| `title` | The Perceptron |
| `subtitle` | The first neuron that learns |
| `credit` | Frank Rosenblatt · 1958 |

## 2. `neuron`

**Narration.** It takes a few inputs, multiplies each one by a weight, adds a bias and passes the sum through a step function. The output is a single decision: plus one or minus one.

| On-screen text | |
|---|---|
| `header` | 1 · One neuron |
| `inputs` | inputs |
| `sum` | weighted sum |
| `step` | step |
| `output` | decision |

## 3. `boundary`

**Narration.** Geometrically, the weights and the bias define a line. Points on one side are classified as plus, points on the other side as minus. Changing the weights moves the line.

| On-screen text | |
|---|---|
| `header` | 2 · A line that decides |
| `boundary` | decision boundary |
| `positive` | classified +1 |
| `negative` | classified −1 |

## 4. `learning`

**Narration.** Learning means turning these dials. When the perceptron gets an example wrong, it nudges each weight toward the correct answer, and the line moves. Then it repeats with the next mistake.

| On-screen text | |
|---|---|
| `header` | 3 · Learning by turning dials |
| `example` | example $x = (-1, -1)$, label $y = -1$ |
| `wrong` | prediction $\hat{y} = +1$: wrong |
| `rule` | perceptron learning rule, $\eta = 0.25$ |
| `fixed` | now $\hat{y} = -1$: correct |
| `next` | repeat with the next mistake until none remain |

## 5. `landscape`

**Narration.** If we measure the squared error of the weighted sum for every value of the weights, we get a landscape. With two weights it becomes a bowl, and the best weights sit at its lowest point.

| On-screen text | |
|---|---|
| `header` | 4 · The error landscape |
| `curve` | one weight: $w_0$ (with $w_1 = b = 1$) |
| `surface` | two weights: $w_0$ and $w_1$ |
| `minimum` | lowest error = best weights |

## 6. `limits`

**Narration.** But a single perceptron can only draw one line. In 1969 Minsky and Papert showed that it cannot solve XOR, where no straight line separates the classes. The answer was to stack neurons in layers.

| On-screen text | |
|---|---|
| `header` | 5 · The limit: XOR |
| `no_line` | no single line separates + and − |
| `credit` | Minsky & Papert, 1969 |
| `fix` | solution: multilayer networks |

## 7. `summary`

**Narration.** Weighted sum, step, and a rule to fix mistakes: the perceptron is the seed of every modern neural network.

| On-screen text | |
|---|---|
| `summary` | Weighted sum + step = one decision · Learning nudges the weights after each mistake · One line is not enough: stack layers |
