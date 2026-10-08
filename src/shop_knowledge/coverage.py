"""What a shop's scenarios formulate: for the Behaviour lines of the capabilities in the shop's reading order, those no
scenario formulates and those more than one does. It reads through the contract alone and reports; a line with no
scenario is never a refusal. Its refusals are raised as `refusal.Refused`, kb's own passed on."""
from collections import Counter

from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.refusal import Refused
from shop_knowledge.renderers import source


def _refusal(read: kb_pb2.ReadResponse) -> list[kb_pb2.Fault]:
    """What stops a coverage: kb's own refusal of the read, else the artifact's not being a shop."""
    if read.WhichOneof("outcome") == "refusal":
        return source.faults(read)
    if read.result.kind != "shop":
        return [kb_pb2.Fault(artifact=read.result.id, rule="coverage-of-a-shop", message=f"{read.result.id} is a {read.result.kind}, not a shop")]
    return []


def of(client, shop: str) -> dict:
    """The shop's lines no scenario formulates and those more than one does, in reading order and then the capability's
    own, each as its link with its capability's title and its own."""
    read = source.whole(client, shop)
    if faults := _refusal(read):
        raise Refused(faults)
    lines = [line for id in loads(read.result.content).get("reading_order", []) for line in _lines(client, id)]
    formulating = _formulating(client)
    return {
        "unformulated": [line for line in lines if formulating[line["link"]] == 0],
        "formulated_twice": [line for line in lines if formulating[line["link"]] > 1],
    }


def _read(client, name: str) -> kb_pb2.Artifact:
    read = source.whole(client, name)
    if faults := source.faults(read):
        raise Refused(faults)
    return read.result


def _lines(client, capability: str) -> list[dict]:
    """Each Behaviour line of the capability, in the order it holds them."""
    held = _read(client, capability)
    return [
        {"link": f"{held.id}#behaviour/{line['id']}", "capability": held.title, "line": line["title"]}
        for line in loads(held.content).get("behaviour", [])
    ]


def _formulating(client) -> Counter:
    """How many scenarios formulate each link, over every feature the knowledge base holds, whichever shop's."""
    found = client.List(kb_pb2.ListRequest(kind="feature", form=kb_pb2.ListRequest.IDS))
    if faults := list(found.refusal.faults):
        raise Refused(faults)
    return Counter(
        scenario["formulates"]
        for name in found.result.ids
        for scenario in loads(_read(client, name).content).get("scenarios", [])
    )
