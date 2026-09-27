from kb import canonical
from kb.content import dumps, loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start, whole

scenarios("check-the-shops-knowledge-is-sound.feature")

WEEKLY = "decision/price-reviews-happen-weekly"
MONTHLY = "decision/prices-are-reviewed-monthly"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given(
    "a shop knowledge base where someone edited a decision's file by hand and left it in a shape the shop cannot read"
)
def _shop_with_a_file_mangled_by_hand(env, shop, tmp_path):
    """Two decisions edited by hand: one left unreadable, one left readable but without the body of its purpose."""
    start(env, shop)
    record(env, tmp_path, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly")
    record(env, tmp_path, "decision", {"title": "Prices are reviewed monthly", "sections": SECTIONS}, "Record monthly")
    (shop / "kb" / f"{WEEKLY}.yaml").write_text("title: [a bracket opened by hand and never closed\n")
    monthly = shop / "kb" / f"{MONTHLY}.yaml"
    held = canonical.load(monthly.read_text())
    del held["sections"][0]["body"]
    monthly.write_text(canonical.dump(held))


@when("the user checks the shop's knowledge", target_fixture="result")
def _check(env):
    return knol(env, "validate")


@then("that file is listed as a fault, naming the file")
def _unreadable_listed(result):
    assert result.stderr.splitlines()[0].startswith(f"{WEEKLY}: the stored file {WEEKLY}.yaml cannot be read: ")


@then("everything else the shop knows is checked and listed alongside it")
def _the_rest_listed(result):
    assert result.stderr.splitlines()[1:] == [f"{MONTHLY} at sections/0: 'body' is a required property"]


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
    """kb refuses to create either fault, so no shop-knol command can leave an artifact unfit (CLAUDE.md, Step
    definitions): both are recorded through shop-knol, then their files are edited by hand."""
    start(env, shop)
    record(env, tmp_path, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly")
    record(env, tmp_path, "work-item", {"title": "Reprice the dairy shelf"}, "Open the repricing")
    _without_its_rationale(shop, WEEKLY)
    work_item = shop / "kb" / "work-item" / "reprice-the-dairy-shelf.yaml"
    held = canonical.load(work_item.read_text())
    held["decisions"] = ["decision/nothing"]
    work_item.write_text(canonical.dump(held))


def _without_its_rationale(shop, decision):
    """A decision's file edited by hand to drop a section its type requires, which no shop-knol command can do."""
    path = shop / "kb" / f"{decision}.yaml"
    held = canonical.load(path.read_text())
    del held["sections"][1]
    path.write_text(canonical.dump(held))


@then("both faults are listed, each naming the artifact and the place in it at fault")
def _both_listed(result):
    lines = result.stderr.splitlines()
    assert len(lines) == 2
    assert lines[0].startswith(f"{WEEKLY} at sections: ")
    assert lines[1].startswith("work-item/reprice-the-dairy-shelf at decisions/0: ")


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
    """Recorded after the decision type is at version 2, so only the first decision is behind it; the second is then
    left unfit by hand (CLAUDE.md, Step definitions), as kb refuses to create it so."""
    decisions = _shop_with_a_decision_behind_its_type(env, shop, tmp_path)
    record(env, tmp_path, "decision", {"title": "Prices are reviewed monthly", "sections": SECTIONS}, "Record monthly")
    _without_its_rationale(shop, MONTHLY)
    return {**decisions, "at_fault": MONTHLY}


@then("the fault is listed, naming the artifact and the place in it at fault")
def _the_fault_listed(result, decisions):
    lines = result.stderr.splitlines()
    assert len(lines) == 1, result.stderr
    assert lines[0].startswith(f"{decisions['at_fault']} at sections: ")


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
