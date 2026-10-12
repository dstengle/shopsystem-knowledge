"""The test seam: every name a test hands kb directly, and every name it reads back from a kb message. On kb 0.6 each
is the identity; when the pin moves, this module alone changes on the test side. It mirrors the roles of the production
seam but never imports it (CLAUDE.md rule 1): it spells kb's forms itself. Imported plainly, never star-imported."""
from kb.contract import kb_pb2


def kind_name(kind: str) -> str:
    """A kind a user names, as kb's request fields name it."""
    return kind


def create_request(kind: str, title: str, content: str, signature: kb_pb2.Signature) -> kb_pb2.CreateRequest:
    """A Create of an artifact of the kind a user names, with the content already written as text."""
    return kb_pb2.CreateRequest(kind=kind_name(kind), title=title, content=content, signature=signature)


def artifact_id(answer) -> str:
    """The id kb named the artifact with, from the answer to a Create."""
    return answer.result.id


def artifact_name(kb_id: str) -> str:
    """kb's id (or any artifact a fault names) as the user is shown it."""
    return kb_id


def create_item(kind: str, title: str, content: str, key: str = "") -> kb_pb2.CreateItem:
    """One item of a BatchCreate, of the kind a user names, with the key the batch file gave it (empty for none)."""
    return kb_pb2.CreateItem(kind=kind_name(kind), key=key, title=title, content=content)


def list_of_types() -> kb_pb2.ListRequest:
    """The names of the types a knowledge base holds: the call shop-knol's own init makes to see what is there."""
    return kb_pb2.ListRequest(kind="schema", form=kb_pb2.ListRequest.IDS)


def read_whole_request(artifact: str) -> kb_pb2.ReadRequest:
    """A Read of the artifact a user names, whole, with no depth."""
    return kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=artifact), whole=kb_pb2.ReadRequest.Whole(depth=0))


def read_request(artifact: str) -> kb_pb2.ReadRequest:
    """A Read of the artifact a user names, as the stand-in is asked for it."""
    return kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=artifact))


def remove_request(artifact: str, signature: kb_pb2.Signature) -> kb_pb2.RemoveRequest:
    """A Remove of the artifact a user names."""
    return kb_pb2.RemoveRequest(locator=kb_pb2.Locator(id=artifact), signature=signature)


def check_request() -> kb_pb2.CheckRequest:
    """A Check of the whole knowledge base."""
    return kb_pb2.CheckRequest()


def history_request(batch: str = "") -> kb_pb2.HistoryRequest:
    """A History of the whole knowledge base, or of one batch's changes: the guard's question of whether a store is there."""
    return kb_pb2.HistoryRequest(batch=batch) if batch else kb_pb2.HistoryRequest()


def stand_in_read_refusal(artifact: str, faults: list) -> dict:
    """The stand-in's entry for a Read of the artifact a user names, refused with the faults a step wrote."""
    return {"call": "Read", "asking": {"locator": {"id": artifact}}, "answer": {"refusal": {"faults": faults}}}


def stand_in_check(violations: list) -> dict:
    """The stand-in's entry for a Check that finds the violations a step wrote, the rest of the answer kb's own."""
    return {"call": "Check", "answer": {"result": {"violations": violations}}, "from_kb": ["stale", "violations"]}
