"""The steps of make-several-changes-at-once for a batch of writes: landing one, and the refusals of a batch that
mixes kinds or writes with a key. Star-imported by the feature's test module alone (adrs/0035)."""
from kb.content import dumps
from kb.contract import kb_pb2
from pytest_bdd import given, then

from decision_fields import decided
from driver import knol, record, whole
from kb_oracle import printed

WORK_ITEM = "work-item/reprice-the-dairy-shelf"
DECISION = "decision/price-reviews-happen-weekly"
NEW_SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with what the shop pays.\n"},
    {"title": "Rationale", "body": "Costs now move every day.\n"},
]
NEW_OWNER = "pricing"
ONE_KIND = "a batch holds one kind of change"
ONLY_A_CREATE = "only a create carries a key"
"""shop-knol's own words, not kb's, for a batch it will not send: kb is not called."""


@given("the shop also holds a decision")
def _the_shop_holds_a_decision(env, tmp_path, held):
    record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        **decided(1, held["shop"]),
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }, "Move price reviews to weekly")


@given("a batch that rewrites the decision and the work item", target_fixture="batch_file")
def _a_batch_of_writes(tmp_path, held):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": [
        {"write": DECISION, "content": {**decided(1, held["shop"]), "sections": NEW_SECTIONS}},
        {"write": WORK_ITEM, "content": {"owner": NEW_OWNER}},
    ]}))
    return path


@then("the shop holds the new wording of both")
def _holds_the_new_wording_of_both(env, result):
    assert result.returncode == 0, result.stderr
    assert whole(env, DECISION)["sections"] == NEW_SECTIONS
    assert whole(env, WORK_ITEM)["owner"] == NEW_OWNER


@given("a batch that rewrites the work item, the write carrying a key", target_fixture="batch_file")
def _a_write_with_a_key(tmp_path):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": [{"write": WORK_ITEM, "key": "weekly", "content": {"owner": NEW_OWNER}}]}))
    return path


@then("the batch is rejected because only a create carries a key, naming the key")
def _rejected_for_a_keyed_write(result, batch_file):
    fault = kb_pb2.Fault(artifact=str(batch_file), place="changes/0/key", message=ONLY_A_CREATE)
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.splitlines() == [printed(fault)], result.stderr


@given("a batch that records a decision and rewrites the work item", target_fixture="batch_file")
def _a_batch_of_mixed_kinds(tmp_path, held):
    path = tmp_path / "batch.yaml"
    path.write_text(dumps({"changes": [
        {"create": "decision",
         "content": {"title": "Price reviews happen weekly", **decided(1, held["shop"]), "sections": NEW_SECTIONS}},
        {"write": WORK_ITEM, "content": {"owner": NEW_OWNER}},
    ]}))
    return path


@then("the batch is rejected because a batch holds one kind of change, naming the batch")
def _rejected_for_mixed_kinds(result, batch_file):
    fault = kb_pb2.Fault(artifact=str(batch_file), message=ONE_KIND)
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.splitlines() == [printed(fault)], result.stderr
