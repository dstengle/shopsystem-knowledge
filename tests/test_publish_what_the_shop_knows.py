import re

import pytest
from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("publish-what-the-shop-knows.feature")

CHECK_THE_STOCK = {"title": "Check the stock", "does": "Count what is on the shelf, front and back.\n", "settings": ["shelf"]}
ROLE = {
    "title": "Stock keeper",
    "harness": {"name": "stock-keeper", "description": "Keeps the shelves stocked.", "tools": ["Read"]},
    "shop": {"responsible_for": "What is on the shelves"},
    "sections": [{"title": "How it works", "body": "Counts, then orders.\n"}],
}


@given(
    "a shop knowledge base holding a process whose steps include a branch and a reused shared step, and a role",
    target_fixture="process_name",
)
def _shop_with_a_process_and_a_role(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "step", CHECK_THE_STOCK, "Share the stock check")
    record(env, tmp_path, "role", ROLE, "Describe the stock keeper")
    return record(env, tmp_path, "process", {
        "title": "Restock a shelf",
        "steps": [
            {"title": "Check it", "uses": "step/check-the-stock", "with": [{"name": "shelf", "value": "dairy"}]},
            {
                "title": "Decide",
                "does": "Decide whether the shelf is short.\n",
                "branches": [{"when": "the shelf is short", "go_to": "order-more"}, {"when": "it is not", "go_to": "stop"}],
            },
            {"title": "Order more", "does": "Order enough to fill the shelf.\n"},
            {"title": "Stop", "does": "Leave the shelf as it is.\n"},
        ],
    }, "Describe restocking a shelf")


def _everything_under(directory):
    # Reads the knowledge base's files directly, to observe that no shop-knol command changed them (CLAUDE.md, Step definitions).
    return {path.relative_to(directory): path.read_bytes() for path in sorted(directory.rglob("*")) if path.is_file()}


@pytest.fixture
def target(tmp_path):
    """The directory the user publishes into, there and empty before they do."""
    target = tmp_path / "published"
    target.mkdir()
    return target


@pytest.fixture
def before(shop):
    """Every file of the shop's knowledge base, byte for byte, as it was when first asked for."""
    return _everything_under(shop / "kb")


@when("the user publishes the process as a skill into a directory", target_fixture="result")
def _publish_as_a_skill(env, process_name, target, before):
    """Asks for `before` so the knowledge base is taken as it was before the command runs."""
    return knol(env, "render", "skill", process_name, "--to", str(target))


def _heading_block_and_body(text):
    match = re.fullmatch(r"---\n(.*?)---\n\n(.*)", text, re.DOTALL)
    assert match, text
    return loads(match.group(1)), match.group(2)


@then(
    "that directory holds a skill whose heading block is the process's identity and whose body is its steps, "
    "with the reused step written out in full"
)
def _a_skill(result, target):
    assert result.returncode == 0, result.stderr
    heading, body = _heading_block_and_body((target / "restock-a-shelf" / "SKILL.md").read_text())
    assert heading == {"name": "restock-a-shelf", "description": "Restock a shelf"}
    assert body.splitlines() == [
        "# Restock a shelf", "",
        "## 1. Check it", "",
        "This is the shared step Check the stock, where shelf is dairy.", "",
        "Count what is on the shelf, front and back.", "",
        "## 2. Decide", "",
        "Decide whether the shelf is short.", "",
        "- If the shelf is short, go to step 3 (Order more).",
        "- If it is not, go to step 4 (Stop).", "",
        "## 3. Order more", "",
        "Order enough to fill the shelf.", "",
        "## 4. Stop", "",
        "Leave the shelf as it is.",
    ]


@then("the shop's knowledge base is unchanged")
def _unchanged(shop, before):
    assert _everything_under(shop / "kb") == before
