"""Check Lessons 2–5 source provenance and offline interface structure."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "Usul" / "00_المقدمة_والمبادئ"
ASSETS = ROOT / "Usul" / "Resources" / "lesson_assets"
BOOKS = ROOT / "Usul" / "Resources" / "books_data"

CONFIG = {
    "02": {
        "stem": "02_تقسيم_المباحث_وحقيقة_الوضع_وأقسامه",
        "book_pages": {
            "l02_mujaz_division": ("mujaz_subhani.json", [10]),
            "l02_mujaz_wad": ("mujaz_subhani.json", [10, 11]),
            "l02_mujaz_four": ("mujaz_subhani.json", [11, 12]),
            "l02_sadr_first": ("sadr_halaqat_1.json", [68]),
            "l02_sadr_second": ("sadr_halaqat_1.json", [186]),
            "l02_muzaffar_four": ("usul_muzaffar_1.json", [56]),
            "l02_murtada_use": ("murtada_dhariyah_1.json", [60, 61]),
            "l02_akhund_wad": ("kifayah_akhund.json", [9, 10]),
            "l02_khoei_commitment": ("khoei_muhadarat_1.json", [52]),
            "l02_sistani_stages": ("sistani_rafid.json", [163]),
        },
    },
    "03": {
        "stem": "03_الدلالة_التصورية_والدلالة_التصديقية",
        "book_pages": {
            "l03_mujaz_meanings": ("mujaz_subhani.json", [13]),
            "l03_sadr_first": ("sadr_halaqat_1.json", [75, 76]),
            "l03_sadr_second": ("sadr_halaqat_1.json", [184, 185, 186]),
            "l03_muzaffar_strict": ("usul_muzaffar_1.json", [65]),
            "l03_murtada_address": ("murtada_dhariyah_1.json", [60]),
            "l03_akhund_will": ("kifayah_akhund.json", [16]),
            "l03_khoei_strict": ("khoei_muhadarat_1.json", [118]),
            "l03_sistani_three": ("sistani_rafid.json", [145]),
        },
    },
    "04": {"stem": "04_الحقيقة_والمجاز_وعلامات_الحقيقة"},
    "05": {"stem": "05_الأصول_اللفظية_العقلائية"},
}


def load_sources(number: str) -> dict[str, dict]:
    data = (ASSETS / f"lesson{number}_sources.js").read_text(encoding="utf-8")
    payload = data.split("window.LESSON_SOURCES = ", 1)[1].strip().removesuffix(";")
    payload = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)", r'\1"\2"\3', payload)
    return json.loads(payload)


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(character for character in value if not unicodedata.combining(character))
    value = value.translate(str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ة": "ه"}))
    return re.sub(r"[^\u0621-\u064A]+", "", value)


class LocalHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.source_ids: list[str] = []
        self.refs: list[str] = []
        self.remote: list[str] = []
        self.panels: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
            if values["id"].startswith("panel-"):
                self.panels.append(values["id"])
        if values.get("data-source"):
            self.source_ids.append(values["data-source"] or "")
        for key in ("href", "src"):
            value = values.get(key)
            if not value or value.startswith(("#", "data:", "mailto:")):
                continue
            if value.startswith(("http://", "https://", "//")):
                self.remote.append(value)
            else:
                self.refs.append(value.split("#", 1)[0].split("?", 1)[0])


def check_lesson(number: str) -> list[str]:
    errors: list[str] = []
    config = CONFIG[number]
    sources = load_sources(number)
    required = {
        "source_id", "layer", "book", "author", "edition", "volume", "printed_page",
        "scan_or_database_page", "content_kind", "verification", "context", "text", "file"
    }
    for sid, source in sources.items():
        missing = required - source.keys()
        if missing:
            errors.append(f"{sid}: missing fields {sorted(missing)}")
        if source.get("source_id") != sid:
            errors.append(f"{sid}: ID mismatch")
        if source.get("content_kind") not in {"verbatim", "summary", "analysis", "teacher_note"}:
            errors.append(f"{sid}: invalid content kind")
        if source.get("verification") == "pending":
            errors.append(f"{sid}: pending text visible")
        if source.get("verification") not in {"exact_text_match", "visually_verified_scan"}:
            errors.append(f"{sid}: invalid verification")
        target = (LESSONS / unquote(source["file"])).resolve()
        if not target.is_file():
            errors.append(f"{sid}: missing source file: {target}")
    book_pages = dict(config.get("book_pages", {}))
    if not book_pages:
        for sid, source in sources.items():
            if source.get("verification") != "exact_text_match":
                continue
            book_name = Path(source["file"]).name
            page_label = source["scan_or_database_page"]
            match = re.search(r"(\d+)(?:–(\d+))?", page_label)
            if not match:
                errors.append(f"{sid}: no database page in provenance")
                continue
            first = int(match.group(1))
            last = int(match.group(2) or first)
            book_pages[sid] = (book_name, list(range(first, last + 1)))
    for sid, (book_name, pages) in book_pages.items():
        book = json.loads((BOOKS / book_name).read_text(encoding="utf-8-sig"))
        corpus = normalize("\n".join(book["pages"][str(page)]["body"] for page in pages))
        quote = normalize(sources[sid]["text"])
        if quote not in corpus:
            errors.append(f"{sid}: quote not found after Arabic normalization")
    parser = LocalHTML()
    parser.feed((LESSONS / f'{config["stem"]}.html').read_text(encoding="utf-8"))
    duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicate_ids:
        errors.append(f"duplicate HTML ids: {duplicate_ids}")
    unknown = sorted(set(parser.source_ids) - sources.keys())
    if unknown:
        errors.append(f"unknown source IDs: {unknown}")
    if len(parser.panels) != 7:
        errors.append(f"expected 7 panels; found {len(parser.panels)}")
    if parser.remote:
        errors.append(f"remote dependencies: {parser.remote}")
    for ref in parser.refs:
        if not (LESSONS / unquote(ref)).resolve().exists():
            errors.append(f"missing local link: {ref}")
    return errors


if __name__ == "__main__":
    failures = [f"Lesson {number}: {issue}" for number in CONFIG for issue in check_lesson(number)]
    if failures:
        print("Lesson 2–5 validation FAILED")
        for failure in failures:
            print("-", failure)
        sys.exit(1)
    print("Lesson 2–5 validation passed")
    print(f"- {sum(len(load_sources(number)) for number in CONFIG)} source records complete, with no pending learner quotations")
    print("- digital quotations matched against local book pages after Arabic normalization")
    print("- 7 panels per lesson, source IDs, local links, and offline dependencies valid")
