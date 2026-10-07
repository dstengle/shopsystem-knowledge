"""What stops a shop's spec being published whole: a shop whose capabilities, decisions and features would publish
inconsistently. Each check gives its faults in plain words, naming what is at fault, and every fault found is given at
once, so nothing is written (rule 6) until the shop is put right. All run before any page is laid out."""
from collections import defaultdict

from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.renderers import names, spec_decisions


def check(client, shop: kb_pb2.Artifact, ordered: list[kb_pb2.Artifact], formulating: dict[str, list[kb_pb2.Artifact]]):
    """The faults of the capabilities in the shop's reading order, the features formulating them, and the decisions the
    shop names and its capabilities rest on; or the faults of the read that could not be made."""
    content = loads(shop.content)
    listed = client.List(kb_pb2.ListRequest(kind="capability", fields={"shop": shop.id}, form=kb_pb2.ListRequest.IDS))
    if listed.refusal.faults:
        return list(listed.refusal.faults)
    own, faults = spec_decisions.read(client, content.get("decisions", []))
    if faults:
        return faults
    unowned, faults = _unowned(client, [loads(each.content) for each in ordered], content.get("decisions", []))
    if faults:
        return faults
    return [
        *_left_out(list(listed.result.ids), content.get("reading_order", [])),
        *_foreign(shop.id, ordered),
        *_shared([(each.id, f"spec/capabilities/{names.from_title(each.title)}.md") for each in ordered], "capabilities-share-a-file"),
        *_shared([(each.id, each.path) for each in own], "decisions-share-a-file"),
        *_numbered(own),
        *[_unowned_fault(id) for id in unowned],
        *_shared([(each.id, f"features/{names.from_title(capability.title)}.feature")
                  for capability in ordered for each in formulating.get(capability.id, [])], "features-share-a-file"),
        *_used(set(listed.result.ids) | set(content.get("reading_order", [])), formulating),
    ]


def _fault(artifact: str, rule: str, message: str) -> kb_pb2.Fault:
    return kb_pb2.Fault(artifact=artifact, rule=rule, message=message)


def _left_out(named_for_shop: list[str], reading_order: list[str]) -> list[kb_pb2.Fault]:
    return [_fault(id, "not-in-reading-order", "names the shop but is not in the shop's reading order")
            for id in named_for_shop if id not in reading_order]


def _foreign(shop: str, ordered: list[kb_pb2.Artifact]) -> list[kb_pb2.Fault]:
    return [_fault(each.id, "belongs-to-another-shop", f"is in the shop's reading order but belongs to another shop, {loads(each.content).get('shop')}")
            for each in ordered if loads(each.content).get("shop") != shop]


def _grouped(pairs: list[tuple[str, str]]) -> list[tuple[str, list[str]]]:
    """The keys that more than one artifact has, each with the artifacts' names in the order they were given."""
    groups = defaultdict(list)
    for id, key in pairs:
        groups[key].append(id)
    return [(key, ids) for key, ids in groups.items() if len(ids) > 1]


def _shared(pairs: list[tuple[str, str]], rule: str) -> list[kb_pb2.Fault]:
    """One fault for each file that more than one artifact would be published as, naming them all."""
    return [_fault(ids[0], rule, f"would share the file {key} with {' and '.join(ids[1:])}") for key, ids in _grouped(pairs)]


def _numbered(decisions: list[spec_decisions.Decision]) -> list[kb_pb2.Fault]:
    pairs = [(each.id, str(each.content["number"])) for each in decisions]
    return [_fault(ids[0], "number-names-one-decision", f"carries number {key}, and a number names one decision; {' and '.join(ids[1:])} carries it too")
            for key, ids in _grouped(pairs)]


def _unowned(client, capabilities: list[dict], own: list[str]):
    """The decisions the capabilities rest on that no shop names, or the faults of the question that was refused."""
    found = []
    for id in spec_decisions.resting_on(capabilities, own):
        owners, faults = spec_decisions.owners_of(client, id)
        if faults:
            return [], faults
        if not owners:
            found.append(id)
    return found, []


def _unowned_fault(id: str) -> kb_pb2.Fault:
    return _fault(id, "decision-belongs-to-no-shop", "belongs to no shop: no shop names it among its decisions")


def _used(shop_capabilities: set[str], formulating: dict[str, list[kb_pb2.Artifact]]) -> list[kb_pb2.Fault]:
    """A fault for each scenario whose `uses` names a capability of its own shop."""
    return [
        _fault(feature.id, "uses-its-own-shop", f"scenario \"{scenario['title']}\" uses {used}, a capability of its own shop; a scenario uses only another shop's capability")
        for features in formulating.values() for feature in features
        for scenario in loads(feature.content).get("scenarios", []) for used in scenario.get("uses", []) if used in shop_capabilities
    ]
