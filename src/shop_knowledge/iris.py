"""The seam between the names a user gives and reads and the fields kb's requests and answers carry: a user's name as
kb is sent it and kb's id back as the user's name, every request field that names a kind or the type of types, the
fields a Create or a batch create item carries besides its title, content and signature, an answer's kind and version
as the user sees them, and whether an id names one of the types. On kb.v1 every one is the identity; moving to another
contract changes this module alone."""
from kb.contract import kb_pb2

TYPE_OF_TYPES = "schema"
"""The kind a user names the types by: a type is `schema/<name>`."""


def to_kb(name: str) -> str:
    """A user's `<kind>/<name>` as kb is sent it."""
    return name


def from_kb(kb_id: str) -> str:
    """kb's id of an artifact as the user's `<kind>/<name>`."""
    return kb_id


def of_kind(kind: str) -> dict:
    """The fields of a List, Follow or Search that keep it to the kind a user names (every kind, given empty)."""
    return {"kind": _kind(kind)}


def of_types() -> dict:
    """The fields of a List that keep it to the types."""
    return of_kind(TYPE_OF_TYPES)


def create_fields(kind: str, title: str, name: str = "") -> dict:
    """The fields of a CreateRequest besides title, content and signature, for an artifact of the kind, with the
    title it is given and the name, where the user or the shop gives one."""
    return {"kind": _kind(kind)}


def item_fields(kind: str, key: str, title: str) -> dict:
    """The fields of a batch's CreateItem besides title and content, for an artifact of the kind, with the title it
    is given and the key a link in the batch names it by (empty where it has none)."""
    return {"kind": _kind(kind), "key": key}


def _kind(kind: str) -> str:
    """The kind a user names, as kb's request fields name it."""
    return kind


def type_id(name: str) -> str:
    """kb's id of the type a user names by its name alone."""
    return to_kb(f"{TYPE_OF_TYPES}/{name}")


def type_name(kb_id: str) -> str:
    """The name alone of the type kb's id names."""
    return from_kb(kb_id).partition("/")[2]


def is_type_of_types(kb_id: str) -> bool:
    """Whether kb's id names the type of types itself."""
    return kb_id == type_id(TYPE_OF_TYPES)


def shown_kind(message) -> str:
    """The kind of an answer's artifact, stub, inbound count or history entry, as the user names it."""
    return message.kind


def version_of(message) -> int:
    """The version of its type an answer's artifact, history entry or stale row was checked against."""
    return message.schema_version


def versioned(message: kb_pb2.Artifact | kb_pb2.Stale) -> dict:
    """An answer's version of its type under the name the user reads it by."""
    return {"schema_version": version_of(message)}
