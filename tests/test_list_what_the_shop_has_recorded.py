import pytest
from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("list-what-the-shop-has-recorded.feature")


def _decision(title, **fields):
    return {
        "title": title,
        **fields,
        "sections": [
            {"title": "Purpose", "body": f"{title}: why it is wanted.\n"},
            {"title": "Rationale", "body": f"{title}: why it was chosen.\n"},
        ],
    }


@given("a shop knowledge base holding three decisions, one of them superseded", target_fixture="recorded")
def _three_decisions(env, shop, tmp_path):
    """The names and titles recorded, in the order recorded: the superseded one, the one superseding it, an unrelated one."""
    start(env, shop)
    monthly = _decision("Prices are reviewed monthly", status="superseded")
    ids = {}
    ids[monthly["title"]] = record(env, tmp_path, "decision", monthly, "Record the monthly review")
    weekly = _decision("Price reviews happen weekly", supersedes=ids[monthly["title"]])
    ids[weekly["title"]] = record(env, tmp_path, "decision", weekly, "Move price reviews to weekly")
    opening = _decision("The shop opens at nine")
    ids[opening["title"]] = record(env, tmp_path, "decision", opening, "Record the opening hour")
    return {"ids": ids, "superseded": ids["Prices are reviewed monthly"]}


@pytest.fixture
def shown(result):
    """What the user is shown, for the steps that expect the list to succeed."""
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)


@when("the user lists the decisions", target_fixture="result")
def _list_them(env):
    return knol(env, "list", "--type", "decision")


@then("the user sees all three, each with its name and title")
def _all_three(shown, recorded):
    assert {entry["id"]: entry["title"] for entry in shown} == {v: k for k, v in recorded["ids"].items()}


@when("the user lists the decisions that are superseded", target_fixture="result")
def _list_superseded(env):
    return knol(env, "list", "--type", "decision", "--where", "status=superseded")


@then("the user sees only the superseded one")
def _only_the_superseded(shown, recorded):
    assert [entry["id"] for entry in shown] == [recorded["superseded"]]


@when("the user lists the decisions asking for names only", target_fixture="result")
def _list_names(env):
    return knol(env, "list", "--type", "decision", "--ids")


@then("the user sees three names and nothing else")
def _three_names(shown, recorded):
    assert isinstance(shown, list)
    assert sorted(shown) == sorted(recorded["ids"].values())
    assert all(isinstance(name, str) for name in shown)
