"""Copy cited pages of a library book into a track's books_data JSON.

    python scripts/extract_pages.py "<library .md>" <out.json> <page> [<page> ...] [--title T --author A --volume V]

Understands the two local library formats: AhlulBayt («--- [ج 1 ص 15] ---») and
Shamela («### صفحة 15» or «### [جـ 1 - ص 15]»). Existing pages in <out.json> are kept,
so the file grows as later sessions cite more pages.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MARKER = re.compile(r"^(?:--- \[ج (\d+) ص (\d+)\] ---|### صفحة (\d+)|### \[جـ (\d+) - ص (\d+)\])\s*$", re.M)


def split_pages(text: str, volume: str | None = None) -> dict[str, str]:
    pages: dict[str, str] = {}
    marks = list(MARKER.finditer(text))
    for mark, nxt in zip(marks, marks[1:] + [None]):
        vol_a, page_a, page_b, vol_c, page_c = mark.groups()
        if volume and (vol_a or vol_c) != volume:
            continue
        number = page_a or page_b or page_c
        body = text[mark.end(): nxt.start() if nxt else len(text)].strip().strip("-").strip()
        pages[number] = (pages.get(number, "") + "\n" + body).strip()
    return pages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("out")
    parser.add_argument("pages", nargs="+")
    parser.add_argument("--title", default="")
    parser.add_argument("--author", default="")
    parser.add_argument("--volume", help="keep only this volume when one file holds several")
    args = parser.parse_args()

    source = Path(args.source)
    pages = split_pages(source.read_text(encoding="utf-8"), args.volume)
    out = Path(args.out)
    data = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {
        "title": args.title, "author": args.author, "library_file": source.name, "pages": {}}
    for page in args.pages:
        if page not in pages:
            print(f"page {page} not found in {source.name}")
            return 1
        data["pages"][page] = {"body": pages[page]}
    data["pages"] = dict(sorted(data["pages"].items(), key=lambda kv: int(kv[0])))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{out.name}: {', '.join(data['pages'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
