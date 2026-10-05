"""The file a user gives: read the way kb reads content, checked against its shape and against what kb can keep, or
refused as a fault on it."""
import sys
from pathlib import Path

from kb.content import NotCanonical, dumps, loads
from kb.contract import kb_pb2

from shop_knowledge import shape
from shop_knowledge.refusal import Refused


def named(source: str) -> str:
    """What a fault on the file the user gave calls it: the path, or standard input for `-`."""
    return "standard input" if source == "-" else source


def read(source: str, shape_name: str) -> dict:
    """A file the user gave, or the text piped in for `-`, read the way kb reads content and checked against its
    shape and against kb's writing of content, or refused as a fault on it."""
    name = named(source)
    try:
        document = loads(sys.stdin.read() if source == "-" else Path(source).read_text())
    except UnicodeDecodeError as fault:
        message = f"it is not text that can be read: {fault}"
        raise Refused([kb_pb2.Fault(artifact=name, rule="content", message=message)])
    except NotCanonical as fault:
        raise Refused([kb_pb2.Fault(artifact=name, place=fault.path, rule="content", message=str(fault))])
    if faults := shape.violations(document, shape_name, name):
        raise Refused(faults)
    _kept(document, name)
    return document


def _kept(document: dict, name: str) -> None:
    """Refused, as kb's writing of content refuses it, if kb cannot keep the document as written, at the place in the
    file where it cannot."""
    try:
        dumps(document)
    except NotCanonical as fault:
        place = fault.path or _unkept_at(document)
        raise Refused([kb_pb2.Fault(artifact=name, place=place, rule="content", message=str(fault))])


def _unkept_at(node, place: str = "") -> str:
    """The place of the deepest value kb's writing refuses, found by asking it of each entry alone in turn, a list's
    item as `{index: item}` since kb writes a mapping: the document knows nothing of which values kb holds to which
    rule. It assumes a refusal is local: looked for in the smallest fragment that still shows it, and where no entry
    alone shows it, the place is the nearest enclosing one that does."""
    entries = node.items() if isinstance(node, dict) else enumerate(node) if isinstance(node, list) else ()
    for key, value in entries:
        if not _keeps({str(key): value}):
            return _unkept_at(value, f"{place}/{key}" if place else str(key))
    return place


def _keeps(node) -> bool:
    try:
        dumps(node)
    except NotCanonical:
        return False
    return True
