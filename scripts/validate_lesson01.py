"""Validate Lesson 1 source provenance and offline asset integrity."""

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
LESSON_DIR = ROOT / "Usul" / "00_المقدمة_والمبادئ"
HTML_PATH = LESSON_DIR / "01_تعريف_علم_الأصول_وموضوعه_وغايته.html"
SOURCES_PATH = ROOT / "Usul" / "Resources" / "lesson_assets" / "lesson01_sources.js"
BOOKS_DIR = ROOT / "Usul" / "Resources" / "books_data"


SOURCE_PAGES = {
    "mujaz_definition": ("mujaz_subhani.json", [9, 10]),
    "sadr_first": ("sadr_halaqat_1.json", [36, 38, 39, 40]),
    "sadr_second": ("sadr_halaqat_1.json", [141, 142, 143, 144, 145]),
    "muzaffar_definition": ("usul_muzaffar_1.json", [49, 50, 51]),
    "mufid_sources": ("mufid_tadhkirah.json", [31]),
    "murtada_dalil": ("murtada_dhariyah_1.json", [59]),
    "tusi_map": ("tusi_uddah_1.json", [33, 34, 36, 37, 39]),
    "akhund_subject": ("kifayah_akhund.json", [7, 8]),
    "khoei_definition": ("khoei_muhadarat_1.json", [11, 12]),
    "sistani_need": ("sistani_rafid.json", [10, 13]),
}


def load_sources() -> dict[str, dict]:
    text = SOURCES_PATH.read_text(encoding="utf-8")
    marker = "window.LESSON01_SOURCES = "
    start = text.index(marker) + len(marker)
    payload = text[start:].strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    payload = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)", r'\1"\2"\3', payload)
    return json.loads(payload)


def normalize_arabic(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.translate(str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ة": "ه"}))
    return re.sub(r"[^\u0621-\u064A]+", "", text)


def quote_chunks(text: str) -> list[str]:
    parts = re.split(r"(?:\n\s*\n|\.{3,}|…)", text)
    return [part.strip() for part in parts if len(normalize_arabic(part)) >= 18]


class LessonHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.local_refs: list[str] = []
        self.source_ids: list[str] = []
        self.remote_refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if values.get("data-source"):
            self.source_ids.append(values["data-source"] or "")
        for key in ("href", "src"):
            value = values.get(key)
            if not value or value.startswith(("#", "data:", "mailto:")):
                continue
            if value.startswith(("http://", "https://", "//")):
                self.remote_refs.append(value)
            else:
                self.local_refs.append(value.split("#", 1)[0])


def validate() -> list[str]:
    errors: list[str] = []
    sources = load_sources()

    required = {
        "source_id", "layer", "book", "author", "edition", "volume",
        "printed_page", "scan_or_database_page", "content_kind",
        "verification", "context", "text", "file", "pdf_page"
    }
    allowed_kind = {"verbatim", "summary", "analysis", "teacher_note"}
    allowed_verification = {"exact_text_match", "visually_verified_scan", "pending"}

    for source_id, source in sources.items():
        missing = required - source.keys()
        if missing:
            errors.append(f"{source_id}: missing fields {sorted(missing)}")
        if source.get("source_id") != source_id:
            errors.append(f"{source_id}: source_id mismatch")
        if source.get("content_kind") not in allowed_kind:
            errors.append(f"{source_id}: invalid content_kind")
        if source.get("verification") not in allowed_verification:
            errors.append(f"{source_id}: invalid verification")
        if source.get("verification") == "pending":
            errors.append(f"{source_id}: pending source exposed to learners")
        if source.get("file"):
            target = (LESSON_DIR / unquote(source["file"])).resolve()
            if not target.is_file():
                errors.append(f"{source_id}: missing local source file {target}")

    for source_id, (book_name, pages) in SOURCE_PAGES.items():
        source = sources[source_id]
        book = json.loads((BOOKS_DIR / book_name).read_text(encoding="utf-8-sig"))
        corpus = "\n".join(book["pages"][str(page)]["body"] for page in pages)
        normalized_corpus = normalize_arabic(corpus)
        for chunk in quote_chunks(source["text"]):
            normalized_chunk = normalize_arabic(chunk)
            if normalized_chunk not in normalized_corpus:
                errors.append(f"{source_id}: unmatched quote chunk: {chunk[:80]!r}")

    parser = LessonHTMLParser()
    parser.feed(HTML_PATH.read_text(encoding="utf-8"))
    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        errors.append(f"duplicate HTML ids: {duplicates}")
    unknown_sources = sorted(set(parser.source_ids) - sources.keys())
    if unknown_sources:
        errors.append(f"unknown data-source ids: {unknown_sources}")
    if parser.remote_refs:
        errors.append(f"remote dependencies break offline mode: {parser.remote_refs}")
    for ref in parser.local_refs:
        target = (LESSON_DIR / unquote(ref)).resolve()
        if not target.exists():
            errors.append(f"missing HTML asset/link: {ref}")

    return errors


if __name__ == "__main__":
    failures = validate()
    if failures:
        print("Lesson 1 validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)
    print("Lesson 1 validation passed")
    print("- source schema complete; no pending learner quotations")
    print("- text-source quotations matched after Arabic normalization")
    print("- HTML ids, source references, local links, and offline dependencies valid")
