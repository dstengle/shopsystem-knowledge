"""The steps of find-the-knowledge-base.feature about where the knowledge base is found that only the
read-back feature uses: the scenarios that give `workdir` from a shop its own Background already started, a directory
since removed among them, and the Thens that say what came of it. The store-refusal Givens and Thens that the check
feature's scenarios also use live in store_not_found.py, which conftest.py star-imports, instead. The feature's test module star-imports this and no other does."""
import pytest
from kb.content import loads
from pytest_bdd import given, then

from driver import connection_in, knol, removed, serve, stop
from kb_oracle import refused_as_kb_refuses


@given(
    "the user is working in a folder deep inside the directory that holds the shop's knowledge",
    target_fixture="workdir",
)
def _working_deep_inside_the_shop(env, shop, decision_id):
    del env["KB_ROOT"]
    deep = shop / "notes" / "pricing" / "2026"
    deep.mkdir(parents=True)
    return deep


@then("the user sees the decision, from the knowledge base found above where they are working")
def _decision_from_above(shown, decision_id):
    assert shown["id"] == decision_id


@given("the user is working outside any knowledge base, with KB_ROOT naming the shop's", target_fixture="workdir")
def _working_elsewhere_naming_the_shop(tmp_path, decision_id):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    return elsewhere


@then("the user sees the decision, from the knowledge base KB_ROOT names")
def _decision_from_kb_root(shown, decision_id):
    assert shown["id"] == decision_id


@given(
    "the user is working in a directory that has since been removed, and nothing names a knowledge base",
    target_fixture="workdir",
)
def _working_in_a_removed_directory(env, tmp_path, decision_id):
    del env["KB_ROOT"]
    return removed(tmp_path)


@then("the command is rejected because the directory they are working in is gone")
def _rejected_as_gone(env, result, workdir, called):
    """kb's own answer from a directory removed the same way, never its words spelled here: the store rule, one line."""
    refused_as_kb_refuses(env, result, workdir, called)


@given(
    "the user is working in a directory that has since been removed, with KB_ROOT naming the shop's",
    target_fixture="workdir",
)
def _working_in_a_removed_directory_naming_the_shop(tmp_path, decision_id):
    return removed(tmp_path)


@pytest.fixture
def server(env, shop):
    """The real `kb serve`, hosting the shop's store on a port of its own, stopped when the test ends however it ends."""
    served = serve(env, shop)
    yield served[1]
    stop(served[0])


@given("the shop's knowledge base is hosted by a server")
def _hosted_by_a_server(server, decision_id):
    """The Background's store, as the server serves it: `server` is its address."""


@given(
    "the user is working in a folder deep inside a directory holding a connection to that server",
    target_fixture="workdir",
)
def _working_deep_inside_a_connection(env, tmp_path, server):
    del env["KB_ROOT"]
    connected = tmp_path / "connected"
    connected.mkdir()
    connection_in(connected, server)
    deep = connected / "notes" / "pricing" / "2026"
    deep.mkdir(parents=True)
    return deep


@then("the user sees the decision, just as they would from the store itself")
def _decision_as_from_the_store(env, shown, shop, decision_id):
    straight = knol({**env, "KB_ROOT": str(shop)}, "read", decision_id)
    assert straight.returncode == 0, straight.stderr
    assert shown == loads(straight.stdout)
