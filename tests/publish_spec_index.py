"""The steps of publish-a-shops-spec for the spec's index. Star-imported by the feature's test module alone (adrs/0035)."""
import pytest
from pytest_bdd import then, when

import spec_shop
from driver import knol
from published_from import markdown


@pytest.fixture
def target(tmp_path):
    """The directory the user publishes the shop's spec into, there and empty before they do."""
    target = tmp_path / "published"
    target.mkdir()
    return target


@pytest.fixture
def observed(env, built):
    """Extends conftest's `observed`: the history and each artifact of the shop's spec, read whole."""
    def _snapshot():
        names = [built.product, built.shop, *built.capabilities, *built.decisions, *built.features]
        return {"journal": knol(env, "journal").stdout, **{name: knol(env, "read", name, "--whole").stdout for name in names}}
    return _snapshot


@when("the user publishes the shop's spec into a directory", target_fixture="result")
def _publish_the_spec(env, built, target, before):
    """Asks for `before` so the knowledge base is taken as it was before the command runs."""
    return knol(env, "render", "spec", built.shop, "--to", str(target))


def _names(built):
    return [capability.split("/", 1)[1] for capability in built.capabilities]


def _joined(names):
    """Names joined with commas and a final "and"."""
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def _expected_index(env, built):
    names = _names(built)
    constraints = [
        f"- **{each['title']}.** {each['says']} Pinned in {_joined([names[index] for index in each['pinned']])}."
        for each in spec_shop.CONSTRAINTS
    ]
    composition = [
        f"{number}. [{name}](capabilities/{name}.md): {each['gist']}"
        for number, (name, each) in enumerate(zip(names, spec_shop.CAPABILITIES), 1)
    ]
    blocks = [markdown(env, built.shop), "# Shelves", "## Purpose", spec_shop.PURPOSE["body"].rstrip(), "## Constraints carried", "\n".join(constraints),
              "## Composition (reading order)", "\n".join(composition)]
    for section in spec_shop.SHOP_SECTIONS[1:]:
        blocks += [f"## {section['title']}", section["body"].rstrip()]
    return "\n\n".join(blocks) + "\n"


@then("that directory holds `spec/index.md` from the shop")
def _holds_the_index(env, result, target, built):
    assert result.returncode == 0, result.stderr
    assert (target / "spec" / "index.md").read_text() == _expected_index(env, built)
