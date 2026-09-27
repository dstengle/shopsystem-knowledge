"""Each kb answer as the document the user is shown: plain dicts, ready for the command line to show."""
from kb.content import loads
from kb.contract import kb_pb2


def created(response: kb_pb2.CreateResponse) -> dict:
    """What a create gives back: the id kb chose and the revision it made."""
    return {"id": response.id, "revision": response.revision}


def glance(response: kb_pb2.ReadResponse) -> dict:
    """A summary read as the user is shown it: identity, the fields the type shows, stubs, parts and inbound counts."""
    return {
        "id": response.id,
        "type": response.type,
        "schema_version": response.schema_version,
        "revision": response.revision,
        "title": response.title,
        **loads(response.content),
        "references": [
            {"field": stub.field, "id": stub.id, "type": stub.type, "title": stub.title, **loads(stub.fields)}
            for stub in response.references
        ],
        "parts": [{"collection": stub.collection, "id": stub.id, "title": stub.title} for stub in response.parts],
        "inbound": [{"type": count.type, "field": count.field, "count": count.count} for count in response.inbound],
    }


def applied(response: kb_pb2.ApplyResponse) -> dict:
    """What a batch gives back: the set's name and each change's id and revision, in the order made."""
    return {
        "batch": response.batch,
        "results": [{"id": result.id, "revision": result.revision} for result in response.results],
    }


def history(response: kb_pb2.JournalResponse) -> dict:
    """The history as the user is shown it: every change, oldest first."""
    return {"changes": [change(entry) for entry in response.entries]}


def change(entry: kb_pb2.Entry) -> dict:
    """One entry of the history as the user is shown it: when, who and for what piece of work, what it did, and why."""
    return {
        "at": entry.at,
        "actor": {"role": entry.actor.role, "execution": entry.actor.execution},
        "op": entry.op,
        "artifact": entry.artifact,
        "revision": entry.revision,
        "message": entry.message,
    }


def written(files) -> dict:
    """What a render gives back: the paths written, sorted."""
    return {"written": sorted(files)}
