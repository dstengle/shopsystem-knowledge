"""Each command's arguments turned into the request it sends kb: one public function per command that calls kb,
named `<command>_request`, and `is_whole`, the one helper `cli._read` uses. The actor and message are read from `args.by`, set by the command line's `_run`; a
command that sends a file's content takes the document that was read. Nothing here shows anything or makes a call."""
from kb.content import dumps, text
from kb.contract import kb_pb2

from shop_knowledge import batch


def init_request(args) -> kb_pb2.InitRequest:
    """The root sent to kb absolute, so a refusal it raises quotes a path that names the place, not the working
    directory's own name for it."""
    return kb_pb2.InitRequest(root=str(args.root.resolve()), actor=args.by["actor"])


def create_request(args, document: dict) -> kb_pb2.CreateRequest:
    """The title is split off the content, since kb takes it as a field of its own."""
    content = dict(document)
    title = text(content.pop("title", None))
    return kb_pb2.CreateRequest(type=args.type, title=title, content=dumps(content), **args.by)


def write_request(args, document: dict) -> kb_pb2.WriteRequest:
    return kb_pb2.WriteRequest(locator=_locator(args.locator), content=dumps(document), **args.by)


def append_request(args, document: dict) -> kb_pb2.AppendRequest:
    return kb_pb2.AppendRequest(locator=_locator(args.locator), content=dumps(document), **args.by)


def delete_request(args) -> kb_pb2.DeleteRequest:
    return kb_pb2.DeleteRequest(locator=_locator(args.locator), **args.by)


def _locator(words: str) -> kb_pb2.Locator:
    """A locator as the user says it: a name, or a name and after # a place inside it."""
    name, _, place = words.partition("#")
    return kb_pb2.Locator(id=name, path=place)


def is_whole(args) -> bool:
    """--resolve implies a whole read, since kb fills links in only on a whole read."""
    return args.whole or args.resolve is not None


def read_request(args) -> kb_pb2.ReadRequest:
    """The level and depth a read asks for: a section, or a whole (filled in when --resolve), or the summary."""
    where = kb_pb2.Locator(id=args.locator)
    if args.section:
        return kb_pb2.ReadRequest(locator=where, level=kb_pb2.ReadRequest.SECTION, section=args.section)
    if is_whole(args):
        return kb_pb2.ReadRequest(locator=where, level=kb_pb2.ReadRequest.WHOLE, depth=args.resolve or 0)
    return kb_pb2.ReadRequest(locator=where)


def validate_request(args) -> kb_pb2.ValidateRequest:
    return kb_pb2.ValidateRequest()


def apply_request(args, document: dict) -> kb_pb2.ApplyRequest:
    return kb_pb2.ApplyRequest(operations=batch.operations(document), **args.by)


def journal_request(args) -> kb_pb2.JournalRequest:
    return kb_pb2.JournalRequest(
        artifact=args.artifact, role=args.actor, execution=args.execution, since=args.since,
    )


def list_request(args) -> kb_pb2.ListRequest:
    fields = dict(where.partition("=")[::2] for where in args.where)
    form = kb_pb2.ListRequest.IDS if args.ids else kb_pb2.ListRequest.STUBS
    return kb_pb2.ListRequest(type=args.type, fields=fields, form=form)


def refs_request(args) -> kb_pb2.RefsRequest:
    direction = kb_pb2.RefsRequest.IN if args.inbound else kb_pb2.RefsRequest.OUT
    return kb_pb2.RefsRequest(
        locator=_locator(args.locator), depth=args.depth, direction=direction,
        via=args.via, type=args.type,
    )


def search_request(args) -> kb_pb2.SearchRequest:
    scope = getattr(kb_pb2.SearchRequest, args.scope.upper())
    return kb_pb2.SearchRequest(text=args.text, type=args.type, scope=scope)


def snapshot_request(args) -> kb_pb2.SnapshotRequest:
    """The piece of work is `--execution`, which replaces any execution KB_ACTOR names (adrs/0025)."""
    actor = kb_pb2.Actor(role=args.by["actor"].role, execution=args.execution)
    return kb_pb2.SnapshotRequest(actor=actor, artifacts=args.names, message=args.by["message"])
