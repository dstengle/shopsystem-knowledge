# 0017 Answers are shaped in answers.py

2026-09-27. Every kb answer shown to the user is turned into a plain dict in `answers.py`, one public function per answer: `created`, `glance`, `applied`, `history` (wrapping `change`, one entry) and `written`. They take kb's response messages, or the renderer's files, and never print, call kb or read arguments. `kb_pb2` is imported for type hints only. `cli.py` calls them and prints through `_show`.
