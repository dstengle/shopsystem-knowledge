"""The skill renderer: a process as SKILL.md in the harness's heading-block-plus-body shape. The heading block is the
process's identity; the body is its steps in order, each reused step written out in full with its own settings, and
each branch saying which step it goes to."""
from kb.content import dumps, loads
from kb.contract import kb_pb2

from shop_knowledge.renderers import limits, source
from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The skill's files by path, or the faults of the reads that could not be made, or of an artifact that is not a
    process."""
    read = source.whole(client, name)
    faults = source.refusal(read, "skill", "process")
    if faults:
        return refused(faults)
    process = read.result
    steps = loads(process.content).get("steps", [])
    reads = {used: source.whole(client, used) for used in dict.fromkeys(step["uses"] for step in steps if "uses" in step)}
    faults = [fault for response in reads.values() for fault in source.faults(response)]
    if faults:
        return refused(faults)
    shared = {used: response.result for used, response in reads.items()}
    return _skill(process, _body(process.title, steps, shared))


def _skill(process: kb_pb2.Artifact, written: str) -> Rendered:
    """SKILL.md in a directory of the skill's name, the process's name without its kind, or refused if the harness would
    reject it."""
    faults = limits.skill(process.id, written)
    if faults:
        return refused(faults)
    slug = source.slug(process.id)
    heading = dumps({"name": slug, "description": process.title})
    return Rendered({f"{slug}/SKILL.md": f"---\n{heading}---\n\n{written}"}, [])


def _body(title: str, steps: list[dict], shared: dict) -> str:
    """The process as instructions: a heading, then each step under a numbered heading of its own."""
    numbers = {step["id"]: number for number, step in enumerate(steps, 1)}
    titles = {step["id"]: step["title"] for step in steps}
    lines = [f"# {title}", ""]
    for step in steps:
        lines += [f"## {numbers[step['id']]}. {step['title']}", ""]
        if "uses" in step:
            lines += _reused(step, shared[step["uses"]])
        else:
            lines += [step["does"].rstrip(), ""]
        branches = step.get("branches", [])
        lines += [f"- If {branch['when']}, go to {_step(branch['go_to'], numbers, titles)}." for branch in branches]
        lines += [""] if branches else []
    return "\n".join(lines)


def _step(name: str, numbers: dict, titles: dict) -> str:
    """Where a branch goes: the step by its number and title, or the name as written if no step of the process has it."""
    return f"step {numbers[name]} ({titles[name]})" if name in numbers else name


def _reused(step: dict, used: kb_pb2.Artifact) -> list[str]:
    """A shared step written out in full where it is used, with the settings this use gives it."""
    settings = ", ".join(f"{binding['name']} is {binding['value']}" for binding in step.get("with", []))
    said = f"This is the shared step {used.title}" + (f", where {settings}." if settings else ".")
    return [said, "", loads(used.content)["does"].rstrip(), ""]

