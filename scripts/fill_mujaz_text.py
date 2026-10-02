"""Fill the «نص الموجز» tab of session files with the full text of their pages.

A session file marks the place with
    <!--MUJAZ-TEXT pages="13-20"-->  …  <!--/MUJAZ-TEXT-->
and this script regenerates everything between the two markers from
Usul/Resources/books_data/mujaz_subhani.json, page by page, with the
footnotes. Run it after creating or changing a session file:

    python scripts/fill_mujaz_text.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "Usul" / "الجلسات"
BOOK = ROOT / "Usul" / "Resources" / "books_data" / "mujaz_subhani.json"
BLOCK = re.compile(r'(<!--MUJAZ-TEXT pages="(\d+)-(\d+)"-->).*?(<!--/MUJAZ-TEXT-->)', re.S)
HARAKAT = re.compile(r"[ً-ْ]")


def line_html(line: str, headings: set[str]) -> str:
    text = html.escape(line)
    letters = len(re.findall(r"[ء-ي]", line)) or 1
    if line in headings or re.match(r"^الأمر \S+ :", line) or (re.match(r"^\d+ \. ", line) and len(line) < 45):
        return f"<h4>{text}</h4>"
    if " * " in line:
        return f'<p class="verse">{text}</p>'
    if len(HARAKAT.findall(line)) / letters > 0.45 and len(line) > 12:
        return f'<p class="ayah">﴿ {text} ﴾</p>'
    return f"<p>{text}</p>"


def render(book: dict, start: int, end: int) -> str:
    headings = {t["title"] for t in book.get("toc", [])}
    parts = []
    for number in range(start, end + 1):
        page = book["pages"][str(number)]
        body = "\n".join(line_html(l.strip(), headings) for l in page["body"].split("\n") if l.strip())
        notes = ""
        if page.get("footnotes", "").strip():
            notes = '<div class="mujaz-notes">' + "<br>".join(html.escape(n) for n in page["footnotes"].split("\n") if n.strip()) + "</div>"
        parts.append(
            f'<article class="card mujaz-page" id="mujaz-p{number}"><div class="mujaz-head">'
            f'<strong>ص {number}</strong><span>{html.escape(page.get("header", ""))}</span></div>'
            f'<div class="mujaz-body">{body}</div>{notes}</article>'
        )
    return "\n".join(parts)


def main() -> int:
    book = json.loads(BOOK.read_text(encoding="utf-8"))
    for path in sorted(SESSIONS.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if not BLOCK.search(text):
            continue
        new = BLOCK.sub(lambda m: f"{m.group(1)}\n{render(book, int(m.group(2)), int(m.group(3)))}\n{m.group(4)}", text)
        path.write_text(new, encoding="utf-8")
        print(f"filled {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
