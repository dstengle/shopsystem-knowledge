"""The spec renderer: a shop's spec, published from the shop and, through it, the capabilities linking to it and the
capabilities its constraints are tested in. It reads through the contract alone and writes nothing; this one gives `spec/index.md`, the capabilities' pages, the decisions' ledger and records and the feature files."""
from shop_knowledge import iris

from shop_knowledge.renderers import (
    gherkin, names, shop_capabilities, source, spec_capabilities, spec_decisions, spec_faults, spec_index)
from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The spec's files by path, or the faults of the read that could not be made, or that the artifact is no shop, or
    that the shop's spec would publish inconsistently."""
    read = source.whole(client, name)
    if faults := source.refusal(read, "spec", "shop"):
        return refused(faults)
    shop = source.mapped(read.result)
    ordered, faults = shop_capabilities.mapped_of(client, shop.id)
    if faults:
        return refused(faults)
    capabilities, faults = _capabilities(client, ordered, _tested(shop.content))
    if faults:
        return refused(faults)
    formulating, faults = _formulating(client, ordered)
    if not faults:
        faults = spec_faults.check(client, shop, ordered, formulating)
    if faults:
        return refused(faults)
    decisions, faults = spec_decisions.files(client, shop)
    if faults:
        return refused(faults)
    index = {"spec/index.md": spec_index.page(
        shop, {id: _described(each) for id, each in capabilities.items()}, [each.id for each in ordered])}
    return Rendered({**index, **_pages(ordered, formulating), **decisions}, [])


def _tested(content: dict) -> list[str]:
    """The capabilities a constraint is tested in."""
    return [id for constraint in content.get("constraints", []) for id in constraint.get("tested_in", [])]


def _capabilities(client, ordered: list[source.Mapped], tested: list[str]):
    """The shop's capabilities by id, with each tested one read whole besides, or the faults of the first read that
    was refused."""
    found = {each.id: each for each in ordered}
    for id in tested:
        if id not in found:
            read = source.whole(client, id)
            if faults := source.faults(read):
                return {}, faults
            found[id] = source.mapped(read.result)
    return found, []


def _described(capability: source.Mapped) -> spec_index.Capability:
    content = capability.content
    return spec_index.Capability(names.from_title(capability.title), content["gist"], content["status"] == "deprecated")


def _formulating(client, capabilities: list[source.Mapped]):
    """The features formulating each capability, each read whole, by the capability's name, or the faults of the first
    search or read that was refused."""
    found = {}
    for capability in capabilities:
        listed = client.List(iris.ids_request("feature", {"formulates": capability.id}))
        if faults := list(listed.refusal.faults):
            return {}, faults
        found[capability.id] = []
        for id in iris.listed_ids(listed):
            read = source.whole(client, id)
            if faults := source.faults(read):
                return {}, faults
            found[capability.id].append(source.mapped(read.result))
    return found, []


def _pages(capabilities: list[source.Mapped], formulating: dict[str, list[source.Mapped]]) -> dict[str, str]:
    """Each capability's page and the feature file formulating it, by path."""
    files = {}
    for capability in capabilities:
        name = names.from_title(capability.title)
        content = capability.content
        features = formulating[capability.id]
        if features:
            files[f"features/{name}.feature"] = gherkin.feature_file(name, features[0], content["narrator"])
        files[f"spec/capabilities/{name}.md"] = spec_capabilities.page(capability, f"features/{name}.feature" if features else None)
    return files
