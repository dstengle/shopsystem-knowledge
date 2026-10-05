"""The steps of start-a-knowledge-base.feature about a knowledge base init would furnish that already holds something
other than the shop's types, which init refuses as not empty, naming what it holds. The feature's test module
star-imports this and no other does."""
import pytest
from kb.contract import kb_pb2
from pytest_bdd import given, parsers, then

from driver import knol, store_in
from kb_oracle import operator_created, operator_started, printed

NOT_EMPTY = "it is not empty"
"""shop-knol's own words, not kb's, for a knowledge base it will not furnish because it holds something already."""

_A_TYPE = {"version": 1, "schema": {"type": "object", "properties": {"title": {"type": "string"}}}}
"""The content of a type of kb's operator's own: any artifact with a title."""


@pytest.fixture
def held():
    """The kinds of the types the knowledge base to furnish holds besides kb's own, filled in by the Given."""
    return []


@pytest.fixture
def journal_before():
    """What `shop-knol journal` answered of the knowledge base to furnish before the user ran init."""
    return {}


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
    journal_before["journal"] = knol(env, "journal").stdout
    return tmp_path


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
    assert knol(env, "journal").stdout == journal_before["journal"]
    assert not store_in(start_in).exists()
