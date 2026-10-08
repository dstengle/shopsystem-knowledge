"""A shop's capabilities: those linking to it, each read whole, in their order. The one place a shop's capabilities are
found, for publishing its spec and for what its scenarios formulate, and the one place dotted orders are compared."""
from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.renderers import source


def of(client, shop: str):
    """The capabilities linking to `shop`, each read whole, in the order of their `order`; or the faults of the first
    search or read that was refused."""
    listed = client.List(kb_pb2.ListRequest(kind="capability", fields={"shop": shop}, form=kb_pb2.ListRequest.IDS))
    if faults := list(listed.refusal.faults):
        return [], faults
    found = []
    for id in listed.result.ids:
        read = source.whole(client, id)
        if faults := source.faults(read):
            return [], faults
        found.append(read.result)
    return sorted(found, key=lambda capability: position(loads(capability.content)["order"])), []


def position(order: str) -> tuple[int, ...]:
    """An order as the whole numbers it is joined from, so that two orders compare part by part as numbers: 1.10 comes
    after 1.2 and 10 after 2."""
    return tuple(int(part) for part in order.split("."))
