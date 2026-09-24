from kb.content import dumps, loads
from pytest_bdd import given, parsers, scenarios, then, when

from driver import knol, record

scenarios("record-a-decision.feature")

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


@when("the user records that file as a decision, saying who they are and why", target_fixture="recorded")
def _record_it(env, decision_file):
    return knol(env, "create", "decision", "--from", str(decision_file), "-m", "Move price reviews to weekly")


@then("the user is shown the name the decision was given, which the user did not choose")
def _shown_the_name(recorded, decision_file):
    assert recorded.returncode == 0, recorded.stderr
    assert loads(recorded.stdout)["id"] == "decision/price-reviews-happen-weekly"
    assert "id" not in loads(decision_file.read_text())


@then("the shop holds the decision under that name and reads it back by it", target_fixture="read_back")
def _reads_back_by_name(env, recorded):
    name = loads(recorded.stdout)["id"]
    result = knol(env, "read", name)
    assert result.returncode == 0, result.stderr
    shown = loads(result.stdout)
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


def _title_read_back(env, recorded, decision_file):
    """The title as the shop reads it back under the name the decision was given, and the title as written."""
    assert recorded.returncode == 0, recorded.stderr
    result = knol(env, "read", loads(recorded.stdout)["id"])
    assert result.returncode == 0, result.stderr
    written = decision_file.read_text().splitlines()[0].removeprefix("title: ")
    return loads(result.stdout)["title"], written


@then("the shop reads the title back as the text that was written, not as a date")
def _title_is_text_not_a_date(env, recorded, decision_file):
    shown, written = _title_read_back(env, recorded, decision_file)
    assert shown == written == "2026-09-24"


@then("the shop reads the title back as the text that was written, not as a yes or a no")
def _title_is_text_not_a_bool(env, recorded, decision_file):
    shown, written = _title_read_back(env, recorded, decision_file)
    assert shown == written == "yes"


@then("the name the decision was given is made from that text")
def _name_from_that_text(recorded, decision_file):
    written = decision_file.read_text().splitlines()[0].removeprefix("title: ")
    assert loads(recorded.stdout)["id"] == f"decision/{written}"
