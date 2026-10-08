"""The steps of use-the-shops-types.feature that record each of the shop's ten types with the fields every shop
artifact carries, and those of a process's steps. The feature's test module star-imports this and no other does."""
from kb.content import dumps
from pytest_bdd import given, parsers, then, when

from decision_fields import without_shop
from driver import knol, record, start, whole

PURPOSE = [{"title": "Purpose", "body": "Why.\n"}]
SECTIONS = [*PURPOSE, {"title": "Rationale", "body": "Because.\n"}]
SHOP_SECTIONS = [*PURPOSE, {"title": "Order of building", "body": "In order.\n"}, {"title": "Testing", "body": "Tested.\n"}]
OWNER, STATUS = "role/shopkeeper", "active"

BY_KIND = {
    "product": ("product", {"title": "Corner shop", "gist": "A shop on the corner.", "sections": PURPOSE}),
    "shop": ("shop", {"title": "Shelves", "gist": "Keeps the shelves.", "sections": SHOP_SECTIONS}),
    "capability": ("capability", {
        "title": "Set prices", "gist": "Prices are set.", "narrator": "the shopkeeper", "order": "1", "status": "active",
        "sections": PURPOSE,
    }),
    "decision": ("decision", {
        "title": "Price reviews happen weekly", **without_shop(1), "sections": SECTIONS,
    }),
    "feature": ("feature", {"title": "Pricing"}),
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


def _a_product(env, tmp_path):
    return record(env, tmp_path, "product", BY_KIND["product"][1], "Record the product")


def _a_shop(env, tmp_path):
    return record(env, tmp_path, "shop", {**BY_KIND["shop"][1], "product": _a_product(env, tmp_path)}, "Record the shop")


def _a_capability(env, tmp_path):
    shop = _a_shop(env, tmp_path)
    return record(env, tmp_path, "capability", {**BY_KIND["capability"][1], "shop": shop}, "Record the capability")


LINKED = {
    "shop": ("product", _a_product), "capability": ("shop", _a_shop), "decision": ("shop", _a_shop),
    "feature": ("formulates", _a_capability),
}
"""The kinds whose required link needs an artifact the shop holds first: the field, and how that artifact is recorded."""


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
    if kind in LINKED:
        field, recorded = LINKED[kind]
        content = {**content, field: recorded(env, tmp_path)}
    path = tmp_path / "artifact.yaml"
    path.write_text(dumps({**content, "owner": OWNER, "status": STATUS, "tags": [tag]}))
    return knol(env, "create", type_name, "--from", str(path), "-m", f"Record a {kind}")


@then(parsers.parse("the {kind} carries that owner, that status and that tag"))
def _carries(env, shown, tag, kind):
    read = whole(env, shown["id"])
    assert (read["owner"], read["status"], read["tags"]) == (OWNER, STATUS, [tag])
