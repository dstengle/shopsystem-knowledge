"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting."""
import argparse
import os
from pathlib import Path

import yaml
from kb import client as kb_client
from kb.content import loads, dumps
from kb.contract import kb_pb2

from shop_knowledge import bootstrap


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="shop-knol")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="start a shop knowledge base at <root>/kb/ with the shop's types")
    init.add_argument("root")

    create = commands.add_parser("create", help="record an artifact from a YAML file; prints the id kb chose")
    create.add_argument("type")
    create.add_argument("--from", dest="source", required=True, metavar="FILE")
    create.add_argument("-m", dest="message", required=True, help="why")

    read = commands.add_parser("read", help="read an artifact at a glance")
    read.add_argument("locator")

    args = parser.parse_args(argv)
    return {"init": _init, "create": _create, "read": _read}[args.command](args)


def _actor() -> kb_pb2.Actor:
    return kb_pb2.Actor(role=os.environ["KB_ACTOR"])


def _client():
    return kb_client.connect(Path(os.environ["KB_ROOT"]))


def _show(document: dict) -> None:
    print(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), end="")


def _init(args) -> int:
    root = Path(args.root)
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root), actor=_actor()))
    bootstrap.load(client, _actor())
    return 0


def _create(args) -> int:
    content = yaml.safe_load(Path(args.source).read_text())
    response = _client().Create(kb_pb2.CreateRequest(
        type=args.type, content=dumps(content), actor=_actor(), message=args.message,
    ))
    _show({"id": response.id, "revision": response.revision})
    return 0


def _read(args) -> int:
    response = _client().Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=args.locator)))
    _show({
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
    })
    return 0
