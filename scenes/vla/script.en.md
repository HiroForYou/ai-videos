# VLA: script (EN)

Generated from script.yaml by scripts/export_scripts.py. Narration time assumes 150 words per minute.

| # | Section | Words | Narration (s) | Scene (s) |
|---|---|---|---|---|
| 1 | `intro` | 12 | 4.8 | 4.8 |
| 2 | `inputs` | 47 | 18.8 | 18.8 |
| 3 | `flow_matching` | 43 | 17.2 | 16.3 |
| 4 | `execution` | 14 | 5.6 | 9.8 |
| 5 | `summary` | 13 | 5.2 | 6.7 |

Words: 129 · Narration: 52 s

## 1. `intro`

**Narration.** Vision-language-action models turn camera images and a text instruction into robot motion.

| On-screen text | |
|---|---|
| `tagline` | from pixels and instructions to robot motion |

## 2. `inputs`

**Narration.** A model like π0 reads three cameras, the instruction and the joint state of the robot. SigLIP turns each image into tokens and the instruction is tokenized. The full sequence goes through the PaliGemma vision-language model, and a smaller action expert attends to all of its tokens.

| On-screen text | |
|---|---|
| `section1` | 1 · Inputs and tokens |
| `cams` | base camera · left wrist · right wrist |
| `sequence` | token sequence |
| `attends` | attends to every VLM token |

## 3. `flow_matching`

**Narration.** The action expert does not output a single action. It generates a chunk of 50 future actions with flow matching. During training it learns a velocity field that moves noise toward real actions. At inference it integrates that field in ten Euler steps.

| On-screen text | |
|---|---|
| `section2` | 2 · Action expert with flow matching |
| `context` | context |
| `x_axis` | chunk step |
| `y_axis` | action per joint |
| `train` | training |
| `infer` | inference: 10 Euler steps |
| `noise` | noise |
| `chunk` | action chunk |

## 4. `execution`

**Narration.** The robot executes the chunk, observes the scene again and generates the next one.

| On-screen text | |
|---|---|
| `section3` | 3 · Chunk execution |
| `replan` | Each chunk runs open-loop; then the robot observes and predicts again |

## 5. `summary`

**Narration.** Tokens in, an action chunk out, and a new plan at every step.

| On-screen text | |
|---|---|
| `summary` | Vision, language and state enter the VLM as tokens · The action expert generates an action chunk with flow matching · The robot executes the chunk and replans |
