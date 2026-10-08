"""What stops a shop's spec being published whole: a shop whose capabilities, decisions and features would publish
inconsistently. Each check gives its faults in plain words, naming what is at fault, and every fault found is given at
once, so nothing is written (rule 6) until the shop is put right. All run before any page is laid out."""
from collections import defaultdict

from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge import consistency
from shop_knowledge.renderers import names, shop_capabilities, source, spec_decisions


def check(client, shop: kb_pb2.Artifact, ordered: list[kb_pb2.Artifact], formulating: dict[str, list[kb_pb2.Artifact]]):
    """The faults of the capabilities linking to the shop, the features formulating them, and the decisions
    linking to the shop; or the faults of the read that could not be made."""
    own, faults = spec_decisions.of(client, shop.id)
    if faults:
        return faults
    retired, faults = _retired(client, shop, ordered)
    if faults:
        return faults
    return [
        *retired,
        *_shared([(each.id, f"spec/capabilities/{names.from_title(each.title)}.md") for each in ordered], "capabilities-share-a-file"),
        *_shared([(each.id, each.path) for each in own], "decisions-share-a-file"),
        *_numbered(own),
        *_ordered(ordered),
        *_borrowed(ordered, {each.id for each in own}),
        *_shared([(each.id, f"features/{names.from_title(capability.title)}.feature")
                  for capability in ordered for each in formulating.get(capability.id, [])], "features-share-a-file"),
        *_undepended(ordered, formulating),
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


def _ordered(capabilities: list[kb_pb2.Artifact]) -> list[kb_pb2.Fault]:
    """A fault for each order that more than one capability carries, orders equal where they compare equal."""
    pairs = [(each.id, str(shop_capabilities.position(loads(each.content)["order"]))) for each in capabilities]
    return [_fault(ids[0], "order-places-one-capability", f"carries an order, and an order places one capability; {' and '.join(ids[1:])} carries it too")
            for _, ids in _grouped(pairs)]


def _borrowed(ordered: list[kb_pb2.Artifact], own: set[str]) -> list[kb_pb2.Fault]:
    """A fault for each decision a capability rests on that is not one of the shop's own."""
    return [_fault(each.id, "rests-on-its-own-shops-decisions", f"rests on {decision}, a decision of another shop; a capability rests only on its own shop's decisions")
            for each in ordered for decision in loads(each.content).get("rests_on", []) if decision not in own]


def _undepended(ordered: list[kb_pb2.Artifact], formulating: dict[str, list[kb_pb2.Artifact]]) -> list[kb_pb2.Fault]:
    """A fault for each scenario whose `uses` names a capability that is not among its capability's `depends_on`."""
    return [fault for capability in ordered for feature in formulating.get(capability.id, [])
            for fault in consistency.undepended(feature, loads(capability.content).get("depends_on", []))]


def _retired(client, shop: kb_pb2.Artifact, ordered: list[kb_pb2.Artifact]):
    """A fault for each published capability whose `depends_on`, and for each constraint of the shop whose
    `tested_in`, names a retired capability, in any shop, each named read whole for its status; or the faults of the
    first read that was refused."""
    asks = [(each.id, "depends-on-a-retired-capability", name, _depends_on_retired)
            for each in ordered for name in loads(each.content).get("depends_on", [])]
    asks += [(shop.id, "tested-in-a-retired-capability", name, _tested_in_retired(constraint["title"]))
             for constraint in loads(shop.content).get("constraints", []) for name in constraint.get("tested_in", [])]
    status = {}
    faults = []
    for artifact, rule, name, message in asks:
        if name not in status:
            read = source.whole(client, name)
            if refused := source.faults(read):
                return [], refused
            status[name] = loads(read.result.content)["status"]
        if status[name] == "retired":
            faults.append(_fault(artifact, rule, message(name)))
    return faults, []


def _depends_on_retired(name: str) -> str:
    return f"depends on {name}, a retired capability; a published capability depends only on one in use"


def _tested_in_retired(title: str):
    """The wording of a constraint of `title` tested in a retired capability, as a function of that capability's name,
    so neither the title nor the name is read as a format."""
    return lambda name: f"carries the constraint \"{title}\", tested in {name}, a retired capability; a constraint is tested only in one in use"


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
