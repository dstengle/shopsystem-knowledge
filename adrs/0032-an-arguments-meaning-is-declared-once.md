# 0032 What an argument means is declared once, where it is declared

2026-09-27. From slice 50.1, an argument's type and default are declared in `arguments.py` alone. The optional texts of `refs` and `search` default to `""`, as `journal`'s do. `refs --depth` defaults to 1, and `init`'s root is typed as a path. `kb_requests.py` then maps arguments to fields without patching them (`or ""`, `is None`, `Path(...)`). `--resolve` keeps `None`, since there "not given" means something. `cli._HANDLERS` lists the commands in the order the parser declares them. Help, which users see, keeps its order.
