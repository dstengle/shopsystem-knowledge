from kb.content import dumps, loads
from pytest_bdd import given, parsers, scenarios, then, when

from driver import knol, record, whole
from record_refused_files import *  # noqa: F403  pytest-bdd registers steps only through a star import
from record_refused_files import SAYING_WHY

scenarios("record-an-artifact.feature")

OLDER = {
    "title": "Prices are reviewed monthly",
    "sections": [
        {"title": "Purpose", "body": "Keep prices current.\n"},
        {"title": "Rationale", "body": "Monthly was enough once.\n"},
    ],
}
WEEKLY = {
    "title": "Price reviews happen weekly",
    "supersedes": "decision/prices-are-reviewed-monthly",
    "sections": [
        {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
        {"title": "Rationale", "body": "Costs move weekly, so a monthly review lags them.\n"},
    ],
}


@given(
    "a decision in a file, with a title, a purpose, a rationale and the decision it supersedes",
    target_fixture="decision_file",
)
def _decision_in_a_file(env, tmp_path):
    record(env, tmp_path, "decision", OLDER, "Record the monthly review")
    path = tmp_path / "weekly.yaml"
    path.write_text(dumps(WEEKLY))
    return path


@when("the user records that file as a decision, saying who they are and why", target_fixture="result")
def _record_it(env, decision_file, before):
    """Asks for `before` so the knowledge base is taken as it was before the command runs."""
    return knol(env, "create", "decision", "--from", str(decision_file), "-m", SAYING_WHY)


@given("a decision in a file", target_fixture="decision_file")
def _decision_in_a_file_unrecorded(tmp_path):
    path = tmp_path / "decision.yaml"
    path.write_text(dumps(OLDER))
    return path


@when("the user records that file as a decision", target_fixture="result")
def _record_it_unsaid(env, decision_file):
    return knol(env, "create", "decision", "--from", str(decision_file), "-m", "Record the monthly review")


@when("the user records that file as a decision without a message", target_fixture="result")
def _record_it_without_a_message(env, decision_file):
    return knol(env, "create", "decision", "--from", str(decision_file))


@then("the decision is rejected because every change must say which role made it")
def _rejected_for_no_role(result):
    assert result.stderr.splitlines() == ["every change must say which role made it, through KB_ACTOR as role or role:execution"]


@then("the decision is rejected because every change must carry a message")
def _rejected_for_no_message(result):
    assert result.stderr.splitlines() == ["every change must carry a message, given with -m"]


@then("the user is shown the name the decision was given, which the user did not choose")
def _shown_the_name(result, decision_file):
    assert result.returncode == 0, result.stderr
    assert loads(result.stdout)["id"] == "decision/price-reviews-happen-weekly"
    assert "id" not in loads(decision_file.read_text())


@then("the shop holds the decision under that name and reads it back by it", target_fixture="read_back")
def _reads_back_by_name(env, result):
    name = loads(result.stdout)["id"]
    read = knol(env, "read", name)
    assert read.returncode == 0, read.stderr
    shown = loads(read.stdout)
    assert shown["id"] == name
    assert shown["title"] == "Price reviews happen weekly"
    return shown


@then("the decision is at its first version")
def _first_version(read_back):
    assert read_back["revision"] == 1


@given(parsers.parse('a decision in a file whose title is written "{title}"'), target_fixture="decision_file")
def _decision_in_a_file_titled(tmp_path, title):
    """The title is written bare, as a person types it, so YAML is free to read it as something else."""
    path = tmp_path / "titled.yaml"
    path.write_text(
        f"title: {title}\n"
        "sections:\n"
        "  - title: Purpose\n    body: Keep prices in step with costs.\n"
        "  - title: Rationale\n    body: Costs move weekly.\n"
    )
    return path


def _title_read_back(env, result, decision_file):
    """The title as the shop reads it back under the name the decision was given, and the title as written."""
    assert result.returncode == 0, result.stderr
    read = knol(env, "read", loads(result.stdout)["id"])
    assert read.returncode == 0, read.stderr
    written = decision_file.read_text().splitlines()[0].removeprefix("title: ")
    return loads(read.stdout)["title"], written


@then("the shop reads the title back as the text that was written, not as a date")
def _title_is_text_not_a_date(env, result, decision_file):
    shown, written = _title_read_back(env, result, decision_file)
    assert shown == written == "2026-09-24"


@then("the shop reads the title back as the text that was written, not as a yes or a no")
def _title_is_text_not_a_bool(env, result, decision_file):
    shown, written = _title_read_back(env, result, decision_file)
    assert shown == written == "yes"


@then("the name the decision was given is made from that text")
def _name_from_that_text(result, decision_file):
    written = decision_file.read_text().splitlines()[0].removeprefix("title: ")
    assert loads(result.stdout)["id"] == f"decision/{written}"


PIECE_OF_WORK = "restock-the-shelves"


@given("the user works as the shopkeeper on a named piece of work")
def _shopkeeper_on_a_piece_of_work(env):
    """Changes the scenario's env in place, so the commands the scenario runs are run as that role on that work."""
    env["KB_ACTOR"] = f"shopkeeper:{PIECE_OF_WORK}"


@then("the change is attributed to the shopkeeper and to that piece of work")
def _attributed_to_role_and_work(env, result):
    assert result.returncode == 0, result.stderr
    journal = knol(env, "journal", "--artifact", loads(result.stdout)["id"])
    assert journal.returncode == 0, journal.stderr
    creates = [change for change in loads(journal.stdout)["changes"] if change["op"] == "create"]
    assert [change["actor"] for change in creates] == [{"role": "shopkeeper", "execution": PIECE_OF_WORK}]


TAKEN = "decision/prices-are-reviewed-monthly"


@given(
    "a decision in a file whose title is already used by a decision the shop holds",
    target_fixture="decision_file",
)
def _decision_in_a_file_with_a_taken_title(env, tmp_path):
    record(env, tmp_path, "decision", OLDER, "Record the monthly review")
    again = {**OLDER, "sections": [
        {"title": "Purpose", "body": "Keep prices current.\n"},
        {"title": "Rationale", "body": "A second reason for the same title.\n"},
    ]}
    path = tmp_path / "again.yaml"
    path.write_text(dumps(again))
    return path


@then("the user is shown a name of its own for the new decision, the name already taken with a number added")
def _shown_a_name_of_its_own(result):
    assert result.returncode == 0, result.stderr
    assert loads(result.stdout)["id"] == TAKEN + "-2"


@then("the decision recorded earlier still reads back by the name it had")
def _earlier_still_reads_back(env):
    read = whole(env, TAKEN)
    assert read["title"] == OLDER["title"]
    assert read["revision"] == 1
    assert "Monthly was enough once." in [section["body"].strip() for section in read["sections"]]


@given("a decision produced by another command", target_fixture="piped_decision")
def _decision_from_another_command():
    """What another command printed, as text: the suite pipes it in rather than naming a file."""
    return dumps(OLDER)


@when("the user records it by piping it in, saying who they are and why", target_fixture="result")
def _record_by_piping(env, piped_decision):
    return knol(env, "create", "decision", "--from", "-", "-m", "Record the monthly review", piped=piped_decision)


@then("the shop holds the decision just as if it had come from a file")
def _holds_the_piped_decision(env, shown):
    read = whole(env, shown["id"])
    assert read["title"] == OLDER["title"]
    assert [(section["title"], section["body"]) for section in read["sections"]] == [
        (section["title"], section["body"]) for section in OLDER["sections"]
    ]
    assert read["revision"] == 1
