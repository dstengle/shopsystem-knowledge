from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("record-what-a-piece-of-work-read.feature")

PIECE_OF_WORK = "restock-the-shelves"
DECISION = {
    "title": "Prices are reviewed monthly",
    "sections": [
        {"title": "Purpose", "body": "Keep prices current.\n"},
        {"title": "Rationale", "body": "Monthly was enough once.\n"},
    ],
}
PROCESS = {
    "title": "Close up",
    "steps": [{"title": "Lock the door", "does": "Lock the front door.\n"}],
    "sections": [{"title": "Purpose", "body": "Restocking before close.\n"}],
}


@given("a shop knowledge base holding a decision and a process", target_fixture="held")
def _holding_a_decision_and_a_process(env, shop, tmp_path):
    start(env, shop)
    return [
        record(env, tmp_path, "decision", DECISION, "Record the monthly review"),
        record(env, tmp_path, "process", PROCESS, "Describe closing up"),
    ]


@when("the agent records, for its piece of work, the decision and the process it read", target_fixture="result")
def _agent_records_what_it_read(env, held):
    """The line gives the role and the piece of work; a change needs a message, so the step gives one."""
    agent = {**env, "KB_ACTOR": "agent"}
    return knol(agent, "snapshot", "--execution", PIECE_OF_WORK, *held, "-m", "Read before restocking")


@then("the shop's history holds one entry naming each of them with the version read")
def _history_names_each(env, held, shown):
    journal = knol(env, "journal", "--execution", PIECE_OF_WORK)
    assert journal.returncode == 0, journal.stderr
    changes = loads(journal.stdout)["changes"]
    assert len(changes) == 1
    assert changes[0]["read"] == [{"artifact": name, "revision": 1} for name in held]
