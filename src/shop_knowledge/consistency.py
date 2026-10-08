"""What the shop's scenarios say that its capabilities do not: for every feature in the knowledge base, of any shop,
the scenarios whose `uses` names a capability outside the `depends_on` of the capability the feature formulates. It
reads through the contract alone and gives a fault for each; its refusals are raised as `refusal.Refused`, kb's own
passed on."""
from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.refusal import Refused
from shop_knowledge.renderers import source

RULE = "uses-not-depended-on"


def of(client) -> list[kb_pb2.Fault]:
    """A fault for each scenario, in every feature of the knowledge base, that uses a capability its own does not
    depend on."""
    listed = client.List(kb_pb2.ListRequest(kind="feature", form=kb_pb2.ListRequest.IDS))
    if faults := list(listed.refusal.faults):
        raise Refused(faults)
    found = []
    for id in listed.result.ids:
        feature = _read(client, id)
        capability = _read(client, loads(feature.content)["formulates"])
        found += undepended(feature, loads(capability.content).get("depends_on", []))
    return found


def undepended(feature: kb_pb2.Artifact, depends_on: list[str]) -> list[kb_pb2.Fault]:
    """A fault for each scenario of the feature whose `uses` names a capability not among `depends_on`."""
    return [
        kb_pb2.Fault(artifact=feature.id, place=f"scenarios/{scenario['id']}", rule=RULE,
                     message=f"scenario \"{scenario['title']}\" uses {used}, which its capability does not depend on; "
                             "a scenario uses only what its capability depends on")
        for scenario in loads(feature.content).get("scenarios", []) for used in scenario.get("uses", [])
        if used not in depends_on
    ]


def _read(client, name: str) -> kb_pb2.Artifact:
    read = source.whole(client, name)
    if faults := source.faults(read):
        raise Refused(faults)
    return read.result
