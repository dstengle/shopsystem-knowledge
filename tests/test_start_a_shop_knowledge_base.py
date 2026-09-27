import pytest
from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, removed, start
from start_roles_and_tags import *  # noqa: F403  pytest-bdd registers steps only through a star import

scenarios("start-a-shop-knowledge-base.feature")

_NO_ROLE = "every change must say which role made it, through KB_ACTOR as role or role:execution"
THE_SHOPS_TYPES = {"shop-artifact", "decision", "feature", "work-item", "role", "process", "step", "tag"}


@given("the user is working in an empty directory for the shop's knowledge")
def _an_empty_directory(shop):
    assert not any(shop.iterdir())


@pytest.fixture
def start_in(shop):
    """The directory the user starts a knowledge base in: the shop's, unless a Given names another."""
    return shop


@when("the user starts a shop knowledge base there without naming a directory, saying who they are", target_fixture="result")
def _start_saying_who(env, start_in):
    return _init(env, start_in)


def _init(env, directory):
    """Run init from the directory the user works in, naming none: it starts the knowledge base there."""
    return knol(env, "init", cwd=directory)


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
    # Reads kb's schema directory directly because no shop-knol command lists the types yet (CLAUDE.md, Step definitions).
    held = {path.stem for path in (shop / "kb" / "schema").glob("*.yaml")}
    assert held == THE_SHOPS_TYPES | {"schema"}


@when(
    "the user starts a shop knowledge base there without naming a directory, saying who they are and giving no reason",
    target_fixture="result",
)
def _start_giving_no_reason(env, shop):
    return _init(env, shop)


@then("the shop's knowledge base is started")
def _is_started(shop, result):
    assert result.returncode == 0, result.stderr
    # Reads the directory because no shop-knol command shows where the store is kept (CLAUDE.md, Step definitions).
    assert (shop / "kb" / "store.yaml").is_file()


@then("everything it was given is recorded in the shop's history under a reason the command writes itself")
def _recorded_with_its_own_reason(env, result):
    assert result.returncode == 0, result.stderr
    changes = loads(knol(env, "journal").stdout)["changes"]
    created = {change["artifact"]: change["message"] for change in changes if change["op"] == "create"}
    for name in THE_SHOPS_TYPES:
        assert created.get(f"schema/{name}"), f"no reason recorded for schema/{name}"


@when("the user starts a shop knowledge base there without naming a directory", target_fixture="result")
def _start(env, shop):
    return _init(env, shop)


@then("starting the knowledge base is rejected because starting one must say which role did it")
def _rejected_for_no_role(result):
    assert result.stderr.strip() == _NO_ROLE


@then("that directory holds no knowledge base")
@then("the directory they are working in holds no knowledge base")
def _holds_none(shop):
    assert not (shop / "kb").exists()


@given("the user is working in a directory holding work of the shop's that is not its knowledge", target_fixture="shops_work")
def _a_directory_with_work(shop):
    (shop / "notes.txt").write_text("Order oats on Monday.\n")
    (shop / "orders").mkdir()
    (shop / "orders" / "monday.txt").write_text("Twelve sacks of oats.\n")
    return {"notes.txt": "Order oats on Monday.\n", "orders/monday.txt": "Twelve sacks of oats.\n"}


@then("the shop's knowledge is kept in a place of its own inside that directory")
def _kept_in_its_own_place(shop, shops_work, result):
    assert result.returncode == 0, result.stderr
    # Lists the directory because no shop-knol command shows where the store is kept (CLAUDE.md, Step definitions).
    assert {path.name for path in shop.iterdir()} == {"notes.txt", "orders", "kb"}
    assert (shop / "kb" / "store.yaml").is_file()


@then("the work that was already in that directory is left as it was")
def _work_left_as_it_was(shop, shops_work):
    for name, text in shops_work.items():
        assert (shop / name).read_text() == text


@pytest.fixture
def known_before(env):
    """What `shop-knol journal` answered before the user started a knowledge base, filled in by the Given that starts one."""
    return {}


def _started_and_noted(env, shop, known_before):
    start(env, shop)
    known_before["journal"] = knol(env, "journal").stdout


@given("the user is working in a directory that already holds the shop's knowledge")
def _a_directory_already_started(env, shop, known_before):
    _started_and_noted(env, shop, known_before)


@given("the user is working in a directory that sits inside the shop's knowledge", target_fixture="start_in")
def _a_directory_inside_a_started_one(env, shop, known_before):
    _started_and_noted(env, shop, known_before)
    # Names kb/schema, a directory kb made, because no shop-knol command names one (CLAUDE.md, Step definitions).
    return shop / "kb" / "schema"


@then("starting the knowledge base is rejected because that directory already holds a knowledge base")
def _rejected_already_started(result):
    assert result.returncode == 1
    assert result.stdout == ""
    assert "already has a store" in result.stderr


@then("starting the knowledge base is rejected because that directory is inside a knowledge base")
def _rejected_inside_one(result):
    assert result.returncode == 1
    assert result.stdout == ""
    assert "stores do not nest" in result.stderr


@then("everything the shop already knows is still there, unchanged")
def _still_there(env, known_before):
    assert knol(env, "journal").stdout == known_before["journal"]


@given("the user is working in one directory, and another directory is empty", target_fixture="elsewhere")
def _another_directory_is_empty(tmp_path):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    return elsewhere


@when(
    "the user starts a shop knowledge base in the other directory by naming it, saying who they are",
    target_fixture="result",
)
def _start_elsewhere_by_naming(env, shop, elsewhere):
    return knol(env, "init", str(elsewhere), cwd=shop)


@then("the shop's knowledge is kept in a place of its own inside the named directory")
def _kept_in_its_own_place_named(elsewhere, result):
    assert result.returncode == 0, result.stderr
    # Lists the directory because no shop-knol command shows where the store is kept (CLAUDE.md, Step definitions).
    assert {path.name for path in elsewhere.iterdir()} == {"kb"}
    assert (elsewhere / "kb" / "store.yaml").is_file()


@given("the user is working in a directory that has since been removed", target_fixture="start_in")
def _a_removed_directory(tmp_path):
    return removed(tmp_path)
