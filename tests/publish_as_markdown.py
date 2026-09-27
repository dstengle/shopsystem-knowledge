"""The steps of publish-what-the-shop-knows.feature about publishing as markdown: the When that renders the role as
markdown and the Then that says what the page holds. The feature's test module star-imports this and no other does."""
from pytest_bdd import then, when

from driver import knol


@when("the user publishes the role as markdown into a directory", target_fixture="result")
def _publish_as_markdown(env, target):
    """The Background records the role from ROLE, which is titled Stock keeper, so its name is role/stock-keeper."""
    return knol(env, "render", "markdown", "role/stock-keeper", "--to", str(target))


@then("that directory holds a page with the identity as a heading, the fields as a list, the sections at their levels and the parts as tables")
def _a_page(result, target):
    """The role's title as the heading, its fields in the order kb gives them (a field group's own fields nested, a list
    of plain values joined), then its section one level below the heading. The role holds no part, so no table."""
    assert result.returncode == 0, result.stderr
    assert [path.name for path in target.iterdir()] == ["stock-keeper.md"]
    assert (target / "stock-keeper.md").read_text().splitlines() == [
        "# Stock keeper",
        "",
        "- **harness**",
        "  - **name**: stock-keeper",
        "  - **description**: Keeps the shelves stocked.",
        "  - **tools**: Read",
        "- **shop**",
        "  - **responsible_for**: What is on the shelves",
        "",
        "## How it works",
        "",
        "Counts, then orders.",
    ]
