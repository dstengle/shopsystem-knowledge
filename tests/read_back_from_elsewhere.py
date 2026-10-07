"""The steps of find-the-knowledge-base.feature about where the knowledge base is found that only the
read-back feature uses: the scenarios that give `workdir` from a shop its own Background already started, a directory
since removed among them, or a folder deep inside a directory holding a connection to a server hosting the shop's store
(served by conftest's `served_store`), and the Thens that say what came of it. The store-refusal Givens and Thens that the check
feature's scenarios also use live in store_not_found.py, which conftest.py star-imports, instead. The feature's test module star-imports this and no other does."""
from kb.content import loads
from pytest_bdd import given, then

from driver import knol, removed
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


@given("the shop's knowledge base is hosted by a server", target_fixture="connected")
def _hosted_by_a_server(served_store, shop, tmp_path, decision_id):
    """The shop's store, its decision already recorded, served by kb's double; gives back the directory of the test's
    own that holds the connection to it, never the shop's own."""
    connected = tmp_path / "office"
    connected.mkdir()
    served_store(shop, connected)
    return connected


@given(
    "the user is working in a folder deep inside a directory holding a connection to that server",
    target_fixture="workdir",
)
def _working_deep_inside_the_connection(env, connected):
    del env["KB_ROOT"]
    deep = connected / "notes" / "pricing" / "2026"
    deep.mkdir(parents=True)
    return deep


@then("the user sees the decision, just as they would from the store itself")
def _decision_as_from_the_store(env, shop, shown, decision_id):
    """What the server showed equals the same read made of the store itself, named by KB_ROOT: a read, which kb does
    not refuse of a store it serves."""
    straight = knol({**env, "KB_ROOT": str(shop)}, "read", decision_id)
    assert straight.returncode == 0, straight.stderr
    assert shown == loads(straight.stdout)
