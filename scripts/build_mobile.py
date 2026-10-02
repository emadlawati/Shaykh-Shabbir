"""Build self-contained phone copies of the session files.

Session files in Usul/الجلسات, علم النحو/الجلسات and بلاغة/الجلسات load shared
assets from Usul/Resources/lesson_assets (lesson.css/js, and for Nahw and
Balagha also lugha.css/js and the Amiri Quran font), so a single file opened on
a phone has no styling or tabs. This script inlines them into a copy under each
track's الجلسات/للجوال/, keeps links between sessions (in any track) pointing at
their phone copies, and turns every other local link into its GitHub page so it
opens in the phone's browser.

Run after every change to a session file:  python scripts/build_mobile.py
"""

from __future__ import annotations

import base64
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
TRACKS = [ROOT / "Usul" / "الجلسات", ROOT / "علم النحو" / "الجلسات", ROOT / "بلاغة" / "الجلسات"]
ASSETS = ROOT / "Usul" / "Resources" / "lesson_assets"
GITHUB = "https://github.com/emadlawati/Shaykh-Shabbir/blob/main/"

STYLESHEET = re.compile(r'<link rel="stylesheet" href="[^"]*lesson_assets/(\w+\.css)">')
SCRIPT = re.compile(r'<script src="[^"]*lesson_assets/(\w+\.js)"></script>')
HREF = re.compile(r'href="([^"#:]+)(#[^"]*)?"')
FONT = re.compile(r'url\("(fonts/[^"]+\.woff2)"\)')


def asset(name: str) -> str:
    text = (ASSETS / name).read_text(encoding="utf-8")
    if name.endswith(".css"):  # embed the font so the copy needs nothing beside it
        text = FONT.sub(lambda m: 'url("data:font/woff2;base64,'
                        + base64.b64encode((ASSETS / m.group(1)).read_bytes()).decode() + '")', text)
    return text


def rewrite_link(match: re.Match, source: Path, out: Path, sessions: set[Path]) -> str:
    target, fragment = match.group(1), match.group(2) or ""
    resolved = (source.parent / unquote(target)).resolve()
    if resolved in sessions:
        phone = resolved.parent / "للجوال" / resolved.name
        return f'href="{Path(os.path.relpath(phone, out)).as_posix().replace(" ", "%20")}{fragment}"'
    return f'href="{GITHUB}{quote(resolved.relative_to(ROOT).as_posix())}{fragment}" target="_blank" rel="noopener"'


def main() -> int:
    sources = [p for track in TRACKS for p in sorted(track.glob("*.html"))]
    sessions = {p.resolve() for p in sources}
    for source in sources:
        out = source.parent / "للجوال"
        out.mkdir(exist_ok=True)
        html = source.read_text(encoding="utf-8")
        if not STYLESHEET.search(html) or not SCRIPT.search(html):
            print(f"SKIP {source.name}: shared asset tags not found")
            continue
        html = STYLESHEET.sub(lambda m: f"<style>\n{asset(m.group(1))}\n</style>", html)
        html = SCRIPT.sub(lambda m: f"<script>\n{asset(m.group(1))}\n</script>", html)
        html = HREF.sub(lambda m: rewrite_link(m, source, out, sessions), html)
        (out / source.name).write_text(html, encoding="utf-8")
        print(f"built {out.relative_to(ROOT).as_posix()}/{source.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
