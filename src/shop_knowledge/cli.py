"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting.

Every file it reads and everything it prints is YAML 1.2, read and written by kb's own reading and writing of content.
A refusal, kb's or its own, is printed in plain words on stderr, one fault a line, with a non-zero exit; never a traceback.
"""
import json
import os
import sys
from pathlib import Path

from kb import canonical, client as kb_client
from kb.content import dumps, loads, text
from kb.contract import kb_pb2

from shop_knowledge import answers, arguments, batch, bootstrap, shape
from shop_knowledge.renderers import RENDERERS


class Refused(Exception):
    """A refusal on its way to the one printer: the faults to print, one line each."""

    def __init__(self, faults):
        super().__init__(faults)
        self.faults = list(faults)


def main(argv=None) -> int:
    args = arguments.command_parser().parse_args(argv)
    try:
        return _run(args)
    except Refused as refusal:
        return _refuse(refusal.faults)


def _run(args) -> int:
    """The command's handler, with the operating system's refusal of a path made a fault that names it."""
    try:
        args.by = _by(args) if args.command in _MUTATING else {}
        return _HANDLERS[args.command](args)
    except OSError as error:
        raise Refused([kb_pb2.Fault(artifact=str(error.filename or ""), message=error.strerror or str(error))]) from error


_MUTATING = ("init", "create", "write", "apply")
_NO_ROLE = "every change must say which role made it, through KB_ACTOR as role or role:execution"
_NO_MESSAGE = "every change must carry a message, given with -m"


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


def _list(args) -> int:
    fields = dict(where.partition("=")[::2] for where in args.where)
    form = kb_pb2.ListRequest.IDS if args.ids else kb_pb2.ListRequest.STUBS
    response = _answered(_client().List(kb_pb2.ListRequest(type=args.type, fields=fields, form=form)))
    _show((answers.names if args.ids else answers.listed)(response))
    return 0


def _refs(args) -> int:
    direction = kb_pb2.RefsRequest.IN if args.inbound else kb_pb2.RefsRequest.OUT
    response = _answered(_client().Refs(kb_pb2.RefsRequest(
        locator=_locator(args.locator), depth=1 if args.depth is None else args.depth, direction=direction,
        via=args.via or "", type=args.type or "",
    )))
    _show(answers.reached(response))
    return 0


def _search(args) -> int:
    scope = getattr(kb_pb2.SearchRequest, args.scope.upper())
    response = _answered(_client().Search(kb_pb2.SearchRequest(text=args.text, type=args.type or "", scope=scope)))
    _show(answers.matched(response))
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


_HANDLERS = {
    "init": _init,
    "create": _create,
    "read": _read,
    "write": _write_artifact,
    "validate": _validate,
    "apply": _apply,
    "journal": _journal,
    "list": _list,
    "refs": _refs,
    "search": _search,
    "render": _render,
}
