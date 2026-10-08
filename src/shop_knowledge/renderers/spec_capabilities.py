"""A capability's page, `spec/capabilities/<name>.md`, laid out from the capability's content: its frontmatter, its
title, its Purpose, its Behaviour, its other sections, then what it does not yet do."""
from kb.content import dumps
from kb.contract import kb_pb2

from shop_knowledge.renderers import published_from, sections


def page(capability: kb_pb2.Artifact, content: dict, formulated_as: str | None) -> str:
    """The capability as a file: the frontmatter first, naming the feature file only where a feature formulates it, then
    the published-from line."""
    id, title = capability.id, capability.title
    held = content.get("sections", [])
    purpose = [section for section in held if section["title"] == "Purpose"]
    others = [section for section in held if section["title"] != "Purpose"]
    blocks = [sections.heading(1, title), *sections.laid_out(purpose, 2)]
    blocks += [sections.heading(2, "Behaviour"), _behaviour(content.get("behaviour", []))]
    blocks += sections.laid_out(others, 2)
    if content.get("not_yet"):
        blocks += [sections.heading(2, "Not yet"), _not_yet(content["not_yet"])]
    line = published_from.markdown(id, capability.revision)
    return _frontmatter(id, title, content, formulated_as) + line + "\n\n" + "\n\n".join(blocks) + "\n"


def _frontmatter(id: str, title: str, content: dict, formulated_as: str | None) -> str:
    fields = {"id": id, "title": title, "narrator": content["narrator"], "rests_on": content.get("rests_on", [])}
    if content.get("depends_on"):
        fields["depends_on"] = content["depends_on"]
    if formulated_as:
        fields["formulated_as"] = formulated_as
    return f"---\n{dumps(fields)}---\n"


def _behaviour(lines: list[dict]) -> str:
    return "\n".join(f"- {line['says']}" for line in lines)


def _not_yet(items: list[dict]) -> str:
    return "\n".join(f"- **{item['title']}.** {item['defers']} Promoted when {item['trigger']}." for item in items)
