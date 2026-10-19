# Project notes for Claude Code

## Engines and skills

| Area | Engine | Skill to load first |
|---|---|---|
| `remotion/` (React videos) | Remotion 4 | `remotion-best-practices` (routes to create, markup, render, studio, captions, docs, upgrade) |
| `scenes/` (Manim videos) | Manim Community 0.22 | - |
| `legacy/` (original fork code) | manimgl 1.7.2 | - |
| READMEs, scripts (guion), docstrings | - | `documentos-profesionales` |

## Conventions

| Topic | Rule |
|---|---|
| Script (guion) | Each video has one source: `scenes/<video>/script.yaml` or `remotion/src/<video>/script.json`, with narration and on-screen text per section in EN and ES. Export readable versions with `python scripts/export_scripts.py`. |
| Languages | Every video ships in English and Spanish (scene or composition suffix `EN` / `ES`). |
| Palette | Single source `assets/theme.json`: colors of cristhianwiki.com ('original' dark theme: background `#191919`, panels `#232323`, primary `#6d83f2`) plus derived accents; read by `scenes/theme.py` and `remotion/src/theme.ts`. |
| Fonts | Manim: Plus Jakarta Sans (`python scripts/fetch_fonts.py`, not versioned). Remotion: the same family via `@remotion/google-fonts/PlusJakartaSans`. |
| Equations | Manim: `MathTex` through `eq()`. Remotion: `<Equation>` (KaTeX) and `$...$` inside `<RichText>`; no Unicode subscripts in text. |
| Legacy images | Use as inspiration only; redraw natively instead of embedding screenshots. |
| Notebooks | Outputs are never committed: the `nbstripout` git filter strips them (`nbstripout --install`). |
| Branches | `dev` (GitHub, single-commit history) is the working branch; `master` exists only locally and tracks `upstream/master`. |

## Commands

| Task | Command |
|---|---|
| Render a Manim scene | `python render.py -qh scenes/vla/vla.py VLAOverviewEN` |
| Render a legacy scene | `python legacy/tools/render_legacy.py legacy/2025/perceptron/p45_51.py P45_48v2 -w` |
| Remotion preview | `cd remotion && npm run dev` |
| Remotion render | `cd remotion && npx remotion render PerceptronEN out/perceptron-en.mp4` |

The repo path on this machine contains `(`, so use `render.py` instead of `manim`, and `legacy/tools/render_legacy.py` instead of `manimgl` (MiKTeX fixes).
