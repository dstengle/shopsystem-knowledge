"""The steps of read-back-what-the-shop-knows.feature about where the knowledge base is found that only the
read-back feature uses: the scenarios that give `workdir` from a shop its own Background already started, a directory
since removed among them, and the Thens that say what came of it. The store-refusal Givens and Thens that the check
feature's scenarios also use live in store_not_found.py, which conftest.py star-imports, instead. The feature's test module star-imports this and no other does."""
from pytest_bdd import given, then

from driver import refused_as_kb_refuses, removed


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
