"""The steps of use-the-shops-types.feature for slice 49's two scenarios, the role and the tag. The feature's
test module star-imports this and no other does."""
from kb.content import dumps
from pytest_bdd import given, then, when

from driver import knol, record, start, whole


@given("a shop knowledge base")
def _a_shop_knowledge_base(env, shop):
    start(env, shop)


THE_HARNESS_FIELDS = {"name": "stock-keeper", "description": "Keeps the shelves stocked.", "tools": ["Read"]}
THE_SHOP_IDENTITY = {"responsible_for": "What is on the shelves", "answers_to": "role/shopkeeper"}


@when("the user records a role, saying who they are and why", target_fixture="result")
def _records_a_role(env, tmp_path):
    path = tmp_path / "role.yaml"
    path.write_text(dumps({
        "title": "Stock keeper",
        "harness": THE_HARNESS_FIELDS,
        "shop": THE_SHOP_IDENTITY,
        "sections": [{"title": "How it works", "body": "Counts, then orders.\n"}],
    }))
    return knol(env, "create", "role", "--from", str(path), "-m", "Describe the stock keeper")


def _kept_as_one_group(env, role, group, fields):
    read = whole(env, role)
    assert read[group] == fields
    assert not fields.keys() & read.keys()


@then("the fields the harness needs are kept as one named group")
def _harness_group(env, shown):
    _kept_as_one_group(env, shown["id"], "harness", THE_HARNESS_FIELDS)


@then("the fields that say who the role is in the shop are kept as another")
def _shop_group(env, shown):
    _kept_as_one_group(env, shown["id"], "shop", THE_SHOP_IDENTITY)


TAG_DESCRIPTION = "How the shop sets its prices.\n"


@given(
    'a shop knowledge base holding a tag "pricing" with a title and a description',
    target_fixture="tag",
)
def _a_base_holding_a_tag(env, shop, tmp_path):
    start(env, shop)
    return record(env, tmp_path, "tag", {"title": "Pricing", "description": TAG_DESCRIPTION}, "Tag pricing")


@when('the user tags a decision with "pricing", saying who they are and why', target_fixture="result")
def _tags_a_decision(env, tmp_path, tag):
    path = tmp_path / "decision.yaml"
    path.write_text(dumps({
        "title": "Price reviews happen weekly",
        "tags": [tag],
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }))
    return knol(env, "create", "decision", "--from", str(path), "-m", "Record weekly reviews")


@then("the decision names that tag")
def _decision_names_tag(env, shown, tag):
    assert whole(env, shown["id"])["tags"] == [tag]


@then("the tag's description is held once, on the tag itself")
def _description_held_once(env, shown, tag):
    assert whole(env, tag)["description"] == TAG_DESCRIPTION
    assert TAG_DESCRIPTION.strip() not in dumps(whole(env, shown["id"]))
