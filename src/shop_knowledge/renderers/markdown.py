"""The markdown renderer: any artifact as a page for a person, laid out from kb's content model alone. Every type keeps
its prose under `sections`, so that is the one entry told apart; every other entry is a field. No schema is read and no
type is named. The page is the title as a heading, the fields as a list in the order kb gives them (a field holding a
list of mappings taken out as a table of its own), then the sections, each a heading one level below the one that
holds it. No value is ever shown the way a program would print it (adrs/0038)."""
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
    """The heading, the field list, a table a field holding a list of mappings in turn, then each section, a blank
    line between them."""
    fields = {key: value for key, value in content.items() if key != "sections"}
    tables = {key: value for key, value in fields.items() if _is_table(value)}
    fields = {key: value for key, value in fields.items() if key not in tables}
    blocks = [f"# {title}"]
    if fields:
        blocks.append("\n".join(_items(fields, 0)))
    blocks += [_table(key, value) for key, value in tables.items()]
    blocks += sections.laid_out(content.get("sections", []), 2)
    return "\n\n".join(blocks) + "\n"


def _is_table(value) -> bool:
    """A field is laid out as a table when it holds a list of mappings and not, say, a part collection's own kind of
    emptiness: an empty list stays in the field list (adrs/0041)."""
    return isinstance(value, list) and bool(value) and all(isinstance(each, dict) for each in value)


def _items(fields: dict, depth: int) -> list[str]:
    """One list item a field: a field holding fields is its name with its own items nested two spaces in; a field
    holding a list of plain values is its name, then each value as a bullet nested one level in the same way; anything
    else is its name and its value laid out inline (adrs/0041)."""
    lines = []
    for key, value in fields.items():
        indent = "  " * depth
        if isinstance(value, dict):
            lines += [f"{indent}- **{key}**", *_items(value, depth + 1)]
        elif isinstance(value, list):
            child = "  " * (depth + 1)
            lines += [f"{indent}- **{key}**", *(f"{child}- {_inline(each)}" for each in value)]
        else:
            lines.append(f"{indent}- **{key}**: {_inline(value)}")
    return lines


def _table(key: str, items: list[dict]) -> str:
    """The field's name in bold, then a table with one column per key, in the order the keys first appear across the
    items, one row an item, an empty cell where an item lacks the key (adrs/0041)."""
    columns = list(dict.fromkeys(column for item in items for column in item))
    rows = [[_inline(item[column]) if column in item else "" for column in columns] for item in items]
    lines = [_row(columns), _row(["---"] * len(columns))] + [_row(row) for row in rows]
    return f"**{key}**\n\n" + "\n".join(lines)


def _row(cells: list[str]) -> str:
    """One table row, its cells between pipes."""
    return "| " + " | ".join(cells) + " |"


def _inline(value) -> str:
    """A value where a block cannot sit: a mapping's `key: value` pairs joined by `, `, a list's items joined by
    `; `, each laid out inline in turn, and a plain value's lines joined by a space, its trailing newline dropped
    (adrs/0038, adrs/0041)."""
    if isinstance(value, dict):
        return ", ".join(f"{field}: {_inline(each)}" for field, each in value.items())
    if isinstance(value, list):
        return "; ".join(_inline(each) for each in value)
    return " ".join(str(value).splitlines())

