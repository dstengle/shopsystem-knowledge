from kb import client as kb_client
from kb.content import dumps, loads
from kb.contract import kb_pb2
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("make-several-changes-at-once.feature")

WORK_ITEM = "work-item/reprice-the-dairy-shelf"
WEEKLY = "decision/price-reviews-happen-weekly"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given("a shop knowledge base holding the shop's types and a work item")
def _shop_with_a_work_item(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "work-item", {"title": "Reprice the dairy shelf"}, "Open the repricing")


@given("a batch that records a decision and points the work item at it", target_fixture="batch_file")
def _a_batch_recording_and_pointing(tmp_path):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": [
        {"create": "decision", "content": {"title": "Price reviews happen weekly", "sections": SECTIONS}},
        {"write": WORK_ITEM, "content": {"decisions": [WEEKLY]}},
    ]}))
    return path


@when("the user applies the batch, saying who they are and why", target_fixture="result")
def _apply(env, batch_file):
    return knol(env, "apply", "--from", str(batch_file), "-m", "Review prices weekly, starting with dairy")


@then("both changes are in the shop")
def _both_in_the_shop(env, result):
    assert result.returncode == 0, result.stderr
    assert [change["id"] for change in loads(result.stdout)["results"]] == [WEEKLY, WORK_ITEM]
    decision = knol(env, "read", WEEKLY)
    assert decision.returncode == 0, decision.stderr
    work_item = loads(knol(env, "read", WORK_ITEM).stdout)
    assert [(stub["field"], stub["id"]) for stub in work_item["references"]] == [("decisions", WEEKLY)]


@then("the shop's history shows them as one change")
def _one_change(shop, result):
    # Calls kb's in-process Journal with the batch because `shop-knol journal` has no --batch filter and does not show the batch.
    batch = loads(result.stdout)["batch"]
    history = kb_client.connect(shop).Journal(kb_pb2.JournalRequest(batch=batch))
    assert [(entry.op, entry.artifact) for entry in history.entries] == [("create", WEEKLY), ("write", WORK_ITEM)]
    assert {entry.message for entry in history.entries} == {"Review prices weekly, starting with dairy"}


@given("a batch whose second change does not fit its type", target_fixture="batch_file")
def _a_batch_with_a_bad_second_change(tmp_path):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": [
        {"create": "decision", "content": {"title": "Price reviews happen weekly", "sections": SECTIONS}},
        {"write": WORK_ITEM, "content": {"owner": 3, "status": 3}},
    ]}))
    return path


@then("the batch is rejected because a change in it does not fit its type")
def _rejected_for_its_type(result):
    assert result.returncode == 1
    assert result.stdout == ""
    lines = result.stderr.splitlines()
    assert lines and all(line.startswith(f"{WORK_ITEM} at ") for line in lines), result.stderr


@then("none of the changes are in the shop")
def _none_in_the_shop(env):
    assert knol(env, "read", WEEKLY).returncode == 1
    work_item = loads(knol(env, "read", WORK_ITEM).stdout)
    assert not work_item.get("references")
    assert "owner" not in work_item and "status" not in work_item


@then("the user is told every fault in the batch, not only the first")
def _every_fault(result):
    lines = result.stderr.splitlines()
    assert [line.split(" ")[1:3] for line in lines] == [["at", "owner:"], ["at", "status:"]], result.stderr
