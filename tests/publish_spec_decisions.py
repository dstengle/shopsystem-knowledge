"""The steps of publish-a-shops-spec for the ledger and the decisions' records. Star-imported by the feature's test
module alone (adrs/0035)."""
from pytest_bdd import given, parsers, then

import spec_shop
from driver import whole


def _file(number, title):
    """The record's name for a title of plain words: lower-cased, a `-` between the words."""
    return f"{number:04d}-{title.lower().replace(' ', '-')}.md"


def _ledger_of_the_shop(built):
    """The ledger of the shop built by spec_shop, whose capabilities rest on its own decisions alone."""
    entries = []
    for index, fields in enumerate(spec_shop.DECISIONS):
        lines = [f"date: {fields['date']}"]
        if "revisit_when" in fields:
            lines.append(f"revisit_when: {fields['revisit_when']}")
        if "supersedes" in fields:
            lines.append(f"supersedes: {built.decisions[fields['supersedes']]}")
        lines.append(f"source: adrs/{_file(fields['number'], fields['title'])}")
        entries.append("\n\n".join([f"## {built.decisions[index]}", fields["statement"], "\n".join(lines)]))
    return "\n\n".join(["# Decisions", *entries]) + "\n"


def _record(built, index):
    fields = spec_shop.DECISIONS[index]
    blocks = [f"# {fields['number']:04d} {fields['title']}",
              f"{fields['date']}. {fields['title']}, because the shelves need it.", "The shop runs better so."]
    if "supersedes" in fields:
        blocks.append(f"Supersedes {spec_shop.DECISIONS[fields['supersedes']]['number']:04d}.")
    blocks += [f"Extends {spec_shop.DECISIONS[at]['number']:04d}." for at in fields.get("extends", [])]
    return "\n\n".join(blocks[:3]) + ("\n\n" + "\n".join(blocks[3:]) if blocks[3:] else "") + "\n"


@then("that directory holds `spec/decisions.md`")
def _holds_the_ledger(result, target, built):
    assert result.returncode == 0, result.stderr
    assert (target / "spec" / "decisions.md").is_file()


@then("the ledger lists each of the shop's decisions and each decision its capabilities rest on")
def _lists_each_decision(result, target, built):
    assert (target / "spec" / "decisions.md").read_text() == _ledger_of_the_shop(built)


@then("that directory holds `adrs/<number>-<name>.md` for each of the shop's decisions")
def _holds_each_record(result, target, built):
    assert result.returncode == 0, result.stderr
    for index, fields in enumerate(spec_shop.DECISIONS):
        assert (target / "adrs" / _file(fields["number"], fields["title"])).read_text() == _record(built, index)


@given(parsers.parse('one of the shop\'s decisions numbered {number:d}, titled "{title}"'), target_fixture="numbered")
def _a_numbered_decision(env, tmp_path, built, number, title):
    return spec_shop.numbered_decision(env, tmp_path, built.shop, number, title), title


@then(parsers.parse("that directory holds `adrs/{file}.md` for that decision"))
def _holds_that_record(result, target, numbered, file):
    assert result.returncode == 0, result.stderr
    _, title = numbered
    assert (target / "adrs" / f"{file}.md").read_text().startswith(f"# {file.split('-')[0]} {title}\n")


@given("the shop's capabilities rest on decisions of the shop")
def _rest_on_the_shops_own(built):
    """The shop spec_shop builds is so: its capabilities rest on its own decisions alone."""


@then("every entry in the ledger is a decision the knowledge base holds")
def _every_entry_is_held(env, result, target):
    assert result.returncode == 0, result.stderr
    headings = [line[3:] for line in (target / "spec" / "decisions.md").read_text().splitlines() if line.startswith("## ")]
    assert headings
    for name in headings:
        assert whole(env, name)["type"] == "decision"


@given("another shop of the same product holds a decision", target_fixture="other")
def _another_shop_holds_a_decision(env, tmp_path, built):
    shop, decision = spec_shop.other_shop_decision(env, tmp_path, built.product, 9, "Aisles are swept")
    return shop, decision


@given("one of the shop's capabilities rests on that decision")
def _a_capability_rests_on_it(env, tmp_path, built, other):
    spec_shop.rest_on(env, tmp_path, built.capabilities[0], other[1])


@then("the ledger lists that decision after the shop's own decisions")
def _lists_it_after(result, target, built, other):
    assert result.returncode == 0, result.stderr
    headings = [line[3:] for line in (target / "spec" / "decisions.md").read_text().splitlines() if line.startswith("## ")]
    assert headings == [*built.decisions, other[1]]


@then("the ledger gives that decision's source as the other shop's record of it")
def _gives_the_other_shops_record(result, target, other):
    text = (target / "spec" / "decisions.md").read_text()
    entry = text[text.index(f"## {other[1]}"):]
    assert entry.endswith(f"source: {other[0]}: adrs/{_file(9, 'Aisles are swept')}\n")
