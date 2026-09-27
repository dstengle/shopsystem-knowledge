"""The steps of publish-what-the-shop-knows.feature about publishing as markdown: the When that renders the role or
the process as markdown, and the Thens that say what the page holds. The feature's test module star-imports this
and no other does."""
import re

from kb.content import dumps
from pytest_bdd import given, parsers, then, when

from driver import knol, record, whole

# A program's spelling of a yes, a no or nothing standing as a whole value where the page lays one out: after a field's
# colon, a bullet or a `; `, or in a table cell, and running to the line's end, a cell's end or the next `, ` or `; `
# (adrs/0043). Prose holding the word is not matched.
_PROGRAM_SPELLING = re.compile(r"(?:: |- |; |\| )(True|False|None|true|false|null)(?= \||, |; |$)", re.MULTILINE)


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
    assert not _PROGRAM_SPELLING.search(text), _PROGRAM_SPELLING.search(text)


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


def _write_over(env, tmp_path, name, content, message):
    """Replace an artifact's content through `shop-knol write`, as a user does."""
    path = tmp_path / "written-over.yaml"
    path.write_text(dumps(content))
    result = knol(env, "write", name, "--from", str(path), "-m", message)
    assert result.returncode == 0, result.stderr


@given("the role holds a field that is a yes and a field that is a no", target_fixture="page")
def _role_holds_a_yes_and_a_no(env, tmp_path, role_content):
    """The Background role, `ROLE` without its title, plus a yes and a no in the user's words; gives the page it
    publishes as."""
    content = {key: value for key, value in role_content.items() if key != "title"}
    _write_over(env, tmp_path, "role/stock-keeper", {**content, "on_call": True, "retired": False}, "On call")
    return {"stock-keeper.md": [
        "# Stock keeper",
        "",
        "- **harness**",
        "  - **name**: stock-keeper",
        "  - **description**: Keeps the shelves stocked.",
        "  - **tools**",
        "    - Read",
        "- **shop**",
        "  - **responsible_for**: What is on the shelves",
        "- **on_call**: yes",
        "- **retired**: no",
        "",
        "## How it works",
        "",
        "Counts, then orders.",
    ]}


@then(parsers.parse("that directory holds a page of the {thing}"))
def _a_page_of(result, target, page):
    """The one page the Given said the thing publishes as, line by line."""
    assert result.returncode == 0, result.stderr
    assert {path.name: path.read_text().splitlines() for path in target.iterdir()} == page


@given("the role holds a field with no value", target_fixture="page")
def _role_holds_no_value(env, tmp_path, role_content):
    """The Background role, `ROLE` without its title, plus a field the user left empty; gives the page it publishes
    as."""
    content = {key: value for key, value in role_content.items() if key != "title"}
    _write_over(env, tmp_path, "role/stock-keeper", {**content, "deputy": None}, "No deputy yet")
    return {"stock-keeper.md": [
        "# Stock keeper",
        "",
        "- **harness**",
        "  - **name**: stock-keeper",
        "  - **description**: Keeps the shelves stocked.",
        "  - **tools**",
        "    - Read",
        "- **shop**",
        "  - **responsible_for**: What is on the shelves",
        "- **deputy**:",
        "",
        "## How it works",
        "",
        "Counts, then orders.",
    ]}


@given("the process holds steps that each say more than one thing, one of them a yes and a no", target_fixture="page")
def _process_step_holds_a_yes_and_a_no(env, tmp_path, process_name):
    """The Background process's steps as its whole read gives them, the order-more step also saying it is optional
    and cannot be skipped; gives the page it publishes as."""
    steps = whole(env, process_name)["steps"]
    steps[2] = {**steps[2], "optional": True, "skippable": False}
    _write_over(env, tmp_path, process_name, {"steps": steps}, "Ordering more is optional")
    return {"restock-a-shelf.md": [
        "# Restock a shelf",
        "",
        "**steps**",
        "",
        "| id | title | uses | with | does | branches | optional | skippable |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
        "| check-it | Check it | step/check-the-stock | name: shelf, value: dairy |  |  |  |  |",
        "| decide | Decide |  |  | Decide whether the shelf is short. | when: the shelf is short, go_to: order-more; "
        "when: it is not, go_to: stop |  |  |",
        "| order-more | Order more |  |  | Order enough to fill the shelf. |  | yes | no |",
        "| stop | Stop |  |  | Leave the shelf as it is. |  |  |  |",
    ]}


@given("the process holds steps that each say more than one thing, one of them with no value", target_fixture="page")
def _process_step_holds_no_value(env, tmp_path, process_name):
    """The Background process's steps as its whole read gives them, the stop step also holding a note the user left
    empty; gives the page it publishes as."""
    steps = whole(env, process_name)["steps"]
    steps[3] = {**steps[3], "note": None}
    _write_over(env, tmp_path, process_name, {"steps": steps}, "A note to write later")
    return {"restock-a-shelf.md": [
        "# Restock a shelf",
        "",
        "**steps**",
        "",
        "| id | title | uses | with | does | branches | note |",
        "| --- | --- | --- | --- | --- | --- | --- |",
        "| check-it | Check it | step/check-the-stock | name: shelf, value: dairy |  |  |  |",
        "| decide | Decide |  |  | Decide whether the shelf is short. | when: the shelf is short, go_to: order-more; "
        "when: it is not, go_to: stop |  |",
        "| order-more | Order more |  |  | Order enough to fill the shelf. |  |  |",
        "| stop | Stop |  |  | Leave the shelf as it is. |  |  |",
    ]}
