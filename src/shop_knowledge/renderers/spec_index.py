"""The shop's spec index, `spec/index.md`, laid out from the shop's content: its title, its Purpose, the constraints it
carries, its capabilities in reading order, then its other sections."""
from shop_knowledge.renderers import sections


class Capability:
    """What the index says of a capability: the name its file is given and its gist."""

    def __init__(self, name: str, gist: str):
        self.name, self.gist = name, gist


def page(title: str, content: dict, capabilities: dict[str, Capability]) -> str:
    """The index as markdown, the capabilities by the names the shop links them under."""
    held = content.get("sections", [])
    purpose = [section for section in held if section["title"] == "Purpose"]
    others = [section for section in held if section["title"] != "Purpose"]
    blocks = [sections.heading(1, title), *sections.laid_out(purpose, 2)]
    blocks += [sections.heading(2, "Constraints carried"), _constraints(content.get("constraints", []), capabilities)]
    blocks += [sections.heading(2, "Composition (reading order)"), _composition(content.get("reading_order", []), capabilities)]
    blocks += sections.laid_out(others, 2)
    return "\n\n".join(blocks) + "\n"


def _constraints(constraints: list[dict], capabilities: dict[str, Capability]) -> str:
    return "\n".join(
        f"- **{each['title']}.** {each['says']} Pinned in {_joined([capabilities[id].name for id in each['pinned_in']])}."
        for each in constraints
    )


def _composition(reading_order: list[str], capabilities: dict[str, Capability]) -> str:
    return "\n".join(
        f"{number}. [{capabilities[id].name}](capabilities/{capabilities[id].name}.md): {capabilities[id].gist}"
        for number, id in enumerate(reading_order, 1)
    )


def _joined(names: list[str]) -> str:
    """Names joined with commas and a final "and"."""
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"
