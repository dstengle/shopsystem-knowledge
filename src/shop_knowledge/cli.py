"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting.

Every file it reads and everything it prints is YAML 1.2, read and written by kb's own reading and writing of content.
A refusal, kb's or its own, is printed in plain words on stderr, one fault a line, with a non-zero exit; never a traceback.
"""
import json
import os
import sys
from pathlib import Path

import kb
from kb.client import connect
from kb.content import dumps
from kb.contract import kb_pb2

from shop_knowledge import answers, arguments, bootstrap, document, kb_requests
from shop_knowledge.refusal import Refused
from shop_knowledge.renderers import RENDERERS


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
    """Who signs a change, and why, or a refusal per lack, before any file is read; init gives no why."""
    role, _, execution = os.environ.get("KB_ACTOR", "").partition(":")
    message = getattr(args, "message", "-")
    lacking = [("actor", _NO_ROLE)] * (not role) + [("message", _NO_MESSAGE)] * (not message)
    if lacking:
        raise Refused([kb_pb2.Fault(rule=rule, message=said) for rule, said in lacking])
    return {"signature": kb_pb2.Signature(role=role, execution=execution, message=message)}


def _client():
    """kb finds the store: upward from the working directory, or through KB_ROOT."""
    return connect()


def _show(document: dict | list, as_json: bool = False) -> None:
    """An answer as YAML, or as the same document in JSON when asked."""
    if as_json:
        print(json.dumps(document, indent=2, ensure_ascii=False))
    else:
        print(dumps(document), end="")


def _plain(fault: kb_pb2.Fault) -> str:
    """One fault as a line a person reads: where, then what is wrong."""
    message = " ".join(line.strip() for line in fault.message.splitlines())
    where = f"{fault.artifact} at {fault.place}" if fault.place else fault.artifact
    return f"{where}: {message}" if where else message


def _refuse(faults) -> int:
    for fault in faults:
        print(_plain(fault), file=sys.stderr)
    return 1


def _answered(response):
    """kb's result, or the refusal it carries: every kb answer's refusal is refused this one way."""
    if response.WhichOneof("outcome") == "refusal":
        _refused(response.refusal.faults)
    return response.result


def _refused(faults) -> None:
    """Refused for these faults, when there are any: what `_answered` refuses a kb refusal with, and what a check's
    violations and a renderer's faults are refused with."""
    if faults:
        raise Refused(faults)


_GONE = "the directory you are working in is gone"


def _init(args) -> int:
    signed = args.by["signature"]
    client = _named(_absolute(args.root), signed) if args.root else _found(_absolute(Path(".")), signed)
    for answer in bootstrap.load(client, signed):
        _answered(answer)
    return 0


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


def _create(args) -> int:
    request = kb_requests.create_request(args, document.read(args.source, "content"))
    response = _answered(_client().Create(request))
    _show(answers.created(response))
    return 0


def _write_artifact(args) -> int:
    request = kb_requests.write_request(args, document.read(args.source, "content"))
    response = _answered(_client().Replace(request))
    _show(answers.written_over(request.locator, response))
    return 0


def _append(args) -> int:
    request = kb_requests.append_request(args, document.read(args.source, "content"))
    response = _answered(_client().Add(request))
    _show(answers.appended(request.locator, response))
    return 0


def _delete(args) -> int:
    request = kb_requests.delete_request(args)
    response = _answered(_client().Remove(request))
    _show(answers.deleted(request.locator, response))
    return 0


def _read(args) -> int:
    response = _answered(_client().Read(kb_requests.read_request(args)))
    answer = answers.section if args.section else answers.whole if kb_requests.is_whole(args) else answers.glance
    _show(answer(response), args.json)
    return 0


def _validate(args) -> int:
    """kb's check answers with a refusal (a check that never ran, no store found) apart from what it found once it ran
    (violations, damaged files included). A call that never ran shows no answer: its refusal is refused through
    `_answered` before anything is shown. A call that ran shows what it found, then refuses any violation as the exit,
    so what is behind its type is shown beside the faults."""
    response = _answered(_client().Check(kb_requests.validate_request(args)))
    _show(answers.checked(response))
    _refused(response.violations)
    return 0


def _apply(args) -> int:
    request = kb_requests.apply_request(args, document.read(args.source, "batch"))
    client = _client()
    batched = client.BatchCreate if isinstance(request, kb_pb2.BatchCreateRequest) else client.BatchReplace
    response = _answered(batched(request))
    _show(answers.applied(response))
    return 0


def _journal(args) -> int:
    response = _answered(_client().History(kb_requests.journal_request(args)))
    _show(answers.history(response))
    return 0


def _list(args) -> int:
    response = _answered(_client().List(kb_requests.list_request(args)))
    _show((answers.names if args.ids else answers.listed)(response))
    return 0


def _refs(args) -> int:
    response = _answered(_client().Follow(kb_requests.refs_request(args)))
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
    rendered = RENDERERS[args.renderer](_client(), args.locator)
    _refused(rendered.faults)
    _write(rendered.files, args.to)
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
    "append": _append,
    "validate": _validate,
    "apply": _apply,
    "journal": _journal,
    "list": _list,
    "refs": _refs,
    "search": _search,
    "render": _render,
    "delete": _delete,
    "snapshot": _snapshot,
}
