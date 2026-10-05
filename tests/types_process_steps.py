"""The steps of use-the-shops-types.feature about a process's steps, in place or shared. The feature's test module
star-imports this and no other does."""
from kb.content import dumps
from pytest_bdd import given, parsers, then, when

from driver import knol, record, start, whole

IN_PLACE = {"title": "Count", "does": "Count what is on the shelf."}
SETTINGS = [{"name": "aisle", "value": "3"}]


@given('a shop knowledge base holding a shared step "check the stock"', target_fixture="shared")
def _a_base_holding_a_shared_step(env, shop, tmp_path):
    start(env, shop)
    return record(env, tmp_path, "step", {"title": "Check the stock", "does": "Count what is on the shelf."}, "Share a step")


def _item(given_as, shared):
    if given_as == "describes what to do in place":
        return IN_PLACE
    return {"title": "Check", "uses": shared, "with": SETTINGS}


@when(parsers.parse("the user records a process with a step that {given_as}, saying who they are and why"), target_fixture="result")
def _records_a_process(env, tmp_path, shared, given_as):
    path = tmp_path / "process.yaml"
    path.write_text(dumps({"title": "Restock", "steps": [_item(given_as, shared)]}))
    return knol(env, "create", "process", "--from", str(path), "-m", "Record a process")


@then(parsers.parse("the process keeps that step {kept_as}"))
def _keeps_the_step(env, shown, shared, kept_as):
    step = whole(env, shown["id"])["steps"][0]
    if kept_as == "as described, in place":
        assert {"title": step["title"], "does": step["does"]} == IN_PLACE
        assert "uses" not in step
    else:
        assert (step["uses"], step["with"]) == (shared, SETTINGS)
