"""A capability's page, `spec/capabilities/<name>.md`, laid out from the capability's content: its frontmatter, its
title, its Purpose, its Behaviour, its other sections, then what it does not yet do."""
from kb.content import dumps

from shop_knowledge.renderers import sections


def page(id: str, title: str, content: dict, formulated_as: str | None) -> str:
    """The capability as a file: the frontmatter first, naming the feature file only where a feature formulates it."""
    held = content.get("sections", [])
    purpose = [section for section in held if section["title"] == "Purpose"]
    others = [section for section in held if section["title"] != "Purpose"]
    blocks = [sections.heading(1, title), *sections.laid_out(purpose, 2)]
    blocks += [sections.heading(2, "Behaviour"), _behaviour(content.get("behaviour", []))]
    blocks += sections.laid_out(others, 2)
    if content.get("not_yet"):
        blocks += [sections.heading(2, "Not yet"), _not_yet(content["not_yet"])]
    return _frontmatter(id, title, content, formulated_as) + "\n\n".join(blocks) + "\n"


def _frontmatter(id: str, title: str, content: dict, formulated_as: str | None) -> str:
    fields = {"id": id, "title": title, "narrator": content["narrator"], "rests_on": content.get("rests_on", [])}
    if formulated_as:
        fields["formulated_as"] = formulated_as
    return f"---\n{dumps(fields)}---\n\n"


def _behaviour(lines: list[dict]) -> str:
    return "\n".join(f"- {line['says']}" for line in lines)


def _not_yet(items: list[dict]) -> str:
    return "\n".join(f"- **{item['title']}.** {item['defers']} Promoted when {item['trigger']}." for item in items)
