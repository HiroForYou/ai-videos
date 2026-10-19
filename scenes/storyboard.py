"""
Script (guion) loader for the Manim scenes in scenes/<video>/.

Each video folder holds a script.yaml with one entry per section (Remotion uses remotion/src/<video>/script.json,
same schema):
| Field | Content |
|---|---|
| `id` | Section name; the scene calls `board.start(self, id)` |
| `narration` | Voice-over text per language |
| `text` | Strings shown on screen per language (plain strings or lists) |

Usage inside a scene
    board=Storyboard(__file__, 'es')
    T=board.text                   # flat dict of on-screen strings (later sections win on repeated keys)
    board.get('xor', 'section')    # one section's string, for keys repeated across sections
    board.start(self, 'intro')     # opens a manim section and starts its timer
    board.hold(self, reserve=1.0)  # pauses until the section covers its narration

Readable scripts (script.<lang>.md): python scripts/export_scripts.py
"""
from pathlib import Path

import yaml

WORDS_PER_SECOND=2.5  # about 150 words per minute


class Storyboard:
    def __init__(self, scene_file, lang):
        self.path=Path(scene_file).resolve().with_name('script.yaml')
        self.data=yaml.safe_load(self.path.read_text(encoding='utf-8'))
        self.lang=lang
        self.title=self.data['title'][lang]
        self.sections=self.data['sections']
        self.section_ids=[s['id'] for s in self.sections]
        self.text={}
        for section in self.sections:
            for key, value in (section.get('text') or {}).items():
                self.text[key]=value[lang]

    def get(self, section_id, key):
        """On-screen string of one section; use it for keys repeated across sections (e.g. 'section')."""
        section=next(s for s in self.sections if s['id']==section_id)
        return section['text'][key][self.lang]

    def narration(self, section_id):
        return next(s['narration'][self.lang] for s in self.sections if s['id']==section_id)

    def narration_seconds(self, section_id):
        return len(self.narration(section_id).split())/WORDS_PER_SECOND

    def start(self, scene, section_id):
        """Open a manim section (one clip with --save_sections) and start its timer."""
        assert section_id in self.section_ids, section_id
        scene.next_section(section_id)
        self._section=section_id
        self._t0=scene.renderer.time

    def hold(self, scene, reserve=1.0):
        """Wait until the section lasts as long as its narration, minus `reserve` s for the outgoing transition."""
        remaining=self.narration_seconds(self._section)-reserve-(scene.renderer.time-self._t0)
        if remaining>0.05:
            scene.wait(remaining)
