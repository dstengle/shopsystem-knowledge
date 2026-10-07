"""The spec renderer: a shop's spec, published from the shop and, through it, the capabilities it orders and its
constraints are pinned in. It reads through the contract alone and writes nothing; this one gives `spec/index.md`, the capabilities' pages, the decisions' ledger and records and the feature files."""
from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.renderers import gherkin, names, source, spec_capabilities, spec_decisions, spec_faults, spec_index
from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The spec's files by path, or the faults of the read that could not be made, or that the artifact is no shop, or
    that the shop's spec would publish inconsistently."""
    read = source.whole(client, name)
    if faults := source.refusal(read, "spec", "shop"):
        return refused(faults)
    shop = read.result
    content = loads(shop.content)
    capabilities, faults = _capabilities(client, _wanted(content))
    if faults:
        return refused(faults)
    ordered = [capabilities[id] for id in content.get("reading_order", [])]
    formulating, faults = _formulating(client, ordered)
    if not faults:
        faults = spec_faults.check(client, shop, ordered, formulating)
    if faults:
        return refused(faults)
    decisions, faults = spec_decisions.files(client, shop, content, [loads(each.content) for each in ordered])
    if faults:
        return refused(faults)
    index = {"spec/index.md": spec_index.page(shop, content, {id: _described(each) for id, each in capabilities.items()})}
    return Rendered({**index, **_pages(ordered, formulating), **decisions}, [])


def _wanted(content: dict) -> list[str]:
    """The capabilities the index names: those in the reading order, and those a constraint is pinned in."""
    pinned = [id for constraint in content.get("constraints", []) for id in constraint.get("pinned_in", [])]
    return list(dict.fromkeys([*content.get("reading_order", []), *pinned]))


def _capabilities(client, ids: list[str]):
    """Each capability read whole, by its id, or the faults of the first read that was refused."""
    found = {}
    for id in ids:
        read = source.whole(client, id)
        if faults := source.faults(read):
            return {}, faults
        found[id] = read.result
    return found, []


def _described(capability: kb_pb2.Artifact) -> spec_index.Capability:
    return spec_index.Capability(names.from_title(capability.title), loads(capability.content)["gist"])


def _formulating(client, capabilities: list[kb_pb2.Artifact]):
    """The features formulating each capability, each read whole, by the capability's name, or the faults of the first
    search or read that was refused."""
    found = {}
    for capability in capabilities:
        listed = client.List(kb_pb2.ListRequest(kind="feature", fields={"formulates": capability.id}, form=kb_pb2.ListRequest.IDS))
        if faults := list(listed.refusal.faults):
            return {}, faults
        found[capability.id] = []
        for id in listed.result.ids:
            read = source.whole(client, id)
            if faults := source.faults(read):
                return {}, faults
            found[capability.id].append(read.result)
    return found, []


def _pages(capabilities: list[kb_pb2.Artifact], formulating: dict[str, list[kb_pb2.Artifact]]) -> dict[str, str]:
    """Each capability's page and the feature file formulating it, by path."""
    files = {}
    for capability in capabilities:
        name = names.from_title(capability.title)
        content = loads(capability.content)
        features = formulating[capability.id]
        if features:
            files[f"features/{name}.feature"] = gherkin.feature_file(name, features[0], content["narrator"], loads(features[0].content))
        files[f"spec/capabilities/{name}.md"] = spec_capabilities.page(capability, content, f"features/{name}.feature" if features else None)
    return files
