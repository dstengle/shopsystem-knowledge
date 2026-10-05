"""The steps of use-the-shops-types.feature that record each of the shop's seven types with the fields every shop
artifact carries, and those of a process's steps. The feature's test module star-imports this and no other does."""
from kb.content import dumps
from pytest_bdd import given, parsers, then, when

from driver import knol, record, start, whole

SECTIONS = [{"title": "Purpose", "body": "Why.\n"}, {"title": "Rationale", "body": "Because.\n"}]
OWNER, STATUS = "role/shopkeeper", "active"

BY_KIND = {
    "decision": ("decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}),
    "feature": ("feature", {"title": "Pricing", "story": "As a shopkeeper I set prices."}),
    "work item": ("work-item", {"title": "Reprice the shelves"}),
    "role": ("role", {
        "title": "Stock keeper",
        "harness": {"name": "stock-keeper", "description": "Keeps the shelves stocked."},
        "shop": {"responsible_for": "What is on the shelves"},
    }),
    "process": ("process", {"title": "Restock", "steps": [{"title": "Count", "does": "Count the shelves."}]}),
    "step": ("step", {"title": "Check the stock", "does": "Count what is on the shelf."}),
    "tag": ("tag", {"title": "Seasonal", "description": "Sold only some of the year.\n"}),
}


@given('a shop knowledge base holding a tag "pricing"', target_fixture="tag")
def _a_base_holding_a_tag(env, shop, tmp_path):
    start(env, shop)
    return record(env, tmp_path, "tag", {"title": "Pricing", "description": "How prices are set.\n"}, "Tag pricing")


@when(
    parsers.parse('the user records a {kind} with an owner, a status and the tag "pricing", saying who they are and why'),
    target_fixture="result",
)
def _records_with_owner_status_tag(env, tmp_path, tag, kind):
    type_name, content = BY_KIND[kind]
    path = tmp_path / "artifact.yaml"
    path.write_text(dumps({**content, "owner": OWNER, "status": STATUS, "tags": [tag]}))
    return knol(env, "create", type_name, "--from", str(path), "-m", f"Record a {kind}")


@then(parsers.parse("the {kind} carries that owner, that status and that tag"))
def _carries(env, shown, tag, kind):
    read = whole(env, shown["id"])
    assert (read["owner"], read["status"], read["tags"]) == (OWNER, STATUS, [tag])
