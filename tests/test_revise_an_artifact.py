import json

import pytest
from kb.content import dumps
from pytest_bdd import given, parsers, scenarios, then, when

from driver import UNKEPT, knol, record, refused_as_unkept, start, whole

scenarios("revise-an-artifact.feature")

NEW_SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with what the shop pays.\n"},
    {"title": "Rationale", "body": "Costs now move every day.\n"},
]


@given(
    "a shop knowledge base holding a decision with a purpose and a rationale, at its first version",
    target_fixture="decision_id",
)
def _shop_with_a_decision(env, shop, tmp_path):
    start(env, shop)
    return record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }, "Move price reviews to weekly")


@pytest.fixture
def before(env, decision_id):
    """The whole decision as the user read it before the change, taken when the When asks for it."""
    return whole(env, decision_id)


@when("the user replaces the decision from a file, saying who they are and why", target_fixture="result")
def _replace_the_decision(env, decision_id, tmp_path, before):
    path = tmp_path / "new-wording.yaml"
    path.write_text(dumps({"sections": NEW_SECTIONS}))
    return knol(env, "write", decision_id, "--from", str(path), "-m", "Costs now move daily")


@then("the shop holds the new wording")
def _holds_the_new_wording(env, decision_id, result):
    assert result.returncode == 0, result.stderr
    assert whole(env, decision_id)["sections"] == NEW_SECTIONS


@then("the decision is at a later version than before")
def _later_version(env, decision_id, before):
    assert whole(env, decision_id)["revision"] > before["revision"] == 1


@when("the user replaces the rationale of the decision from a file, saying who they are and why", target_fixture="result")
def _replace_the_rationale(env, decision_id, tmp_path, before):
    path = tmp_path / "new-rationale.yaml"
    path.write_text(dumps({"title": "Rationale", "body": "Costs now move every day.\n"}))
    return knol(env, "write", f"{decision_id}#sections/rationale", "--from", str(path), "-m", "Costs now move daily")


def _without_the_rationale(document):
    """A whole read with what a revision of the rationale is allowed to change taken out."""
    return {
        **{key: value for key, value in document.items() if key != "revision"},
        "sections": [section for section in document["sections"] if section["title"] != "Rationale"],
    }


@then("only the rationale changes")
def _only_the_rationale_changes(env, decision_id, result, before):
    assert result.returncode == 0, result.stderr
    after = whole(env, decision_id)
    assert after["revision"] > before["revision"]
    rationale = [section for section in after["sections"] if section["title"] == "Rationale"]
    assert rationale == [{"title": "Rationale", "body": "Costs now move every day.\n"}]


@then("the rest of the decision reads as before")
def _the_rest_reads_as_before(env, decision_id, before):
    assert _without_the_rationale(whole(env, decision_id)) == _without_the_rationale(before)


@given("a file whose prose has a line ending in a space before its last line", target_fixture="unkept")
def _files_with_unkept_prose(tmp_path):
    """For each part the user may replace, a file of that part whose rationale's first line ends in a space, written
    as a quoted scalar, and the place in the file where it is. Which one the user gives is the When's to say."""
    whole_file, section_file = tmp_path / "unkept-decision.yaml", tmp_path / "unkept-rationale.yaml"
    whole_file.write_text(
        "sections:\n"
        "  - title: Purpose\n    body: Keep prices in step with what the shop pays.\n"
        f"  - title: Rationale\n    body: {json.dumps(UNKEPT)}\n"
    )
    section_file.write_text(f"title: Rationale\nbody: {json.dumps(UNKEPT)}\n")
    return {
        "the decision": ("", whole_file, "sections/1/body"),
        "the rationale of the decision": ("#sections/rationale", section_file, "body"),
    }


@when(parsers.parse("the user replaces {what} from that file, saying who they are and why"), target_fixture="result")
def _replace_from_that_file(env, decision_id, unkept, what, before):
    """Notes which file it gave as `unkept["given"]`, for the Then."""
    unkept["given"] = unkept[what]
    inside, path, _ = unkept[what]
    return knol(env, "write", f"{decision_id}{inside}", "--from", str(path), "-m", "Costs now move daily")


@then(
    "the change is rejected because the shop cannot keep prose in which a line before the last ends in a space, "
    "naming the place in the file"
)
def _rejected_as_unkept(result, unkept):
    _, path, place = unkept["given"]
    refused_as_unkept(result, path, place)


@then("the decision reads as before, still at its first version")
def _reads_as_before(env, decision_id, before):
    assert before["revision"] == 1
    assert whole(env, decision_id) == before
