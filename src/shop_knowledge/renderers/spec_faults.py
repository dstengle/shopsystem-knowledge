"""What stops a shop's spec being published whole: a shop whose capabilities, decisions and features would publish
inconsistently. Each check gives its faults in plain words, naming what is at fault, and every fault found is given at
once, so nothing is written (rule 6) until the shop is put right. All run before any page is laid out."""
from collections import defaultdict

from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.renderers import names, source, spec_decisions


def check(client, shop: kb_pb2.Artifact, ordered: list[kb_pb2.Artifact], formulating: dict[str, list[kb_pb2.Artifact]]):
    """The faults of the capabilities linking to the shop, the features formulating them, and the decisions
    linking to the shop; or the faults of the read that could not be made."""
    own, faults = spec_decisions.of(client, shop.id)
    if faults:
        return faults
    depended, faults = _retired_dependencies(client, ordered)
    if faults:
        return faults
    return [
        *depended,
        *_shared([(each.id, f"spec/capabilities/{names.from_title(each.title)}.md") for each in ordered], "capabilities-share-a-file"),
        *_shared([(each.id, each.path) for each in own], "decisions-share-a-file"),
        *_numbered(own),
        *_shared([(each.id, f"features/{names.from_title(capability.title)}.feature")
                  for capability in ordered for each in formulating.get(capability.id, [])], "features-share-a-file"),
        *_used({each.id for each in ordered}, formulating),
        *_ragged(formulating),
    ]


def _fault(artifact: str, rule: str, message: str) -> kb_pb2.Fault:
    return kb_pb2.Fault(artifact=artifact, rule=rule, message=message)


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


def _used(shop_capabilities: set[str], formulating: dict[str, list[kb_pb2.Artifact]]) -> list[kb_pb2.Fault]:
    """A fault for each scenario whose `uses` names a capability of its own shop."""
    return [
        _fault(feature.id, "uses-its-own-shop", f"scenario \"{scenario['title']}\" uses {used}, a capability of its own shop; a scenario uses only another shop's capability")
        for features in formulating.values() for feature in features
        for scenario in loads(feature.content).get("scenarios", []) for used in scenario.get("uses", []) if used in shop_capabilities
    ]


def _retired_dependencies(client, ordered: list[kb_pb2.Artifact]):
    """A fault for each published capability whose `depends_on` names a retired capability, in any shop, each named
    read whole for its status; or the faults of the first read that was refused."""
    status = {}
    faults = []
    for each in ordered:
        for name in loads(each.content).get("depends_on", []):
            if name not in status:
                read = source.whole(client, name)
                if refused := source.faults(read):
                    return [], refused
                status[name] = loads(read.result.content)["status"]
            if status[name] == "retired":
                faults.append(_fault(each.id, "depends-on-a-retired-capability",
                                     f"depends on {name}, a retired capability; a published capability depends only on one in use"))
    return faults, []


def _ragged(formulating: dict[str, list[kb_pb2.Artifact]]) -> list[kb_pb2.Fault]:
    """A fault for each scenario, or background, holding a table whose rows are not all as wide as its first."""
    faults = []
    for features in formulating.values():
        for feature in features:
            content = loads(feature.content)
            holders = [("the background", _tables(content.get("background", []), []))] + [
                (f"scenario \"{each['title']}\"", _tables(each["steps"], [each["examples"]] if each.get("examples") else []))
                for each in content.get("scenarios", [])]
            faults += [_fault(feature.id, "table-rows-differ-in-width",
                              f"{name} holds a table whose rows differ in width; a table's rows must each have one cell per column")
                       for name, tables in holders if any(len({len(row) for row in table}) > 1 for table in tables)]
    return faults


def _tables(steps: list[dict], more: list[list[list[str]]]) -> list[list[list[str]]]:
    return [*[step["table"] for step in steps if step.get("table")], *more]
