"""The agent renderer: a role as `.claude/agents/<name>.md` in the harness's heading-block-plus-body shape. The heading
block is the role's harness field group as kb gives it; the body is its sections."""
from kb.content import dumps, loads

from shop_knowledge.renderers import limits, sections, source
from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The agent's file by path, the role's name without its kind, or the faults of the read that could not be made, or
    of an artifact that is not a role."""
    read = source.whole(client, name)
    faults = source.refusal(read, "agent", "role")
    if faults:
        return refused(faults)
    role = read.result
    content = loads(role.content)
    harness = content.get("harness", {})
    body = "\n\n".join(sections.laid_out(content.get("sections", []), 1))
    return _agent(role.id, harness, body)


def _agent(artifact: str, harness: dict, body: str) -> Rendered:
    """The agent's file, or refused if the harness would reject the role's harness fields."""
    faults = limits.agent(artifact, harness.get("name", ""))
    if faults:
        return refused(faults)
    heading = dumps(harness)
    return Rendered({f".claude/agents/{source.slug(artifact)}.md": f"---\n{heading}---\n\n{body}\n"}, [])
