"""The spec renderer: a shop's spec, published from the shop and, through it, the capabilities it orders and its
constraints are pinned in. It reads through the contract alone and writes nothing; this one gives `spec/index.md`."""
from kb.content import loads

from shop_knowledge.renderers import names, source, spec_index
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
    return Rendered({"spec/index.md": spec_index.page(shop.title, content, capabilities)}, [])


def _wanted(content: dict) -> list[str]:
    """The capabilities the index names: those in the reading order, and those a constraint is pinned in."""
    pinned = [id for constraint in content.get("constraints", []) for id in constraint.get("pinned_in", [])]
    return list(dict.fromkeys([*content.get("reading_order", []), *pinned]))


def _capabilities(client, ids: list[str]):
    """Each capability read whole, as the index says it, or the faults of the first read that was refused."""
    found = {}
    for id in ids:
        read = source.whole(client, id)
        if faults := source.faults(read):
            return {}, faults
        found[id] = spec_index.Capability(names.from_title(read.result.title), loads(read.result.content)["gist"])
    return found, []
