"""Furnishing the shop's knowledge base, what `init` does: finding one from where the user works, telling whether it is empty, furnishing
it with the shop's types through bootstrap, or starting one with `kb.init`. One found or named that holds something
other than the shop's types is refused as not empty, naming what it holds; one that holds the shop's types, as
already holding the shop's knowledge. Every refusal is raised as `Refused`, a kb answer's through the caller's
`answered`; nothing here prints."""
from collections.abc import Callable
import os
from pathlib import Path

import kb
from kb.client import connect
from kb.contract import kb_pb2

from shop_knowledge import bootstrap, kb_requests
from shop_knowledge.refusal import Refused

_GONE = "the directory you are working in is gone"
_NOT_EMPTY = "it is not empty"
_ALREADY_HOLDS = "it already holds the shop's knowledge"


def furnished(root: Path | None, signed: kb_pb2.Signature, answered: Callable):
    """bootstrap's Create answers for the knowledge base to furnish: the named root's, or, with none named, the one kb
    finds from the working directory, a kb answer it is found by refused through `answered`. Each Create is made as
    the caller asks for its answer, so the caller refuses the first one kb refuses before the next is made."""
    client = _named(_absolute(root), signed) if root else _found(_absolute(Path(".")), signed, answered)
    return bootstrap.load(client, signed)


def _found(here: Path, signed: kb_pb2.Signature, answered: Callable):
    """The knowledge base kb finds from the working directory, when it is empty; otherwise a store started here. Where
    KB_ROOT is set, even empty, kb's refusal to find one is refused through `answered`, as it gave it: only finding
    nothing, with nothing named, starts a store. One found holding something other than the shop's types is refused
    as not empty, naming what it holds; one KB_ROOT names elsewhere holding the shop's types, as already holding the
    shop's knowledge."""
    listed = (client := connect()).List(kb_requests.init_request())
    named = os.environ.get("KB_ROOT")
    if named is not None:
        answered(listed)
    if _empty(listed):
        return client
    _refuse_unless_furnished(listed, named or "")
    if named is not None and Path(named).resolve() != here.resolve() and _holds_the_shops_types(listed):
        raise Refused([kb_pb2.Fault(artifact=named, message=_ALREADY_HOLDS)])
    _started(here, signed)
    return connect(here)


def _refuse_unless_furnished(listed: kb_pb2.ListResponse, named: str) -> None:
    """Refused, naming the knowledge base as KB_ROOT names it and the kinds of the types it holds besides kb's own,
    where kb found one holding types but not all of the shop's."""
    if listed.WhichOneof("outcome") == "result" and not _holds_the_shops_types(listed):
        said = f"{_NOT_EMPTY}: it holds the types {', '.join(sorted(_kinds(listed)))}"
        raise Refused([kb_pb2.Fault(artifact=named, message=said)])


def _kinds(listed: kb_pb2.ListResponse) -> list[str]:
    """The kinds of the types kb's answer to init's List names, besides kb's own."""
    return [held.removeprefix("schema/") for held in listed.result.ids if held != "schema/schema"]


def _holds_the_shops_types(listed: kb_pb2.ListResponse) -> bool:
    """Whether kb's answer to init's List names every one of the shop's types."""
    return listed.WhichOneof("outcome") == "result" and set(bootstrap.TYPES) <= set(_kinds(listed))


def _named(root: Path, signed: kb_pb2.Signature):
    """A store started at the named root; where kb refuses to start one, the store already there, when it is empty,
    refused in shop-knol's own words, naming the root, when it holds the shop's types or holds something other than
    them, and otherwise refused as kb refused it."""
    try:
        _started(root, signed)
    except Refused as refused:
        listed = connect(root).List(kb_requests.init_request())
        if _holds_the_shops_types(listed):
            raise Refused([kb_pb2.Fault(artifact=str(root), message=_ALREADY_HOLDS)]) from refused
        if not _empty(listed):
            _refuse_unless_furnished(listed, str(root))
            raise
    return connect(root)


def _empty(listed: kb_pb2.ListResponse) -> bool:
    """Whether kb's answer to init's List names no type but kb's own."""
    return listed.WhichOneof("outcome") == "result" and list(listed.result.ids) == ["schema/schema"]


def _started(root: Path, signature: kb_pb2.Signature) -> None:
    """A store started in this process at the root, sent to kb absolute so a refusal it raises quotes a path that
    names the place, not the working directory's own name for it; kb's refusal to start one is refused as any other."""
    try:
        kb.init(str(root.resolve()), signature.role, execution=signature.execution)
    except kb.NotStarted as refusal:
        raise Refused(refusal.faults) from refusal


def _absolute(root: Path) -> Path:
    """The root to start in, a relative one taken from the working directory, which is refused in shop-knol's own
    words if it is gone, before kb is called."""
    try:
        return root.absolute()
    except FileNotFoundError as error:
        raise Refused([kb_pb2.Fault(message=_GONE)]) from error
