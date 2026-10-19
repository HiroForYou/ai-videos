"""
Companion book renders for the ResNets video (colorbar for book).

Scenes
| Scene | Base class |
|---|---|
| `ColorBarForBookOne` | InteractiveScene |

Local data (paths relative to the repo root; files not in this repo)
| Variable | Path |
|---|---|
| `data_dir` | legacy/2026/resnets/data/resnet/hackin/ |

Render from the repo root with manimgl (legacy/requirements.txt)
    manimgl legacy/2026/resnets/colorbar_for_book.py ColorBarForBookOne -w
"""
from manimlib import *
import numpy as np
import matplotlib.pyplot as plt
import os

# data_dir='legacy/2026/resnets/data/resnet/hackin/'
data_dir='legacy/2026/resnets/data/resnet/hackin/'



class ColorBarForBookOne(InteractiveScene):

    def construct(self):
        img=ImageMobject(data_dir+'colorbar_for_book_1.png')
        self.add(img)

        self.frame.reorient(0, 0, 0, (np.float32(-0.04), np.float32(-0.08), np.float32(0.0)), 3.59)
        self.wait(2)
        self.embed()