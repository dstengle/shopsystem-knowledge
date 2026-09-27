"""The steps of publish-what-the-shop-knows.feature about a publish that is refused: a process or role past the
limits the harness publishes, and the type-refusal outline (publishing a kind from the wrong type). The feature's
test module star-imports this and no other does."""
from pytest_bdd import given, parsers, then, when

from driver import knol, record


@given("a process whose steps run past the limits the harness publishes", target_fixture="process_name")
def _a_process_past_the_limits(env, tmp_path):
    """Two hundred steps written out at four lines each is past the five hundred lines a skill's body may run to."""
    steps = [{"title": f"Count shelf {number}", "does": f"Count what is on shelf {number}.\n"} for number in range(1, 201)]
    return record(env, tmp_path, "process", {"title": "Count every shelf", "steps": steps}, "Describe the stocktake")


@then("the skill is rejected because it goes beyond the limits the harness publishes")
def _rejected_for_the_limits(result):
    assert result.stderr.splitlines() == [
        "process/count-every-shelf at steps: a skill's body is under 500 lines, the limit the harness publishes; "
        "this one is 801",
    ]
    assert result.returncode != 0


@then("nothing is written to the directory")
def _nothing_written(target):
    assert list(target.iterdir()) == []


@given("a role whose harness fields run past the limits the harness publishes", target_fixture="role_name")
def _a_role_past_the_limits(env, tmp_path):
    return record(env, tmp_path, "role", {
        "title": "Shop steward",
        "harness": {"name": "-shop:steward", "description": "Keeps the shop."},
        "shop": {"responsible_for": "The shop"},
    }, "Describe the shop steward")


@then("the agent is rejected because it goes beyond the limits the harness publishes")
def _rejected_agent_for_the_limits(result):
    assert result.stderr.splitlines() == [
        'role/shop-steward at harness.name: an agent\'s name holds no ":", the limit the harness publishes; '
        "this one is -shop:steward",
        'role/shop-steward at harness.name: an agent\'s name does not start with "-", the limit the harness '
        "publishes; this one is -shop:steward",
    ]
    assert result.returncode != 0


@when(
    parsers.re(r"the user publishes the (?P<thing>process|role) as (?P<kind>agent|skill|diagram) into a directory"),
    target_fixture="result",
)
def _publish_as_a_kind_it_cannot_become(env, thing, kind, process_name, role_name, target):
    """The process by the Background's `process_name`, or its role by `role_name`, with the renderer the kind names."""
    name = process_name if thing == "process" else role_name
    return knol(env, "render", kind, name, "--to", str(target))


# The refusal each of the outline's three rows gets, spelled out in `renderers.source.refusal`'s own words, not
# recomputed here with a copy of its article rule (a wrong article in both would otherwise pass).
_REFUSAL = {
    "agent": "an agent is made from a role; this one is a process",
    "skill": "a skill is made from a process; this one is a role",
    "diagram": "a diagram is made from a process; this one is a role",
}


@then(parsers.parse("the {kind} is rejected because it is not made from a {thing}, naming the type {named}"))
def _rejected_for_its_type(result, kind, process_name, role_name):
    """One line on the artifact published from: the process by name for the agent row, the role by name for skill
    and diagram, then `_REFUSAL`'s line for that kind."""
    name = process_name if kind == "agent" else role_name
    assert result.stderr.splitlines() == [f"{name}: {_REFUSAL[kind]}"]
