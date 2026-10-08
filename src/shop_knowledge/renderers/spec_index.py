"""The shop's spec index, `spec/index.md`, laid out from the shop's content: its title, its Purpose, the constraints it
carries, its capabilities in their order, then its other sections."""
from kb.contract import kb_pb2

from shop_knowledge.renderers import published_from, sections


class Capability:
    """What the index says of a capability: the name its file is given, its gist, and whether it is deprecated."""

    def __init__(self, name: str, gist: str, deprecated: bool = False):
        self.name, self.gist, self.deprecated = name, gist, deprecated


def page(shop: kb_pb2.Artifact, content: dict, capabilities: dict[str, Capability], order: list[str]) -> str:
    """The index as markdown, the capabilities by the names they are published under, those of `order` listed in it."""
    held = content.get("sections", [])
    purpose = [section for section in held if section["title"] == "Purpose"]
    others = [section for section in held if section["title"] != "Purpose"]
    blocks = [published_from.markdown(shop.id, shop.revision), sections.heading(1, shop.title), *sections.laid_out(purpose, 2)]
    blocks += [sections.heading(2, "Constraints carried"), _constraints(content.get("constraints", []), capabilities)]
    blocks += [sections.heading(2, "Composition (reading order)"), _composition(order, capabilities)]
    blocks += sections.laid_out(others, 2)
    return "\n\n".join(blocks) + "\n"


def _constraints(constraints: list[dict], capabilities: dict[str, Capability]) -> str:
    return "\n".join(_constraint(each, capabilities) for each in constraints)


def _constraint(constraint: dict, capabilities: dict[str, Capability]) -> str:
    """One bullet; the Tested-in clause only where the constraint is tested in a capability."""
    line = f"- **{constraint['title']}.** {constraint['says']}"
    if tested := constraint.get("tested_in"):
        line += f" Tested in {_joined([capabilities[id].name for id in tested])}."
    return line


def _composition(order: list[str], capabilities: dict[str, Capability]) -> str:
    return "\n".join(_entry(number, capabilities[id]) for number, id in enumerate(order, 1))


def _entry(number: int, capability: Capability) -> str:
    line = f"{number}. [{capability.name}](capabilities/{capability.name}.md): {capability.gist}"
    return line + " (deprecated)" if capability.deprecated else line


def _joined(names: list[str]) -> str:
    """Names joined with commas and a final "and"."""
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"
