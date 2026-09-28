"""The steps of record-a-decision.feature about a file the shop refuses to record: one that does not fit the decision
type, one that names an entry twice, one whose prose kb cannot keep as written, and one given an empty name. Each
Then here compares what the user is shown with kb's own refusal of the same thing, so no step spells kb's wording (kb
adrs/0018). The feature's test module star-imports this and no other does."""
import json

from kb.content import NotCanonical, dumps, loads
from kb.contract import kb_pb2
from pytest_bdd import given, then, when

from driver import UNKEPT, actor, kb_answer, knol, printed, refused_as_unkept

SAYING_WHY = "Move price reviews to weekly"
"""The message the user records a file with when "saying who they are and why"."""


@given("a file missing something the shop's decision type requires", target_fixture="decision_file")
def _file_missing_a_section(tmp_path):
    """A title and a Purpose but no Rationale, so kb's answer is one fault naming the artifact and the place."""
    path = tmp_path / "unfinished.yaml"
    path.write_text(dumps({
        "title": "Prices are reviewed monthly",
        "sections": [{"title": "Purpose", "body": "Keep prices current.\n"}],
    }))
    return path


@then("the decision is rejected because it does not fit the shop's decision type")
def _rejected_for_not_fitting(env, result, decision_file):
    """Printed as kb returned it: every fault kb's own answer to the same Create gives, one line each."""
    faults = _kb_refuses_to_create(env, decision_file)
    assert faults and all(fault.artifact.startswith("decision/") for fault in faults), faults
    assert sorted(result.stderr.splitlines()) == sorted(printed(fault) for fault in faults), result.stderr


def _kb_refuses_to_create(env, decision_file):
    """kb's own answer to the Create the user's command made of the file ("saying who they are and why"), asked of the
    same store: its faults, whose words are kb's (kb adrs/0018)."""
    content = loads(decision_file.read_text())
    title = content.pop("title")
    request = kb_pb2.CreateRequest(
        type="decision", title=title, content=dumps(content), actor=actor(env), message=SAYING_WHY,
    )
    return kb_answer(env, "Create", request).faults


@then("the user is told which artifact and which place in it is at fault")
def _told_artifact_and_place(env, result, decision_file):
    """One line, naming the artifact and the place the shop's spec says, in kb's words for the fault there."""
    faults = _kb_refuses_to_create(env, decision_file)
    assert [(fault.artifact, fault.path) for fault in faults] == [("decision/prices-are-reviewed-monthly", "sections")]
    assert result.stderr.splitlines() == [printed(faults[0])], result.stderr


@given("a decision in a file that names the same entry twice in the same place", target_fixture="decision_file")
def _decision_in_a_file_naming_an_entry_twice(tmp_path):
    path = tmp_path / "twice.yaml"
    path.write_text(
        "title: Price reviews happen weekly\n"
        "sections:\n"
        "  - title: Purpose\n"
        "    body: Keep prices in step with costs.\n"
        "    body: Keep prices low.\n"
        "  - title: Rationale\n"
        "    body: Costs move weekly.\n"
    )
    return path


@then("the decision is rejected because an entry is named once and only once, naming the place in the file")
def _rejected_for_an_entry_named_twice(result, decision_file):
    """One line naming the file and the place in it the step wrote twice, in the words kb's published reading of
    content (`kb.content.loads`) refuses the same text with (kb adrs/0018). The place is pinned to the step's own
    knowledge of its own file, in the contract's Fault.path form, beside the comparison with kb's own refusal: a
    regression in where kb reports the place would otherwise pass unnoticed."""
    fault = _kb_refuses_to_read(decision_file)
    assert fault.path == "sections/0/body", fault.path
    assert result.stderr.splitlines() == [printed(fault)], result.stderr


def _kb_refuses_to_read(path) -> kb_pb2.Fault:
    """kb's own refusal of the file's text, read the way kb reads content (`kb.content.NotCanonical`, kb adrs/0018),
    as the fault on the file it names: the place is the refusal's own `path`, never spelled here."""
    try:
        loads(path.read_text())
    except NotCanonical as refusal:
        return kb_pb2.Fault(artifact=str(path), path=refusal.path, message=str(refusal))
    raise AssertionError(f"kb reads {path} plainly")


@when("the user records a decision from a file whose name is given empty, saying who they are and why", target_fixture="result")
def _record_from_an_empty_name(env, before):
    """Asks for `before` so the knowledge base is taken as it was before the command runs."""
    return knol(env, "create", "decision", "--from", "", "-m", SAYING_WHY)


@given("a decision in a file whose prose has a line ending in a space before its last line", target_fixture="decision_file")
def _decision_in_a_file_with_unkept_prose(tmp_path):
    """Its rationale's first line ends in a space, written as a quoted scalar the way a person might."""
    path = tmp_path / "unkept.yaml"
    path.write_text(
        "title: Price reviews happen weekly\n"
        "sections:\n"
        "  - title: Purpose\n"
        "    body: Keep prices in step with costs.\n"
        "  - title: Rationale\n"
        f"    body: {json.dumps(UNKEPT)}\n"
    )
    return path


@then(
    "the decision is rejected because the shop cannot keep prose in which a line before the last ends in a space, "
    "naming the place in the file"
)
def _rejected_as_unkept(result, decision_file):
    refused_as_unkept(result, decision_file, "sections/1/body")
