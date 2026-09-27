"""The markdown pages the publish feature's steps expect, built once for both its step modules: `publish_as_markdown`
and `markdown_well_formed` each import this plainly, as `driver.py` is (adrs/0035). It holds no step of its own."""
from kb.content import dumps

from driver import knol


def pages(target) -> dict:
    """Every page in `target`, by file name, as its lines: the one reader `_a_page_of` and `_every_value_shown` both
    assert with."""
    return {path.name: path.read_text().splitlines() for path in target.iterdir()}


def _write_over(env, tmp_path, name, content, message):
    """Replace an artifact's content through `shop-knol write`, as a user does."""
    path = tmp_path / "written-over.yaml"
    path.write_text(dumps(content))
    result = knol(env, "write", name, "--from", str(path), "-m", message)
    assert result.returncode == 0, result.stderr


def _role_page(extra=()):
    """The role's base page (its harness and shop fields, then its section as `## How it works`). `extra` is the
    lines a Given's own field adds or changes, spliced in before the section, so each row's own lines stay the only
    thing said once for it."""
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
        *extra,
        "",
        "## How it works",
        "",
        "Counts, then orders.",
    ]}


def _row(cells):
    """One table row of the process's expected page, its cells between pipes."""
    return "| " + " | ".join(cells) + " |"


_STEP_ROWS = {
    "check-it": ["check-it", "Check it", "step/check-the-stock", "name: shelf, value: dairy", "", ""],
    "decide": [
        "decide", "Decide", "", "", "Decide whether the shelf is short.",
        "when: the shelf is short, go_to: order-more; when: it is not, go_to: stop",
    ],
    "order-more": ["order-more", "Order more", "", "", "Order enough to fill the shelf.", ""],
    "stop": ["stop", "Stop", "", "", "Leave the shelf as it is.", ""],
}


def _process_page(columns, cells):
    """The process's expected page: its table's six base columns for every step, plus `columns`, each step's cells
    there taken from `cells` by id, empty where a step holds none of its own."""
    header = ["id", "title", "uses", "with", "does", "branches", *columns]
    rows = [[*_STEP_ROWS[step_id], *cells.get(step_id, [""] * len(columns))] for step_id in _STEP_ROWS]
    lines = ["# Restock a shelf", "", "**steps**", "", _row(header), _row(["---"] * len(header))]
    lines += [_row(row) for row in rows]
    return {"restock-a-shelf.md": lines}


def _step_holding(steps, step_id, **fields):
    """`steps`, in the same order, the one whose id is `step_id` given `fields` besides its own. Refuses (`ValueError`)
    an id no step holds, rather than passing `steps` through unchanged."""
    if step_id not in {step["id"] for step in steps}:
        raise ValueError(f"no step holds the id {step_id!r}")
    return [{**step, **fields} if step["id"] == step_id else step for step in steps]
