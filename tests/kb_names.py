"""The test seam: every name a test hands kb directly, and every name it reads back from a kb message. On kb.v2 a
user's `<kind>/<name>` is the IRI `https://missingmass.io/shopsystem/<kind>/missingmass.io/shopsystem/shop-knowledge/
<name>`, a type `schema/<name>` is `https://missingmass.io/shopsystem/<name>`, the type of types is kb's own
`https://missingmass.io/kb/type`, and a create is named by the name its title makes, at its type's first version. It
mirrors the roles of the production seam but never imports it (CLAUDE.md rule 1): it spells kb's forms itself.
Imported plainly, never star-imported."""
import re

from kb.content import dumps, loads
from kb.contract import kb_pb2

_BASE = "https://missingmass.io/shopsystem/"
_PLACE = "missingmass.io/shopsystem/shop-knowledge/"
_TYPE_OF_TYPES = "https://missingmass.io/kb/type"
_NAME = re.compile(r"(?P<kind>[a-z][a-z-]*)/(?P<name>[^\s/#]+)(?P<part>#\S+)?")
"""A whole string naming an artifact or a type, `<kind>/<name>`, or a part of one."""


def iri(name: str) -> str:
    """A user's `<kind>/<name>` (or a part of one) as kb names it; anything else as it is."""
    named = _NAME.fullmatch(name)
    if named is None:
        return name
    kind, slug, part = named["kind"], named["name"], named["part"] or ""
    if kind == "schema":
        return (_TYPE_OF_TYPES if slug == "schema" else _BASE + slug) + part
    return f"{_BASE}{kind}/{_PLACE}{slug}{part}"


def kind_name(kind: str) -> str:
    """A kind a user names, as kb's request fields name it: its type's IRI."""
    return iri(f"schema/{kind}")


def _created(kind: str, title: str, content: str) -> dict:
    """The fields of a create of the kind a user names: its IRI from the name its title makes, its type's first
    version, and the content with every name in it as kb names it."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return {"id": iri(f"{kind}/{slug}"), "type": f"{kind_name(kind)}@1", "title": title, "content": _content(content)}


def _content(text: str) -> str:
    """Content written as text, with every whole string naming an artifact or a type as kb names it."""
    def renamed(value):
        if isinstance(value, dict):
            return {key: renamed(item) for key, item in value.items()}
        if isinstance(value, list):
            return [renamed(item) for item in value]
        return iri(value) if isinstance(value, str) else value
    return dumps(renamed(loads(text)))


def create_request(kind: str, title: str, content: str, signature: kb_pb2.Signature) -> kb_pb2.CreateRequest:
    """A Create of an artifact of the kind a user names, with the content already written as text."""
    return kb_pb2.CreateRequest(**_created(kind, title, content), signature=signature)


def artifact_id(answer) -> str:
    """The name kb gave the artifact, from the answer to a Create, as the user is shown it."""
    return artifact_name(answer.result.id)


def artifact_name(kb_id: str) -> str:
    """kb's id (or any artifact a fault names) as the user is shown it: `<kind>/<name>`, a type `schema/<name>`."""
    whole, hashed, part = kb_id.partition("#")
    if whole == _TYPE_OF_TYPES:
        return "schema/schema" + hashed + part
    if not whole.startswith(_BASE):
        return kb_id
    kind, slash, rest = whole[len(_BASE):].partition("/")
    if not slash:
        return f"schema/{kind}" + hashed + part
    return (f"{kind}/{rest[len(_PLACE):]}" if rest.startswith(_PLACE) else whole) + hashed + part


def create_item(kind: str, title: str, content: str, key: str = "") -> kb_pb2.CreateItem:
    """One item of a BatchCreate, of the kind a user names. kb.v2 carries no key: a link written `@<key>` that names
    no one create of the set is sent as written, which is the only form these items are compared in."""
    return kb_pb2.CreateItem(**_created(kind, title, content))


def list_of_types() -> kb_pb2.ListRequest:
    """The names of the types a knowledge base holds: the call shop-knol's own init makes to see what is there."""
    return kb_pb2.ListRequest(kind=_TYPE_OF_TYPES, form=kb_pb2.ListRequest.IDS)


def read_whole_request(artifact: str) -> kb_pb2.ReadRequest:
    """A Read of the artifact a user names, whole, with no depth."""
    return kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=iri(artifact)), whole=kb_pb2.ReadRequest.Whole(depth=0))


def read_request(artifact: str) -> kb_pb2.ReadRequest:
    """A Read of the artifact a user names, as the stand-in is asked for it."""
    return kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=iri(artifact)))


def remove_request(artifact: str, signature: kb_pb2.Signature) -> kb_pb2.RemoveRequest:
    """A Remove of the artifact a user names."""
    return kb_pb2.RemoveRequest(locator=kb_pb2.Locator(id=iri(artifact)), signature=signature)


def check_request() -> kb_pb2.CheckRequest:
    """A Check of the whole knowledge base."""
    return kb_pb2.CheckRequest()


def history_request(batch: str = "") -> kb_pb2.HistoryRequest:
    """A History of the whole knowledge base, or of one batch's changes: the guard's question of whether a store is there."""
    return kb_pb2.HistoryRequest(batch=batch) if batch else kb_pb2.HistoryRequest()


def stand_in_read_refusal(artifact: str, faults: list) -> dict:
    """The stand-in's entry for a Read of the artifact a user names, refused with the faults a step wrote."""
    return {"call": "Read", "asking": {"locator": {"id": iri(artifact)}}, "answer": {"refusal": {"faults": faults}}}


def stand_in_check(violations: list) -> dict:
    """The stand-in's entry for a Check that finds the violations a step wrote, the rest of the answer kb's own."""
    return {"call": "Check", "answer": {"result": {"violations": violations}}, "from_kb": ["stale", "violations"]}
