# Backpropagation, part 1: script (EN)

Generated from script.yaml by scripts/export_scripts.py. Narration time assumes 150 words per minute.

| # | Section | Words | Narration (s) | Scene (s) |
|---|---|---|---|---|
| 1 | `intro` | 38 | 15.2 | not rendered |
| 2 | `next_token` | 34 | 13.6 | not rendered |
| 3 | `loss` | 44 | 17.6 | not rendered |
| 4 | `two_weights` | 39 | 15.6 | not rendered |
| 5 | `gradient` | 36 | 14.4 | not rendered |
| 6 | `slices` | 47 | 18.8 | not rendered |
| 7 | `landscape` | 40 | 16.0 | not rendered |
| 8 | `hidden_valley` | 44 | 17.6 | not rendered |
| 9 | `fit` | 40 | 16.0 | not rendered |
| 10 | `summary` | 33 | 13.2 | not rendered |

Words: 395 · Narration: 158 s

## 1. `intro`

**Narration.** Training a neural network means nudging over a billion numbers until its predictions improve. Backpropagation tells us which way to nudge each one. In this first part we look at the loss landscape of a real language model.

| On-screen text | |
|---|---|
| `title` | Backpropagation |
| `part` | Part 1 |
| `subtitle` | Finding the way downhill |
| `credit` | Llama 3.2 1B · 1,235,814,400 parameters |

## 2. `next_token`

**Narration.** We give Llama 3.2 the text: the capital of France is. The model returns a probability for each of its 128,256 tokens. Paris gets 39 percent; a, the, one and also follow far behind.

| On-screen text | |
|---|---|
| `section` | 1 · Predicting the next token |
| `prompt` | The capital of France is |
| `vocab` | probability over 128,256 tokens |

## 3. `loss`

**Narration.** The prediction is scored with the loss, minus the log of the probability of the right answer. At 39 percent the loss is 0.94. As the probability of Paris approaches one, the loss falls to zero; as it approaches zero, the loss shoots up.

| On-screen text | |
|---|---|
| `section` | 2 · Measuring the error |
| `probability` | probability of Paris |
| `loss_label` | loss |

## 4. `two_weights`

**Narration.** Now pick two of the 1.2 billion parameters, both in the last layer, and call them theta one and theta two. Sweeping both across a range and recomputing the loss at every point draws a surface, the loss landscape.

| On-screen text | |
|---|---|
| `section` | 3 · Two weights, one surface |
| `layer` | two weights of the last layer |
| `surface` | loss over two weights |

## 5. `gradient`

**Narration.** At any point the gradient points where the loss climbs fastest. Stepping against it, again and again, walks the two weights downhill to the bottom of the bowl, and the loss drops from 1.7 to 0.3.

| On-screen text | |
|---|---|
| `section` | 4 · Following the gradient |
| `overhead` | seen from above |
| `descent` | gradient descent |

## 6. `slices`

**Narration.** A real model has far more than two directions. A common view picks one random direction through all the parameters and plots the loss along it. With random weights the curve is high and jagged; after training it has a deep, smooth valley at the trained weights.

| On-screen text | |
|---|---|
| `section` | 5 · Slices through a billion dimensions |
| `random` | random weights |
| `trained` | trained weights |

## 7. `landscape`

**Narration.** Two random directions through the first eight layers give a two dimensional view. While the model trains on this sentence, the landscape itself changes. A valley opens under the current weights and the loss falls from 14 to about 1.

| On-screen text | |
|---|---|
| `section` | 6 · A landscape that moves |
| `step` | training step |
| `current` | current weights |

## 8. `hidden_valley`

**Narration.** Gradient descent only sees the local slope. On this surface the deepest point is a narrow valley off to the side. From far away the slope points at the center of the bowl; only near the center does the valley pull the path in.

| On-screen text | |
|---|---|
| `section` | 7 · Hidden valleys |
| `valley` | hidden valley |

## 9. `fit`

**Narration.** The same picture holds for the smallest model, a line with a slope and an intercept fit to twenty points. Every point of the loss surface is one line, and gradient descent moves the line until it fits the data.

| On-screen text | |
|---|---|
| `section` | 8 · The same idea, small |
| `data_fit` | data fitting |
| `loss_surface` | loss surface |
| `slope` | slope |
| `intercept` | intercept |

## 10. `summary`

**Narration.** Every step needs the slope of the loss for every parameter, 1,235,814,400 of them in this model. Backpropagation computes all of them in one backward pass through the network; part two shows how.

| On-screen text | |
|---|---|
| `summary` | One loss, 1,235,814,400 parameters · One slope per parameter · Backpropagation: every slope in one backward pass |
| `next_part` | Part 2: how backpropagation computes the slopes |
