"""The steps of publish-what-the-shop-knows.feature about a markdown page staying well-formed whatever a value holds:
the Givens that give a process step or the role a value that could break the page, each giving the outline's `page`
fixture, and the Thens that check the page's tables, its lines' ends and its values. The feature's test module
star-imports this and no other does (adrs/0035). The pages it builds come from `markdown_pages`, which no step module
star-imports."""
import re

from pytest_bdd import given, parsers, then

from driver import whole
from markdown_pages import _process_page, _role_page, _step_holding, _write_over, pages

# A backslash and the character after it, which a markdown reader takes as that character, never as a cell's end.
_ESCAPED = re.compile(r"\\.")


@given(
    "the process holds steps that each say more than one thing, one of them holding the character that separates "
    "table cells",
    target_fixture="page",
)
def _process_step_holds_the_separator(env, tmp_path, process_name):
    """The Background process's steps, the order-more step also holding a note with the character between its words;
    gives the page it publishes as, that character escaped in its cell."""
    steps = _step_holding(whole(env, process_name)["steps"], "order-more", note="milk | cream")
    _write_over(env, tmp_path, process_name, {"steps": steps}, "Say what to order")
    return _process_page(["note"], {"order-more": [r"milk \| cream"]})


@given(
    "the process holds steps that each say more than one thing, one of them holding text over more than one line",
    target_fixture="page",
)
def _process_step_holds_lines(env, tmp_path, process_name):
    """The Background process's steps, the order-more step also holding a note over two lines; gives the page it
    publishes as, the note's lines joined by a space in its cell (adrs/0041)."""
    steps = _step_holding(whole(env, process_name)["steps"], "order-more", note="Order milk first.\nThen cream.\n")
    _write_over(env, tmp_path, process_name, {"steps": steps}, "Say what to order first")
    return _process_page(["note"], {"order-more": ["Order milk first. Then cream."]})


@given("the role holds a list of plain values with an empty value among its items", target_fixture="page")
def _role_list_holds_an_empty_item(env, tmp_path, role_content, role_name):
    """The Background role, `ROLE` without its title, plus a list whose second item the user left empty; gives the
    page it publishes as, that item a bullet with nothing after its dash (adrs/0043)."""
    content = {key: value for key, value in role_content.items() if key != "title"}
    _write_over(env, tmp_path, role_name, {**content, "aisles": ["dairy", None]}, "Keeps the dairy aisle")
    return _role_page(["- **aisles**", "  - dairy", "  -"])


@given("the role holds a field whose text ends in a space", target_fixture="page")
def _role_text_ends_in_a_space(env, tmp_path, role_content, role_name):
    """The Background role, `ROLE` without its title, plus a field whose text the user ended in a space; gives the
    page it publishes as, the line ending where the text's words end (the trailing space not shown, as the user chose
    on 2026-09-27)."""
    content = {key: value for key, value in role_content.items() if key != "title"}
    _write_over(env, tmp_path, role_name, {**content, "motto": "Full shelves "}, "A motto for the stock keeper")
    return _role_page(["- **motto**: Full shelves"])


def _the_page(target) -> list[str]:
    """The lines of the one page in the directory."""
    [path] = target.iterdir()
    return path.read_text().splitlines()


def _cell_count(line: str) -> int:
    """The cells of a table row by a rule stricter than a markdown reader's own: its pipes, less the outer two, where
    a pipe after a backslash is text, not a boundary, and backslashes are paired off left to right, so only an odd
    run right before a pipe escapes it. GFM instead escapes a pipe behind any backslash at all, so this never counts
    fewer boundaries than GFM does (final review, finding 5)."""
    return _ESCAPED.sub("", line.strip()).count("|") - 1


def _tables(lines: list[str]) -> list[list[str]]:
    """Each run of consecutive lines that begin with a pipe."""
    tables, run = [], []
    for line in [*lines, ""]:
        if line.startswith("|"):
            run.append(line)
        elif run:
            tables.append(run)
            run = []
    return tables


@then("that directory holds a page where every table row has one cell for each column")
def _one_cell_for_each_column(result, target):
    assert result.returncode == 0, result.stderr
    for table in _tables(_the_page(target)):
        columns = _cell_count(table[0])
        assert [_cell_count(row) for row in table] == [columns] * len(table), table


@then("no line on the page ends in a space")
def _no_trailing_space(target):
    trailing = [line for line in _the_page(target) if line.endswith(" ")]
    assert not trailing, trailing


@then(parsers.parse("every value the {thing} holds is shown on the page"))
def _every_value_shown(target, page):
    """Each value the Given wrote, where the page the Given gave lays it out: the page, line by line."""
    assert pages(target) == page
