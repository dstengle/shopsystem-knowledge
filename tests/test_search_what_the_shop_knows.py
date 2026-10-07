from pytest_bdd import given, scenarios, then, when

from decision_fields import decided
from driver import knol, record, start

scenarios("search-what-the-shop-knows.feature")

PROSE_DECISIONS = {"decision/restocking-is-weekly", "decision/shelves-are-counted-first"}
OFTEN = "decision/restocking-is-weekly"
TITLE_DECISION = "decision/who-owns-restocking"


@given("a shop knowledge base where two decisions and a process mention restocking in their prose")
def _shop_where_restocking_is_mentioned(env, shop, tmp_path):
    """The fourth artifact is the decision whose title alone carries the word, which the fields scenario finds."""
    start(env, shop)
    record(env, tmp_path, "decision", {
        "title": "Restocking is weekly",
        **decided(1),
        "sections": [{
            "title": "Purpose",
            "body": "Restocking happens every week. Restocking on Mondays, restocking again on Thursdays.\n",
        }, {"title": "Rationale", "body": "Shelves empty at a steady pace.\n"}],
    }, "Record the weekly restocking")
    record(env, tmp_path, "decision", {
        "title": "Shelves are counted first",
        **decided(2),
        "sections": [
            {"title": "Purpose", "body": "Count the shelves before restocking.\n"},
            {"title": "Rationale", "body": "A count shows what is short.\n"},
        ],
    }, "Record the count")
    record(env, tmp_path, "process", {
        "title": "Close up",
        "steps": [{"title": "Lock the door", "does": "Lock the front door.\n"}],
        "sections": [{"title": "Purpose", "body": "Restocking before close.\n"}],
    }, "Describe closing up")
    record(env, tmp_path, "decision", {
        "title": "Who owns restocking",
        **decided(3),
        "sections": [
            {"title": "Purpose", "body": "The shift lead decides.\n"},
            {"title": "Rationale", "body": "One person answers for the shelves.\n"},
        ],
    }, "Record who owns it")


@when("the user searches for restocking", target_fixture="result")
def _search(env):
    return knol(env, "search", "restocking")


@then("each result names the section it matched and shows a snippet of it")
def _each_result_says_where_and_shows(shown):
    assert shown
    for entry in shown:
        assert entry["section"]
        assert "restocking" in entry["snippet"].lower()


@then("the one that mentions restocking most often in a section comes first")
def _most_often_first(shown):
    assert shown[0]["id"] == OFTEN


@when("the user searches for restocking among decisions only", target_fixture="result")
def _search_decisions(env):
    return knol(env, "search", "restocking", "--type", "decision")


@then("the user sees the two decisions and not the process")
def _sees_the_two_decisions(shown):
    assert {entry["id"] for entry in shown} == PROSE_DECISIONS


@when("the user searches for restocking in the fields as well as the prose", target_fixture="result")
def _search_fields_too(env):
    return knol(env, "search", "restocking", "--in", "all")


@then("the user also sees a decision whose title mentions restocking")
def _also_sees_the_title_decision(shown):
    assert {entry["id"] for entry in shown} == PROSE_DECISIONS | {"process/close-up", TITLE_DECISION}
