"""The seam between the names a user gives and reads and the fields kb's requests and answers carry: a user's name as
kb is sent it and kb's id back as the user's name, in a request's fields and inside content; every request field that
names a kind or the type of types; the fields a Create or a batch create item carries besides its title, content and
signature; an answer's kind and version as the user sees them; and whether an id names one of the types. On kb.v1
every one is the identity. It knows the shop's types by name, from bootstrap, and never a type's fields."""
import re

from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge import bootstrap

TYPE_OF_TYPES = "schema"
"""The kind a user names the types by: a type is `schema/<name>`."""

_LINK = re.compile(r"(?P<name>(?P<kind>[^\s/#]+)/[^\s/#]+)(?P<part>#\S+)?")
"""A whole string naming an artifact, `<kind>/<name>`, or a part of one, `<kind>/<name>#<place>`."""


def to_kb(name: str) -> str:
    """A user's `<kind>/<name>` as kb is sent it."""
    return name


def from_kb(kb_id: str) -> str:
    """kb's id of an artifact as the user's `<kind>/<name>`; anything else a fault names, a file, as it is."""
    return kb_id


def of_kind(kind: str) -> dict:
    """The fields of a List, Follow or Search that keep it to the kind a user names (every kind, given empty)."""
    return {"kind": _kind(kind)}


def of_types() -> dict:
    """The fields of a List that keep it to the types."""
    return of_kind(TYPE_OF_TYPES)


def ids_request(kind: str, fields: dict[str, str] | None = None) -> kb_pb2.ListRequest:
    """A List of the ids of the artifacts of the kind a user names, those whose fields hold the names given."""
    return kb_pb2.ListRequest(**of_kind(kind), fields={key: to_kb(value) for key, value in (fields or {}).items()},
                              form=kb_pb2.ListRequest.IDS)


def listed_ids(response: kb_pb2.ListResponse) -> list[str]:
    """The ids a List answered with, as the user's names."""
    return [from_kb(each) for each in response.result.ids]


def holds_type(client, name: str) -> bool:
    """Whether the store holds the type a user names by its name alone, by kb's answer naming the types it holds."""
    return type_id(name) in {to_kb(each) for each in listed_ids(client.List(ids_request(TYPE_OF_TYPES)))}


def create_fields(client, kind: str, title: str, name: str = "") -> dict:
    """The fields of a CreateRequest besides title, content and signature, for an artifact of the kind, with the
    title it is given and the name, where the user or the shop gives one. The client is what the type's current
    version is read through where kb is sent it; kb.v1 is sent none, so no call is made."""
    return {"kind": _kind(kind)}


def created_items(client, creates: list[tuple[str, str, str, dict]]) -> list[tuple[dict, dict]]:
    """For each create of a batch, given as its kind, its key (empty where it has none), its title and its content:
    the CreateItem's fields besides title and content, and the content as kb is sent it. On kb.v1 kb resolves a link
    written `@<key>` itself, so the key is sent and the link left as written."""
    return [(_item_fields(client, kind, key, title), content_to_kb(content)) for kind, key, title, content in creates]


def _item_fields(client, kind: str, key: str, title: str) -> dict:
    """A batch create item's fields besides title and content, as `create_fields` gives a Create's."""
    return {"kind": _kind(kind), "key": key}


def _kind(kind: str) -> str:
    """The kind a user names, as kb's request fields name it."""
    return kind


def content_of(artifact: kb_pb2.Artifact):
    """An artifact's content as the user reads it."""
    return content_from_kb(loads(artifact.content))


def content_to_kb(content):
    """Content as kb is sent it: every whole string, at any depth, naming one of the shop's artifacts or a part of
    one, as kb's id for it."""
    return _each_string(content, lambda value: _linked(value, to_kb))


def content_from_kb(content):
    """Content as kb gave it, as the user reads it: every whole string, at any depth, that is kb's id of one of the
    shop's artifacts or of a part of one, as the user's name for it."""
    return _each_string(content, lambda value: _linked(value, from_kb))


def _each_string(value, change):
    """The value with every string in it, at any depth, changed; keys and other values as they are."""
    if isinstance(value, dict):
        return {key: _each_string(item, change) for key, item in value.items()}
    if isinstance(value, list):
        return [_each_string(item, change) for item in value]
    return change(value) if isinstance(value, str) else value


def _linked(value: str, rename) -> str:
    """The string renamed, its place inside kept, where it names one of the shop's artifacts or a part of one; on
    kb.v1 kb's id and the user's name are spelled alike."""
    link = _LINK.fullmatch(value)
    if link is None or link["kind"] not in bootstrap.SHOP_TYPES:
        return value
    return rename(link["name"]) + (link["part"] or "")


def type_id(name: str) -> str:
    """kb's id of the type a user names by its name alone."""
    return to_kb(f"{TYPE_OF_TYPES}/{name}")


def type_name(kb_id: str) -> str:
    """The name alone of the type kb's id names."""
    return from_kb(kb_id).partition("/")[2]


def is_type_of_types(kb_id: str) -> bool:
    """Whether kb's id names the type of types itself."""
    return kb_id == type_id(TYPE_OF_TYPES)


def shown_kind(message: kb_pb2.Artifact | kb_pb2.Stub | kb_pb2.InboundCount) -> str:
    """The kind of an answer's artifact, stub or inbound count, as the user names it."""
    return message.kind


def version_of(message: kb_pb2.Artifact | kb_pb2.Entry | kb_pb2.Stale) -> int:
    """The version of its type an answer's artifact, history entry or stale row was checked against."""
    return message.schema_version


def versioned(message: kb_pb2.Artifact | kb_pb2.Entry | kb_pb2.Stale) -> dict:
    """An answer's version of its type under the name the user reads it by."""
    return {"schema_version": version_of(message)}
