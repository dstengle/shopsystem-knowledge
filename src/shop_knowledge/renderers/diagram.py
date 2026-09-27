"""The diagram renderer: a process as a Mermaid flowchart, laid out by whatever draws it, so nothing here places a node.
Each step is a node numbered in the process's order, a reused step drawn as a subroutine. A step without branches goes
on to the next; a step with branches goes where each says, the edge labelled with its condition."""
from kb.content import loads

from shop_knowledge.renderers import source
from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The diagram's file by path, the process's name without its kind, or the faults of the read that could not be
    made."""
    process = source.whole(client, name)
    if process.faults:
        return refused(process.faults)
    slug = source.slug(process.id)
    return Rendered({f"{slug}.mmd": _flowchart(loads(process.content).get("steps", []))}, [])


def _flowchart(steps: list[dict]) -> str:
    """Every step's node, then every edge between them, top to bottom."""
    nodes = {step["id"]: f"step{number}" for number, step in enumerate(steps, 1)}
    lines = ["flowchart TD"]
    lines += [_node(nodes[step["id"]], number, step) for number, step in enumerate(steps, 1)]
    for step, following in zip(steps, [*steps[1:], None]):
        lines += _edges(step, following, nodes)
    return "\n".join(lines) + "\n"


def _node(node: str, number: int, step: dict) -> str:
    """A step by its number and title; a reused step in the subroutine shape."""
    label = f'"{number}. {step["title"]}"'
    return f"    {node}[[{label}]]" if "uses" in step else f"    {node}[{label}]"


def _edges(step: dict, following: dict | None, nodes: dict) -> list[str]:
    """Where a step goes: each branch's step, labelled with its condition, or else the step after it, if there is one.
    A branch to a name no step of the process has goes to that name as written."""
    node = nodes[step["id"]]
    if "branches" in step:
        return [
            f'    {node} -->|"{branch["when"]}"| {nodes.get(branch["go_to"], branch["go_to"])}'
            for branch in step["branches"]
        ]
    return [f"    {node} --> {nodes[following['id']]}"] if following else []
