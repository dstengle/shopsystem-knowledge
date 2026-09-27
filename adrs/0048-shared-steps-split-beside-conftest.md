# 0048 Shared steps of one concern may sit beside conftest.py

2026-09-27. Extends 0035. When `tests/conftest.py`, which holds the fixtures and steps more than one feature shares, would pass the size limit, the shared steps of one concern move to a module of their own beside it, not named `test_*`, whose docstring names the features it serves, and which `conftest.py` alone star-imports. The session guard's hooks may move the same way, since pytest sees them through `conftest.py`.
