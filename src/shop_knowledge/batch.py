"""A batch file: several changes that land as one set. Each change is a create of a kind or a write to a name, with
its own content; the set as a whole carries one actor and one message, given on the command line like any other."""
from kb.content import dumps, text
from kb.contract import kb_pb2


def operations(document: dict) -> list[kb_pb2.Operation]:
    """The batch's changes, in the order written, as the operations of one Apply."""
    return [_operation(change) for change in document["changes"]]


def _operation(change: dict) -> kb_pb2.Operation:
    content = dict(change["content"])
    if "create" in change:
        title = text(content.pop("title", None))
        return kb_pb2.Operation(create=kb_pb2.Creation(type=change["create"], title=title, content=dumps(content)))
    return kb_pb2.Operation(write=kb_pb2.Replacement(locator=kb_pb2.Locator(id=change["write"]), content=dumps(content)))
