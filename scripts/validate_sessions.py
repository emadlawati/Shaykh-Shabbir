"""Check the session files: Usul/الجلسات, علم النحو/الجلسات and بلاغة/الجلسات.

Every <blockquote class="matn" data-book=".." data-page=".."> quote must occur,
after Arabic normalisation, in the named book's local text on those pages (each
track has its own Resources/books_data); every <span class="ayah" data-ref="س:آ">
must be a verbatim excerpt of that verse in Resources/quran/quran_uthmani.json
(fill them with scripts/fill_ayat.py); every local link must resolve; and every
page in Curriculum_Map.md's Mujaz column must fall inside the book (1–248).
"""

from __future__ import annotations

import json
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import unquote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
TRACKS = [  # (session files, their books_data)
    (ROOT / "Usul" / "الجلسات", ROOT / "Usul" / "Resources" / "books_data"),
    (ROOT / "علم النحو" / "الجلسات", ROOT / "علم النحو" / "Resources" / "books_data"),
    (ROOT / "بلاغة" / "الجلسات", ROOT / "بلاغة" / "Resources" / "books_data"),
]
QURAN = ROOT / "Resources" / "quran" / "quran_uthmani.json"

QUOTE = re.compile(
    r'<blockquote class="matn" data-book="([^"]+)" data-page="([^"]+)"><span class="q">(.*?)</span>',
    re.S,
)
LINK = re.compile(r'(?:href|src)="([^"#:]+)(?:#[^"]*)?"')
AYAH = re.compile(r'<span class="ayah" data-ref="([^"]+)"[^>]*>(.*?)</span>', re.S)


def normalise(text: str) -> str:
    text = re.sub(r"[ً-ٰٟـ]", "", unescape(text))
    text = re.sub("[أإآٱ]", "ا", text).replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"[^ء-ي0-9]", "", text)


def pages(books: Path, book: str, spec: str) -> str:
    data = json.loads((books / f"{book}.json").read_text(encoding="utf-8"))["pages"]
    start, _, end = spec.partition("-")
    return "".join(data[str(p)]["body"] for p in range(int(start), int(end or start) + 1))


def main() -> int:
    errors: list[str] = []
    quotes = ayat = files = 0
    verses = json.loads(QURAN.read_text(encoding="utf-8"))["verses"]
    for sessions, books in TRACKS:
        for html in sorted(sessions.glob("*.html")):
            files += 1
            text = html.read_text(encoding="utf-8")
            for book, spec, quote in QUOTE.findall(text):
                quotes += 1
                try:
                    found = normalise(quote) in normalise(pages(books, book, spec))
                except (OSError, KeyError):
                    found = False
                if not found:
                    errors.append(f"{html.name}: quote not found in {book} p.{spec}: {quote[:60]}…")
            for ref, body in AYAH.findall(text):
                ayat += 1
                excerpt = re.sub(r"</?mark>", "", body).strip("﴿﴾")
                if not excerpt or ref not in verses or excerpt not in verses[ref]:
                    errors.append(f"{html.name}: verse {ref} is empty or not verbatim (run scripts/fill_ayat.py)")
            for target in LINK.findall(text):
                if not (html.parent / unquote(target)).exists():
                    errors.append(f"{html.name}: broken link {target}")
            if 'class="matn"' in text and text.count('class="matn"') != len(QUOTE.findall(text)):
                errors.append(f"{html.name}: a matn blockquote lacks data-book/data-page/span.q")

    curriculum = (ROOT / "Usul" / "Curriculum_Map.md").read_text(encoding="utf-8")
    for row in curriculum.splitlines():
        cells = [c.strip() for c in row.split("|")]
        if len(cells) > 4 and re.match(r"\*\*\d+\*\*", cells[1] or ""):
            for number in re.findall(r"\d+", cells[3]):
                if not 1 <= int(number) <= 248:
                    errors.append(f"Curriculum_Map.md: Mujaz page {number} out of range in row {cells[1]}")

    for error in errors:
        print("FAIL", error)
    print(f"{quotes} quotes and {ayat} verses checked across {files} session files; {len(errors)} problem(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
