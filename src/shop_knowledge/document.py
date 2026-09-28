"""The file a user gives: read the way kb reads content, checked against its shape and against what kb can keep, or
refused as a fault on it."""
import sys
from pathlib import Path

from kb import canonical
from kb.content import dumps, loads
from kb.contract import kb_pb2

from shop_knowledge import shape
from shop_knowledge.refusal import Refused


def read(source: str, shape_name: str) -> dict:
    """A file the user gave, or the text piped in for `-`, read the way kb reads content and checked against its
    shape and against kb's writing of content, or refused as a fault on it."""
    name = "standard input" if source == "-" else source
    try:
        document = loads(sys.stdin.read() if source == "-" else Path(source).read_text())
    except UnicodeDecodeError as fault:
        message = f"it is not text that can be read: {fault}"
        raise Refused([kb_pb2.Fault(artifact=name, rule="content", message=message)])
    except canonical.NotCanonical as fault:
        raise Refused([kb_pb2.Fault(artifact=name, path=fault.path, rule="content", message=str(fault))])
    if faults := shape.violations(document, shape_name, name):
        raise Refused(faults)
    _kept(document, name)
    return document


def _kept(document: dict, name: str) -> None:
    """Refused, as kb's writing of content refuses it, if kb cannot keep the document as written, at the place in the
    file where it cannot."""
    try:
        dumps(document)
    except canonical.NotCanonical as fault:
        place = fault.path or _unkept_at(document)
        raise Refused([kb_pb2.Fault(artifact=name, path=place, rule="content", message=str(fault))])


def _unkept_at(node, place: str = "") -> str:
    """The place of the deepest value kb's writing refuses, found by asking it of each entry alone in turn: the
    document knows nothing of which values kb holds to which rule."""
    entries = node.items() if isinstance(node, dict) else enumerate(node) if isinstance(node, list) else ()
    for key, value in entries:
        if not _keeps({key: value} if isinstance(node, dict) else [value]):
            return _unkept_at(value, f"{place}/{key}" if place else str(key))
    return place


def _keeps(node) -> bool:
    try:
        dumps(node)
    except canonical.NotCanonical:
        return False
    return True
