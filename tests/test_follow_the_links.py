from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("follow-the-links.feature")

OLDER = "decision/prices-are-reviewed-monthly"
DECISION = "decision/price-reviews-happen-weekly"
TAG = "tag/pricing"
WORK_ITEMS = {"work-item/move-the-review-to-mondays", "work-item/tell-the-pricing-team"}


@given("a shop knowledge base where a decision supersedes an older decision", target_fixture="decision_id")
def _shop_with_a_decision_over_an_older_one(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "tag", {"title": "pricing", "description": "How the shop sets prices.\n"}, "Add the pricing tag")
    record(env, tmp_path, "decision", {
        "title": "Prices are reviewed monthly",
        "tags": [TAG],
        "sections": [
            {"title": "Purpose", "body": "Keep prices current.\n"},
            {"title": "Rationale", "body": "Monthly was enough once.\n"},
        ],
    }, "Record the monthly review")
    return record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        "supersedes": OLDER,
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }, "Move price reviews to weekly")


@given("two work items point at that decision")
def _two_work_items_point_at_it(env, tmp_path, decision_id):
    record(env, tmp_path, "work-item", {"title": "Move the review to Mondays", "decisions": [decision_id]}, "Plan the move")
    record(env, tmp_path, "work-item", {"title": "Tell the pricing team", "decisions": [decision_id]}, "Plan the telling")


@given('the older decision is tagged "pricing"')
def _older_decision_is_tagged():
    """Already so: the shop's first decision is recorded tagged pricing."""


@when("the user follows the links out of the decision", target_fixture="result")
def _follow_out(env, decision_id):
    return knol(env, "refs", decision_id, "--outbound")


@then("the user sees the older decision")
def _sees_the_older_decision(shown):
    assert [entry["id"] for entry in shown] == [OLDER]


@when("the user follows the links into the decision", target_fixture="result")
def _follow_in(env, decision_id):
    return knol(env, "refs", decision_id, "--inbound")


@then("the user sees both work items")
def _sees_both_work_items(shown):
    assert {entry["id"] for entry in shown} == WORK_ITEMS


@when(
    "the user follows the links into the decision, only through the link a work item uses, and only from work items",
    target_fixture="result",
)
def _follow_in_narrowed(env, decision_id):
    return knol(env, "refs", decision_id, "--inbound", "--via", "decisions", "--type", "work-item")


@then("the user sees both work items and nothing else")
def _sees_both_work_items_and_nothing_else(shown):
    assert {entry["id"] for entry in shown} == WORK_ITEMS
    assert len(shown) == len(WORK_ITEMS)


@when("the user follows the links out of the decision two steps", target_fixture="result")
def _follow_out_two_steps(env, decision_id):
    return knol(env, "refs", decision_id, "--outbound", "--depth", "2")


@then('the user sees the older decision and the tag "pricing"')
def _sees_the_older_decision_and_the_tag(shown):
    assert [entry["id"] for entry in shown] == [OLDER, TAG]


@then("the user sees the route taken to each of them")
def _sees_the_routes(shown):
    routes = {entry["id"]: [(hop["field"], hop["id"]) for hop in entry["route"]] for entry in shown}
    assert routes == {
        OLDER: [("supersedes", OLDER)],
        TAG: [("supersedes", OLDER), ("tags", TAG)],
    }
