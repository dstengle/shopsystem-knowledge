import re

import pytest
from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start, whole
from markdown_well_formed import *  # noqa: F403  pytest-bdd registers steps only through a star import
from publish_as_markdown import *  # noqa: F403  pytest-bdd registers steps only through a star import
from publish_refused import *  # noqa: F403  pytest-bdd registers steps only through a star import

scenarios("publish-what-the-shop-knows.feature")

CHECK_THE_STOCK = {"title": "Check the stock", "does": "Count what is on the shelf, front and back.\n", "settings": ["shelf"]}
ROLE = {
    "title": "Stock keeper",
    "harness": {"name": "stock-keeper", "description": "Keeps the shelves stocked.", "tools": ["Read"]},
    "shop": {"responsible_for": "What is on the shelves"},
    "sections": [{"title": "How it works", "body": "Counts, then orders.\n"}],
}


@pytest.fixture
def observed(env, process_name):
    """Extends conftest's `observed`: what shop-knol shows of the knowledge base a skill is published from, its
    history and the process and the shared step it uses, each read whole."""
    def _snapshot():
        return {"journal": knol(env, "journal").stdout, **{
            name: whole(env, name) for name in (process_name, "step/check-the-stock")
        }}
    return _snapshot


@pytest.fixture
def role_content():
    """The Background role's content, so a sibling module can change what it asks for without importing ROLE
    directly."""
    return ROLE


@pytest.fixture
def target(tmp_path):
    """The directory the user publishes into, there and empty before they do."""
    target = tmp_path / "published"
    target.mkdir()
    return target


@pytest.fixture
def role_name():
    """The role the user publishes as an agent, or as markdown: the Background's, unless a Given names another."""
    return "role/stock-keeper"


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


@when("the user publishes the process as a diagram into a directory", target_fixture="result")
def _publish_as_a_diagram(env, process_name, target):
    return knol(env, "render", "diagram", process_name, "--to", str(target))


@then("that directory holds a diagram of the process's steps and their branches")
def _a_diagram(result, target):
    """One node a step, in order and numbered, the reused step drawn as a subroutine; a step without branches goes on to
    the next, and a step with them goes where each says, labelled with its condition. Nothing places a node."""
    assert result.returncode == 0, result.stderr
    assert [path.name for path in target.iterdir()] == ["restock-a-shelf.mmd"]
    assert (target / "restock-a-shelf.mmd").read_text().splitlines() == [
        "flowchart TD",
        '    step1[["1. Check it"]]',
        '    step2["2. Decide"]',
        '    step3["3. Order more"]',
        '    step4["4. Stop"]',
        "    step1 --> step2",
        '    step2 -->|"the shelf is short"| step3',
        '    step2 -->|"it is not"| step4',
        "    step3 --> step4",
    ]


@when("the user publishes the role as an agent into a directory", target_fixture="result")
def _publish_as_an_agent(env, role_name, target):
    return knol(env, "render", "agent", role_name, "--to", str(target))


@then("that directory holds an agent whose heading block is the role's harness fields and whose body is the role's prose")
def _an_agent(result, target):
    """The one file under the directory: the role's harness group as its heading block, then its sections as the body,
    each a heading and its text, and nothing of the role's shop fields."""
    assert result.returncode == 0, result.stderr
    files = [path.relative_to(target) for path in target.rglob("*") if path.is_file()]
    assert [str(path) for path in files] == [".claude/agents/stock-keeper.md"]
    heading, body = _heading_block_and_body((target / files[0]).read_text())
    assert heading == ROLE["harness"]
    for section in ROLE["sections"]:
        assert f"# {section['title']}\n\n{section['body'].rstrip()}" in body
        assert f"# {section['title']}" in body.splitlines()
    assert ROLE["shop"]["responsible_for"] not in body
