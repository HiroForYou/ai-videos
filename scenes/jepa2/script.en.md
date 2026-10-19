# JEPA 2: script (EN)

Generated from script.yaml by scripts/export_scripts.py. Narration time assumes 150 words per minute.

| # | Section | Words | Narration (s) | Scene (s) |
|---|---|---|---|---|
| 1 | `intro` | 20 | 8.0 | 8.0 |
| 2 | `masked_prediction` | 59 | 23.6 | 23.6 |
| 3 | `planning` | 61 | 24.4 | 23.4 |
| 4 | `summary` | 16 | 6.4 | 6.7 |

Words: 156 · Narration: 62 s

## 1. `intro`

**Narration.** JEPA 2 is a world model from Meta. Its core idea is simple: instead of predicting pixels, it predicts representations.

| On-screen text | |
|---|---|
| `subtitle` | Predict in representation space, not in pixels |

## 2. `masked_prediction`

**Narration.** V-JEPA 2 is pretrained on more than a million hours of video. A tube of patches is masked across every frame. The context encoder sees only the visible patches, and a predictor estimates the embeddings of the hidden ones. The targets come from an exponential moving average of the encoder, and the loss is an L1 distance between embeddings.

| On-screen text | |
|---|---|
| `section1` | 1 · Video pretraining (V-JEPA 2) |
| `video` | video |
| `mask` | masked tube |
| `predicted` | (predicted) |
| `target` | (target) |
| `no_pixels` | No pixel reconstruction: the loss compares embeddings |

## 3. `planning`

**Narration.** V-JEPA 2-AC adds an action-conditioned predictor, trained on less than 62 hours of robot video. To plan, the robot encodes its current observation and a goal image. The cross-entropy method samples action sequences, rolls them out in latent space, keeps the ones that end closest to the goal and refits the distribution. The robot executes the first action and plans again.

| On-screen text | |
|---|---|
| `section2` | 2 · Planning with the world model (V-JEPA 2-AC) |
| `latent` | latent space |
| `cem_title` | Cross-entropy method |
| `cem` | sample action sequences · roll out the predictor · keep the k lowest-energy · refit the Gaussian |
| `iteration` | iteration {} |
| `mpc` | execute the first action, then replan |

## 4. `summary`

**Narration.** Learn to predict representations from video, then use that predictor as a world model to plan.

| On-screen text | |
|---|---|
| `summary` | V-JEPA 2 learns to predict video representations · V-JEPA 2-AC uses that predictor as a world model · Planning searches for actions that move z toward the goal |
