"""What a shop depends on: for the shop's active or deprecated capabilities, each that depends on a deprecated or
retired capability, in any shop, with the scenarios of its features that use it. It reads through the contract alone
and reports; what it finds is never a refusal. Its refusals are raised as `refusal.Refused`, kb's own passed on."""
from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.refusal import Refused
from shop_knowledge.renderers import shop_capabilities, source

PUBLISHED = {"active", "deprecated"}
LEAVING = {"deprecated", "retired"}


def _refusal(read: kb_pb2.ReadResponse) -> list[kb_pb2.Fault]:
    """What stops an answer: kb's own refusal of the read, else the artifact's not being a shop."""
    if read.WhichOneof("outcome") == "refusal":
        return source.faults(read)
    if read.result.kind != "shop":
        return [kb_pb2.Fault(artifact=read.result.id, rule="dependencies-of-a-shop", message=f"{read.result.id} is a {read.result.kind}, not a shop")]
    return []


def of(client, shop: str) -> list[dict]:
    """One entry for each pair of a capability of the shop and a deprecated or retired capability it depends on, in
    the capabilities' order and then the order the capability names what it depends on."""
    if faults := _refusal(source.whole(client, shop)):
        raise Refused(faults)
    capabilities, faults = shop_capabilities.of(client, shop)
    if faults:
        raise Refused(faults)
    entries = []
    for held in capabilities:
        content = loads(held.content)
        if content["status"] not in PUBLISHED:
            continue
        for name in dict.fromkeys(content.get("depends_on", [])):
            target = _read(client, name)
            if loads(target.content)["status"] in LEAVING:
                entries.append(_entry(held, target, _scenarios(client, held.id, name)))
    return entries


def _read(client, name: str) -> kb_pb2.Artifact:
    read = source.whole(client, name)
    if faults := source.faults(read):
        raise Refused(faults)
    return read.result


def _entry(held: kb_pb2.Artifact, target: kb_pb2.Artifact, scenarios: list[str]) -> dict:
    content = loads(target.content)
    return {
        "capability": held.id, "capability_title": held.title,
        "depends_on": target.id, "depends_on_title": target.title,
        "shop": content["shop"], "status": content["status"],
        "scenarios": scenarios,
    }


def _scenarios(client, capability: str, used: str) -> list[str]:
    """The titles of the scenarios, in the features formulating `capability`, whose `uses` name `used`."""
    found = client.List(kb_pb2.ListRequest(kind="feature", fields={"formulates": capability}, form=kb_pb2.ListRequest.IDS))
    if faults := list(found.refusal.faults):
        raise Refused(faults)
    return [
        scenario["title"]
        for name in found.result.ids
        for scenario in loads(_read(client, name).content).get("scenarios", [])
        if used in scenario.get("uses", [])
    ]
