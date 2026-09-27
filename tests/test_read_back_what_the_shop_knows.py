import json

import pytest
from kb.content import dumps, loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("read-back-what-the-shop-knows.feature")

OLDER = "decision/prices-are-reviewed-monthly"
DECISION = "decision/price-reviews-happen-weekly"


@given(
    'a shop knowledge base holding a decision with a purpose and a rationale, tagged "pricing", '
    "superseding an older decision, and pointed at by two work items",
    target_fixture="decision_id",
)
def _shop_with_a_linked_decision(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "tag", {"title": "pricing", "description": "How the shop sets prices.\n"}, "Add the pricing tag")
    record(env, tmp_path, "decision", {
        "title": "Prices are reviewed monthly",
        "sections": [
            {"title": "Purpose", "body": "Keep prices current.\n"},
            {"title": "Rationale", "body": "Monthly was enough once.\n"},
        ],
    }, "Record the monthly review")
    decision_id = record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        "supersedes": OLDER,
        "tags": ["tag/pricing"],
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }, "Move price reviews to weekly")
    record(env, tmp_path, "work-item", {"title": "Move the review to Mondays", "decisions": [DECISION]}, "Plan the move")
    record(env, tmp_path, "work-item", {"title": "Tell the pricing team", "decisions": [DECISION]}, "Plan the telling")
    return decision_id


@pytest.fixture
def workdir():
    """Where the user works, when a Given moves them; None is where the suite runs."""
    return None


@when("the user reads the decision", target_fixture="result")
def _read_the_decision(env, decision_id, workdir):
    return knol(env, "read", decision_id, cwd=workdir)


@pytest.fixture
def shown(result):
    """What the user is shown, for the steps that expect the read to succeed."""
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)


@then("the user sees its name, its title and the few fields the shop shows for a decision")
def _name_title_and_fields(shown):
    assert shown["id"] == DECISION
    assert shown["title"] == "Price reviews happen weekly"
    assert shown["supersedes"] == OLDER
    assert shown["tags"] == ["tag/pricing"]


@then("the user sees a stub of each thing it points at")
def _stubs(shown):
    stubs = {(stub["field"], stub["id"], stub["type"], stub["title"]) for stub in shown["references"]}
    assert stubs == {
        ("supersedes", OLDER, "decision", "Prices are reviewed monthly"),
        ("tags", "tag/pricing", "tag", "pricing"),
    }


@then("the user sees how many things point back at it, and of what kind")
def _inbound(shown):
    assert shown["inbound"] == [{"type": "work-item", "field": "decisions", "count": 2}]



@given("someone edited the decision's file by hand and left it in a shape the shop cannot read")
def _decision_file_mangled_by_hand(shop):
    (shop / "kb" / f"{DECISION}.yaml").write_text("title: [a bracket opened by hand and never closed\n")


@then("the command is rejected because that file cannot be read, naming the file")
def _rejected_as_unreadable(result):
    assert result.stderr.startswith(f"{DECISION}: the stored file {DECISION}.yaml cannot be read: ")


@when("the user reads the whole decision", target_fixture="result")
def _read_the_whole_decision(env, decision_id):
    return knol(env, "read", decision_id, "--whole")


