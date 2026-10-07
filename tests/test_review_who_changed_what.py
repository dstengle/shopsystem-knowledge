from kb.content import dumps, loads
from pytest_bdd import given, parsers, scenarios, then, when

from decision_fields import decided
from driver import at, knol, record

scenarios("review-who-changed-what.feature")

WEEKLY = "decision/price-reviews-happen-weekly"
PIECE_OF_WORK = "reprice-dairy"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given(parsers.parse("today is {day}"), target_fixture="today")
def _today(day):
    return day


@given(
    "a shop knowledge base where the shopkeeper recorded a decision on 2026-09-21 and an agent revised it today "
    "as part of a named piece of work"
)
def _recorded_then_revised(env, shop, tmp_path, today):
    # The Background does not say who started the store; a role of its own keeps the start out of the shopkeeper's
    # history (adrs/0027).
    started = knol({**at(env, "2026-09-21T09:00:00"), "KB_ACTOR": "founder"}, "init", str(shop))
    assert started.returncode == 0, started.stderr
    record(at(env, "2026-09-21T10:00:00"), tmp_path, "decision",
           {"title": "Price reviews happen weekly", **decided(1), "sections": SECTIONS}, "Record weekly reviews")
    revision = tmp_path / "revision.yaml"
    revision.write_text(dumps({"changes": [{"write": WEEKLY, "content": {
        **decided(1), "status": "accepted", "sections": SECTIONS,
    }}]}))
    agent = {**at(env, f"{today}T10:00:00"), "KB_ACTOR": f"agent:{PIECE_OF_WORK}"}
    revised = knol(agent, "apply", "--from", str(revision), "-m", "Accept weekly reviews")
    assert revised.returncode == 0, revised.stderr


@when("the user reviews the changes to that decision", target_fixture="result")
def _review_the_decision(env):
    return knol(env, "journal", "--artifact", WEEKLY)


@then("the user sees both changes, each with who made it, when, what it did and why")
def _both_changes(result, today):
    assert result.returncode == 0, result.stderr
    assert [
        (change["actor"], change["at"][:10], change["op"], change["message"])
        for change in loads(result.stdout)["changes"]
    ] == [
        ({"role": "shopkeeper", "execution": ""}, "2026-09-21", "create", "Record weekly reviews"),
        ({"role": "agent", "execution": PIECE_OF_WORK}, today, "write", "Accept weekly reviews"),
    ]


@when("the user reviews the changes made by the shopkeeper", target_fixture="result")
def _review_the_shopkeeper(env):
    return knol(env, "journal", "--actor", "shopkeeper")


@then("the user sees only the recording of the decision")
def _only_the_recording(shown):
    assert [(change["actor"]["role"], change["op"], change["artifact"]) for change in shown["changes"]] == [
        ("shopkeeper", "create", WEEKLY),
    ]


def _revision_by_the_agent(shown, today):
    assert [(change["actor"], change["at"][:10], change["op"], change["artifact"]) for change in shown["changes"]] == [
        ({"role": "agent", "execution": PIECE_OF_WORK}, today, "write", WEEKLY),
    ]


@when("the user reviews the changes made for that piece of work", target_fixture="result")
def _review_the_piece_of_work(env):
    return knol(env, "journal", "--execution", PIECE_OF_WORK)


@then("the user sees only the revision made by the agent")
def _only_the_agents_revision(shown, today):
    _revision_by_the_agent(shown, today)


@when(parsers.parse("the user reviews the changes since {day}"), target_fixture="result")
def _review_since(env, day):
    return knol(env, "journal", "--since", day)


@then("the user sees only the revision made today")
def _only_todays_revision(shown, today):
    _revision_by_the_agent(shown, today)
