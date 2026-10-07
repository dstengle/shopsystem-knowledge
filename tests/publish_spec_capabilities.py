"""The steps of publish-a-shops-spec for the capabilities' files. Star-imported by the feature's test module alone
(adrs/0035)."""
from kb.content import dumps, loads
from pytest_bdd import given, parsers, then

import spec_shop
from published_from import markdown


def _page(target, name):
    """A published capability's file, split into its frontmatter and the markdown after it."""
    text = (target / "spec" / "capabilities" / f"{name}.md").read_text()
    assert text.startswith("---\n"), text
    frontmatter, _, body = text[4:].partition("---\n")
    return loads(frontmatter), body


def _expected(env, name, built, index):
    """The page the shop's `index`th capability is published as, laid out from what spec_shop gave it."""
    each = spec_shop.CAPABILITIES[index]
    frontmatter = {
        "id": built.capabilities[index], "title": each["title"], "narrator": each["narrator"],
        "rests_on": [built.decisions[at] for at in each["rests_on"]], "formulated_as": f"features/{name}.feature",
    }
    blocks = [f"# {each['title']}", "## Purpose", spec_shop.PURPOSE["body"].rstrip(), "## Behaviour",
              "\n".join(f"- {line['says']}" for line in each["behaviour"])]
    if each["not_yet"]:
        blocks += ["## Not yet", "\n".join(
            f"- **{item['title']}.** {item['defers']} Promoted when {item['trigger']}." for item in each["not_yet"])]
    line = markdown(env, built.capabilities[index])
    return f"---\n{dumps(frontmatter)}---\n{line}\n\n" + "\n\n".join(blocks) + "\n"


@then("that directory holds `spec/capabilities/<name>.md` for each capability of the shop")
def _holds_each_capability(env, result, target, built):
    assert result.returncode == 0, result.stderr
    for index, name in enumerate(capability.split("/", 1)[1] for capability in built.capabilities):
        assert (target / "spec" / "capabilities" / f"{name}.md").read_text() == _expected(env, name, built, index)


@given(parsers.parse('one of the shop\'s capabilities titled "{title}", and a feature formulating it'),
       target_fixture="formulated")
def _a_capability_and_its_feature(env, tmp_path, built, title):
    return spec_shop.ordered_capability(env, tmp_path, built.shop, title)


@then(parsers.parse("that directory holds `spec/capabilities/{name}.md` for that capability"))
def _holds_that_capability(result, target, formulated, name):
    assert result.returncode == 0, result.stderr
    frontmatter, _ = _page(target, name)
    assert frontmatter["id"] == formulated[0]


@then(parsers.parse("that directory holds `features/{name}.feature` for the feature formulating it"))
def _names_that_feature(result, target, formulated, name):
    """The capability's page names the feature file under the same name, and the file is in the directory."""
    assert result.returncode == 0, result.stderr
    frontmatter, _ = _page(target, name)
    assert frontmatter["formulated_as"] == f"features/{name}.feature"
    assert (target / "features" / f"{name}.feature").is_file()