@then("the user sees every field, every section and every part it holds")
def _every_field_and_section(shown):
    assert shown["id"] == DECISION
    assert shown["title"] == "Price reviews happen weekly"
    assert shown["tags"] == ["tag/pricing"]
    assert shown["sections"] == [
        {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
        {"title": "Rationale", "body": "Costs move weekly.\n"},
    ]


@then("what it points at is shown by name only")
def _pointers_are_names(shown):
    assert shown["supersedes"] == OLDER
    assert shown["tags"] == ["tag/pricing"]


@when("the user reads the rationale of the decision", target_fixture="result")
def _read_the_rationale(env, decision_id):
    return knol(env, "read", decision_id, "--section", "Rationale")


@then("the user sees that section and nothing else")
def _that_section_only(shown):
    assert shown == {"title": "Rationale", "body": "Costs move weekly.\n"}


@when(
    "the user reads the whole decision asking for what it points at to be filled in, without saying how far",
    target_fixture="result",
)
def _read_filled_in(env, decision_id):
    return knol(env, "read", decision_id, "--resolve")


def _all_links_are_names(document):
    links = [document.get("supersedes"), *document.get("tags", [])]
    return all(link is None or isinstance(link, str) for link in links)


@then("the superseded decision is shown in place of the pointer, as the shop holds it now")
def _superseded_shown_in_place(shown):
    older = shown["supersedes"]
    assert older["id"] == OLDER
    assert older["title"] == "Prices are reviewed monthly"
    assert older["revision"] == 1
    assert [section["title"] for section in older["sections"]] == ["Purpose", "Rationale"]


@then("what that older decision points at is shown by name only")
def _older_points_by_name(shown):
    # The Background's older decision points at nothing, so this cannot tell one step from two; see the slice log.
    assert _all_links_are_names(shown["supersedes"])


@given('the older decision is tagged "seasonal"')
def _older_decision_tagged_seasonal(env, tmp_path):
    # Drives shop-knol as a user does: `apply`, since `write` does not exist yet.
    path = tmp_path / "tag-the-older-decision.yaml"
    path.write_text(dumps({"changes": [
        {"create": "tag", "content": {"title": "seasonal", "description": "Changes with the season.\n"}},
        {"write": OLDER, "content": {"tags": ["tag/seasonal"], "sections": [
            {"title": "Purpose", "body": "Keep prices current.\n"},
            {"title": "Rationale", "body": "Monthly was enough once.\n"},
        ]}},
    ]}))
    result = knol(env, "apply", "--from", str(path), "-m", "Tag the older decision seasonal")
    assert result.returncode == 0, result.stderr


@when(
    "the user reads the whole decision asking for what it points at to be filled in two steps",
    target_fixture="result",
)
def _read_filled_in_two_steps(env, decision_id):
    return knol(env, "read", decision_id, "--resolve", "2")


@then("the superseded decision is shown in place of the pointer")
def _superseded_in_place(shown):
    assert shown["supersedes"]["id"] == OLDER


@then('the tag "seasonal" is shown in place of the pointer inside it')
def _tag_in_place(shown):
    tags = shown["supersedes"]["tags"]
    assert [tag["title"] for tag in tags] == ["seasonal"]
    assert tags[0]["id"] == "tag/seasonal"


@when("the user reads the decision asking for JSON", target_fixture="result")
def _read_as_json(env, decision_id):
    return knol(env, "read", decision_id, "--json")


@then("the user gets the same answer as the default, written as JSON")
def _same_answer_as_json(env, decision_id, result):
    assert result.returncode == 0, result.stderr
    default = knol(env, "read", decision_id)
    assert default.returncode == 0, default.stderr
    assert json.loads(result.stdout) == loads(default.stdout)


@given(
    "the user is working in a folder deep inside the directory that holds the shop's knowledge",
    target_fixture="workdir",
)
def _working_deep_inside_the_shop(env, shop, decision_id):
    del env["KB_ROOT"]
    deep = shop / "notes" / "pricing" / "2026"
    deep.mkdir(parents=True)
    return deep


@then("the user sees the decision, from the knowledge base found above where they are working")
def _decision_from_above(shown):
    assert shown["id"] == DECISION


@given("the user is working outside any knowledge base, with KB_ROOT naming the shop's", target_fixture="workdir")
def _working_elsewhere_naming_the_shop(tmp_path, decision_id):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    return elsewhere


@then("the user sees the decision, from the knowledge base KB_ROOT names")
def _decision_from_kb_root(shown):
    assert shown["id"] == DECISION


@given("the user is working outside any knowledge base and nothing names one", target_fixture="workdir")
def _working_elsewhere_naming_nothing(env, tmp_path, decision_id):
    del env["KB_ROOT"]
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    return elsewhere


@then("the command is rejected because no knowledge base was found, neither above where they are working nor named outright")
def _rejected_no_store(result, workdir):
    assert result.stderr == f"no store was found, neither above {workdir.resolve()} nor named outright\n"
    assert result.stdout == ""


@given(
    "the user is working outside any knowledge base, with KB_ROOT naming a directory that holds no knowledge base",
    target_fixture="workdir",
)
def _kb_root_names_an_empty_directory(env, tmp_path, decision_id):
    empty = tmp_path / "empty"
    empty.mkdir()
    env["KB_ROOT"] = str(empty)
    return tmp_path


@then("the command is rejected because KB_ROOT names a directory that holds no knowledge base")
def _rejected_kb_root_holds_none(env, result):
    assert result.stderr == f"KB_ROOT names a directory that holds no store: {env['KB_ROOT']}\n"
    assert result.stdout == ""


@given(
    "the user is working inside the shop's knowledge base, with KB_ROOT naming a different one",
    target_fixture="workdir",
)
def _kb_root_names_another_store(env, shop, tmp_path, decision_id):
    other = tmp_path / "other"
    other.mkdir()
    start(env, other)
    env["KB_ROOT"] = str(other)
    return shop


@then(
    "the command is rejected because KB_ROOT names a knowledge base other than the one they are working in, "
    "and neither of the two is guessed at"
)
def _rejected_two_stores(env, result, workdir):
    assert result.stderr == (
        f"KB_ROOT names a store other than the one {workdir.resolve()} is working in: KB_ROOT is {env['KB_ROOT']}, "
        f"the working directory is inside {workdir.resolve()}; neither is guessed at\n"
    )
    assert result.stdout == ""
