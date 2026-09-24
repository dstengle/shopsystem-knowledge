import yaml
from pytest_bdd import given, scenarios, then, when

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
    path.write_text(yaml.safe_dump(WEEKLY, sort_keys=False))
    return path


@when("the user records that file as a decision, saying who they are and why", target_fixture="recorded")
def _record_it(env, decision_file):
    return knol(env, "create", "decision", "--from", str(decision_file), "-m", "Move price reviews to weekly")


@then("the user is shown the name the decision was given, which the user did not choose")
def _shown_the_name(recorded, decision_file):
    assert recorded.returncode == 0, recorded.stderr
    assert yaml.safe_load(recorded.stdout)["id"] == "decision/price-reviews-happen-weekly"
    assert "id" not in yaml.safe_load(decision_file.read_text())


@then("the shop holds the decision under that name and reads it back by it", target_fixture="read_back")
def _reads_back_by_name(env, recorded):
    name = yaml.safe_load(recorded.stdout)["id"]
    result = knol(env, "read", name)
    assert result.returncode == 0, result.stderr
    shown = yaml.safe_load(result.stdout)
    assert shown["id"] == name
    assert shown["title"] == "Price reviews happen weekly"
    return shown


@then("the decision is at its first version")
def _first_version(read_back):
    assert read_back["revision"] == 1
