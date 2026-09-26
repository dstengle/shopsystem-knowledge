from pytest_bdd import given, scenarios, then, when

from driver import knol, record

scenarios("start-a-shop-knowledge-base.feature")

THE_SHOPS_TYPES = {"shop-artifact", "decision", "feature", "work-item", "role", "process", "step", "tag"}


@given("an empty directory for the shop's knowledge")
def _an_empty_directory(shop):
    assert not any(shop.iterdir())


@when("the user starts a shop knowledge base in that directory, saying who they are", target_fixture="result")
def _start_saying_who(env, shop):
    return knol(env, "init", str(shop))


@then("the shop can hold decisions, features, work items, roles, processes, steps and tags")
def _holds_the_seven(env, tmp_path, result):
    assert result.returncode == 0, result.stderr
    record(env, tmp_path, "tag", {"title": "Pricing", "description": "How the shop sets its prices.\n"}, "Tag pricing")
    record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        "tags": ["tag/pricing"],
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }, "Record weekly reviews")
    record(env, tmp_path, "work-item", {
        "title": "Reprice the dairy shelf", "decisions": ["decision/price-reviews-happen-weekly"],
    }, "Open the repricing")
    record(env, tmp_path, "feature", {
        "title": "Restock the shelves",
        "story": "So that nothing runs out, the shopkeeper restocks the shelves.\n",
        "scenarios": [{"title": "A short shelf is restocked", "pins": "A shelf below its level is filled.\n"}],
    }, "Describe restocking")
    record(env, tmp_path, "role", {
        "title": "Stock keeper",
        "harness": {"name": "stock-keeper", "description": "Keeps the shelves stocked.", "tools": ["Read"]},
        "shop": {"responsible_for": "What is on the shelves", "answers_to": "role/shopkeeper"},
        "sections": [{"title": "How it works", "body": "Counts, then orders.\n"}],
    }, "Describe the stock keeper")
    record(env, tmp_path, "step", {
        "title": "Check the stock", "does": "Count what is on the shelf.\n", "settings": ["shelf"],
    }, "Share the stock check")
    record(env, tmp_path, "process", {
        "title": "Restock a shelf",
        "steps": [
            {"title": "Check it", "uses": "step/check-the-stock", "with": [{"name": "shelf", "value": "dairy"}]},
            {
                "title": "Decide",
                "does": "Decide whether the shelf is short.\n",
                "branches": [{"when": "the shelf is short", "go_to": "order-more"}, {"when": "it is not", "go_to": "stop"}],
            },
            {"title": "Order more", "does": "Order enough to fill the shelf.\n"},
            {"title": "Stop", "does": "Leave the shelf as it is.\n"},
        ],
    }, "Describe restocking a shelf")


@then("the user defines nothing of their own before recording the first one")
def _defines_nothing(shop):
    held = {path.stem for path in (shop / "kb" / "schema").glob("*.yaml")}
    assert held == THE_SHOPS_TYPES | {"schema"}
