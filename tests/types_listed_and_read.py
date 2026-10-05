"""The steps of use-the-shops-types.feature that ask for the shop's types through the command of their own. The
feature's test module star-imports this and no other does."""
from importlib import resources

from kb.content import loads
from pytest_bdd import then, when

from driver import knol

THE_SEVEN = {"decision", "feature", "work-item", "role", "process", "step", "tag"}


@when("the user asks which types the shop holds", target_fixture="result")
def _asks_which_types(env):
    return knol(env, "types")


@then("the user is shown each of the shop's seven types")
def _each_of_the_seven(shown):
    assert {entry["name"] for entry in shown} == THE_SEVEN
    assert all(entry["title"] for entry in shown)


@when("the user reads the role type by its name", target_fixture="result")
def _reads_the_role_type(env):
    return knol(env, "types", "role")


@then("the user is shown the role type as the shop holds it")
def _the_role_type(shown):
    held = loads(resources.files("shop_knowledge.types").joinpath("role.yaml").read_text())
    assert shown["id"] == "schema/role"
    assert shown["type"] == "schema"
    assert shown["title"] == held["title"]
    assert shown["schema"] == held["schema"]
