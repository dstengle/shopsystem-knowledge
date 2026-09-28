"""Where the knowledge base is found, the steps the read-back and check features share: `workdir`, the kb call the
scenario's own When made (`called`), the three "working …" Givens, and the Thens that say a store was not found.
`conftest.py` alone star-imports this (adrs/0048)."""
import pytest
from pytest_bdd import given, then

from driver import NO_STORE, kb_answer, printed, start


@pytest.fixture
def workdir(tmp_path):
    """Where the user works: the test's own temporary directory, unless a Given moves them elsewhere in it."""
    return tmp_path


@pytest.fixture
def called():
    """The kb call and request the scenario's own When made, for the store-refusal Thens below to repeat via `kb_answer`."""
    return {}


@given("the user is working outside any knowledge base and nothing names one", target_fixture="workdir")
def _working_elsewhere_naming_nothing(env, tmp_path):
    del env["KB_ROOT"]
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    return elsewhere


@given(
    "the user is working outside any knowledge base, with KB_ROOT naming a directory that holds no knowledge base",
    target_fixture="workdir",
)
def _kb_root_names_an_empty_directory(env, tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    env["KB_ROOT"] = str(empty)
    return tmp_path


@given(
    "the user is working inside the shop's knowledge base, with KB_ROOT naming a different one",
    target_fixture="workdir",
)
def _kb_root_names_another_store(env, started_shop, tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    start(env, other)
    env["KB_ROOT"] = str(other)
    return started_shop


def _refused_as_kb_refuses(env, result, workdir, called):
    """kb's own answer to the call the scenario's own When made, from the same directory and KB_ROOT, refuses the
    store rule it publishes (kb adrs/0018); the user is shown that one fault, in kb's words, and nothing else."""
    faults = kb_answer(env, called["call"], called["request"], cwd=workdir).faults
    assert [fault.rule for fault in faults] == [NO_STORE], faults
    assert result.stderr.splitlines() == [printed(faults[0])], result.stderr
    assert result.stdout == ""


@then("the command is rejected because no knowledge base was found, neither above where they are working nor named outright")
def _rejected_no_store(env, result, workdir, called):
    _refused_as_kb_refuses(env, result, workdir, called)


@then("the command is rejected because KB_ROOT names a directory that holds no knowledge base")
def _rejected_kb_root_holds_none(env, result, workdir, called):
    _refused_as_kb_refuses(env, result, workdir, called)


@then(
    "the command is rejected because KB_ROOT names a knowledge base other than the one they are working in, "
    "and neither of the two is guessed at"
)
def _rejected_two_stores(env, result, workdir, called):
    _refused_as_kb_refuses(env, result, workdir, called)
