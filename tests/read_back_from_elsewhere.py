"""The steps of read-back-what-the-shop-knows.feature about where the knowledge base is found: the six scenarios
that give `workdir` and the Thens that say what came of it. The feature's test module star-imports this and no other does."""
from pytest_bdd import given, then

from driver import Removed, start


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


@given("the user is working outside any knowledge base and nothing names one", target_fixture="workdir")
def _working_elsewhere_naming_nothing(env, tmp_path, decision_id):
    del env["KB_ROOT"]
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    return elsewhere


@given(
    "the user is working in a directory that has since been removed, and nothing names a knowledge base",
    target_fixture="workdir",
)
def _working_in_a_removed_directory(env, tmp_path, decision_id):
    del env["KB_ROOT"]
    gone = tmp_path / "gone"
    gone.mkdir()
    return Removed(gone)


@then("the command is rejected because no knowledge base was found, neither above where they are working nor named outright")
def _rejected_no_store(result, workdir):
    assert result.stderr == f"no store was found, neither above {workdir.resolve()} nor named outright\n"
    assert result.stdout == ""


@given(
    "the user is working outside any knowledge base, with KB_ROOT naming a directory that holds no knowledge base",
    target_fixture="workdir",
)
def _kb_root_names_an_empty_directory(env, tmp_path, decision_id):
    empty = tmp_path / "empty"
    empty.mkdir()
    env["KB_ROOT"] = str(empty)
    return tmp_path


@then("the command is rejected because KB_ROOT names a directory that holds no knowledge base")
def _rejected_kb_root_holds_none(env, result):
    assert result.stderr == f"KB_ROOT names a directory that holds no store: {env['KB_ROOT']}\n"
    assert result.stdout == ""


@given(
    "the user is working inside the shop's knowledge base, with KB_ROOT naming a different one",
    target_fixture="workdir",
)
def _kb_root_names_another_store(env, shop, tmp_path, decision_id):
    other = tmp_path / "other"
    other.mkdir()
    start(env, other)
    env["KB_ROOT"] = str(other)
    return shop


@then(
    "the command is rejected because KB_ROOT names a knowledge base other than the one they are working in, "
    "and neither of the two is guessed at"
)
def _rejected_two_stores(env, result, workdir):
    assert result.stderr == (
        f"KB_ROOT names a store other than the one {workdir.resolve()} is working in: KB_ROOT is {env['KB_ROOT']}, "
        f"the working directory is inside {workdir.resolve()}; neither is guessed at\n"
    )
    assert result.stdout == ""
