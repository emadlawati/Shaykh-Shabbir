"""Fill the Qur'anic verses in the Nahw/Balagha session files from the local Tanzil text.

Write a verse in a session file as an empty (or stale) span:

    <span class="ayah" data-ref="20:67"></span>                                  whole verse
    <span class="ayah" data-ref="9:3" data-part="أن الله بريء من المشركين ورسوله"></span>
    <span class="ayah" data-ref="35:28" data-part="إنما يخشى الله من عباده العلماء" data-mark="الله|العلماء"></span>

`data-part` and `data-mark` are written in ordinary spelling; they are matched on a
consonant skeleton (so Uthmani spellings like «إِبۡرَ ٰ⁠هِـۧمَ» still match «إبراهيم») and
widened to whole words. `data-mark` words (separated by |) are wrapped in <mark>.
The span is then filled with the exact Tanzil text. Run before validate_sessions.py:

    python scripts/fill_ayat.py            # all Nahw and Balagha session files
"""

from __future__ import annotations

import html
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quran import load  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
TRACKS = [ROOT / "علم النحو" / "الجلسات", ROOT / "بلاغة" / "الجلسات"]
SPAN = re.compile(r'<span class="ayah" data-ref="(\d+:\d+)"((?: data-(?:part|mark)="[^"]*")*)>(.*?)</span>', re.S)
ATTR = re.compile(r'data-(part|mark)="([^"]*)"')
DROP = set("اأإآٱءئؤوىيی") | {"ـ"}


def is_mark(ch: str) -> bool:
    return unicodedata.category(ch) in ("Mn", "Me", "Cf") or "ۖ" <= ch <= "ۭ"


def skeleton(text: str) -> str:
    """Consonants only: drop vowels, Qur'anic marks, alif/hamza/waw/ya; open and tied tā' agree."""
    letters = []
    for ch in text:
        if ch.isspace() or is_mark(ch) or ch in DROP or not ("ء" <= ch <= "ي"):
            continue
        ch = "ت" if ch == "ة" else ch
        if not letters or letters[-1] != ch:  # «الليل» and «ٱلَّیۡل» both give one lam
            letters.append(ch)
    return "".join(letters)


def words(text: str) -> list[tuple[int, int]]:
    """Word spans. A space followed by a mark (as in «إِبۡرَ ٰ⁠هِـۧمَ») is inside a word."""
    spans, start = [], None
    for i, ch in enumerate(text):
        nxt = text[i + 1] if i + 1 < len(text) else ""
        inside = ch != " " or is_mark(nxt) or nxt == "⁠"
        if inside and start is None:
            start = i
        if not inside and start is not None:
            spans.append((start, i))
            start = None
    if start is not None:
        spans.append((start, len(text)))
    return spans


def locate(text: str, phrase: str, after: int = 0) -> tuple[int, int]:
    """Span of the first run of whole words in `text` (from `after`) whose joined skeleton equals
    the phrase's, so «يا قومنا» still finds the single Uthmani word «یَـٰقَوۡمَنَاۤ»."""
    spans = [w for w in words(text) if w[0] >= after]
    target = skeleton(phrase)
    for i in range(len(spans)):
        if not skeleton(text[spans[i][0]:spans[i][1]]):
            continue  # a run never starts on a consonant-less word like «أو»
        joined = ""
        for j in range(i, len(spans)):
            joined = skeleton(text[spans[i][0]:spans[j][1]])
            if joined == target and target:
                return spans[i][0], spans[j][1]
            if len(joined) >= len(target):
                break
    raise LookupError(phrase)


def render(verse: str, part: str | None, marks: list[str]) -> str:
    verse = verse.replace("۞", "").strip()
    if part:
        start, end = locate(verse, part)
        verse = verse[start:end]
    out, cursor = [], 0
    for word in marks:
        start, end = locate(verse, word, cursor)
        out += [verse[cursor:start], "<mark>", verse[start:end], "</mark>"]
        cursor = end
    out.append(verse[cursor:])
    return "﴿" + "".join(out) + "﴾"


def fill(path: Path, verses: dict) -> int:
    text = path.read_text(encoding="utf-8")
    problems = 0

    def replace(match: re.Match) -> str:
        nonlocal problems
        ref, attrs, _ = match.groups()
        found = {k: html.unescape(v) for k, v in ATTR.findall(attrs)}
        try:
            body = render(verses[ref], found.get("part"), [m for m in found.get("mark", "").split("|") if m])
        except (KeyError, LookupError) as error:
            problems += 1
            print(f"FAIL {path.name}: {ref} cannot place «{error.args[0] if error.args else ref}»")
            return match.group(0)
        return f'<span class="ayah" data-ref="{ref}"{attrs}>{body}</span>'

    new = SPAN.sub(replace, text)
    if new != text:
        path.write_text(new, encoding="utf-8")
    print(f"{path.name}: {len(SPAN.findall(new))} verses")
    return problems


def main(argv: list[str]) -> int:
    verses = load()["verses"]
    files = [Path(a) for a in argv] or [f for d in TRACKS for f in sorted(d.glob("*.html"))]
    return 1 if sum(fill(f, verses) for f in files) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
