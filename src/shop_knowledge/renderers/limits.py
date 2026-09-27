"""The limits the harness publishes for what it loads, checked before anything is written. Anthropic's Agent Skills
documentation (platform.claude.com/docs/en/agents-and-tools/agent-skills, best practices) publishes that a SKILL.md
body is under 500 lines. It also publishes limits on a skill's name and description; no scenario asks for those yet.
The harness's subagent documentation (code.claude.com/docs/en/sub-agents, read 2026-09-27) publishes that an agent's
name may not contain ":", reserved for plugin-scoped names, and may not start with "-"; it publishes no length limit
on the name, the description or the body."""
from kb.contract import kb_pb2

BODY_LINES = 500


def _fault(artifact: str, path: str, message: str) -> kb_pb2.Fault:
    """One harness-limit fault, on the artifact and the path a limit was broken at, worded with what the harness
    publishes and what this one is."""
    return kb_pb2.Fault(artifact=artifact, path=path, rule="harness-limit", message=message)


def skill(artifact: str, body: str) -> list[kb_pb2.Fault]:
    """Every way a skill goes beyond what the harness accepts, each a fault on the artifact it was published from."""
    lines = len(body.splitlines())
    if lines < BODY_LINES:
        return []
    return [_fault(
        artifact, "steps",
        f"a skill's body is under {BODY_LINES} lines, the limit the harness publishes; this one is {lines}",
    )]


def agent(artifact: str, name: str) -> list[kb_pb2.Fault]:
    """Every way an agent's harness name goes beyond what the harness accepts, each a fault on the artifact it was
    published from, in the order the harness's documentation gives them."""
    faults = []
    if ":" in name:
        faults.append(_fault(
            artifact, "harness.name",
            f'an agent\'s name holds no ":", the limit the harness publishes; this one is {name}',
        ))
    if name.startswith("-"):
        faults.append(_fault(
            artifact, "harness.name",
            f'an agent\'s name does not start with "-", the limit the harness publishes; this one is {name}',
        ))
    return faults
