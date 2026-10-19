"""
Download the fonts used by the Manim scenes into assets/fonts/ (not versioned).

    python scripts/fetch_fonts.py

| Font | Source | License | Files |
|---|---|---|---|
| Plus Jakarta Sans 2.7.1 | github.com/tokotype/PlusJakartaSans (release zip) | SIL OFL 1.1 | Regular, Medium, SemiBold, Bold, ExtraBold, OFL.txt |

Remotion compositions load the same family through @remotion/google-fonts and do not need these files.
"""
import io
import urllib.request
import zipfile
from pathlib import Path

URL='https://github.com/tokotype/PlusJakartaSans/releases/download/2.7.1/PlusJakartaSans-2.7.1.zip'
WEIGHTS=['Regular', 'Medium', 'SemiBold', 'Bold', 'ExtraBold']
TARGET=Path(__file__).resolve().parents[1]/'assets'/'fonts'/'plus-jakarta-sans'


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(URL, timeout=60) as response:
        archive=zipfile.ZipFile(io.BytesIO(response.read()))
    wanted={f'PlusJakartaSans-{w}.ttf' for w in WEIGHTS} | {'OFL.txt'}
    for member in archive.namelist():
        name=member.rsplit('/', 1)[-1]
        if name in wanted and ('/ttf/' in member or name=='OFL.txt'):
            (TARGET/name).write_bytes(archive.read(member))
            print('saved', (TARGET/name).relative_to(TARGET.parents[2]))


if __name__=='__main__':
    main()
