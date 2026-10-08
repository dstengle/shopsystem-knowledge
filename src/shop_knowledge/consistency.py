"""What the shop's scenarios say that its capabilities do not: for every feature in the knowledge base, of any shop,
the scenarios whose `uses` names a capability outside the `depends_on` of the capability the feature formulates. It
reads through the contract alone and gives one fault for each scenario and capability. It runs beside kb's own
check and never takes its answer away: where the store holds no `feature` type it finds nothing, and what it cannot
read, or what does not fit its type, it passes over, since kb's check reports that itself."""
from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.renderers import source

RULE = "uses-not-depended-on"


def of(client) -> list[kb_pb2.Fault]:
    """A fault for each scenario, in every feature of the knowledge base, that uses a capability its own does not
    depend on; none where the store holds no `feature` type."""
    if not _holds_features(client):
        return []
    listed = client.List(kb_pb2.ListRequest(kind="feature", form=kb_pb2.ListRequest.IDS))
    found = []
    for id in listed.result.ids:
        feature = _read(client, id)
        formulates = _fields(feature).get("formulates")
        capability = _read(client, formulates) if isinstance(formulates, str) else None
        if feature and capability:
            found += undepended(feature, _names(_fields(capability).get("depends_on")))
    return found


def undepended(feature: kb_pb2.Artifact, depends_on: list[str]) -> list[kb_pb2.Fault]:
    """A fault for each scenario of the feature and each capability, named once however often its `uses` names it,
    not among `depends_on`; a scenario that does not fit its type is passed over."""
    return [
        kb_pb2.Fault(artifact=feature.id, place=f"scenarios/{scenario['id']}", rule=RULE,
                     message=f"scenario \"{scenario['title']}\" uses {used}, which its capability does not depend on; "
                             "a scenario uses only what its capability depends on")
        for scenario in _scenarios(feature) for used in dict.fromkeys(_names(scenario.get("uses")))
        if used not in depends_on
    ]


def _holds_features(client) -> bool:
    """Whether the store holds the `feature` type, by kb's answer naming the types it holds."""
    listed = client.List(kb_pb2.ListRequest(kind="schema", form=kb_pb2.ListRequest.IDS))
    return "schema/feature" in listed.result.ids


def _read(client, name: str) -> kb_pb2.Artifact | None:
    """The artifact read whole, or None where kb refused to read it."""
    read = source.whole(client, name)
    return None if source.faults(read) else read.result


def _fields(artifact: kb_pb2.Artifact | None) -> dict:
    content = loads(artifact.content) if artifact else None
    return content if isinstance(content, dict) else {}


def _scenarios(feature: kb_pb2.Artifact) -> list[dict]:
    """The feature's scenarios that carry the id and title a fault names them by."""
    scenarios = _fields(feature).get("scenarios")
    return [each for each in scenarios if isinstance(each, dict) and isinstance(each.get("id"), str)
            and isinstance(each.get("title"), str)] if isinstance(scenarios, list) else []


def _names(value) -> list[str]:
    """The names a list of links holds; none where it is not one."""
    return [each for each in value if isinstance(each, str)] if isinstance(value, list) else []
