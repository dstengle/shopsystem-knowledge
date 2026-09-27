"""Suite wiring, and the fixtures and steps more than one feature shares. The rest live beside their scenarios."""
import os
import re
import tempfile
from pathlib import Path

import pytest
from kb.content import loads
from kb.contract import kb_pb2
from pytest_bdd import given, then

import driver
from driver import NO_STORE, start


def _reachable_from(directory: Path, env: dict) -> bool:
    """Whether kb finds a store looking upward from `directory` alone: no KB_ROOT to name one outright, and the
    developer's own KB_ROOT (if the shell running the suite has one) never consulted, `env` carrying none. Anything
    but kb's own no-store refusal (`rule == "store"`, kb adrs/0018) counts as a store found - an empty answer, a
    fault of another rule, or more than one fault - so a cause kb adds later is never mistaken for "no store here";
    an exception from the call counts the same way, refused rather than let escape as a traceback."""
    try:
        faults = driver.kb_answer(env, "Journal", kb_pb2.JournalRequest(), cwd=directory).faults
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


def pytest_configure(config):
    """Register every @slice-<n> tag in the feature files as a marker, so -m slice-<n> selects a slice."""
    tags = set()
    for feature in Path(config.rootpath, "features").glob("*.feature"):
        tags.update(re.findall(r"@(slice-\d+(?:\.\d+)?)", feature.read_text()))
    for tag in sorted(tags):
        config.addinivalue_line("markers", f"{tag}: scenario of that slice in the plan")


@pytest.fixture
def shop(tmp_path):
    """The directory the shop's knowledge base is started in, there before it starts; the store is its kb/ subdirectory."""
    shop = tmp_path / "shop"
    shop.mkdir()
    return shop


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


@pytest.fixture
def env(shop, tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    return {**_allowlisted(home), "KB_ROOT": str(shop), "KB_ACTOR": "shopkeeper"}


@pytest.fixture(autouse=True)
def _working_directory(tmp_path, monkeypatch):
    """Every shop-knol run the driver makes, when a step names no working directory of its own, runs under this
    test's own temporary directory - never wherever the suite happens to be run from."""
    monkeypatch.setattr(driver, "_default_cwd", tmp_path)


@pytest.fixture
def shown(result):
    """What the user is shown, for every Then that expects the command to have succeeded."""
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)


@given("a shop knowledge base holding the shop's types")
def _shop_knowledge_base(env, shop):
    start(env, shop)


@given("the user has not said which role they are")
def _no_role(env):
    """Changes the scenario's env in place, so the commands the scenario runs are run with no KB_ACTOR."""
    env.pop("KB_ACTOR")


@then("the user is shown that fault in plain words, never a traceback")
def _shown_in_plain_words(result):
    """Something said on stderr, no traceback anywhere, and nothing on stdout but, for a check that found faults, its
    answer (adrs/0046): exactly `sound: false` and what is behind its type. Told apart by what stdout holds, since the
    step does not know which command ran."""
    assert result.stderr.strip(), "nothing was said"
    assert "Traceback" not in result.stderr + result.stdout, result.stderr
    assert result.stdout == "" or _a_failing_checks_answer(loads(result.stdout)), result.stdout


def _a_failing_checks_answer(document) -> bool:
    """Whether `document` is what `validate` still prints on stdout when the check itself fails: `sound: false` and
    the `behind` list, and nothing else."""
    return isinstance(document, dict) and document.keys() == {"sound", "behind"} and document["sound"] is False


@then("the user is shown the refusal in plain words, never a traceback")
def _refusal_in_plain_words(result):
    """Everything the shared body checks, plus the one-line count: this Then, unlike the shared one, is never used
    where a command reports more than one fault (a check lists one line per fault), so the scenarios that use it can
    also ask for exactly one line."""
    _shown_in_plain_words(result)
    assert result.stderr.count("\n") == 1, result.stderr


@then("the command reports failure to whatever ran it")
def _reports_failure(result):
    assert result.returncode != 0, result.stdout
