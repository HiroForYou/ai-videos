# The Perceptron: script (EN)

Generated from script.yaml by scripts/export_scripts.py. Narration time assumes 150 words per minute.

| # | Section | Words | Narration (s) | Scene (s) |
|---|---|---|---|---|
| 1 | `intro` | 24 | 9.6 | 9.6 |
| 2 | `neuron` | 44 | 17.6 | 17.6 |
| 3 | `dials` | 48 | 19.2 | 19.2 |
| 4 | `landscape` | 32 | 12.8 | 12.8 |
| 5 | `xor` | 35 | 14.0 | 14.0 |
| 6 | `step_surface` | 41 | 16.4 | 16.4 |
| 7 | `scale` | 25 | 10.0 | 10.0 |
| 8 | `summary` | 18 | 7.2 | 7.2 |

Words: 267 · Narration: 107 s

## 1. `intro`

**Narration.** In 1958 Frank Rosenblatt built the perceptron: a single artificial neuron that learns from examples. Every modern neural network still uses its core idea.

| On-screen text | |
|---|---|
| `title` | The Perceptron |
| `subtitle` | The first neuron that learns |
| `credit` | Frank Rosenblatt · 1958 |

## 2. `neuron`

**Narration.** Take four points with two inputs each. The perceptron multiplies each input by a weight, adds a bias and compares the result with the label. For this point the prediction is one, but the label is minus one, so the squared error is four.

| On-screen text | |
|---|---|
| `section` | 1 · One neuron, four points |
| `example` | example |

## 3. `dials`

**Narration.** The weights are dials we can turn. Nudging the first weight from minus one to minus zero point nine lowers the error from four to three point six one. Sweeping that dial traces the error as a curve, with its lowest point where the first weight equals one.

| On-screen text | |
|---|---|
| `section` | 2 · Weights are dials |
| `sweep` | sweeping the first weight |
| `minimum` | lowest error |

## 4. `landscape`

**Narration.** With two weights the error becomes a surface over the plane, a smooth bowl when we add up all four points. Learning means walking downhill, step by step, to its lowest point.

| On-screen text | |
|---|---|
| `section` | 3 · The error landscape |
| `surface` | error over two weights, all four points |
| `descent` | gradient descent |

## 5. `xor`

**Narration.** Now change the labels to XOR. No single line separates the plus points from the minus points. Two hidden neurons solve it: each one draws a line, and the output keeps the band between them.

| On-screen text | |
|---|---|
| `section` | 4 · The XOR problem |
| `no_line` | no single line separates + and − |
| `two_neurons` | two hidden neurons, two lines |

## 6. `step_surface`

**Narration.** But with step activations the error landscape is made of flat terraces. The slope is zero almost everywhere, so there is no direction to follow. Smooth activations like the sigmoid turn the terraces into slopes that gradient descent can walk down.

| On-screen text | |
|---|---|
| `section` | 5 · Why smooth activations |
| `step` | step activation |
| `sigmoid` | sigmoid activation |
| `flat` | slope = 0 almost everywhere |
| `smooth` | a slope to follow |

## 7. `scale`

**Narration.** Smooth activations, many layers and lots of data: stack enough of these neurons, add attention, and you get the transformer blocks inside today's language models.

| On-screen text | |
|---|---|
| `section` | 6 · From one neuron to transformers |
| `mlp` | multilayer perceptron |
| `attention` | Attention |
| `block_mlp` | MLP |
| `blocks` | one block, repeated dozens of times |

## 8. `summary`

**Narration.** Weighted sums, an error to minimize and a smooth path downhill. That is the legacy of the perceptron.

| On-screen text | |
|---|---|
| `summary` | Weighted sum + bias, compared with a label · Learning = walking downhill on the error · Smooth activations and many layers scale it up |
