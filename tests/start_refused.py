"""The steps of start-a-knowledge-base.feature about a start that kb refuses: a directory already holding a
knowledge base, or inside one, and a directory since removed. The feature's test module star-imports this and no
other does."""
import pytest
from kb.contract import kb_pb2
from pytest_bdd import given, then

from driver import actor, kb_answer, knol, printed, removed, start, store_in


@pytest.fixture
def known_before(env):
    """What `shop-knol journal` answered before the user started a knowledge base, filled in by the Given that starts one."""
    return {}


def _started_and_noted(env, shop, known_before):
    start(env, shop)
    known_before["journal"] = knol(env, "journal").stdout


@given("the user is working in a directory that already holds the shop's knowledge")
def _a_directory_already_started(env, shop, known_before):
    _started_and_noted(env, shop, known_before)


@given("the user is working in a directory that sits inside the shop's knowledge", target_fixture="start_in")
def _a_directory_inside_a_started_one(env, shop, known_before):
    _started_and_noted(env, shop, known_before)
    # Works in the directory kb's contract says init made (its Init row), inside the knowledge base.
    return store_in(shop)


@then("starting the knowledge base is rejected because that directory already holds a knowledge base")
def _rejected_already_started(env, result, start_in):
    _refused_as_kb_refuses_init(env, result, start_in)


@then("starting the knowledge base is rejected because that directory is inside a knowledge base")
def _rejected_inside_one(env, result, start_in):
    _refused_as_kb_refuses_init(env, result, start_in)


ROOT = "root"
"""The `rule` kb's contract publishes (kb adrs/0018) for a store refused where it was to be started."""


def _refused_as_kb_refuses_init(env, result, start_in):
    """One line, printed as kb returned it: kb's own answer to the same Init, starting a store in the same directory,
    is a refusal of the directory given, and the user is shown that fault in kb's words. Which refusal, the Given
    decides; a refused Init changes nothing."""
    request = kb_pb2.InitRequest(root=str(start_in.resolve()), actor=actor(env))
    faults = kb_answer(env, "Init", request, cwd=start_in).faults
    assert [fault.rule for fault in faults] == [ROOT], faults
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.splitlines() == [printed(faults[0])], result.stderr


@then("everything the shop already knows is still there, unchanged")
def _still_there(env, known_before):
    assert knol(env, "journal").stdout == known_before["journal"]


@given("the user is working in a directory that has since been removed", target_fixture="start_in")
def _a_removed_directory(tmp_path):
    return removed(tmp_path)


GONE = "the directory you are working in is gone"
"""shop-knol's own words, not kb's, for a start from a working directory that no longer exists: kb is not called."""


@then("starting the knowledge base is rejected because the directory they are working in is gone")
def _rejected_as_gone(result):
    """One plain line, naming no rule and no place, since the place is the one that is gone."""
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.splitlines() == [GONE], result.stderr
