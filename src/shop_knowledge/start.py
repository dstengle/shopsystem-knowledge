"""Starting the shop's knowledge base: finding one from where the user works, telling whether it is empty, furnishing
it with the shop's types through bootstrap, or starting one with `kb.init`. Every refusal is raised as `Refused`;
nothing here prints."""
import os
from pathlib import Path

import kb
from kb.client import connect
from kb.contract import kb_pb2

from shop_knowledge import bootstrap, kb_requests
from shop_knowledge.refusal import Refused

_GONE = "the directory you are working in is gone"
_NOT_EMPTY = "it is not empty"


def furnished(root: Path | None, signed: kb_pb2.Signature):
    """bootstrap's Create answers for the knowledge base to furnish: the named root's, or, with none named, the one kb
    finds from the working directory. Each Create is made as the caller asks for its answer, so the caller refuses
    the first one kb refuses before the next is made."""
    client = _named(_absolute(root), signed) if root else _found(_absolute(Path(".")), signed)
    return bootstrap.load(client, signed)


def _found(here: Path, signed: kb_pb2.Signature):
    """The knowledge base kb finds from the working directory, when it is empty; otherwise a store started here. Where
    KB_ROOT is set, kb's refusal to find one is refused as it gave it: only finding nothing, with nothing named, starts
    a store."""
    listed = (client := connect()).List(kb_requests.init_request())
    if listed.WhichOneof("outcome") == "refusal" and os.environ.get("KB_ROOT"):
        raise Refused(listed.refusal.faults)
    if _empty(listed):
        return client
    _refuse_unless_furnished(listed)
    _started(here, signed)
    return connect(here)


def _refuse_unless_furnished(listed: kb_pb2.ListResponse) -> None:
    """Refused, naming the knowledge base as KB_ROOT names it and the kinds of the types it holds besides kb's own,
    where kb found one holding types but not all of the shop's."""
    if listed.WhichOneof("outcome") != "result":
        return
    kinds = [held.removeprefix("schema/") for held in listed.result.ids if held != "schema/schema"]
    if not set(bootstrap.TYPES) <= set(kinds):
        said = f"{_NOT_EMPTY}: it holds the types {', '.join(sorted(kinds))}"
        raise Refused([kb_pb2.Fault(artifact=os.environ.get("KB_ROOT", ""), message=said)])


def _named(root: Path, signed: kb_pb2.Signature):
    """A store started at the named root; where kb refuses to start one, the store already there, when it is empty."""
    try:
        _started(root, signed)
    except Refused:
        if not _empty(connect(root).List(kb_requests.init_request())):
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
