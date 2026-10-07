"""The steps of start-a-knowledge-base.feature about a start that kb refuses: a directory already holding a
knowledge base, or inside one, and a directory since removed. The feature's test module star-imports this and no
other does."""
from pathlib import Path

import pytest
from kb.contract import kb_pb2
from pytest_bdd import given, parsers, then

from driver import knol, removed, start, store_in
from kb_oracle import kb_answer, kb_refuses_to_start, operator_started, printed


@pytest.fixture
def started_before():
    """The directories a Given started a knowledge base in before the user ran init."""
    return set()


@pytest.fixture
def known_before(env):
    """What `shop-knol journal` answered before the user started a knowledge base, filled in by the Given that starts one."""
    return {}


def _started_and_noted(env, shop, known_before):
    """The shop's knowledge base started, with nothing naming a different one: KB_ROOT, if set, names the shop's."""
    start(env, shop)
    known_before["journal"] = knol(env, "journal").stdout
    assert env.get("KB_ROOT") in (None, str(shop)), env.get("KB_ROOT")


@given(
    "the user is working in a directory that already holds the shop's knowledge, and nothing names a different "
    "knowledge base"
)
def _a_directory_already_started(env, shop, known_before):
    _started_and_noted(env, shop, known_before)


@given(
    "the user is working in a directory that sits inside the shop's knowledge, and nothing names a different "
    "knowledge base",
    target_fixture="start_in",
)
def _a_directory_inside_a_started_one(env, shop, known_before):
    _started_and_noted(env, shop, known_before)
    # Works in the directory kb's contract says init made (`kb.init`), inside the knowledge base.
    return store_in(shop)


_ABOVE = {"kb's operator started empty": operator_started, "holding the shop's types": start}
"""How the knowledge base above the named directory is started: by kb's operator, empty, or by shop-knol's init,
furnished with the shop's types."""


@pytest.fixture
def named_inside():
    """The directory the user names to start a knowledge base in, inside one, as the Given made it: filled in by it."""
    return {}


@given(
    parsers.parse(
        "the user is working in one directory, and another directory sits inside a knowledge base {holding} but holds "
        "none of its own"
    ),
    target_fixture="elsewhere",
)
def _another_directory_inside_one(env, tmp_path, holding, journal_before, named_inside):
    """A knowledge base started above the named directory, its journal as read before init ran; the named directory
    is a subdirectory of it with nothing of its own."""
    above = tmp_path / "above"
    above.mkdir()
    _ABOVE[holding](env, above)
    journal_before["root"] = str(above)
    journal_before["journal"] = knol({**env, "KB_ROOT": str(above)}, "journal").stdout
    named_inside["root"] = above / "room"
    named_inside["root"].mkdir()
    return named_inside["root"]


@then("starting the knowledge base is rejected because that directory already holds a knowledge base")
def _rejected_already_started(env, result, start_in):
    _refused_as_kb_refuses_init(env, result, start_in, start_in)


@then("starting the knowledge base is rejected because that directory is inside a knowledge base")
def _rejected_inside_one(env, result, start_in, named_inside):
    """kb's refusal to start a store in the directory the user named, or, with none named, where they work."""
    _refused_as_kb_refuses_init(env, result, start_in, named_inside.get("root", start_in))


ROOT = "root"
"""The `rule` kb's contract publishes (kb adrs/0018) for a store refused where it was to be started."""


def _refused_as_kb_refuses_init(env, result, start_in, root):
    """One line, printed as kb returned it: kb's own refusal to start a store at the same root, asked from where the
    user works (`start_in`), is a refusal of the directory given, and the user is shown that fault in kb's words.
    Which refusal, the Given decides; a refused start changes nothing."""
    faults = kb_refuses_to_start(env, root.resolve(), cwd=start_in)
    assert [fault.rule for fault in faults] == [ROOT], faults
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.splitlines() == [printed(faults[0])], result.stderr


@then("everything the shop already knows is still there, unchanged")
def _still_there(env, known_before):
    assert knol(env, "journal").stdout == known_before["journal"]


@given(
    "the user is working in a directory that has since been removed, and nothing names a knowledge base",
    target_fixture="start_in",
)
def _a_removed_directory(env, tmp_path):
    del env["KB_ROOT"]
    return removed(tmp_path)


GONE = "the directory you are working in is gone"
"""shop-knol's own words, not kb's, for a start from a working directory that no longer exists: kb is not called."""


@then("starting the knowledge base is rejected because the directory they are working in is gone")
def _rejected_as_gone(result):
    """One plain line, naming no rule and no place, since the place is the one that is gone."""
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.splitlines() == [GONE], result.stderr


def _finding(env, start_in) -> list:
    """kb's own refusal to find a knowledge base from where the user started one, asked with the call init finds it
    by: the names of the types it holds."""
    asked = kb_pb2.ListRequest(kind="schema", form=kb_pb2.ListRequest.IDS)
    return kb_answer(env, "List", asked, cwd=start_in).refusal.faults


def _refused_as_kb_refuses_finding(env, result, start_in):
    """Every line printed is one of kb's own faults for finding no knowledge base from the same place, under the
    same KB_ROOT, and nothing else is shown."""
    faults = _finding(env, start_in)
    assert faults, "kb finds a knowledge base from there"
    assert result.returncode == 1
    assert result.stdout == ""
    assert set(result.stderr.splitlines()) == {printed(fault) for fault in faults}, result.stderr


@then("starting the knowledge base is rejected because KB_ROOT names a directory that holds no knowledge base")
def _rejected_kb_root_holds_none(env, result, start_in):
    _refused_as_kb_refuses_finding(env, result, start_in)


@then("no knowledge base is started")
def _none_started(env, start_in, tmp_path, started_before):
    """Neither where the user works, nor the test's own directory, nor KB_ROOT's directory, holds one now, unless a
    Given started it there before the user ran init."""
    for directory in {start_in, tmp_path, Path(env.get("KB_ROOT", tmp_path))} - started_before:
        assert not store_in(directory).exists(), directory


@given(
    "the user is working inside a knowledge base kb's operator started empty, with KB_ROOT naming a different one",
    target_fixture="start_in",
)
def _inside_one_kb_root_names_another(env, shop, tmp_path, started_before):
    other = tmp_path / "other"
    other.mkdir()
    for root in (shop, other):
        operator_started(env, root)
    started_before.update({shop, other})
    env["KB_ROOT"] = str(other)
    # Works in the directory kb's contract says init made (`kb.init`), inside the knowledge base.
    return store_in(shop)


@then("starting the knowledge base is rejected because KB_ROOT names a knowledge base other than the one they are working in")
def _rejected_two_stores(env, result, start_in):
    _refused_as_kb_refuses_finding(env, result, start_in)
