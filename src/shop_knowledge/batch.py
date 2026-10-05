"""A batch file: several changes that land as one set. Each change is a create of a kind or a write to a name, with
its own content, and a create may carry a key that a link anywhere in the set, written `@<key>`, names its artifact by
(kb puts the name in); the set as a whole carries one signature, given on the command line like any other."""
from kb.content import dumps, text
from kb.contract import kb_pb2

from shop_knowledge.refusal import Refused


def items(document: dict, name: str) -> list[kb_pb2.CreateItem | kb_pb2.ReplaceItem]:
    """The batch's changes, in the order written, as the items of one BatchCreate or one BatchReplace, or refused as a
    fault on the batch file called `name` when they are of both kinds or a write carries a key."""
    changes = document["changes"]
    if len({"create" in change for change in changes}) > 1:
        raise Refused([kb_pb2.Fault(artifact=name, message="a batch holds one kind of change")])
    for number, change in enumerate(changes):
        if "write" in change and "key" in change:
            fault = kb_pb2.Fault(artifact=name, place=f"changes/{number}/key", message="only a create carries a key")
            raise Refused([fault])
    return [_item(change) for change in changes]


def _item(change: dict) -> kb_pb2.CreateItem | kb_pb2.ReplaceItem:
    content = dict(change["content"])
    if "create" in change:
        title = text(content.pop("title", None))
        return kb_pb2.CreateItem(kind=change["create"], key=change.get("key", ""), title=title, content=dumps(content))
    return kb_pb2.ReplaceItem(locator=kb_pb2.Locator(id=change["write"]), content=dumps(content))
