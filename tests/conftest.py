"""Suite wiring, and the fixtures and steps more than one feature shares. The rest live beside their scenarios."""
import re
from pathlib import Path

import pytest
from kb.content import loads
from pytest_bdd import given, then

import driver
from driver import knol, start
from session_guard import _allowlisted
from session_guard import *  # noqa: F403  conftest.py alone star-imports this, so pytest sees `pytest_sessionstart` (adrs/0048)
from store_not_found import *  # noqa: F403  conftest.py alone star-imports this (adrs/0048)


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


@pytest.fixture
def started_shop(env, shop):
    """`shop`, started once for the scenario: by a feature's own Background, or, when it has none, by a Given here."""
    start(env, shop)
    return shop


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
def _shop_knowledge_base(started_shop):
    """`started_shop` alone: asking for it is what starts the store."""


@pytest.fixture
def observed(env):
    """What the "unchanged" Then below watches: shop-knol's own history, at least. A feature that watches more
    overrides this fixture with a fuller snapshot, in the same shape before and after."""
    def _snapshot():
        return {"journal": knol(env, "journal").stdout}
    return _snapshot


@pytest.fixture
def before(observed):
    """What `observed` showed of the knowledge base, and how many shop-knol runs the driver had made, both before the
    command under test ran: every When the "unchanged" Then follows must take `before` itself, or the snapshot below
    is taken here instead, after the fact, and the run count catches that."""
    return observed(), driver.runs()


@then("the shop's knowledge base is unchanged")
def _unchanged(observed, before):
    """Refuses to pass on a `before` no When asked for: at least one shop-knol run must have happened since it was
    taken, or it was resolved lazily, after the command under test rather than ahead of it."""
    snapshot, runs_before = before
    assert driver.runs() > runs_before, "before was not taken before the command under test ran"
    assert observed() == snapshot


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
