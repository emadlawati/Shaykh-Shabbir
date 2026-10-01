"""Build self-contained phone copies of the session files.

Each Usul/الجلسات/NN_*.html loads ../Resources/lesson_assets/lesson.css and
lesson.js, so a single file opened on a phone has no styling or tabs. This
script inlines both into a copy under Usul/الجلسات/للجوال/, keeps links between
sessions pointing at their phone copies, and turns every other local link into
its GitHub page so it opens in the phone's browser.

Run after every change to a session file:  python scripts/build_mobile.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "Usul" / "الجلسات"
OUT = SESSIONS / "للجوال"
ASSETS = ROOT / "Usul" / "Resources" / "lesson_assets"
GITHUB = "https://github.com/emadlawati/Shaykh-Shabbir/blob/main/"

CSS_TAG = '<link rel="stylesheet" href="../Resources/lesson_assets/lesson.css">'
JS_TAG = '<script src="../Resources/lesson_assets/lesson.js"></script>'
HREF = re.compile(r'href="([^"#:]+)(#[^"]*)?"')


def rewrite_link(match: re.Match, source: Path, sessions: set[str]) -> str:
    target, fragment = match.group(1), match.group(2) or ""
    if target in sessions:
        return f'href="{target}{fragment}"'
    resolved = (source.parent / unquote(target)).resolve().relative_to(ROOT)
    return f'href="{GITHUB}{quote(resolved.as_posix())}{fragment}" target="_blank" rel="noopener"'


def main() -> int:
    css = (ASSETS / "lesson.css").read_text(encoding="utf-8")
    js = (ASSETS / "lesson.js").read_text(encoding="utf-8")
    OUT.mkdir(exist_ok=True)
    sources = sorted(SESSIONS.glob("*.html"))
    names = {p.name for p in sources}
    for source in sources:
        html = source.read_text(encoding="utf-8")
        if CSS_TAG not in html or JS_TAG not in html:
            print(f"SKIP {source.name}: shared asset tags not found")
            continue
        html = html.replace(CSS_TAG, f"<style>\n{css}\n</style>")
        html = html.replace(JS_TAG, f"<script>\n{js}\n</script>")
        html = HREF.sub(lambda m: rewrite_link(m, source, names), html)
        (OUT / source.name).write_text(html, encoding="utf-8")
        print(f"built للجوال/{source.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
