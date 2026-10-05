"""Each command's arguments turned into the request it sends kb: one public function per command that calls kb,
named `<command>_request`, and `is_whole`, the one helper `cli._read` uses. Who signs a change is read from
`args.by`, set by the command line's `_run`; a command that sends a file's content takes the document that was read.
Nothing here shows anything or makes a call."""
from kb.content import dumps, text
from kb.contract import kb_pb2

from shop_knowledge import batch
from shop_knowledge.document import named


def init_request() -> kb_pb2.ListRequest:
    """The names of the types a knowledge base holds, which tell init whether it is empty."""
    return kb_pb2.ListRequest(kind="schema", form=kb_pb2.ListRequest.IDS)


def create_request(args, document: dict) -> kb_pb2.CreateRequest:
    """The title is split off the content, since kb takes it as a field of its own."""
    content = dict(document)
    title = text(content.pop("title", None))
    return kb_pb2.CreateRequest(kind=args.type, title=title, content=dumps(content), signature=args.by["signature"])


def write_request(args, document: dict) -> kb_pb2.ReplaceRequest:
    return kb_pb2.ReplaceRequest(
        locator=_locator(args.locator), content=dumps(document), signature=args.by["signature"],
    )


def append_request(args, document: dict) -> kb_pb2.AddRequest:
    return kb_pb2.AddRequest(locator=_locator(args.locator), content=dumps(document), signature=args.by["signature"])


def delete_request(args) -> kb_pb2.RemoveRequest:
    return kb_pb2.RemoveRequest(locator=_locator(args.locator), signature=args.by["signature"])


def _locator(words: str) -> kb_pb2.Locator:
    """A locator as the user says it: a name, or a name and after # a place inside it."""
    name, _, place = words.partition("#")
    return kb_pb2.Locator(id=name, place=place)


def is_whole(args) -> bool:
    """--resolve implies a whole read, since kb fills links in only on a whole read."""
    return args.whole or args.resolve is not None


def read_request(args) -> kb_pb2.ReadRequest:
    """The level a read asks for: a section, or a whole (filled in as deep as --resolve says), or the summary."""
    where = kb_pb2.Locator(id=args.locator)
    if args.section:
        return kb_pb2.ReadRequest(locator=where, section=kb_pb2.ReadRequest.Section(title=args.section))
    if is_whole(args):
        return kb_pb2.ReadRequest(locator=where, whole=kb_pb2.ReadRequest.Whole(depth=args.resolve or 0))
    return kb_pb2.ReadRequest(locator=where, summary=kb_pb2.ReadRequest.Summary())


def validate_request(args) -> kb_pb2.CheckRequest:
    return kb_pb2.CheckRequest()


def apply_request(args, document: dict) -> kb_pb2.BatchCreateRequest | kb_pb2.BatchReplaceRequest:
    """One set of creates, or one set of writes, as the batch's changes are."""
    items = batch.items(document, named(args.source))
    if all(isinstance(item, kb_pb2.CreateItem) for item in items):
        return kb_pb2.BatchCreateRequest(items=items, signature=args.by["signature"])
    return kb_pb2.BatchReplaceRequest(items=items, signature=args.by["signature"])


def journal_request(args) -> kb_pb2.HistoryRequest:
    return kb_pb2.HistoryRequest(
        artifact=args.artifact, role=args.actor, execution=args.execution, since=args.since,
    )


def list_request(args) -> kb_pb2.ListRequest:
    fields = dict(where.partition("=")[::2] for where in args.where)
    form = kb_pb2.ListRequest.IDS if args.ids else kb_pb2.ListRequest.STUBS
    return kb_pb2.ListRequest(kind=args.type, fields=fields, form=form)


def refs_request(args) -> kb_pb2.FollowRequest:
    direction = kb_pb2.FollowRequest.IN if args.inbound else kb_pb2.FollowRequest.OUT
    return kb_pb2.FollowRequest(
        locator=_locator(args.locator), depth=args.depth, direction=direction,
        via=args.via, kind=args.type,
    )


def search_request(args) -> kb_pb2.SearchRequest:
    scope = getattr(kb_pb2.SearchRequest, args.scope.upper())
    return kb_pb2.SearchRequest(text=args.text, kind=args.type, scope=scope)


def snapshot_request(args) -> kb_pb2.SnapshotRequest:
    """The piece of work is `--execution`, which replaces any execution KB_ACTOR names (adrs/0025)."""
    signed = args.by["signature"]
    signature = kb_pb2.Signature(role=signed.role, execution=args.execution, message=signed.message)
    return kb_pb2.SnapshotRequest(signature=signature, artifacts=args.names)


def types_request(args) -> kb_pb2.ListRequest | kb_pb2.ReadRequest:
    """Every type as a stub, or the one named, read whole at depth 0."""
    if args.name is None:
        return kb_pb2.ListRequest(kind="schema", form=kb_pb2.ListRequest.STUBS)
    return kb_pb2.ReadRequest(
        locator=kb_pb2.Locator(id=f"schema/{args.name}"), whole=kb_pb2.ReadRequest.Whole(depth=0),
    )
