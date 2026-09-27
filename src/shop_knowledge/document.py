"""The file a user gives: read the way kb reads content, checked against its shape, or refused as a fault on it."""
import sys
from pathlib import Path

from kb import canonical
from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge import shape
from shop_knowledge.refusal import Refused


def read(source: str, shape_name: str) -> dict:
    """A file the user gave, or the text piped in for `-`, read the way kb reads content and checked against its
    shape, or refused as a fault on it."""
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
    return document
