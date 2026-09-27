"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting.

Every file it reads and everything it prints is YAML 1.2, read and written by kb's own reading and writing of content.
A refusal, kb's or its own, is printed in plain words on stderr, one fault a line, with a non-zero exit; never a traceback.
"""
import argparse
import json
import os
import sys
from pathlib import Path

from kb import canonical, client as kb_client
from kb.content import dumps, loads, text
from kb.contract import kb_pb2

from shop_knowledge import answers, batch, bootstrap, shape
from shop_knowledge.renderers import RENDERERS


class Refused(Exception):
    """A refusal on its way to the one printer: the faults to print, one line each."""

    def __init__(self, faults):
        super().__init__(faults)
        self.faults = list(faults)


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        return _run(args)
    except Refused as refusal:
        return _refuse(refusal.faults)


def _run(args) -> int:
    """The command's handler, with the operating system's refusal of a path made a fault that names it."""
    try:
        args.by = _by(args) if args.command in _MUTATING else {}
        return args.handler(args)
    except OSError as error:
        raise Refused([kb_pb2.Fault(artifact=str(error.filename or ""), message=error.strerror or str(error))]) from error


_MUTATING = ("init", "create", "write", "apply")
_NO_ROLE = "every change must say which role made it, through KB_ACTOR as role or role:execution"
_NO_MESSAGE = "every change must carry a message, given with -m"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shop-knol")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="start a shop knowledge base at <root>/kb/ with the shop's types")
    init.add_argument("root")
    init.set_defaults(handler=_init)

    create = commands.add_parser("create", help="record an artifact from a YAML file; prints the id kb chose")
    create.add_argument("type")
    create.add_argument("--from", dest="source", required=True, metavar="FILE")
    create.add_argument("-m", dest="message", help="why")
    create.set_defaults(handler=_create)

    read = commands.add_parser("read", help="read an artifact at a glance")
    read.add_argument("locator")
    read.add_argument("--json", action="store_true", help="the same answer written as JSON")
    read.add_argument("--section", metavar="TITLE", help="only the section with this title")
    read.add_argument("--whole", action="store_true", help="every field and section, links as names")
    read.add_argument(
        "--resolve", nargs="?", const=1, type=int, metavar="DEPTH",
        help="a whole read with links filled in, DEPTH steps (one when not said)",
    )
    read.set_defaults(handler=_read)

    write = commands.add_parser("write", help="replace an artifact, or a part of it as <name>#<place>, from a YAML file")
    write.add_argument("locator")
    write.add_argument("--from", dest="source", required=True, metavar="FILE")
    write.add_argument("-m", dest="message", help="why")
    write.set_defaults(handler=_write_artifact)

    validate = commands.add_parser(
        "validate", help="check everything the shop knows; lists every fault, exits non-zero if any",
    )
    validate.set_defaults(handler=_validate)

    apply = commands.add_parser("apply", help="make every change in a batch file as one change; prints the set's name")
    apply.add_argument("--from", dest="source", required=True, metavar="FILE")
    apply.add_argument("-m", dest="message", help="why")
    apply.set_defaults(handler=_apply)

    journal = commands.add_parser("journal", help="review who changed what: every change, oldest first")
    journal.add_argument("--artifact", default="", help="only the changes to this one")
    journal.set_defaults(handler=_journal)

    render = commands.add_parser("render", help="publish an artifact into a directory; the shop is only read")
    render.add_argument("renderer", choices=sorted(RENDERERS))
    render.add_argument("locator")
    render.add_argument("--to", required=True, metavar="DIR")
    render.set_defaults(handler=_render)
    return parser


def _by(args) -> dict:
    """Who made a change and why, as request fields, or a refusal per lack, before any file is read; init gives no why."""
    role, _, execution = os.environ.get("KB_ACTOR", "").partition(":")
    message = getattr(args, "message", "-")
    lacking = [("actor", _NO_ROLE)] * (not role) + [("message", _NO_MESSAGE)] * (not message)
    if lacking:
        raise Refused([kb_pb2.Fault(rule=rule, message=said) for rule, said in lacking])
    return {"actor": kb_pb2.Actor(role=role, execution=execution), "message": message}


def _client():
    """kb finds the store: upward from the working directory, or through KB_ROOT."""
    return kb_client.connect()


def _show(document: dict, as_json: bool = False) -> None:
    """An answer as YAML, or as the same document in JSON when asked."""
    if as_json:
        print(json.dumps(document, indent=2, ensure_ascii=False))
    else:
        print(dumps(document), end="")


def _plain(fault: kb_pb2.Fault) -> str:
    """One fault as a line a person reads: where, then what is wrong."""
    message = " ".join(line.strip() for line in fault.message.splitlines())
    where = f"{fault.artifact} at {fault.path}" if fault.path else fault.artifact
    return f"{where}: {message}" if where else message


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
    client.Init(kb_pb2.InitRequest(root=str(root), actor=args.by["actor"]))
    bootstrap.load(client, args.by["actor"])
    return 0


def _document(source: str, shape_name: str) -> dict:
    """A file the user gave, read the way kb reads content and checked against its shape, or refused as a fault on it."""
    try:
        document = loads(Path(source).read_text())
    except UnicodeDecodeError as fault:
        message = f"it is not text that can be read: {fault}"
        raise Refused([kb_pb2.Fault(artifact=source, rule="content", message=message)])
    except canonical.NotCanonical as fault:
        raise Refused([kb_pb2.Fault(artifact=source, path=fault.path, rule="content", message=str(fault))])
    if faults := shape.violations(document, shape_name, source):
        raise Refused(faults)
    return document


def _create(args) -> int:
    content = _document(args.source, "content")
    title = text(content.pop("title", None))
    response = _answered(_client().Create(kb_pb2.CreateRequest(
        type=args.type, title=title, content=dumps(content), **args.by,
    )))
    _show(answers.created(response))
    return 0


def _locator(words: str) -> kb_pb2.Locator:
    """A locator as the user says it: a name, or a name and after # a place inside it."""
    name, _, place = words.partition("#")
    return kb_pb2.Locator(id=name, path=place)


