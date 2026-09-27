"""What a renderer publishes from: an artifact read whole through the contract, and its name without its kind. kb's
answer comes back as it is; whether its faults refuse the render is the renderer's to say."""
from kb.contract import kb_pb2


def whole(client, name: str, depth: int = 0) -> kb_pb2.ReadResponse:
    """The artifact read whole, its links followed as many steps as depth says; at 0 they are left as names."""
    request = kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=name), level=kb_pb2.ReadRequest.WHOLE, depth=depth)
    return client.Read(request)


def slug(artifact_id: str) -> str:
    """An artifact's name without its kind: `process/deploy` is `deploy`."""
    return artifact_id.split("/", 1)[1]
