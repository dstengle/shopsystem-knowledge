"""Starting the shop's knowledge base: finding one from where the user works, telling whether it is empty, furnishing
it with the shop's types through bootstrap, or starting one with `kb.init`. Every refusal is raised as `Refused`;
nothing here prints."""
from pathlib import Path

import kb
from kb.client import connect
from kb.contract import kb_pb2

from shop_knowledge import bootstrap, kb_requests
from shop_knowledge.refusal import Refused

_GONE = "the directory you are working in is gone"


def furnished(root: Path | None, signed: kb_pb2.Signature):
    """bootstrap's Create answers for the knowledge base to furnish: the named root's, or, with none named, the one kb
    finds from the working directory. Each Create is made as the caller asks for its answer, so the caller refuses
    the first one kb refuses before the next is made."""
    client = _named(_absolute(root), signed) if root else _found(_absolute(Path(".")), signed)
    return bootstrap.load(client, signed)


def _found(here: Path, signed: kb_pb2.Signature):
    """The knowledge base kb finds from the working directory, when it is empty; otherwise a store started here."""
    if _empty(client := connect()):
        return client
    _started(here, signed)
    return connect(here)


def _named(root: Path, signed: kb_pb2.Signature):
    """A store started at the named root; where kb refuses to start one, the store already there, when it is empty."""
    try:
        _started(root, signed)
    except Refused:
        if not _empty(connect(root)):
            raise
    return connect(root)


def _empty(client) -> bool:
    """Whether the knowledge base the client reaches holds no type but kb's own."""
    listed = client.List(kb_requests.init_request())
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
