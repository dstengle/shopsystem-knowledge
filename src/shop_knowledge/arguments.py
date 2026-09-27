"""The arguments of every shop-knol command, declared with argparse; it knows what a command is called and takes, not what it does."""
import argparse

from shop_knowledge.renderers import RENDERERS


def command_parser() -> argparse.ArgumentParser:
    """Every command's arguments and help, the renderer names from RENDERERS as the choices of render."""
    parser = argparse.ArgumentParser(prog="shop-knol")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="start a shop knowledge base at <root>/kb/ with the shop's types")
    init.add_argument("root")

    create = commands.add_parser("create", help="record an artifact from a YAML file; prints the id kb chose")
    create.add_argument("type")
    create.add_argument("--from", dest="source", required=True, metavar="FILE")
    create.add_argument("-m", dest="message", help="why")

    read = commands.add_parser("read", help="read an artifact at a glance")
    read.add_argument("locator")
    read.add_argument("--json", action="store_true", help="the same answer written as JSON")
    read.add_argument("--section", metavar="TITLE", help="only the section with this title")
    read.add_argument("--whole", action="store_true", help="every field and section, links as names")
    read.add_argument(
        "--resolve", nargs="?", const=1, type=int, metavar="DEPTH",
        help="a whole read with links filled in, DEPTH steps (one when not said)",
    )

    write = commands.add_parser("write", help="replace an artifact, or a part of it as <name>#<place>, from a YAML file")
    write.add_argument("locator")
    write.add_argument("--from", dest="source", required=True, metavar="FILE")
    write.add_argument("-m", dest="message", help="why")

    validate = commands.add_parser(
        "validate", help="check everything the shop knows; lists every fault, exits non-zero if any",
    )

    apply = commands.add_parser("apply", help="make every change in a batch file as one change; prints the set's name")
    apply.add_argument("--from", dest="source", required=True, metavar="FILE")
    apply.add_argument("-m", dest="message", help="why")

    journal = commands.add_parser("journal", help="review who changed what: every change, oldest first")
    journal.add_argument("--artifact", default="", help="only the changes to this one")

    listing = commands.add_parser("list", help="list what the shop has recorded of one type, each with its name and title")
    listing.add_argument("--type", required=True, help="the type to list")
    listing.add_argument(
        "--where", action="append", default=[], metavar="FIELD=VALUE",
        help="only those whose field has this value; repeat to narrow further",
    )
    listing.add_argument("--ids", action="store_true", help="the names alone")

    refs = commands.add_parser("refs", help="follow the links out of an artifact or into it, nearest first, each with its route")
    refs.add_argument("locator")
    direction = refs.add_mutually_exclusive_group(required=True)
    direction.add_argument("--outbound", action="store_true", help="what the artifact points at")
    direction.add_argument("--inbound", action="store_true", help="what points at the artifact")
    refs.add_argument("--via", metavar="FIELD", help="only through this link")
    refs.add_argument("--type", help="only the artifacts of this type")
    refs.add_argument("--depth", type=int, help="how many steps to follow (one when not said)")

    render = commands.add_parser("render", help="publish an artifact into a directory; the shop is only read")
    render.add_argument("renderer", choices=sorted(RENDERERS))
    render.add_argument("locator")
    render.add_argument("--to", required=True, metavar="DIR")
    return parser
