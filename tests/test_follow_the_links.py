import pytest
from pytest_bdd import given, scenarios, then, when

from decision_fields import decided, shop_of
from driver import knol, record, start, whole

from follow_into_capability_steps import *  # noqa: F403  pytest-bdd registers steps only through a star import

scenarios("follow-the-links.feature")

OLDER = "decision/prices-are-reviewed-monthly"
DECISION = "decision/price-reviews-happen-weekly"
TAG = "tag/pricing"
WORK_ITEMS = {"work-item/move-the-review-to-mondays", "work-item/tell-the-pricing-team"}


@pytest.fixture
def held():
    """The names kb minted for the decisions' shop and its product, as the Background records them."""
    return {}


@given("a shop knowledge base where a decision supersedes an older decision", target_fixture="decision_id")
def _shop_with_a_decision_over_an_older_one(env, shop, tmp_path, held):
    start(env, shop)
    held["shop"] = shop_of(env, tmp_path)
    held["product"] = whole(env, held["shop"])["product"]
    record(env, tmp_path, "tag", {"title": "pricing", "description": "How the shop sets prices.\n"}, "Add the pricing tag")
    record(env, tmp_path, "decision", {
        "title": "Prices are reviewed monthly",
        **decided(1, held["shop"]),
        "tags": [TAG],
        "sections": [
            {"title": "Purpose", "body": "Keep prices current.\n"},
            {"title": "Rationale", "body": "Monthly was enough once.\n"},
        ],
    }, "Record the monthly review")
    return record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        **decided(2, held["shop"]),
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


@then("the user sees the older decision and the decision's shop")
def _sees_the_older_decision_and_the_shop(shown, held):
    assert {entry["id"] for entry in shown} == {OLDER, held["shop"]}


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


@then('the user sees the older decision, the tag "pricing", the decision\'s shop and that shop\'s product')
def _sees_the_older_decision_the_tag_the_shop_and_its_product(shown, held):
    assert {entry["id"] for entry in shown} == {OLDER, TAG, held["shop"], held["product"]}


@then("the user sees the route taken to each of them")
def _sees_the_routes(shown, held):
    routes = {entry["id"]: [(hop["field"], hop["id"]) for hop in entry["route"]] for entry in shown}
    assert routes == {
        OLDER: [("supersedes", OLDER)],
        TAG: [("supersedes", OLDER), ("tags", TAG)],
        held["shop"]: [("shop", held["shop"])],
        held["product"]: [("shop", held["shop"]), ("product", held["product"])],
    }
