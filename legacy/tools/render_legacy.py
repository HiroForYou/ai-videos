"""
manimgl launcher for the legacy scenes. Same arguments as the manimgl CLI; adds legacy/config/custom_config.yml.

    python legacy/tools/render_legacy.py legacy/2025/perceptron/p45_51.py P45_48v2 -w

| Issue in manimgl 1.7.2 on Windows with MiKTeX | Fix |
|---|---|
| `latex` receives the XeLaTeX-only flag `-no-pdf` and pdfTeX rejects it | Drop the flag for `latex` |
| MiKTeX fails on 8.3 short temp paths (e.g. `C:/Users/ABCDEF~1`) | Expand paths to their long form |
| MiKTeX installed per user is not on PATH until a new terminal opens | Prepend its bin folder when `latex` is missing |
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import manimlib.utils.tex_file_writing as tex_file_writing

REPO_ROOT=Path(__file__).resolve().parents[2]


def _miktex_compatible_run(cmd, *args, **kwargs):
    if isinstance(cmd, list) and cmd and cmd[0]=='latex':
        fixed=[]
        for c in cmd:
            if c=='-no-pdf':
                continue
            if isinstance(c, str) and c.startswith('-output-directory='):
                c='-output-directory='+os.path.realpath(c.split('=', 1)[1])
            elif isinstance(c, Path):
                c=os.path.realpath(c)
            fixed.append(c)
        cmd=fixed
    return subprocess.run(cmd, *args, **kwargs)


tex_file_writing.subprocess=SimpleNamespace(run=_miktex_compatible_run)

if shutil.which('latex') is None:
    miktex_bin=Path(os.environ.get('LOCALAPPDATA', ''))/'Programs'/'MiKTeX'/'miktex'/'bin'/'x64'
    if miktex_bin.is_dir():
        os.environ['PATH']=str(miktex_bin)+os.pathsep+os.environ['PATH']

if __name__=='__main__':
    from manimlib.__main__ import main
    args=sys.argv[1:]
    if '--config_file' not in args:
        args+=['--config_file', str(REPO_ROOT/'legacy'/'config'/'custom_config.yml')]
    sys.argv=['manimgl', *args]
    main()
