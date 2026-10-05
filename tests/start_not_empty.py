"""The steps of start-a-knowledge-base.feature about a knowledge base init would furnish that already holds something:
the shop's types, which init refuses as already holding the shop's knowledge, or something else, which it refuses as
not empty, naming what it holds. The feature's test module star-imports this and no other does."""
import pytest
from kb.contract import kb_pb2
from pytest_bdd import given, parsers, then

from driver import connection_in, knol, serve, start, stop, store_in
from kb_oracle import operator_created, operator_started, printed

NOT_EMPTY = "it is not empty"
"""shop-knol's own words, not kb's, for a knowledge base it will not furnish because it holds something already."""

ALREADY_HOLDS = "it already holds the shop's knowledge"
"""shop-knol's own words, not kb's, for a knowledge base it will not furnish because it holds the shop's types."""

_A_TYPE = {"version": 1, "schema": {"type": "object", "properties": {"title": {"type": "string"}}}}
"""The content of a type of kb's operator's own: any artifact with a title."""


@pytest.fixture
def held():
    """The kinds of the types the knowledge base to furnish holds besides kb's own, filled in by the Given."""
    return []


@pytest.fixture
def journal_before():
    """What `shop-knol journal` answered of the knowledge base to furnish before the user ran init, and its root, as
    the Given named it: filled in by the Given."""
    return {}


def _noted(env, root, journal_before, named=None):
    """The knowledge base at `root`, named outright, as its journal read before init ran, and the name the user finds
    it by: `root` itself, unless a server's address names it."""
    journal_before["root"] = str(root)
    journal_before["named"] = named or str(root)
    journal_before["journal"] = knol({**env, "KB_ROOT": str(root)}, "journal").stdout


def _types_of_its_own(env, root):
    for title in ("Recipe", "Supplier"):
        operator_created(env, root, "schema", title, _A_TYPE)
    return ["recipe", "supplier"]


def _content(env, root):
    operator_created(env, root, "schema", "Note", _A_TYPE)
    operator_created(env, root, "note", "Order oats", {})
    return ["note"]


_HOLDING = {"types other than the shop's": _types_of_its_own, "content": _content}


@given(
    parsers.parse(
        "the user is working outside any knowledge base, with KB_ROOT naming a knowledge base holding {what} and not "
        "the shop's types"
    ),
    target_fixture="start_in",
)
def _kb_root_names_one_holding(env, tmp_path, what, held, journal_before):
    root = tmp_path / "operated"
    root.mkdir()
    operator_started(env, root)
    held.extend(_HOLDING[what](env, root))
    env["KB_ROOT"] = str(root)
    _noted(env, root, journal_before)
    return tmp_path


@given(
    "the user is working outside any knowledge base, with KB_ROOT naming a knowledge base holding the shop's types",
    target_fixture="start_in",
)
def _kb_root_names_a_furnished_one(env, tmp_path, journal_before):
    root = tmp_path / "furnished"
    root.mkdir()
    start(env, root)
    env["KB_ROOT"] = str(root)
    _noted(env, root, journal_before)
    return tmp_path


@given(
    "the user is working in one directory, and another directory holds a knowledge base holding the shop's types",
    target_fixture="elsewhere",
)
def _another_directory_furnished(env, tmp_path, journal_before):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    start(env, elsewhere)
    _noted(env, elsewhere, journal_before)
    return elsewhere


@pytest.fixture
def hosting(env, tmp_path):
    """A store holding the shop's types, started by the shop's own init, and the real `kb serve` hosting it on a port
    of its own, stopped when the test ends however it ends: its root and its address."""
    hosted = tmp_path / "hosted"
    hosted.mkdir()
    start(env, hosted)
    server, address = serve(env, hosted)
    yield hosted, address
    stop(server)


@given(
    "the user is working where kb finds a connection to a server hosting a store holding the shop's types",
    target_fixture="start_in",
)
def _connected_to_a_furnished_one(env, tmp_path, hosting, journal_before):
    del env["KB_ROOT"]
    hosted, address = hosting
    connected = tmp_path / "connected"
    connected.mkdir()
    connection_in(connected, address)
    _noted(env, hosted, journal_before, named=address)
    return connected


@then("starting the knowledge base is rejected because it already holds the shop's knowledge")
def _rejected_already_holds(result, journal_before):
    """One line, in shop-knol's own words, naming the knowledge base as the user named it: KB_ROOT's value, or the
    directory given."""
    said = kb_pb2.Fault(artifact=journal_before["named"], message=ALREADY_HOLDS)
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.splitlines() == [printed(said)], result.stderr


@then("starting the knowledge base is rejected because it is not empty")
def _rejected_not_empty(env, result, held):
    """One line, in shop-knol's own words, naming the knowledge base as the user named it, through KB_ROOT."""
    said = kb_pb2.Fault(artifact=env["KB_ROOT"], message=f"{NOT_EMPTY}: it holds the types {', '.join(held)}")
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.splitlines() == [printed(said)], result.stderr


@then("the refusal names what it holds")
def _names_what_it_holds(result, held):
    named = result.stderr.rpartition("it holds the types ")[2].strip()
    assert set(named.split(", ")) == set(held), result.stderr


@then("nothing changes")
def _nothing_changes(env, start_in, journal_before):
    assert knol({**env, "KB_ROOT": journal_before["root"]}, "journal").stdout == journal_before["journal"]
    assert not store_in(start_in).exists()
