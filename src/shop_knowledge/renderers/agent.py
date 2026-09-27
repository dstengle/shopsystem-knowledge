"""The agent renderer: a role as `.claude/agents/<name>.md` in the harness's heading-block-plus-body shape. The heading
block is the role's harness field group as kb gives it; the body is its sections."""
from kb.content import dumps, loads

from shop_knowledge.renderers import sections, source
from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The agent's file by path, the role's name without its kind, or the faults of the read that could not be made."""
    role = source.whole(client, name)
    if role.faults:
        return refused(role.faults)
    content = loads(role.content)
    heading = dumps(content.get("harness", {}))
    body = "\n\n".join(sections.laid_out(content.get("sections", []), 1))
    return Rendered({f".claude/agents/{source.slug(role.id)}.md": f"---\n{heading}---\n\n{body}\n"}, [])
