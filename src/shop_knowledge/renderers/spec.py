"""The spec renderer: a shop's spec, published from the shop and, through it, the capabilities it orders and its
constraints are pinned in. It reads through the contract alone and writes nothing; this one gives `spec/index.md`."""
from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.renderers import names, source, spec_capabilities, spec_index
from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The spec's files by path, or the faults of the read that could not be made, or that the artifact is no shop."""
    read = source.whole(client, name)
    if faults := source.refusal(read, "spec", "shop"):
        return refused(faults)
    shop = read.result
    content = loads(shop.content)
    capabilities, faults = _capabilities(client, _wanted(content))
    if faults:
        return refused(faults)
    pages, faults = _pages(client, [capabilities[id] for id in content.get("reading_order", [])])
    if faults:
        return refused(faults)
    index = {"spec/index.md": spec_index.page(shop.title, content, {id: _described(each) for id, each in capabilities.items()})}
    return Rendered({**index, **pages}, [])


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


def _pages(client, capabilities: list[kb_pb2.Artifact]):
    """Each capability's page by its path, or the faults of the first search for its feature that was refused."""
    pages = {}
    for capability in capabilities:
        features = client.List(kb_pb2.ListRequest(kind="feature", fields={"formulates": capability.id}, form=kb_pb2.ListRequest.IDS))
        if faults := list(features.refusal.faults):
            return {}, faults
        name = names.from_title(capability.title)
        formulated_as = f"features/{name}.feature" if features.result.ids else None
        pages[f"spec/capabilities/{name}.md"] = spec_capabilities.page(
            capability.id, capability.title, loads(capability.content), formulated_as)
    return pages, []
