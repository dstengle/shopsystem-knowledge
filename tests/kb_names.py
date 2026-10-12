"""The test seam: every name a test hands kb directly, and every name it reads back from a kb message. On kb 0.6 each
is the identity; when the pin moves, this module alone changes on the test side. It mirrors the roles of the production
seam but never imports it (CLAUDE.md rule 1): it spells kb's forms itself. Imported plainly, never star-imported."""
from kb.contract import kb_pb2


def kind_name(kind: str) -> str:
    """A kind a user names, as kb's request fields name it."""
    return kind


def create_request(kind: str, title: str, content: str, signature: kb_pb2.Signature) -> kb_pb2.CreateRequest:
    """A Create of an artifact of the kind a user names, with the content already written as text."""
    return kb_pb2.CreateRequest(kind=kind_name(kind), title=title, content=content, signature=signature)


def artifact_id(answer) -> str:
    """The id kb named the artifact with, from the answer to a Create."""
    return answer.result.id


def artifact_name(kb_id: str) -> str:
    """kb's id (or any artifact a fault names) as the user is shown it."""
    return kb_id
