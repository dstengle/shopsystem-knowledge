"""A shop's capabilities: those linking to it that are active or deprecated, each read whole, in their order. The one
place a shop's capabilities are found, for publishing its spec and for what its scenarios formulate, and the one place dotted orders are compared."""
from kb.contract import kb_pb2

from shop_knowledge import iris
from shop_knowledge.renderers import source

PUBLISHED = {"active", "deprecated"}
"""The statuses a capability is published and counted under; a retired one is neither."""


def of(client, shop: str):
    """`mapped_of`, each capability as kb answered it, for what reads an answer itself."""
    found, faults = _found(client, shop)
    return [artifact for artifact, _ in found], faults


def mapped_of(client, shop: str):
    """The capabilities linking to `shop` (named as a user names it) whose status is active or deprecated, each read
    whole and mapped, in the order of their `order`; or the faults of the first search or read that was refused."""
    found, faults = _found(client, shop)
    return [mapped for _, mapped in found], faults


def _found(client, shop: str) -> tuple[list[tuple[kb_pb2.Artifact, source.Mapped]], list[kb_pb2.Fault]]:
    """Each such capability as kb answered it and as mapped, in order."""
    listed = client.List(iris.ids_request("capability", {"shop": shop}))
    if faults := list(listed.refusal.faults):
        return [], faults
    found = []
    for id in iris.listed_ids(listed):
        read = source.whole(client, id)
        if faults := source.faults(read):
            return [], faults
        found.append((read.result, source.mapped(read.result)))
    found = [each for each in found if each[1].content["status"] in PUBLISHED]
    return sorted(found, key=lambda each: position(each[1].content["order"])), []


def position(order: str) -> tuple[int, ...]:
    """An order as the whole numbers it is joined from, without trailing zeros, so that two orders compare part by part
    as numbers: 1.10 comes after 1.2, 10 after 2, and 3.0 is the order 3 is."""
    parts = [int(part) for part in order.split(".")]
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)
