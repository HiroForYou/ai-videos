"""
Export readable scripts (guion) for every video: script.<lang>.md next to each script source.

    python scripts/export_scripts.py                         # all videos
    python scripts/export_scripts.py remotion/src/perceptron # one folder

| Engine | Script source | Scene duration column |
|---|---|---|
| Manim | scenes/<video>/script.yaml | Measured from the newest `--save_sections` render, else "not rendered" |
| Remotion | remotion/src/<video>/script.json | Narration + 0.8 s, the rule in remotion/src/<video>/script.ts |

Narration time assumes 150 words per minute (scenes/storyboard.py, remotion script.ts).
Measured durations come from, e.g.: python render.py -qh --save_sections scenes/jepa2/jepa2.py JEPA2OverviewEN
"""
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT=Path(__file__).resolve().parents[1]
SCENES_DIR=REPO_ROOT/'scenes'
REMOTION_DIR=REPO_ROOT/'remotion'/'src'
WORDS_PER_SECOND=2.5
REMOTION_TAIL_SECONDS=0.8

LABELS={
    'en': ('Script', 'Section', 'Narration', 'Words', 'Narration (s)', 'Scene (s)', 'On-screen text', 'not rendered',
           'Generated from {source} by scripts/export_scripts.py. Narration time assumes 150 words per minute.'),
    'es': ('Guion', 'Sección', 'Narración', 'Palabras', 'Narración (s)', 'Escena (s)', 'Texto en pantalla', 'sin render',
           'Generado desde {source} con scripts/export_scripts.py. El tiempo de narración asume 150 palabras por minuto.'),
}


def measured_durations(video, scene_name):
    """Section durations (s) from the newest --save_sections render, if any."""
    candidates=sorted((REPO_ROOT/'videos'/video).glob(f'*/sections/{scene_name}.json'),
                      key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        return {}
    entries=json.loads(candidates[0].read_text(encoding='utf-8'))
    return {e['name']: float(e['duration']) for e in entries if 'duration' in e}


def export_markdown(video_dir):
    video=video_dir.name
    source=video_dir/'script.yaml'
    remotion=not source.exists()
    if remotion:
        source=video_dir/'script.json'  # YAML is a superset of JSON
    data=yaml.safe_load(source.read_text(encoding='utf-8'))
    for lang in data['languages']:
        title, h_sec, h_nar, h_words, h_nar_s, h_scene_s, h_text, not_rendered, note=LABELS[lang]
        measured={} if remotion else measured_durations(video, f'{video.upper()}Overview{lang.upper()}')
        lines=[f"# {data['title'][lang]}: {title.lower()} ({lang.upper()})", '', note.format(source=source.name), '',
               f'| # | {h_sec} | {h_words} | {h_nar_s} | {h_scene_s} |', '|---|---|---|---|---|']
        total_words=0
        for i, section in enumerate(data['sections'], 1):
            words=len(section['narration'][lang].split())
            total_words+=words
            if remotion:
                scene_s=f'{words/WORDS_PER_SECOND+REMOTION_TAIL_SECONDS:.1f}'
            else:
                scene_s=f"{measured[section['id']]:.1f}" if section['id'] in measured else not_rendered
            lines.append(f"| {i} | `{section['id']}` | {words} | {words/WORDS_PER_SECOND:.1f} | {scene_s} |")
        lines+=['', f'{h_words}: {total_words} · {h_nar}: {total_words/WORDS_PER_SECOND:.0f} s', '']
        for i, section in enumerate(data['sections'], 1):
            lines+=[f"## {i}. `{section['id']}`", '', f"**{h_nar}.** {section['narration'][lang]}", '']
            texts=section.get('text') or {}
            if texts:
                lines+=[f'| {h_text} | |', '|---|---|']
                for key, value in texts.items():
                    shown=' · '.join(value[lang]) if isinstance(value[lang], list) else value[lang]
                    lines.append(f'| `{key}` | {shown} |')
                lines.append('')
        out=video_dir/f'script.{lang}.md'
        out.write_text('\n'.join(lines), encoding='utf-8')
        print('wrote', out.relative_to(REPO_ROOT))


def main():
    targets=[Path(a) for a in sys.argv[1:]] or (sorted(p.parent for p in SCENES_DIR.glob('*/script.yaml'))
                                                + sorted(p.parent for p in REMOTION_DIR.glob('*/script.json')))
    for target in targets:
        export_markdown(target.resolve())


if __name__=='__main__':
    main()
