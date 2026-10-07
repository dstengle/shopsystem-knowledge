"""The steps of start-a-knowledge-base.feature about a knowledge base kb's operator started empty, which init
furnishes with the shop's types: found upward, through KB_ROOT, or in a directory the user names. The feature's test
module star-imports this and no other does."""
import pytest
from kb.content import loads
from pytest_bdd import given, then, when

from driver import knol, store_in
from kb_oracle import operator_started

THE_SHOPS_TYPES = {"shop-artifact", "decision", "feature", "work-item", "role", "process", "step", "tag"}


@pytest.fixture
def operated():
    """Where kb's operator started the empty knowledge base the scenario furnishes, filled in by the Given that starts it."""
    return {}


def _operator_started(env, root, operated):
    operator_started(env, root)
    operated["root"] = root


@given(
    "the user is working in a folder inside a knowledge base kb's operator started empty, and nothing names one",
    target_fixture="start_in",
)
def _inside_an_operated_one(env, shop, operated):
    del env["KB_ROOT"]
    _operator_started(env, shop, operated)
    # Works in the directory kb's contract says init made (`kb.init`), inside the knowledge base.
    return store_in(shop)


@given(
    "the user is working outside any knowledge base, with KB_ROOT naming a knowledge base kb's operator started empty",
    target_fixture="start_in",
)
def _kb_root_names_an_operated_one(env, tmp_path, operated):
    operated_root = tmp_path / "operated"
    operated_root.mkdir()
    _operator_started(env, operated_root, operated)
    env["KB_ROOT"] = str(operated_root)
    return tmp_path


@given(
    "the user is working where kb finds a connection to a server hosting a store kb's operator started empty",
    target_fixture="start_in",
)
def _served_an_operated_one(env, tmp_path, served_store, operated):
    """An empty store started by kb's operator, served by kb's double, its connection in the directory the user works
    in, nothing naming a knowledge base."""
    root = tmp_path / "operated"
    root.mkdir()
    _operator_started(env, root, operated)
    office = tmp_path / "office"
    office.mkdir()
    served_store(root, office)
    del env["KB_ROOT"]
    return office


@given(
    "the user is working in one directory, and another directory holds a knowledge base kb's operator started empty",
    target_fixture="elsewhere",
)
def _another_directory_operated(env, tmp_path, operated):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    _operator_started(env, elsewhere, operated)
    return elsewhere


@when("the user starts a shop knowledge base without naming a directory, saying who they are", target_fixture="result")
def _start_where_found(env, start_in):
    """init run from where the user works, under the scenario's own environment: whatever it names, it names."""
    return knol(env, "init", cwd=start_in)


@then("that knowledge base holds the shop's types and nothing else of the shop's")
def _holds_the_types_alone(env, operated, result):
    """The operator's knowledge base, named outright: its types are kb's own and the shop's, and its history has
    touched nothing else."""
    assert result.returncode == 0, result.stderr
    there = {**env, "KB_ROOT": str(operated["root"])}
    expected = {f"schema/{name}" for name in THE_SHOPS_TYPES | {"schema"}}
    listed = knol(there, "list", "--type", "schema", "--ids")
    assert set(loads(listed.stdout)) == expected, listed.stderr
    changes = loads(knol(there, "journal").stdout)["changes"]
    assert {change["artifact"] for change in changes} == expected
