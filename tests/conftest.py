"""Suite wiring, and the fixtures and steps more than one feature shares. The rest live beside their scenarios."""
import os
import re
from pathlib import Path

import pytest
from kb.content import loads
from pytest_bdd import given, then

from driver import start


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
def env(shop):
    return {**os.environ, "KB_ROOT": str(shop), "KB_ACTOR": "shopkeeper"}


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
