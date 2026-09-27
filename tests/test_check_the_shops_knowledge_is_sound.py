from kb.content import dumps, loads
from pytest_bdd import given, scenarios, then, when

from driver import answering, knol, record, start, whole

scenarios("check-the-shops-knowledge-is-sound.feature")

WEEKLY = "decision/price-reviews-happen-weekly"
MONTHLY = "decision/prices-are-reviewed-monthly"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]
WORK_ITEM = "work-item/reprice-the-dairy-shelf"


def _checked_as(env, tmp_path, *violations):
    """kb refuses to store an artifact unreadable, unfit for its type or pointing at nothing, so no contract call can
    leave the shop so: kb's check answers for that state through the stand-in (adrs/0047), with the violations as this
    module words them, beside what the real check finds behind its type."""
    env.update(answering(env, tmp_path, {
        "call": "Validate", "answer": {"violations": list(violations)}, "from_kb": ["stale"],
    }))


def _line(fault: dict) -> str:
    """A fault the stand-in gave, as the line the user is shown."""
    where = f"{fault['artifact']} at {fault['path']}" if fault.get("path") else fault["artifact"]
    return f"{where}: {fault['message']}"


def _without_its_rationale(decision: str) -> dict:
    """The fault of a decision whose file was edited by hand to drop a section its type requires."""
    return {"artifact": decision, "path": "sections", "rule": "sections", "message": "its rationale was removed by hand"}


UNREADABLE = {"artifact": WEEKLY, "rule": "unreadable", "message": "the decision's file, edited by hand, cannot be read"}
NO_BODY = {"artifact": MONTHLY, "path": "sections/0", "rule": "required", "message": "its purpose lost its body by hand"}
DANGLING = {
    "artifact": WORK_ITEM, "path": "decisions/0", "rule": "ref",
    "message": "it was pointed by hand at decision/nothing, which the shop does not hold",
}


@given(
    "a shop knowledge base where someone edited a decision's file by hand and left it in a shape the shop cannot read"
)
def _shop_with_a_file_mangled_by_hand(env, shop, tmp_path):
    """Two decisions recorded, then edited by hand: one left unreadable, one left readable but without the body of its
    purpose; the check's answer for that comes from the stand-in."""
    start(env, shop)
    record(env, tmp_path, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly")
    record(env, tmp_path, "decision", {"title": "Prices are reviewed monthly", "sections": SECTIONS}, "Record monthly")
    _checked_as(env, tmp_path, UNREADABLE, NO_BODY)


@when("the user checks the shop's knowledge", target_fixture="result")
def _check(env):
    return knol(env, "validate")


@then("that file is listed as a fault, naming the file")
def _unreadable_listed(result):
    assert _line(UNREADABLE) in result.stderr.splitlines()


@then("everything else the shop knows is checked and listed alongside it")
def _the_rest_listed(result):
    """kb states no order among a check's faults, so the two lines are held to as a set, not a position."""
    assert set(result.stderr.splitlines()) == {_line(UNREADABLE), _line(NO_BODY)}


@given("a shop knowledge base where everything fits its type")
def _shop_where_everything_fits(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly")
    return shop


@then("the user is told nothing is wrong")
def _told_nothing_is_wrong(result, shown):
    assert shown["sound"] is True
    assert shown["behind"] == []
    assert result.stderr == ""


@given(
    "a shop knowledge base where a decision is missing something its type requires and a work item points at something the shop does not hold"
)
def _shop_with_two_faults(env, shop, tmp_path):
    """Both are recorded through shop-knol, then their files edited by hand; the check's answer for that comes from
    the stand-in."""
    start(env, shop)
    record(env, tmp_path, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly")
    record(env, tmp_path, "work-item", {"title": "Reprice the dairy shelf"}, "Open the repricing")
    _checked_as(env, tmp_path, _without_its_rationale(WEEKLY), DANGLING)


@then("both faults are listed, each naming the artifact and the place in it at fault")
def _both_listed(result):
    """kb states no order among a check's faults, so the two lines are held to as a set, not a position."""
    assert set(result.stderr.splitlines()) == {_line(_without_its_rationale(WEEKLY)), _line(DANGLING)}


@given(
    "a shop knowledge base where a decision was last checked against an older version of the decision type",
    target_fixture="decisions",
)
def _shop_with_a_decision_behind_its_type(env, shop, tmp_path):
    """The decision recorded before the decision type is brought to version 2 is behind it."""
    start(env, shop)
    record(env, tmp_path, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly")
    held = whole(env, "schema/decision")
    for identity in ("id", "type", "schema_version", "revision", "title"):
        del held[identity]  # a write carries content alone
    path = tmp_path / "decision-type-2.yaml"
    path.write_text(dumps({**held, "version": 2}))
    written = knol(env, "write", "schema/decision", "--from", str(path), "-m", "Bring the decision type to version 2")
    assert written.returncode == 0, written.stderr
    return {"behind": WEEKLY}


@given(
    "a shop knowledge base where a decision is missing something its type requires and another decision was last "
    "checked against an older version of the decision type",
    target_fixture="decisions",
)
def _shop_with_a_fault_and_a_decision_behind(env, shop, tmp_path):
    """Recorded after the decision type is at version 2, so only the first decision is behind it, which the real check
    finds; the second is then left unfit by hand, which the stand-in answers for."""
    decisions = _shop_with_a_decision_behind_its_type(env, shop, tmp_path)
    record(env, tmp_path, "decision", {"title": "Prices are reviewed monthly", "sections": SECTIONS}, "Record monthly")
    _checked_as(env, tmp_path, _without_its_rationale(MONTHLY))
    return {**decisions, "at_fault": _without_its_rationale(MONTHLY)}


@then("the fault is listed, naming the artifact and the place in it at fault")
def _the_fault_listed(result, decisions):
    assert result.stderr.splitlines() == [_line(decisions["at_fault"])], result.stderr


@then("the other decision is listed as behind its type")
def _other_listed_as_behind(result, decisions):
    """Read from stdout directly: the shared `shown` is for a command that succeeded, and a check with faults fails."""
    assert loads(result.stdout)["behind"] == [{"artifact": decisions["behind"], "schema_version": 1, "current": 2}]


@then("that decision is listed as behind its type")
def _listed_as_behind(shown):
    assert shown["behind"] == [{"artifact": WEEKLY, "schema_version": 1, "current": 2}]


@then("it is not listed as a fault")
def _not_a_fault(result, decisions):
    """No fault line names what is behind its type; a check that listed no fault at all succeeded."""
    assert not [line for line in result.stderr.splitlines() if line.startswith(decisions["behind"])], result.stderr
    if not result.stderr:
        assert result.returncode == 0
