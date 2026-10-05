import json

from kb.content import dumps, loads
from kb.contract import kb_pb2
from pytest_bdd import given, parsers, scenarios, then, when

from driver import knol, record, start
from kb_oracle import UNKEPT, kb_answer, printed, refused_as_unkept, signature

scenarios("make-several-changes-at-once.feature")

WORK_ITEM = "work-item/reprice-the-dairy-shelf"
WEEKLY = "decision/price-reviews-happen-weekly"
NEW_ITEM = "work-item/start-weekly-price-reviews"
NEW_ITEM_TITLE = "Start weekly price reviews"
KEY = "weekly"
UNCARRIED = "monthly"
LINK = "ref"
"""The `rule` kb's contract publishes for a key in a set that names no create, or more than one."""
SAYING_WHY = "Review prices weekly, starting with dairy"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given("a shop knowledge base holding the shop's types and a work item")
def _shop_with_a_work_item(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "work-item", {"title": "Reprice the dairy shelf"}, "Open the repricing")


def _linked_creates(work_item_first: bool = False, link: str = KEY) -> list:
    """A decision carrying KEY, and a new work item whose link is written with `link`, in the order asked."""
    decision = {
        "create": "decision", "key": KEY, "content": {"title": "Price reviews happen weekly", "sections": SECTIONS},
    }
    work_item = {"create": "work-item", "content": {"title": NEW_ITEM_TITLE, "decisions": [f"@{link}"]}}
    return [work_item, decision] if work_item_first else [decision, work_item]


@given("a batch that records a decision and a work item pointing at it", target_fixture="batch_file")
def _a_batch_of_linked_creates(tmp_path):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": _linked_creates()}))
    return path


@given(
    parsers.parse(
        "a batch that records a decision carrying a key of the user's choosing, and a work item whose link is written "
        "with that key, the work item coming {order} the decision in the batch"
    ),
    target_fixture="batch_file",
)
def _a_batch_ordered(tmp_path, order):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": _linked_creates(work_item_first=order == "before")}))
    return path


@given(
    "a batch that records a decision and a work item whose link is written with a key no create in the batch carries",
    target_fixture="batch_file",
)
def _a_batch_linking_to_no_key(tmp_path):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": _linked_creates(link=UNCARRIED)}))
    return path


@given("a batch that records a decision and a work item, both carrying the same key", target_fixture="batch_file")
def _a_batch_sharing_a_key(tmp_path):
    decision, _ = _linked_creates()
    work_item = {"create": "work-item", "key": KEY, "content": {"title": NEW_ITEM_TITLE}}
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": [decision, work_item]}))
    return path


@when("the user applies the batch, saying who they are and why", target_fixture="result")
def _apply(env, batch_file):
    return knol(env, "apply", "--from", str(batch_file), "-m", SAYING_WHY)


@then("both changes are in the shop")
def _both_in_the_shop(env, result):
    assert result.returncode == 0, result.stderr
    assert [change["id"] for change in loads(result.stdout)["results"]] == [WEEKLY, NEW_ITEM]
    decision = knol(env, "read", WEEKLY)
    assert decision.returncode == 0, decision.stderr
    _links_to_the_decision(env)


def _links_to_the_decision(env):
    work_item = knol(env, "read", NEW_ITEM)
    assert work_item.returncode == 0, work_item.stderr
    references = loads(work_item.stdout)["references"]
    assert [(stub["field"], stub["id"]) for stub in references] == [("decisions", WEEKLY)]


@then("the work item's link names the decision the batch created")
def _link_names_the_decision(env, result):
    assert result.returncode == 0, result.stderr
    _links_to_the_decision(env)


@then("the shop's history shows them as one change")
def _one_change(env, result):
    # Asks kb in-process, through the driver and the scenario's own allowlisted environment, because
    # `shop-knol journal` has no batch filter and does not show the batch.
    applied = loads(result.stdout)
    history = kb_answer(env, "History", kb_pb2.HistoryRequest(batch=applied["batch"])).result
    assert [entry.artifact for entry in history.entries] == [change["id"] for change in applied["results"]]
    assert {entry.message for entry in history.entries} == {SAYING_WHY}


