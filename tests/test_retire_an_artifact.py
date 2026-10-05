from kb.content import loads
from kb.contract import kb_pb2
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start
from kb_oracle import kb_answer, printed, signature

scenarios("retire-an-artifact.feature")

SEASONAL = "tag/seasonal"
PRICING = "tag/pricing"
MONTHLY = "decision/prices-are-reviewed-monthly"
NO_LONGER_NEEDED = "No longer needed"


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
    return knol(env, "delete", PRICING, "-m", NO_LONGER_NEEDED)


@then("the removal is rejected because something in the shop still points at it")
def _rejected(result, env):
    """Refused for the rule kb publishes for a link still pointing at what is removed, each fault printed as kb
    returned it."""
    faults = _kb_refuses_to_remove(env)
    assert faults and all(fault.rule == STILL_LINKED for fault in faults), faults
    assert result.returncode != 0
    assert result.stdout == ""
    assert sorted(result.stderr.splitlines()) == sorted(printed(fault) for fault in faults), result.stderr
    assert knol(env, "read", PRICING).returncode == 0


@then("the user is told everything that points at it")
def _told_what_points_at_it(env, result):
    """One line for the one decision tagged with it, naming that decision, in kb's words."""
    faults = _kb_refuses_to_remove(env)
    assert [fault.artifact for fault in faults] == [MONTHLY], faults
    assert result.stderr.splitlines() == [printed(faults[0])], result.stderr


STILL_LINKED = "on_delete"
"""The `rule` kb's contract publishes (kb adrs/0018) for a link that still points at what a removal takes out."""


def _kb_refuses_to_remove(env):
    """kb's own answer to the removal the user asked for, asked of the same store: refused, so nothing is removed;
    its faults' words are kb's."""
    request = kb_pb2.RemoveRequest(locator=kb_pb2.Locator(id=PRICING), signature=signature(env, NO_LONGER_NEEDED))
    return kb_answer(env, "Remove", request).refusal.faults
