"""Suite wiring, and the fixtures and steps more than one feature shares. The rest live beside their scenarios."""
import os
import re
import tempfile
from pathlib import Path

import pytest
from kb.client import connect
from kb.content import loads
from kb.contract import kb_pb2
from pytest_bdd import given, then

import driver
from driver import start


def _reachable_from(directory: Path) -> bool:
    """Whether kb finds a store looking upward from `directory` alone: no KB_ROOT to name one outright, and the
    developer's own KB_ROOT (if the shell running the suite has one) never consulted."""
    kept = os.environ.pop("KB_ROOT", None)
    here = Path.cwd()
    os.chdir(directory)
    try:
        return not connect().Journal(kb_pb2.JournalRequest()).faults
    finally:
        os.chdir(here)
        if kept is not None:
            os.environ["KB_ROOT"] = kept


def _refuse_near_a_real_store(config):
    """The suite refuses to start rather than risk reading or writing a knowledge base outside a test's own
    temporary directory (adrs/0047): one is looked for, upward, from the checkout and from the system's temporary
    directory, the way every other kb call looks for its store."""
    for directory in (config.rootpath, Path(tempfile.gettempdir())):
        if _reachable_from(directory):
            raise pytest.UsageError(f"a knowledge base is reachable above {directory}; refusing to run near one")


def pytest_configure(config):
    """Refuse to start near a real knowledge base, then register every @slice-<n> tag in the feature files as a
    marker, so -m slice-<n> selects a slice."""
    _refuse_near_a_real_store(config)
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


@pytest.fixture
def env(shop):
    return {**os.environ, "KB_ROOT": str(shop), "KB_ACTOR": "shopkeeper"}


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
