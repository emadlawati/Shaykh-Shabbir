# Working notes for Claude

- **Merge every update into `main`.** After each change (session prep, session report, ledger updates), commit, push, and merge the pull request into `main` right away, so the user always finds the latest files on `main`.
- **Do not watch or poll pull requests** unless the user asks.
- The study workflow (prep → class → report) and the Shaykh's teaching-style profile are in `Usul/Templates/قالب_جلسة_الشيخ_شبير.md`. Session files are in `Usul/الجلسات/`.
- Run `python3 scripts/validate_sessions.py` before every commit; every quoted Mujaz/Kifaya passage must match the local text in `Usul/Resources/books_data/`.
- **Nahw and Balagha** (`علم النحو/`, `بلاغة/`) are self-study tracks in the Shaykh's style, centred on Qur'anic تطبيق. Method and session structure: `Usul/Templates/قالب_جلسة_النحو_والبلاغة.md`; syllabus and status: each folder's `خريطة_المنهج.md`.
  - Never type verses by hand: write `<span class="ayah" data-ref="س:آ" data-part=".." data-mark="..">` and run `python3 scripts/fill_ayat.py` (Tanzil text in `Resources/quran/`).
  - Both PDFs lack usable text: transcribe each new session's pages from the page images into the track's `Resources/books_data/*.json` before quoting. Classical-text gems are extracted with `scripts/extract_pages.py`.
