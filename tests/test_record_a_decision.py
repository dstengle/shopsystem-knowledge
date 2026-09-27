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


@when("the user records that file as a decision, saying who they are and why", target_fixture="result")
def _record_it(env, decision_file):
    return knol(env, "create", "decision", "--from", str(decision_file), "-m", "Move price reviews to weekly")


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


@given("a file missing something the shop's decision type requires", target_fixture="decision_file")
def _file_missing_a_section(tmp_path):
    """A title and a Purpose but no Rationale, so kb's answer is one fault naming the artifact and the place."""
    path = tmp_path / "unfinished.yaml"
    path.write_text(dumps({
        "title": "Prices are reviewed monthly",
        "sections": [{"title": "Purpose", "body": "Keep prices current.\n"}],
    }))
    return path


@then("the decision is rejected because it does not fit the shop's decision type")
def _rejected_for_not_fitting(result):
    assert result.stderr.splitlines()[0].startswith("decision/"), result.stderr
    assert "the sections the type requires must all be present" in result.stderr


@then("the user is told which artifact and which place in it is at fault")
def _told_artifact_and_place(result):
    assert result.stderr.splitlines() == [
        "decision/prices-are-reviewed-monthly at sections: the sections the type requires must all be present, "
        "in order; 'Rationale' is missing",
    ]


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


@given("a decision in a file that names the same entry twice in the same place", target_fixture="decision_file")
def _decision_in_a_file_naming_an_entry_twice(tmp_path):
    path = tmp_path / "twice.yaml"
    path.write_text(
        "title: Price reviews happen weekly\n"
        "sections:\n"
        "  - title: Purpose\n"
        "    body: Keep prices in step with costs.\n"
        "    body: Keep prices low.\n"
        "  - title: Rationale\n"
        "    body: Costs move weekly.\n"
    )
    return path


@then("the decision is rejected because an entry is named once and only once, naming the place in the file")
def _rejected_for_an_entry_named_twice(result, decision_file):
    assert result.stderr.splitlines() == [
        f"{decision_file} at sections/0/body: an entry is named once and only once; 'body' is named again at line 5",
    ]
