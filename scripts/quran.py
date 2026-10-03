"""Look up Qur'anic verses in the local Tanzil Uthmani text (Resources/quran).

    python scripts/quran.py get 36:14 36:16        # print verses verbatim
    python scripts/quran.py span 20:67             # print a ready <span class="ayah"> tag
    python scripts/quran.py search "في نفسه خيفة"   # find verses (diacritics ignored)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

QURAN = Path(__file__).resolve().parents[1] / "Resources" / "quran" / "quran_uthmani.json"


def load() -> dict:
    return json.loads(QURAN.read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    data = load()
    verses, surahs = data["verses"], data["surahs"]
    command, args = argv[0], argv[1:]
    if command in ("get", "span"):
        for ref in args:
            text = verses[ref]
            name = surahs[ref.split(":")[0]].replace("سُورَةُ ", "")
            if command == "get":
                print(f"{ref} ({name}): {text}")
            else:
                print(f'<span class="ayah" data-ref="{ref}">﴿{text}﴾</span> <cite>[{name} {ref.split(":")[1]}]</cite>')
    elif command == "search":
        from fill_ayat import skeleton as consonants  # same matching as the verse filler
        needle = consonants(" ".join(args))
        for ref, text in verses.items():
            if needle in consonants(text):
                print(f"{ref}: {text}")
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
