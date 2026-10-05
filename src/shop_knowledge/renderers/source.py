"""What a renderer publishes from: an artifact read whole through the contract, whether it is of the type the renderer
is made from, and its name without its kind. kb's answer comes back as it is; `refusal` decides what stops a render:
the read's own refusal first, then, only once it was read, whether its type is the one the render is made from."""
from kb.contract import kb_pb2


def whole(client, name: str, depth: int = 0) -> kb_pb2.ReadResponse:
    """The artifact read whole, its links followed as many steps as depth says; at 0 they are left as names."""
    request = kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=name), whole=kb_pb2.ReadRequest.Whole(depth=depth))
    return client.Read(request)


def faults(read: kb_pb2.ReadResponse) -> list[kb_pb2.Fault]:
    """The faults of the refusal a read was answered with; none when it was read."""
    return list(read.refusal.faults)


def refusal(read: kb_pb2.ReadResponse, kind: str, made_from: str) -> list[kb_pb2.Fault]:
    """What stops a kind of file being made from the artifact read: the read's own faults first, then, if it was read,
    one fault on it if it is not of the type the kind is made from, worded with that type and the one it is."""
    if read.WhichOneof("outcome") == "refusal":
        return faults(read)
    artifact = read.result
    if artifact.kind == made_from:
        return []
    message = f"{_a(kind)} is made from {_a(made_from)}; this one is {_a(artifact.kind)}"
    return [kb_pb2.Fault(artifact=artifact.id, rule="renderer-type", message=message)]


def _a(word: str) -> str:
    """A kind or a type with its article: `an agent`, `a role`."""
    return f"an {word}" if word[0] in "aeiou" else f"a {word}"


def slug(artifact_id: str) -> str:
    """An artifact's name without its kind: `process/deploy` is `deploy`."""
    return artifact_id.split("/", 1)[1]
