"""The markdown renderer: any artifact as a page for a person, laid out from kb's content model alone. Every type keeps
its prose under `sections`, so that is the one entry told apart; every other entry is a field. No schema is read and no
type is named. The page is the title as a heading, the fields as a list in the order kb gives them, then the sections,
each a heading one level below the one that holds it."""
from kb.content import loads

from shop_knowledge.renderers import sections, source
from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The page's file by path, the artifact's name without its kind, or the faults of the read that could not be
    made."""
    artifact = source.whole(client, name)
    if artifact.faults:
        return refused(artifact.faults)
    return Rendered({f"{source.slug(artifact.id)}.md": _page(artifact.title, loads(artifact.content))}, [])


def _page(title: str, content: dict) -> str:
    """The heading, the field list and each section, a blank line between them."""
    fields = {key: value for key, value in content.items() if key != "sections"}
    blocks = [f"# {title}"]
    if fields:
        blocks.append("\n".join(_items(fields, 0)))
    blocks += sections.laid_out(content.get("sections", []), 2)
    return "\n\n".join(blocks) + "\n"


def _items(fields: dict, depth: int) -> list[str]:
    """One list item a field; a field that holds fields is its name with its own items nested two spaces in."""
    lines = []
    for key, value in fields.items():
        indent = "  " * depth
        if isinstance(value, dict):
            lines += [f"{indent}- **{key}**", *_items(value, depth + 1)]
        else:
            lines.append(f"{indent}- **{key}**: {_value(value)}")
    return lines


def _value(value) -> str:
    """A list of plain values joined with commas; anything else as it is written."""
    return ", ".join(str(each) for each in value) if isinstance(value, list) else str(value)

