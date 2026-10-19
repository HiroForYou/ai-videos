"""
Shared visual theme for the Manim Community scenes in scenes/<video>/.

Palette: assets/theme.json (cristhianwiki.com, 'original' dark theme), shared with remotion/src/theme.ts.
Importing this module sets the scene background.
| Name | Hex | Source | Use | Contrast vs background / panel |
|---|---|---|---|---|
| `BG` | #191919 | site bg | Scene background | - |
| `PANEL` | #232323 | site surface | Cards, plots, latent space | - |
| `PANEL_STROKE` | #303030 | site border | Panel borders, axes | - |
| `TEXT` | #f8f8f8 | site text | Body text and arrows | 16.6 / 14.8 |
| `MUTED` | #b3b3b3 | site textMuted | Secondary labels | 8.4 / 7.5 |
| `PRIMARY` | #6d83f2 | site primary | Brand accent | 5.2 / 4.6 |
| `SKY` | #6a98f0 | site primaryLight | Encoders, current state, negative class | 6.2 / 5.5 |
| `SAND` | #c7d0ff | site light-theme border | Target encoder, bias, text tokens | 11.6 / 10.4 |
| `AMBER` | #f2c36d | derived (complement) | Predictor, goals, loss, positive class | 10.7 / 9.6 |
| `PINK` | #f28fb0 | derived | Masks, mistakes | 7.8 / 7.0 |
| `EMERALD` | #6fd8b4 | derived | Correct results, cursor | 10.2 / 9.1 |

Typography
| Element | Font |
|---|---|
| Text | Plus Jakarta Sans (assets/fonts/plus-jakarta-sans, SIL OFL; python scripts/fetch_fonts.py), registered at import time |
| Equations | LaTeX through `MathTex`, scaled by `EQ_SCALE` to match the text size |

Public API
| Name | Type |
|---|---|
| `label` | function |
| `eq` | function |
| `eq_label` | function |
| `card` | function |
| `mix` | function |
"""
import json
from pathlib import Path

import manimpango
from manim import RIGHT, ManimColor, MathTex, RoundedRectangle, Text, VGroup, config

_PALETTE=json.loads((Path(__file__).resolve().parents[1]/'assets'/'theme.json').read_text(encoding='utf-8'))
BG=_PALETTE['background']
PANEL=_PALETTE['panel']
PANEL_STROKE=_PALETTE['panelStroke']
TEXT=_PALETTE['text']
MUTED=_PALETTE['muted']
SKY=_PALETTE['sky']
AMBER=_PALETTE['amber']
PINK=_PALETTE['pink']
EMERALD=_PALETTE['emerald']
SAND=_PALETTE['sand']
PRIMARY=_PALETTE['primary']
PATCH_LOW=_PALETTE['patchLow']
config.background_color=BG

FONT='Plus Jakarta Sans'
EQ_SCALE=1.4  # MathTex renders smaller than Text at the same font_size
FONT_DIR=Path(__file__).resolve().parents[1]/'assets'/'fonts'/'plus-jakarta-sans'
_font_files=sorted(FONT_DIR.glob('*.ttf'))
if not _font_files:
    raise FileNotFoundError(f'{FONT} not found in {FONT_DIR}. Run: python scripts/fetch_fonts.py')
for _font_file in _font_files:
    manimpango.register_font(str(_font_file))


def mix(color_a, color_b, alpha):
    """Linear blend of two hex colors."""
    return ManimColor(color_a).interpolate(ManimColor(color_b), alpha)


def label(text, font_size=28, color=TEXT, weight='NORMAL', **kwargs):
    """Plus Jakarta Sans text. weight: NORMAL, MEDIUM, SEMIBOLD, BOLD, ULTRABOLD (ExtraBold)."""
    return Text(text, font=FONT, font_size=font_size, color=color, weight=weight, **kwargs)


def eq(tex, font_size=36, color=TEXT, **kwargs):
    """LaTeX equation in math mode."""
    return MathTex(tex, font_size=font_size*EQ_SCALE, color=color, **kwargs)


def eq_label(tex, text, font_size=28, color=TEXT, buff=0.12):
    """Equation followed by a plain-text caption, e.g. ŝ (predicted)."""
    return VGroup(eq(tex, font_size=font_size, color=color),
                  label(text, font_size=font_size, color=color)).arrange(RIGHT, buff=buff)


def card(text, width=2.0, height=1.0, color=SKY, font_size=26):
    """Dark rounded card with a colored stroke and a semibold label."""
    box=RoundedRectangle(width=width, height=height, corner_radius=0.15)
    box.set_stroke(color, 3).set_fill(PANEL, 1)
    text_mob=label(text, font_size=font_size, color=color, weight='SEMIBOLD')
    if text_mob.width>width-0.3:
        text_mob.scale_to_fit_width(width-0.3)
    return VGroup(box, text_mob.move_to(box))
