from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("retire-what-the-shop-no-longer-uses.feature")

SEASONAL = "tag/seasonal"
PRICING = "tag/pricing"


@given('a shop knowledge base holding a tag "seasonal" that nothing points at')
def _shop_with_an_unused_tag(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "tag", {"title": "seasonal", "description": "Goods that sell for a season.\n"}, "Add the seasonal tag")


@given('a tag "pricing" that a decision is tagged with')
def _tag_a_decision_carries(env, tmp_path):
    record(env, tmp_path, "tag", {"title": "pricing", "description": "How the shop sets prices.\n"}, "Add the pricing tag")
    record(env, tmp_path, "decision", {
        "title": "Prices are reviewed monthly",
        "tags": [PRICING],
        "sections": [
            {"title": "Purpose", "body": "Keep prices current.\n"},
            {"title": "Rationale", "body": "Monthly was enough once.\n"},
        ],
    }, "Record the monthly review")


@when('the user retires "seasonal", saying who they are and why', target_fixture="result")
def _retire_the_unused_tag(env):
    return knol(env, "delete", SEASONAL, "-m", "No longer sold by season")


@then("the shop no longer holds it")
def _no_longer_held(env, shown):
    assert knol(env, "read", SEASONAL).returncode != 0
    listed = knol(env, "list", "--type", "tag", "--ids")
    assert listed.returncode == 0, listed.stderr
    assert loads(listed.stdout) == [PRICING]


@when('the user retires "pricing", saying who they are and why', target_fixture="result")
def _retire_the_tag_in_use(env):
    return knol(env, "delete", PRICING, "-m", "No longer needed")


@then("the removal is rejected because something in the shop still points at it")
def _rejected(result, env):
    assert result.returncode != 0
    assert result.stdout == ""
    assert "cannot be removed while" in result.stderr
    assert knol(env, "read", PRICING).returncode == 0


@then("the user is told everything that points at it")
def _told_what_points_at_it(result):
    pointers = [line for line in result.stderr.splitlines() if "points at it" in line]
    assert len(pointers) == 1 and "decision/prices-are-reviewed-monthly" in pointers[0], result.stderr
