import json

import pytest
from kb.content import dumps
from pytest_bdd import given, scenarios, then, when

from driver import UNKEPT, knol, record, refused_as_unkept, start, whole

scenarios("add-a-step-to-a-process.feature")

CHECK_THE_STOCK = {"title": "Check the stock", "does": "Count what is on the shelf, front and back.\n", "settings": ["shelf"]}
TIDY = {"title": "Tidy", "does": "Put back what customers left out of place.\n"}


@given("a shop knowledge base holding a process with two steps", target_fixture="process_name")
def _shop_with_a_process(env, shop, tmp_path):
    start(env, shop)
    return record(env, tmp_path, "process", {
        "title": "Close up",
        "steps": [
            {"title": "Lock the till", "does": "Count the takings and lock the till.\n"},
            {"title": "Turn off the lights", "does": "Switch off every light.\n"},
        ],
    }, "Describe closing up")


@given('a shared step "check the stock" that other processes already use', target_fixture="other_process_name")
def _shared_step_in_use(env, tmp_path):
    record(env, tmp_path, "step", CHECK_THE_STOCK, "Share the stock check")
    return record(env, tmp_path, "process", {
        "title": "Open up",
        "steps": [{"title": "Check it", "uses": "step/check-the-stock", "with": [{"name": "shelf", "value": "bread"}]}],
    }, "Describe opening up")


@when("the user adds a step describing what to do, saying who they are and why", target_fixture="result")
def _add_a_step_in_place(env, process_name, tmp_path):
    path = tmp_path / "tidy.yaml"
    path.write_text(dumps(TIDY))
    return knol(env, "append", f"{process_name}#steps", "--from", str(path), "-m", "Tidy before leaving")


@then("the new step is the last step of the process")
def _last_step(env, process_name, shown):
    steps = whole(env, process_name)["steps"]
    assert len(steps) == 3
    assert steps[-1]["title"] == TIDY["title"] and steps[-1]["does"] == TIDY["does"]


@then("the user is told the name the new step is known by")
def _told_the_name(env, process_name, shown):
    name = shown["id"]
    assert name.startswith(f"{process_name}#steps/")
    assert name.endswith(whole(env, process_name)["steps"][-1]["id"])


USE = {"title": "Check the dairy", "uses": "step/check-the-stock", "with": [{"name": "shelf", "value": "dairy"}]}


@pytest.fixture
def before(env, other_process_name):
    """The shared step and the other process using it, read whole before the change, taken when the When asks for it."""
    return {name: whole(env, name) for name in ("step/check-the-stock", other_process_name)}


@when('the user adds a step that uses "check the stock" with its own settings, saying who they are and why', target_fixture="result")
def _add_a_step_that_uses_a_shared_step(env, process_name, tmp_path, before):
    path = tmp_path / "check-the-dairy.yaml"
    path.write_text(dumps(USE))
    return knol(env, "append", f"{process_name}#steps", "--from", str(path), "-m", "Check the dairy shelf")


@then('the process runs "check the stock" at that point with those settings')
def _runs_the_shared_step(env, process_name, shown):
    last = whole(env, process_name)["steps"][-1]
    assert last["uses"] == USE["uses"] and last["with"] == USE["with"]


@then('"check the stock" itself is unchanged')
def _shared_step_unchanged(env, shown, before):
    assert whole(env, "step/check-the-stock") == before["step/check-the-stock"]


@then("another process using it is unaffected")
def _other_process_unaffected(env, other_process_name, shown, before):
    assert whole(env, other_process_name) == before[other_process_name]


@given("a step written in a file whose prose has a line ending in a space before its last line", target_fixture="step_file")
def _a_step_with_unkept_prose(tmp_path):
    """What the step does, its first line ending in a space, written as a quoted scalar."""
    path = tmp_path / "unkept-step.yaml"
    path.write_text(f"title: Tidy\ndoes: {json.dumps(UNKEPT)}\n")
    return path


@when("the user adds that step, saying who they are and why", target_fixture="result")
def _add_that_step(env, process_name, step_file):
    return knol(env, "append", f"{process_name}#steps", "--from", str(step_file), "-m", "Tidy before leaving")


@then(
    "the step is rejected because the shop cannot keep prose in which a line before the last ends in a space, "
    "naming the place in the file"
)
def _rejected_as_unkept(result, step_file):
    refused_as_unkept(result, step_file, "does")


@then("the process still has its two steps")
def _still_two_steps(env, process_name):
    assert [step["title"] for step in whole(env, process_name)["steps"]] == ["Lock the till", "Turn off the lights"]
