"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting.

Every file it reads and everything it prints is YAML 1.2, read and written by kb's own reading and writing of content.
A refusal, kb's or its own, is printed in plain words on stderr, one fault a line, with a non-zero exit; never a traceback.
"""
import argparse
import os
import sys
from pathlib import Path

from kb import canonical, client as kb_client
from kb.content import dumps, loads, text
from kb.contract import kb_pb2

from shop_knowledge import batch, bootstrap


class Refused(Exception):
    """A refusal on its way to the one printer: the faults to print, one line each."""

    def __init__(self, faults):
        super().__init__(faults)
        self.faults = list(faults)


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        return args.handler(args)
    except Refused as refusal:
        return _refuse(refusal.faults)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shop-knol")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="start a shop knowledge base at <root>/kb/ with the shop's types")
    init.add_argument("root")
    init.set_defaults(handler=_init)

    create = commands.add_parser("create", help="record an artifact from a YAML file; prints the id kb chose")
    create.add_argument("type")
    create.add_argument("--from", dest="source", required=True, metavar="FILE")
    create.add_argument("-m", dest="message", required=True, help="why")
    create.set_defaults(handler=_create)

    read = commands.add_parser("read", help="read an artifact at a glance")
    read.add_argument("locator")
    read.set_defaults(handler=_read)

    validate = commands.add_parser(
        "validate", help="check everything the shop knows; lists every fault, exits non-zero if any",
    )
    validate.set_defaults(handler=_validate)

    apply = commands.add_parser("apply", help="make every change in a batch file as one change; prints the set's name")
    apply.add_argument("--from", dest="source", required=True, metavar="FILE")
    apply.add_argument("-m", dest="message", required=True, help="why")
    apply.set_defaults(handler=_apply)

    journal = commands.add_parser("journal", help="review who changed what: every change, oldest first")
    journal.add_argument("--artifact", default="", help="only the changes to this one")
    journal.set_defaults(handler=_journal)
    return parser


def _actor() -> kb_pb2.Actor:
    """KB_ACTOR is the role, or the role and the piece of work it acts for as role:execution."""
    role, _, execution = os.environ["KB_ACTOR"].partition(":")
    return kb_pb2.Actor(role=role, execution=execution)


def _client():
    return kb_client.connect(Path(os.environ["KB_ROOT"]))


def _show(document: dict) -> None:
    print(dumps(document), end="")


def _plain(fault: kb_pb2.Fault) -> str:
    """One fault as a line a person reads: where, then what is wrong."""
    where = f"{fault.artifact} at {fault.path}" if fault.path else fault.artifact
    return f"{where}: {fault.message}"


def _refuse(faults) -> int:
    for fault in faults:
        print(_plain(fault), file=sys.stderr)
    return 1


def _answered(response):
    """kb's answer, or the refusal it carries: every kb answer's faults are refused this one way."""
    if response.faults:
        raise Refused(response.faults)
    return response


def _init(args) -> int:
    root = Path(args.root)
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root), actor=_actor()))
    bootstrap.load(client, _actor())
    return 0


def _document(source: str) -> dict:
    """A file the user gave, read the way kb reads content, or refused with the place kb could not read it at."""
    try:
        return loads(Path(source).read_text())
    except canonical.NotCanonical as fault:
        raise Refused([kb_pb2.Fault(artifact=source, path=fault.path, rule="content", message=str(fault))])


def _create(args) -> int:
    content = _document(args.source)
    title = text(content.pop("title", None))
    response = _answered(_client().Create(kb_pb2.CreateRequest(
        type=args.type, title=title, content=dumps(content), actor=_actor(), message=args.message,
    )))
    _show({"id": response.id, "revision": response.revision})
    return 0


def _read(args) -> int:
    response = _answered(_client().Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=args.locator))))
    _show(_glance(response))
    return 0


def _glance(response: kb_pb2.ReadResponse) -> dict:
    """A summary read as the user is shown it: identity, the fields the type shows, stubs, parts and inbound counts."""
    return {
        "id": response.id,
        "type": response.type,
        "schema_version": response.schema_version,
        "revision": response.revision,
        "title": response.title,
        **loads(response.content),
        "references": [
            {"field": stub.field, "id": stub.id, "type": stub.type, "title": stub.title, **loads(stub.fields)}
            for stub in response.references
        ],
        "parts": [{"collection": stub.collection, "id": stub.id, "title": stub.title} for stub in response.parts],
        "inbound": [{"type": count.type, "field": count.field, "count": count.count} for count in response.inbound],
    }


def _validate(args) -> int:
    """kb's check answers with the store's faults and violations alike; any of either is a refusal."""
    response = _client().Validate(kb_pb2.ValidateRequest())
    if response.faults or response.violations:
        raise Refused([*response.faults, *response.violations])
    return 0


def _apply(args) -> int:
    operations = batch.operations(_document(args.source))
    response = _answered(_client().Apply(kb_pb2.ApplyRequest(
        operations=operations, actor=_actor(), message=args.message,
    )))
    _show({
        "batch": response.batch,
        "results": [{"id": result.id, "revision": result.revision} for result in response.results],
    })
    return 0


def _journal(args) -> int:
    response = _answered(_client().Journal(kb_pb2.JournalRequest(artifact=args.artifact)))
    _show({"changes": [_change(entry) for entry in response.entries]})
    return 0


def _change(entry: kb_pb2.Entry) -> dict:
    """One entry of the history as the user is shown it: when, who and for what piece of work, what it did, and why."""
    return {
        "at": entry.at,
        "actor": {"role": entry.actor.role, "execution": entry.actor.execution},
        "op": entry.op,
        "artifact": entry.artifact,
        "revision": entry.revision,
        "message": entry.message,
    }
