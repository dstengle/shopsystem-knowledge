"""The seam between the names a user gives and reads and the fields kb's requests and answers carry: a user's name as
kb is sent it and kb's id back as the user's name, in a request's fields and inside content; every request field that
names a kind or the type of types; the fields a Create or a batch create item carries besides its title, content and
signature; an answer's kind and version as the user sees them; and whether an id names one of the types. On kb.v2 a
user's `<kind>/<name>` is the IRI `https://missingmass.io/shopsystem/<kind>/missingmass.io/shopsystem/shop-knowledge/
<name>`, a type `schema/<name>` is `https://missingmass.io/shopsystem/<name>`, and the type of types, `schema/schema`,
is kb's own `https://missingmass.io/kb/type`. It knows the shop's types by name, from bootstrap, and never a type's
fields but the version every type carries."""
import re

from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge import bootstrap

TYPE_OF_TYPES = "schema"
"""The kind a user names the types by: a type is `schema/<name>`."""

_BASE = "https://missingmass.io/shopsystem/"
"""The IRI every one of the shop's types is named under, and so every artifact of one."""

_PLACE = "missingmass.io/shopsystem/shop-knowledge/"
"""The path below its type that every artifact the shop records is named under."""

_TYPE_OF_TYPES_IRI = "https://missingmass.io/kb/type"
"""kb's own type that describes types."""

_LINK = re.compile(r"(?P<name>(?P<kind>[^\s/#]+)/[^\s/#]+)(?P<part>#\S+)?")
"""A whole string naming an artifact, `<kind>/<name>`, or a part of one, `<kind>/<name>#<place>`."""

_KEYED = re.compile(r"@(?P<key>[^\s#]+)(?P<part>#\S+)?")
"""A whole string in a batch naming what another create of the set makes, by its key, `@<key>`, or a part of it."""


def to_kb(name: str) -> str:
    """A user's `<kind>/<name>`, or a part of one after `#`, as kb is sent it; anything else as it is."""
    whole, hashed, part = name.partition("#")
    kind, slash, rest = whole.partition("/")
    if not (kind and slash and rest) or "/" in rest:
        return name
    if kind == TYPE_OF_TYPES:
        iri = _TYPE_OF_TYPES_IRI if rest == TYPE_OF_TYPES else _BASE + rest
    else:
        iri = f"{_BASE}{kind}/{_PLACE}{rest}"
    return iri + hashed + part


def from_kb(kb_id: str) -> str:
    """kb's id of an artifact, or of a part of one, as the user's `<kind>/<name>`; anything else a fault names, a
    file, as it is."""
    whole, hashed, part = kb_id.partition("#")
    if whole == _TYPE_OF_TYPES_IRI:
        return f"{TYPE_OF_TYPES}/{TYPE_OF_TYPES}" + hashed + part
    if not whole.startswith(_BASE):
        return kb_id
    kind, slash, rest = whole[len(_BASE):].partition("/")
    if not slash:
        return f"{TYPE_OF_TYPES}/{kind}" + hashed + part
    if not rest.startswith(_PLACE):
        return kb_id
    return f"{kind}/{rest[len(_PLACE):]}" + hashed + part


def of_kind(kind: str) -> dict:
    """The fields of a List, Follow or Search that keep it to the kind a user names (every kind, given empty)."""
    return {"kind": _kind(kind)}


def of_types() -> dict:
    """The fields of a List that keep it to the types."""
    return of_kind(TYPE_OF_TYPES)


def ids_request(kind: str, fields: dict[str, str] | None = None) -> kb_pb2.ListRequest:
    """A List of the ids of the artifacts of the kind a user names, those whose fields hold the names given."""
    return kb_pb2.ListRequest(**of_kind(kind), fields=fields_to_kb(fields or {}), form=kb_pb2.ListRequest.IDS)


def fields_to_kb(fields: dict[str, str]) -> dict[str, str]:
    """A List's field values as kb is sent them: a value naming one of the shop's artifacts or types, or a part of
    one, as kb's id for it, as content is sent; any other value as it is."""
    return {key: _to_kb_linked(value) for key, value in fields.items()}


def listed_ids(response: kb_pb2.ListResponse) -> list[str]:
    """The ids a List answered with, as the user's names."""
    return [from_kb(each) for each in response.result.ids]


def holds_type(client, name: str) -> bool:
    """Whether the store holds the type a user names by its name alone, by kb's answer naming the types it holds."""
    return type_id(name) in {to_kb(each) for each in listed_ids(client.List(ids_request(TYPE_OF_TYPES)))}


def create_fields(client, kind: str, title: str, name: str = "") -> dict:
    """The fields of a CreateRequest besides title, content and signature, for an artifact of the kind, with the
    title it is given and the name, where the user or the shop gives one, or else the name its title makes: its IRI,
    and the version of its type it conforms to, the type's current one, read through the client."""
    return {"id": to_kb(f"{kind}/{name or _slug(title)}"), "type": _current(client, kind)}