def _write_artifact(args) -> int:
    locator = _locator(args.locator)
    response = _answered(_client().Write(kb_pb2.WriteRequest(
        locator=locator, content=dumps(_document(args.source, "content")), **args.by,
    )))
    _show(answers.written_over(locator, response))
    return 0


def _is_whole(args) -> bool:
    """--resolve implies a whole read, since kb fills links in only on a whole read."""
    return args.whole or args.resolve is not None


def _read_request(args) -> kb_pb2.ReadRequest:
    """The level and depth a read asks for: a section, or a whole (filled in when --resolve), or the summary."""
    locator = kb_pb2.Locator(id=args.locator)
    if args.section:
        return kb_pb2.ReadRequest(locator=locator, level=kb_pb2.ReadRequest.SECTION, section=args.section)
    if _is_whole(args):
        return kb_pb2.ReadRequest(locator=locator, level=kb_pb2.ReadRequest.WHOLE, depth=args.resolve or 0)
    return kb_pb2.ReadRequest(locator=locator)


def _read(args) -> int:
    response = _answered(_client().Read(_read_request(args)))
    shape = answers.section if args.section else answers.whole if _is_whole(args) else answers.glance
    _show(shape(response), args.json)
    return 0


def _validate(args) -> int:
    """kb's check answers with the store's faults and violations alike; any of either is a refusal."""
    response = _client().Validate(kb_pb2.ValidateRequest())
    if response.faults or response.violations:
        raise Refused([*response.faults, *response.violations])
    return 0


def _apply(args) -> int:
    operations = batch.operations(_document(args.source, "batch"))
    response = _answered(_client().Apply(kb_pb2.ApplyRequest(
        operations=operations, **args.by,
    )))
    _show(answers.applied(response))
    return 0


def _journal(args) -> int:
    response = _answered(_client().Journal(kb_pb2.JournalRequest(artifact=args.artifact)))
    _show(answers.history(response))
    return 0


def _render(args) -> int:
    rendered = _answered(RENDERERS[args.renderer](_client(), args.locator))
    _write(rendered.files, Path(args.to))
    _show(answers.written(rendered.files))
    return 0


def _write(files: dict[str, str], directory: Path) -> None:
    """The files a renderer gave back, each written at its path under the directory asked for."""
    for relative, content in files.items():
        path = directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
