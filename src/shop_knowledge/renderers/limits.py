"""The limits the harness publishes for what it loads, checked before anything is written. Anthropic's Agent Skills
documentation (platform.claude.com/docs/en/agents-and-tools/agent-skills, best practices) publishes that a SKILL.md
body is under 500 lines. It also publishes limits on a skill's name and description; no scenario asks for those yet."""
from kb.contract import kb_pb2

BODY_LINES = 500


def skill(artifact: str, body: str) -> list[kb_pb2.Fault]:
    """Every way a skill goes beyond what the harness accepts, each a fault on the artifact it was published from."""
    lines = len(body.splitlines())
    if lines < BODY_LINES:
        return []
    return [kb_pb2.Fault(
        artifact=artifact, path="steps", rule="harness-limit",
        message=f"a skill's body is under {BODY_LINES} lines, the limit the harness publishes; this one is {lines}",
    )]
