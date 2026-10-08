"""The steps of publish-a-shops-spec for the capabilities' files. Star-imported by the feature's test module alone
(adrs/0035)."""
from kb.content import dumps, loads
from pytest_bdd import given, parsers, then

import spec_shop
from driver import whole
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


@given("one of the capabilities linking to the shop is deprecated", target_fixture="deprecated")
def _one_is_deprecated(env, tmp_path, built):
    spec_shop.deprecate(env, tmp_path, built.capabilities[1])
    return built.capabilities[1]


@then("that directory holds that capability's page")
def _holds_the_deprecated_page(result, target, deprecated):
    assert result.returncode == 0, result.stderr
    assert (target / "spec" / "capabilities" / f"{deprecated.split('/', 1)[1]}.md").is_file()


@then("that page says the capability is deprecated")
def _page_says_deprecated(result, target, deprecated):
    frontmatter, _ = _page(target, deprecated.split("/", 1)[1])
    assert frontmatter["status"] == "deprecated"


@then("that capability's line in the index says it is deprecated")
def _index_says_deprecated(result, target, deprecated):
    name = deprecated.split("/", 1)[1]
    lines = [line for line in (target / "spec" / "index.md").read_text().splitlines() if f"[{name}](" in line]
    assert len(lines) == 1 and lines[0].endswith(" (deprecated)"), lines


@then("that directory holds `spec/capabilities/<name>.md` for each capability linking to the shop whose status is active or deprecated")
def _holds_each_capability(env, result, target, built):
    """An active capability's page is laid out whole; a deprecated one's is there."""
    assert result.returncode == 0, result.stderr
    for index, name in enumerate(capability.split("/", 1)[1] for capability in built.capabilities):
        page = target / "spec" / "capabilities" / f"{name}.md"
        if whole(env, built.capabilities[index])["status"] == "active":
            assert page.read_text() == _expected(env, name, built, index)
        else:
            assert page.is_file()


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


@given("a capability linking to the shop whose status is retired, and a feature formulating it", target_fixture="retired")
def _a_retired_capability(env, tmp_path, built):
    return spec_shop.retired_capability(env, tmp_path, built.shop, "Old cache")


@then("that directory holds no page for that capability")
def _holds_no_page(result, target, retired):
    assert result.returncode == 0, result.stderr
    assert not (target / "spec" / "capabilities" / "old-cache.md").exists()


@then("that directory holds no feature file for it")
def _holds_no_feature(result, target, retired):
    assert result.returncode == 0, result.stderr
    assert not (target / "features" / "old-cache.feature").exists()


@then("the index does not list it")
def _index_lists_not(result, target, retired):
    assert "old-cache" not in (target / "spec" / "index.md").read_text()
