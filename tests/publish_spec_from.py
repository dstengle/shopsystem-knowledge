"""The steps of publish-a-shops-spec for the published-from line. Star-imported by the feature's test module alone
(adrs/0035)."""
from pytest_bdd import parsers, then

import spec_shop
from driver import whole
from shop_knowledge.renderers import names

LINE = "published from the knowledge base"


def _page_names():
    """The names the publisher gives the pages of the shop's capabilities and their features: its naming of their titles."""
    return [names.from_title(each["title"]) for each in spec_shop.CAPABILITIES]


def _files(label, built, target):
    """The published files the example's `file` names, each with the name of the artifact it is published from."""
    if label == "`spec/index.md`":
        return [(target / "spec" / "index.md", built.shop)]
    if label == "`spec/decisions.md`":
        return [(target / "spec" / "decisions.md", built.shop)]
    if label == "each capability's file":
        return [(target / "spec" / "capabilities" / f"{page}.md", name) for page, name in zip(_page_names(), built.capabilities)]
    if label == "each feature file":
        return [(target / "features" / f"{page}.feature", feature) for page, feature in zip(_page_names(), built.features)]
    assert label == "each decision's record", label
    return list(zip(sorted((target / "adrs").glob("*.md")), built.decisions))


@then(parsers.parse("{file} carries a line saying it was published from the knowledge base and is not to be edited by hand"),
      target_fixture="published")
def _carries_the_line(result, target, built, file):
    assert result.returncode == 0, result.stderr
    published = _files(file, built, target)
    assert published
    for path, _ in published:
        lines = [line for line in path.read_text().splitlines() if LINE in line]
        assert len(lines) == 1 and "do not edit by hand" in lines[0], (path, lines)
        assert lines[0].startswith("#" if path.suffix == ".feature" else "<!--"), lines[0]
    return published


@then(parsers.parse("that line names {subject} and {again}'s revision"))
def _names_what_it_is_published_from(env, published):
    for path, name in published:
        line = next(line for line in path.read_text().splitlines() if LINE in line)
        assert f"{name}@{whole(env, name)['revision']}" in line, (path, line)


@then(parsers.parse("that line is {where}"))
def _is_placed(published, where):
    for path, _ in published:
        lines = path.read_text().splitlines()
        at = next(index for index, line in enumerate(lines) if LINE in line)
        if where.startswith("directly after the frontmatter"):
            assert lines[0] == "---" and lines.index("---", 1) == at - 1, (path, at)
        else:
            assert at == 0, (path, at)
