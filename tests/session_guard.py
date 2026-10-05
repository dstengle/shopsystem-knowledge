"""The suite's own guard, and the allowlisted environment it and a scenario's shop-knol are both given: refuses the
whole run rather than risk reading or writing a knowledge base outside a test's own temporary directory (adrs/0047).
`conftest.py` alone star-imports this, so pytest sees `pytest_sessionstart` through it, and imports `_allowlisted`
explicitly for its own `env` fixture (adrs/0048)."""
import os
import tempfile
from pathlib import Path

import pytest
from kb.contract import kb_pb2

import kb_oracle
from kb_oracle import NO_STORE

_ALLOWED_NAMES = ("PATH", "LANG", "SYSTEMROOT", "TMPDIR")
"""What a scenario's shop-knol, or the guard's own call to kb, needs from the machine the suite runs on - never the
developer's whole shell (adrs/0047): PATH and LANG outright, LC_* alongside them, and the odd variable an
interpreter or its C library reads before anything of ours runs (SYSTEMROOT on Windows, TMPDIR wherever `tempfile`
looks for it)."""


def _allowlisted(home: Path) -> dict:
    """The environment a scenario's shop-knol, or the session guard's own call to kb, is given: only
    `_ALLOWED_NAMES` and `LC_*`, taken from the developer's shell if set there, with HOME pointed at `home` instead
    of the developer's own. Everything else - a shell GIT_DIR, a shell sitecustomize on PYTHONPATH, global git
    config reached through the developer's own HOME - never reaches kb this way; a fault the reviewer found (a
    scenario committed its knowledge base into the reviewer's own scratch repository, the suite passing throughout)."""
    kept = {name: value for name, value in os.environ.items() if name in _ALLOWED_NAMES or name.startswith("LC_")}
    return {**kept, "HOME": str(home)}


def _reachable_from(directory: Path, env: dict) -> bool:
    """Whether kb finds a store looking upward from `directory` alone: no KB_ROOT to name one outright, and the
    developer's own KB_ROOT (if the shell running the suite has one) never consulted, `env` carrying none. Anything
    but kb's own no-store refusal (`rule == "store"`, kb adrs/0018) counts as a store found - an empty answer, a
    fault of another rule, or more than one fault - so a cause kb adds later is never mistaken for "no store here";
    an exception from the call counts the same way, refused rather than let escape as a traceback."""
    try:
        faults = kb_oracle.kb_answer(env, "History", kb_pb2.HistoryRequest(), cwd=directory).refusal.faults
    except Exception:
        return True
    return not (len(faults) == 1 and faults[0].rule == NO_STORE)


def _starting_directories(config) -> list[Path]:
    """Every directory the guard looks upward from: the checkout, the system's own temporary directory, and
    pytest's own base temp root beneath it, since every test's `tmp_path` sits under that one. A seam of its own,
    so a throwaway demonstration can point the guard at a directory of its choosing instead of the real ones."""
    return [config.rootpath, Path(tempfile.gettempdir()), config._tmp_path_factory.getbasetemp().parent]


def _refuse_near_a_real_store(config):
    """The suite refuses to start rather than risk reading or writing a knowledge base outside a test's own
    temporary directory (adrs/0047): one is looked for, upward, from each of `_starting_directories`, the way
    every other kb call looks for its store. The guard's own call to kb runs in the same allowlisted environment a
    scenario would (`_allowlisted`), a throwaway HOME of its own, never the developer's shell whole - a shell
    GIT_DIR must never lead kb to a store the developer's shell knows of but this checkout does not."""
    with tempfile.TemporaryDirectory() as home:
        env = _allowlisted(Path(home))
        for directory in _starting_directories(config):
            if _reachable_from(directory, env):
                raise pytest.UsageError(f"a knowledge base is reachable above {directory}; refusing to run near one")


def pytest_sessionstart(session):
    """Refuse to start near a real knowledge base (adrs/0047), before any test is collected. Waits for session
    start, not configure, so pytest's own `_tmp_path_factory` (`_starting_directories`) is already attached to
    `config`."""
    _refuse_near_a_real_store(session.config)
