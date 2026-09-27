# 0021 The command line's arguments sit apart from its handlers

2026-09-27. Slice 28.1 moves `cli._parser` to a module of its own, `arguments.py`, which declares every command's arguments with argparse and the renderer names from `RENDERERS`, and knows no handler. `cli.py` keeps `main`, one handler per command, the actor from the environment, the client, `_document`, `_answered` and printing, and chooses a command's handler by its name from one table of its own. A new command adds its arguments to `arguments.py` and its handler, and one entry in that table, to `cli.py`.
