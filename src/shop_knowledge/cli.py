"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting.

Every file it reads and everything it prints is YAML 1.2, read and written by kb's own reading and writing of content.
A refusal, kb's or its own, is printed in plain words on stderr, one fault a line, with a non-zero exit; never a traceback.
"""
import json
import os
import sys
from pathlib import Path

from kb import canonical, client as kb_client
from kb.content import dumps, loads
from kb.contract import kb_pb2

from shop_knowledge import answers, arguments, bootstrap, kb_requests, shape
from shop_knowledge.renderers import RENDERERS


class Refused(Exception):
    """A refusal on its way to the one printer: the faults to print, one line each."""

    def __init__(self, faults):
        super().__init__(faults)
        self.faults = list(faults)


def main(argv=None) -> int:
    try:
        return _run(_parsed(argv))
    except Refused as refusal:
        return _refuse(refusal.faults)


def _parsed(argv):
    """The arguments the user gave, or a refusal naming the command that could not take them."""
    try:
        return arguments.command_parser().parse_args(argv)
    except arguments.ArgumentRefused as error:
        raise Refused([kb_pb2.Fault(artifact=error.prog, message=error.message)]) from error


def _run(args) -> int:
    """The command's handler, with the operating system's refusal of a path made a fault that names it."""
    try:
        args.by = _by(args) if args.command in _MUTATING else {}
        return _HANDLERS[args.command](args)
    except OSError as error:
        raise Refused([kb_pb2.Fault(artifact=str(error.filename or ""), message=error.strerror or str(error))]) from error


_MUTATING = ("init", "create", "write", "apply", "snapshot", "append", "delete")
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


def _show(document: dict | list, as_json: bool = False) -> None:
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


def _answered(response, also=()):
    """kb's answer, or the refusal it carries: every kb answer's faults, and any `also` it counts as faults, are refused this one way."""
    faults = [*response.faults, *also]
    if faults:
        raise Refused(faults)
    return response


def _init(args) -> int:
    client = kb_client.connect(Path(args.root))
    client.Init(kb_requests.init_request(args))
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
    request = kb_requests.create_request(args, _document(args.source, "content"))
    response = _answered(_client().Create(request))
    _show(answers.created(response))
    return 0


def _write_artifact(args) -> int:
    request = kb_requests.write_request(args, _document(args.source, "content"))
    response = _answered(_client().Write(request))
    _show(answers.written_over(request.locator, response))
    return 0


def _append(args) -> int:
    request = kb_requests.append_request(args, _document(args.source, "content"))
    response = _answered(_client().Append(request))
    _show(answers.appended(request.locator, response))
    return 0


def _delete(args) -> int:
    request = kb_requests.delete_request(args)
    response = _answered(_client().Delete(request))
    _show(answers.deleted(request.locator, response))
    return 0


def _read(args) -> int:
    response = _answered(_client().Read(kb_requests.read_request(args)))
    answer = answers.section if args.section else answers.whole if kb_requests.is_whole(args) else answers.glance
    _show(answer(response), args.json)
    return 0


def _validate(args) -> int:
    """kb's check answers with the store's faults and violations alike; any of either is a refusal."""
    response = _client().Validate(kb_requests.validate_request(args))
    _answered(response, response.violations)
    return 0


def _apply(args) -> int:
    request = kb_requests.apply_request(args, _document(args.source, "batch"))
    response = _answered(_client().Apply(request))
    _show(answers.applied(response))
    return 0


def _journal(args) -> int:
    response = _answered(_client().Journal(kb_requests.journal_request(args)))
    _show(answers.history(response))
    return 0


def _list(args) -> int:
    response = _answered(_client().List(kb_requests.list_request(args)))
    _show((answers.names if args.ids else answers.listed)(response))
    return 0


def _refs(args) -> int:
    response = _answered(_client().Refs(kb_requests.refs_request(args)))
    _show(answers.reached(response))
    return 0


def _search(args) -> int:
    response = _answered(_client().Search(kb_requests.search_request(args)))
    _show(answers.matched(response))
    return 0


def _snapshot(args) -> int:
    response = _answered(_client().Snapshot(kb_requests.snapshot_request(args)))
    _show(answers.recorded(response))
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
    "append": _append,
    "delete": _delete,
    "read": _read,
    "write": _write_artifact,
    "validate": _validate,
    "apply": _apply,
    "journal": _journal,
    "list": _list,
    "refs": _refs,
    "search": _search,
    "snapshot": _snapshot,
    "render": _render,
}
