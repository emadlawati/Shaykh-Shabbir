# Working notes for Claude

- **Merge every update into `main`.** After each change (session prep, session report, ledger updates), commit, push, and merge the pull request into `main` right away, so the user always finds the latest files on `main`.
- **Do not watch or poll pull requests** unless the user asks.
- The study workflow (prep → class → report) and the Shaykh's teaching-style profile are in `Usul/Templates/قالب_جلسة_الشيخ_شبير.md`. Session files are in `Usul/الجلسات/`.
- **Phone copies:** after any change to a session file, run `python3 scripts/build_mobile.py`. It writes a self-contained copy (CSS and JS inlined, other links pointing to GitHub) to `Usul/الجلسات/للجوال/`, and commits it with the change. Send the user the phone copy of any new or updated session.
- Run `python3 scripts/validate_sessions.py` before every commit; every quoted Mujaz/Kifaya passage must match the local text in `Usul/Resources/books_data/`.
