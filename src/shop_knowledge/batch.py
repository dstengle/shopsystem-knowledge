"""A batch file: several changes that land as one set. Each change is a create of a kind or a write to a name, with
its own content, and a create may carry a key that a link anywhere in the set, written `@<key>`, names its artifact by
(kb puts the name in); the set as a whole carries one signature, given on the command line like any other."""
from kb.content import dumps, text
from kb.contract import kb_pb2

from shop_knowledge import iris
from shop_knowledge.refusal import Refused


def items(document: dict, name: str, client) -> list[kb_pb2.CreateItem | kb_pb2.ReplaceItem]:
    """The batch's changes, in the order written, as the items of one BatchCreate or one BatchReplace, or refused as a
    fault on the batch file called `name` when they are of both kinds or a write carries a key. The client is the
    seam's, as a Create's is."""
    changes = document["changes"]
    if len({"create" in change for change in changes}) > 1:
        raise Refused([kb_pb2.Fault(artifact=name, message="a batch holds one kind of change")])
    for number, change in enumerate(changes):
        if "write" in change and "key" in change:
            fault = kb_pb2.Fault(artifact=name, place=f"changes/{number}/key", message="only a create carries a key")
            raise Refused([fault])
    if changes and "create" in changes[0]:
        return _created(changes, client)
    return [_written(change) for change in changes]


def _created(changes: list[dict], client) -> list[kb_pb2.CreateItem]:
    """The creates as items, each its fields and content as the seam gives them for the whole set."""
    asked = [(change["create"], change.get("key", ""), *_titled(change["content"])) for change in changes]
    made = iris.created_items(client, asked)
    return [
        kb_pb2.CreateItem(**fields, title=title, content=dumps(content))
        for (fields, content), (_, _, title, _) in zip(made, asked)
    ]


def _titled(content: dict) -> tuple[str, dict]:
    """A create's title, which kb takes as a field of its own, and the rest of its content."""
    rest = dict(content)
    return text(rest.pop("title", None)), rest


def _written(change: dict) -> kb_pb2.ReplaceItem:
    content = iris.content_to_kb(dict(change["content"]))
    return kb_pb2.ReplaceItem(locator=kb_pb2.Locator(id=iris.to_kb(change["write"])), content=dumps(content))
