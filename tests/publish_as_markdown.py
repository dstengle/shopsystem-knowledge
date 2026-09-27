"""The steps of publish-what-the-shop-knows.feature about publishing as markdown: the When that renders the role or
the process as markdown, and the Thens that say what the page holds. The feature's test module star-imports this
and no other does."""
from kb.content import dumps
from pytest_bdd import given, parsers, then, when

from driver import knol, record, whole


@when(parsers.parse("the user publishes the {thing} as markdown into a directory"), target_fixture="result")
def _publish_as_markdown(env, thing, process_name, target):
    """The process by the Background's `process_name`; the role by its name, since the Background records it from
    ROLE, which is titled Stock keeper, so its name is role/stock-keeper."""
    name = process_name if thing == "process" else "role/stock-keeper"
    return knol(env, "render", "markdown", name, "--to", str(target))


@given("the process holds steps that each say more than one thing")
def _process_steps_each_say_more_than_one_thing(env, process_name):
    steps = whole(env, process_name)["steps"]
    assert all(len(step) > 1 for step in steps)


@then("that directory holds a page showing its steps as a table with one column for each thing a step says")
def _steps_as_a_table(result, target):
    assert result.returncode == 0, result.stderr
    assert [path.name for path in target.iterdir()] == ["restock-a-shelf.md"]
    assert (target / "restock-a-shelf.md").read_text().splitlines() == [
        "# Restock a shelf",
        "",
        "**steps**",
        "",
        "| id | title | uses | with | does | branches |",
        "| --- | --- | --- | --- | --- | --- |",
        "| check-it | Check it | step/check-the-stock | name: shelf, value: dairy |  |  |",
        "| decide | Decide |  |  | Decide whether the shelf is short. | when: the shelf is short, go_to: order-more; "
        "when: it is not, go_to: stop |",
        "| order-more | Order more |  |  | Order enough to fill the shelf. |  |",
        "| stop | Stop |  |  | Leave the shelf as it is. |  |",
    ]


@given("the role holds more than one tag")
def _role_holds_more_than_one_tag(env, tmp_path, role_content):
    """Records two tags through the driver, then replaces the Background role's content through `shop-knol write`,
    as a user does: `ROLE` without its title, plus the two tags' names under `tags`."""
    stock = record(env, tmp_path, "tag", {"title": "Stock", "description": "Stock on the shelves.\n"}, "Tag stock")
    dairy = record(env, tmp_path, "tag", {"title": "Dairy", "description": "Dairy on the shelves.\n"}, "Tag dairy")
    content = {key: value for key, value in role_content.items() if key != "title"}
    content["tags"] = [stock, dairy]
    path = tmp_path / "role-with-tags.yaml"
    path.write_text(dumps(content))
    result = knol(env, "write", "role/stock-keeper", "--from", str(path), "-m", "Tag the stock keeper")
    assert result.returncode == 0, result.stderr


@then("that directory holds a page showing its tags as a bullet list")
def _tags_as_a_bullet_list(result, target):
    assert result.returncode == 0, result.stderr
    assert [path.name for path in target.iterdir()] == ["stock-keeper.md"]
    assert (target / "stock-keeper.md").read_text().splitlines() == [
        "# Stock keeper",
        "",
        "- **tags**",
        "  - tag/stock",
        "  - tag/dairy",
        "- **harness**",
        "  - **name**: stock-keeper",
        "  - **description**: Keeps the shelves stocked.",
        "  - **tools**",
        "    - Read",
        "- **shop**",
        "  - **responsible_for**: What is on the shelves",
        "",
        "## How it works",
        "",
        "Counts, then orders.",
    ]


@then("nothing on the page is a programming language's representation of a value")
def _no_repr_on_the_page(target):
    files = list(target.iterdir())
    assert len(files) == 1
    text = files[0].read_text()
    for marker in ("{'", "['", "'}", "']", '{"', '["'):
        assert marker not in text, marker


@then("that directory holds a page with the identity as a heading, the fields as a list, the sections at their levels and the parts as tables")
def _a_page(result, target):
    """The role's title as the heading, its fields in the order kb gives them (a field group's own fields nested, a list
    of plain values as a bullet list), then its section one level below the heading. The role holds no part, so no table."""
    assert result.returncode == 0, result.stderr
    assert [path.name for path in target.iterdir()] == ["stock-keeper.md"]
    assert (target / "stock-keeper.md").read_text().splitlines() == [
        "# Stock keeper",
        "",
        "- **harness**",
        "  - **name**: stock-keeper",
        "  - **description**: Keeps the shelves stocked.",
        "  - **tools**",
        "    - Read",
        "- **shop**",
        "  - **responsible_for**: What is on the shelves",
        "",
        "## How it works",
        "",
        "Counts, then orders.",
    ]
