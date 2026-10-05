"""Each kb answer as the document the user is shown: plain dicts and lists, ready for the command line to show."""
from kb.content import loads
from kb.contract import kb_pb2


def _identity(response: kb_pb2.Artifact) -> dict:
    return {
        "id": response.id,
        "type": response.kind,
        "schema_version": response.schema_version,
        "revision": response.revision,
        "title": response.title,
    }


def created(response: kb_pb2.Created) -> dict:
    """What a create gives back: the id kb chose and the revision it made."""
    return {"id": response.id, "revision": response.revision}


def written_over(locator: kb_pb2.Locator, response: kb_pb2.Replaced) -> dict:
    """What a write gives back: the artifact's id, which kb's answer leaves out, and the revision it made, as a create does."""
    return {"id": locator.id, "revision": response.revision}


def appended(locator: kb_pb2.Locator, response: kb_pb2.Added) -> dict:
    """What an append gives back: the new item as a later write names it, <name>#<collection>/<item>, and the revision."""
    return {"id": f"{locator.id}#{locator.place}/{response.id}", "revision": response.revision}


def deleted(locator: kb_pb2.Locator, response: kb_pb2.Removed) -> dict:
    """What a delete gives back: the artifact retired, by its name, and the revision the removal left behind."""
    return {"id": locator.id, "revision": response.revision}


def glance(response: kb_pb2.Artifact) -> dict:
    """A summary read as the user is shown it: identity, the fields the type shows, stubs, parts and inbound counts."""
    return {
        **_identity(response),
        **loads(response.content),
        "references": [
            {"field": stub.field, "id": stub.id, "type": stub.kind, "title": stub.title, **loads(stub.fields)}
            for stub in response.references
        ],
        "parts": [{"collection": stub.collection, "id": stub.id, "title": stub.title} for stub in response.parts],
        "inbound": [{"type": count.kind, "field": count.field, "count": count.count} for count in response.inbound],
    }


def whole(response: kb_pb2.Artifact) -> dict:
    """A whole read as the user is shown it: the identity, then the content as kb gives it."""
    return {**_identity(response), **loads(response.content)}


def section(response: kb_pb2.Artifact) -> dict:
    """A section read as the user is shown it: the section as kb gives it, and nothing else."""
    return loads(response.content)


def applied(response: kb_pb2.BatchCreated | kb_pb2.BatchReplaced) -> dict:
    """What a batch gives back: the set's name and each change's id and revision, in the order made."""
    return {
        "batch": response.batch,
        "results": [{"id": result.id, "revision": result.revision} for result in response.results],
    }


def history(response: kb_pb2.Entries) -> dict:
    """The history as the user is shown it: every change, oldest first."""
    return {"changes": [change(entry) for entry in response.entries]}


def change(entry: kb_pb2.Entry) -> dict:
    """One entry of the history as the user is shown it: when, who and for what piece of work, what it did, and why;
    and, when it recorded what a piece of work read, each artifact read with the revision read."""
    shown = {
        "at": entry.at,
        "actor": {"role": entry.actor.role, "execution": entry.actor.execution},
        "op": entry.op,
        "artifact": entry.artifact,
        "revision": entry.revision,
        "message": entry.message,
    }
    if entry.read:
        shown["read"] = [{"artifact": read.artifact, "revision": read.revision} for read in entry.read]
    return shown


def recorded(response: kb_pb2.Recorded) -> dict:
    """What a snapshot gives back: the name of the history entry kb made."""
    return {"entry": response.entry}


def listed(response: kb_pb2.Listed) -> list:
    """What a list gives back: one entry for each artifact, its name, type and title, then the fields the type shows."""
    return [{"id": stub.id, "type": stub.kind, "title": stub.title, **loads(stub.fields)} for stub in response.stubs]


def reached(response: kb_pb2.Followed) -> list:
    """What following the links gives back, nearest first: each artifact reached, the link of its last step, its
    stub's fields, and the route taken to it."""
    return [
        {
            "id": found.stub.id, "type": found.stub.kind, "title": found.stub.title, "via": found.stub.field,
            **loads(found.stub.fields),
            "route": [{"field": hop.field, "id": hop.id} for hop in found.route],
        }
        for found in response.reached
    ]


def matched(response: kb_pb2.Found) -> list:
    """What a search gives back, in kb's order: each match's name, type and title, the section or field that matched
    and its snippet."""
    return [
        {
            "id": match.stub.id, "type": match.stub.kind, "title": match.stub.title,
            **({"section": match.section} if match.section else {"field": match.field}),
            "snippet": match.snippet,
        }
        for match in response.matches
    ]


def names(response: kb_pb2.Listed) -> list:
    """What a list asking for names alone gives back: the names, and nothing else."""
    return list(response.ids)


def written(files) -> dict:
    """What a render gives back: the paths written, sorted."""
    return {"written": sorted(files)}


def checked(response: kb_pb2.Checked) -> dict:
    """What every check that ran gives back: sound when it found no violation, and each artifact last checked
    against an older version of its type, whether or not it found any. A check that never ran shows no answer; its
    refusal is refused by the caller before this is reached, so it plays no part in `sound` here."""
    return {
        "sound": not response.violations,
        "behind": [
            {"artifact": stale.artifact, "schema_version": stale.schema_version, "current": stale.current}
            for stale in response.stale
        ],
    }


def types(response: kb_pb2.Listed, shop_types) -> list:
    """What asking for the types gives back: each of the shop's types, kb's own left out, by its name without its kind
    and its title."""
    held = {stub.id.partition("/")[2]: stub.title for stub in response.stubs}
    return [{"name": name, "title": held[name]} for name in shop_types if name in held]


def type_(response: kb_pb2.Artifact) -> dict:
    """A type read as the user is shown it: as kb holds it, shown as any artifact read whole."""
    return whole(response)
