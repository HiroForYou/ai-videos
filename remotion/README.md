# Remotion videos

React compositions rendered with [Remotion](https://www.remotion.dev/). Same palette (`assets/theme.json`) and typeface (Plus Jakarta Sans) as the Manim scenes, KaTeX equations.

## Compositions

| Folder | Composition | Language | Source |
|---|---|---|---|
| Perceptron | `PerceptronEN` | English | `src/perceptron/Perceptron.tsx` |
| Perceptron | `PerceptronES` | Spanish | `src/perceptron/Perceptron.tsx` |

## Structure

```
src/
├── Root.tsx                 composition registry
├── theme.ts                 palette from ../assets/theme.json, Plus Jakarta Sans (@remotion/google-fonts), safe area
├── components/              Equation (KaTeX), RichText ($...$ inline math), Dial, SceneHeader
└── perceptron/
    ├── Perceptron.tsx       TransitionSeries with one sequence per script section
    ├── script.json          script (guion): narration and on-screen text per section, EN/ES
    ├── script.ts            typed access; section length = narration at 150 words per minute
    ├── script.en.md, script.es.md   readable script (python scripts/export_scripts.py)
    └── scenes/              Intro, Neuron, Boundary, Learning, Landscape, Limits, Summary
```

## Commands

Run from this folder (`remotion/`). Requires Node.js 20.19 or later.

| Task | Command |
|---|---|
| Install | `npm i` |
| Preview in Studio | `npm run dev` |
| Render a video | `npx remotion render PerceptronEN out/perceptron-en.mp4` |
| Render frames as PNG | `npx remotion render PerceptronEN out/frames --frames=0,300,900 --image-format=png` |
| Type check and lint | `npm run lint` |

When Studio is running on port 3000, add `--port=3123` to render commands.

## Agent skills

The official Remotion skills are installed for Claude Code in `.claude/skills/` at the repo root (versions pinned in `skills-lock.json`). `remotion-best-practices` routes to the rest.

| Task | Command (repo root) |
|---|---|
| Update skills | `npx skills update -p` |
| List installed skills | `npx skills list` |
