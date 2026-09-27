import pytest
from kb.content import dumps
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start, whole

scenarios("revise-what-the-shop-knows.feature")

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


def _without_the_rationale(whole):
    """A whole read with what a revision of the rationale is allowed to change taken out."""
    return {
        **{key: value for key, value in whole.items() if key != "revision"},
        "sections": [section for section in whole["sections"] if section["title"] != "Rationale"],
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
