"""
Manim Community launcher. Same arguments as the manim CLI.

    python render.py -qh scenes/vla_overview.py VLAOverviewEN

| Issue in manim 0.22 | Fix |
|---|---|
| The scene module name is built from the absolute path and passed to `warnings.filterwarnings` as a regex; paths with `(`, `)` or `+` (e.g. `C:/Users/Name(Org)`) fail with `re.error` | Escape the module name |
| MiKTeX installed per user is not on PATH until a new terminal opens | Prepend its bin folder when `latex` is missing |

On paths without regex characters, `manim <args>` works the same.
"""
import os
import re
import shutil
import sys
import warnings
from pathlib import Path
from types import SimpleNamespace

import manim.utils.module_ops as module_ops


def _filterwarnings_escaped(action, message='', category=Warning, module='', lineno=0, append=False):
    return warnings.filterwarnings(action, message, category, re.escape(module) if module else module, lineno, append)


module_ops.warnings=SimpleNamespace(filterwarnings=_filterwarnings_escaped)

if shutil.which('latex') is None:
    miktex_bin=Path(os.environ.get('LOCALAPPDATA', ''))/'Programs'/'MiKTeX'/'miktex'/'bin'/'x64'
    if miktex_bin.is_dir():
        os.environ['PATH']=str(miktex_bin)+os.pathsep+os.environ['PATH']

if __name__=='__main__':
    from manim.__main__ import main
    sys.argv=['manim', *sys.argv[1:]]
    main()