@given("a batch whose second change does not fit its type", target_fixture="batch_file")
def _a_batch_with_a_bad_second_change(tmp_path):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": [
        {"create": "decision", "content": {"title": "Price reviews happen weekly", "sections": SECTIONS}},
        {"create": "work-item", "content": {"title": NEW_ITEM_TITLE, "owner": 3, "status": 3}},
    ]}))
    return path


@then("the batch is rejected because a change in it does not fit its type")
def _rejected_for_its_type(result):
    assert result.returncode == 1
    assert result.stdout == ""
    lines = result.stderr.splitlines()
    assert lines and all(line.startswith(f"{NEW_ITEM} at ") for line in lines), result.stderr


@then("the batch is rejected because the link lands on nothing, naming the key")
def _rejected_for_a_key_no_create_carries(env, result, batch_file):
    _refused_in_kbs_words(env, result, batch_file, UNCARRIED)


@then("the batch is rejected because a key names one create in the batch, naming the key")
def _rejected_for_a_key_carried_twice(env, result, batch_file):
    _refused_in_kbs_words(env, result, batch_file, KEY)


def _refused_in_kbs_words(env, result, batch_file, key):
    """Printed as kb returned it: every fault kb's own answer to the same BatchCreate gives, one line each, the key
    named in kb's words."""
    faults = _kb_refuses_the_batch(env, batch_file)
    assert faults and any(fault.rule == LINK and key in printed(fault) for fault in faults), faults
    assert result.returncode == 1
    assert result.stdout == ""
    assert sorted(result.stderr.splitlines()) == sorted(printed(fault) for fault in faults), result.stderr


def _kb_refuses_the_batch(env, batch_file):
    """kb's own answer to the BatchCreate the user's command made of the batch, asked of the same store: its faults,
    whose words are kb's (kb adrs/0018)."""
    items = []
    for change in loads(batch_file.read_text())["changes"]:
        content = dict(change["content"])
        title = content.pop("title")
        key = change.get("key", "")
        items.append(kb_pb2.CreateItem(kind=change["create"], key=key, title=title, content=dumps(content)))
    request = kb_pb2.BatchCreateRequest(items=items, signature=signature(env, SAYING_WHY))
    return kb_answer(env, "BatchCreate", request).refusal.faults


@then("none of the changes are in the shop")
def _none_in_the_shop(env):
    assert knol(env, "read", WEEKLY).returncode == 1
    assert knol(env, "read", NEW_ITEM).returncode == 1
    work_item = loads(knol(env, "read", WORK_ITEM).stdout)
    assert not work_item.get("references")
    assert "owner" not in work_item and "status" not in work_item


@then("the user is told every fault in the batch, not only the first")
def _every_fault(result):
    """kb states no order among a batch's faults, so the pairs are held to sorted, not by position: each still
    counted once, not merely present."""
    lines = result.stderr.splitlines()
    pairs = sorted(tuple(line.split(" ")[1:3]) for line in lines)
    assert pairs == sorted([("at", "owner:"), ("at", "status:")]), result.stderr


@given(
    "a batch that records a decision and a work item pointing at it, the decision's prose having a line ending in a "
    "space before its last line",
    target_fixture="batch_file",
)
def _a_batch_with_unkept_prose(tmp_path):
    """The decision's rationale, its first line ending in a space, written as a quoted scalar."""
    path = tmp_path / "batch.yaml"
    path.write_text(
        "changes:\n"
        "  - create: decision\n"
        f"    key: {KEY}\n"
        "    content:\n"
        "      title: Price reviews happen weekly\n"
        "      sections:\n"
        "        - title: Purpose\n"
        "          body: Keep prices in step with costs.\n"
        "        - title: Rationale\n"
        f"          body: {json.dumps(UNKEPT)}\n"
        "  - create: work-item\n"
        "    content:\n"
        f"      title: {NEW_ITEM_TITLE}\n"
        f"      decisions: ['@{KEY}']\n"
    )
    return path


@then(
    "the batch is rejected because the shop cannot keep prose in which a line before the last ends in a space, "
    "naming the place in the batch"
)
def _rejected_as_unkept(result, batch_file):
    refused_as_unkept(result, batch_file, "changes/0/content/sections/1/body")
