"""A batch file: several changes that land as one set. Each change is a create of a kind or a write to a name, with
its own content, and a create may carry a key that a link anywhere in the set, written `@<key>`, names its artifact by
(kb puts the name in); the set as a whole carries one signature, given on the command line like any other."""
from kb.content import dumps, text
from kb.contract import kb_pb2


def items(document: dict) -> list[kb_pb2.CreateItem | kb_pb2.ReplaceItem]:
    """The batch's changes, in the order written, as the items of one BatchCreate or one BatchReplace."""
    return [_item(change) for change in document["changes"]]


def _item(change: dict) -> kb_pb2.CreateItem | kb_pb2.ReplaceItem:
    content = dict(change["content"])
    if "create" in change:
        title = text(content.pop("title", None))
        return kb_pb2.CreateItem(kind=change["create"], key=change.get("key", ""), title=title, content=dumps(content))
    return kb_pb2.ReplaceItem(locator=kb_pb2.Locator(id=change["write"]), content=dumps(content))
