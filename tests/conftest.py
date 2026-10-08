"""Suite wiring, and the fixtures and steps more than one feature shares. The rest live beside their scenarios."""
import re
from pathlib import Path

import pytest
from kb.content import loads
from kb.contract import kb_pb2
from pytest_bdd import given, parsers, then

import driver
from driver import knol, start
from kb_oracle import kb_answer, printed
from session_guard import _allowlisted
from session_guard import *  # noqa: F403  conftest.py alone star-imports this, so pytest sees `pytest_sessionstart` (adrs/0048)
from served_store import *  # noqa: F403  conftest.py alone star-imports this (adrs/0048)
from store_not_found import *  # noqa: F403  conftest.py alone star-imports this (adrs/0048)


def pytest_configure(config):
    """Register every @slice-<n> tag in the feature files as a marker, so -m slice-<n> selects a slice."""
    tags = set()
    for feature in Path(config.rootpath, "features").glob("*.feature"):
        tags.update(re.findall(r"@(slice-\d+(?:\.\d+)*)", feature.read_text()))
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


_EMPTY_NAMES = {
    "starting the knowledge base": ("init", "root"),
    "the decision": ("create", "--from"),
    "the command": ("read", "locator"),
    "publishing": ("render", "--to"),
}
"""The command each feature's "given an empty name" scenario runs, and the argument it gives empty, by how its Then
names what was rejected."""


@then(parsers.re(
    r"(?P<rejected>starting the knowledge base|the decision|the command|publishing) is rejected because the "
    r"(?P<kind>directory|file|artifact) it was given has an empty name, which names no place"
))
def _rejected_for_an_empty_name(result, rejected, kind):
    """One line, the way every argument shop-knol cannot take is refused (adrs/0023): the command, the argument, and
    that a name given empty names no place of the kind it was to name."""
    command, argument = _EMPTY_NAMES[rejected]
    assert result.stderr.splitlines() == [
        f"shop-knol {command}: argument {argument}: a name given empty names no {kind}",
    ], result.stderr


@given(parsers.parse('a shop knowledge base holding no shop "{shop}"'), target_fixture="held")
def _no_such_shop(started_shop, shop):
    return {"shop": f"shop/{shop}"}


@then("the user is answered")
def _answered(result):
    assert result.stdout.strip() != ""


@then("the command is not refused")
def _not_refused(result):
    assert result.returncode == 0 and result.stderr == "", result.stderr


@then(parsers.parse('the answer is rejected because that shop is not there, naming "{shop}"'))
def _rejected(env, result, held, shop):
    """kb's own refusal of the same read, one line to each fault, and it names the shop."""
    request = kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=held["shop"]), whole=kb_pb2.ReadRequest.Whole(depth=0))
    faults = kb_answer(env, "Read", request).refusal.faults
    assert faults, "kb holds the shop"
    assert result.returncode == 1 and result.stdout == "", result.stdout
    assert sorted(result.stderr.splitlines()) == sorted(printed(fault) for fault in faults), result.stderr
    assert shop in result.stderr