def created_items(client, creates: list[tuple[str, str, str, dict]]) -> list[tuple[dict, dict]]:
    """For each create of a batch, given as its kind, its key (empty where it has none), its title and its content:
    the CreateItem's fields besides title and content, and the content as kb is sent it, every link written
    `@<key>` naming the IRI the create carrying that key is given (batch.py has refused a key two creates carry);
    a key no create carries is sent as written, for kb to refuse."""
    fields = [create_fields(client, kind, title) for kind, _, title, _ in creates]
    keys = [key for _, key, _, _ in creates]
    keyed = {key: made["id"] for key, made in zip(keys, fields) if key}
    return [
        (made, _each_string(content_to_kb(content), lambda value: _resolved(value, keyed)))
        for made, (_, _, _, content) in zip(fields, creates)
    ]


def _resolved(value: str, keyed: dict[str, str]) -> str:
    """A link written `@<key>`, or into a part of what that key names, as the IRI the key's create is given; any
    other string, and a key no create carries, as it is."""
    link = _KEYED.fullmatch(value)
    if link is None or link["key"] not in keyed:
        return value
    return keyed[link["key"]] + (link["part"] or "")


def _slug(title: str) -> str:
    """The name a title makes: lowercased, each run of anything but letters and digits one hyphen, none at either
    end."""
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _current(client, kind: str) -> str:
    """The IRI of the version a type stands at now, by kb's answer to reading the type whole; a type kb does not
    give is named at its first version, for kb to refuse."""
    read = client.Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=_kind(kind)), whole=kb_pb2.ReadRequest.Whole()))
    held = loads(read.result.content) if read.WhichOneof("outcome") == "result" else None
    version = held.get("version", 1) if isinstance(held, dict) else 1
    return f"{_kind(kind)}@{version}"


def _kind(kind: str) -> str:
    """The kind a user names, as kb's request fields name it: its type's IRI (every kind, given empty)."""
    return type_id(kind) if kind else ""


def content_of(artifact: kb_pb2.Artifact):
    """An artifact's content as the user reads it."""
    return content_from_kb(loads(artifact.content))


def content_to_kb(content):
    """Content as kb is sent it: every whole string, at any depth, naming one of the shop's artifacts or types, or a
    part of one, as kb's id for it."""
    return _each_string(content, _to_kb_linked)


def content_from_kb(content):
    """Content as kb gave it, as the user reads it: every whole string, at any depth, that is kb's id of one of the
    shop's artifacts or types, or of a part of one, as the user's name for it."""
    return _each_string(content, from_kb)


def _each_string(value, change):
    """The value with every string in it, at any depth, changed; keys and other values as they are."""
    if isinstance(value, dict):
        return {key: _each_string(item, change) for key, item in value.items()}
    if isinstance(value, list):
        return [_each_string(item, change) for item in value]
    return change(value) if isinstance(value, str) else value


def _to_kb_linked(value: str) -> str:
    """The string as kb's id, its place inside kept, where it names one of the shop's artifacts or types, or a part
    of one; any other string as it is."""
    link = _LINK.fullmatch(value)
    if link is None or link["kind"] not in (*bootstrap.SHOP_TYPES, TYPE_OF_TYPES):
        return value
    return to_kb(value)


def type_id(name: str) -> str:
    """kb's id of the type a user names by its name alone."""
    return to_kb(f"{TYPE_OF_TYPES}/{name}")


def type_name(kb_id: str) -> str:
    """The name alone of the type kb's id names: the last segment of its IRI, the type of types' `schema`."""
    return TYPE_OF_TYPES if is_type_of_types(kb_id) else kb_id.rstrip("/").rpartition("/")[2]


def is_type_of_types(kb_id: str) -> bool:
    """Whether kb's id names the type of types itself."""
    return kb_id == _TYPE_OF_TYPES_IRI


def shown_kind(message: kb_pb2.Artifact | kb_pb2.Stub | kb_pb2.InboundCount) -> str:
    """The kind of an answer's artifact, stub or inbound count, as the user names it: the name of the type its
    version IRI, or an inbound count's type IRI, names; empty where kb names none."""
    named = message.kind if isinstance(message, kb_pb2.InboundCount) else message.type
    return type_name(named.partition("@")[0]) if named else ""


def version_of(message: kb_pb2.Artifact | kb_pb2.Entry | kb_pb2.Stale) -> int:
    """The version of its type an answer's artifact, history entry or stale row was checked against: a stale row's
    number, or the number after `@` in the version IRI an artifact or entry names."""
    if isinstance(message, kb_pb2.Stale):
        return message.schema_version
    number = message.type.rpartition("@")[2]
    return int(number) if number.isdigit() else 0


def versioned(message: kb_pb2.Artifact | kb_pb2.Entry | kb_pb2.Stale) -> dict:
    """An answer's version of its type under the name the user reads it by."""
    return {"schema_version": version_of(message)}
