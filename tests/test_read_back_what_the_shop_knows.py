import pytest
from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("read-back-what-the-shop-knows.feature")

OLDER = "decision/prices-are-reviewed-monthly"
DECISION = "decision/price-reviews-happen-weekly"


@given(
    'a shop knowledge base holding a decision with a purpose and a rationale, tagged "pricing", '
    "superseding an older decision, and pointed at by two work items",
    target_fixture="decision_id",
)
def _shop_with_a_linked_decision(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "tag", {"title": "pricing", "description": "How the shop sets prices.\n"}, "Add the pricing tag")
    record(env, tmp_path, "decision", {
        "title": "Prices are reviewed monthly",
        "sections": [
            {"title": "Purpose", "body": "Keep prices current.\n"},
            {"title": "Rationale", "body": "Monthly was enough once.\n"},
        ],
    }, "Record the monthly review")
    decision_id = record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        "supersedes": OLDER,
        "tags": ["tag/pricing"],
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }, "Move price reviews to weekly")
    record(env, tmp_path, "work-item", {"title": "Move the review to Mondays", "decisions": [DECISION]}, "Plan the move")
    record(env, tmp_path, "work-item", {"title": "Tell the pricing team", "decisions": [DECISION]}, "Plan the telling")
    return decision_id


@when("the user reads the decision", target_fixture="result")
def _read_the_decision(env, decision_id):
    return knol(env, "read", decision_id)


@pytest.fixture
def shown(result):
    """What the user is shown, for the steps that expect the read to succeed."""
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)


@then("the user sees its name, its title and the few fields the shop shows for a decision")
def _name_title_and_fields(shown):
    assert shown["id"] == DECISION
    assert shown["title"] == "Price reviews happen weekly"
    assert shown["supersedes"] == OLDER
    assert shown["tags"] == ["tag/pricing"]


@then("the user sees a stub of each thing it points at")
def _stubs(shown):
    stubs = {(stub["field"], stub["id"], stub["type"], stub["title"]) for stub in shown["references"]}
    assert stubs == {
        ("supersedes", OLDER, "decision", "Prices are reviewed monthly"),
        ("tags", "tag/pricing", "tag", "pricing"),
    }


@then("the user sees how many things point back at it, and of what kind")
def _inbound(shown):
    assert shown["inbound"] == [{"type": "work-item", "field": "decisions", "count": 2}]



@given("someone edited the decision's file by hand and left it in a shape the shop cannot read")
def _decision_file_mangled_by_hand(shop):
    (shop / "kb" / f"{DECISION}.yaml").write_text("title: [a bracket opened by hand and never closed\n")


@then("the command is rejected because that file cannot be read, naming the file")
def _rejected_as_unreadable(result):
    assert result.stderr.startswith(f"{DECISION}: the stored file {DECISION}.yaml cannot be read: ")
