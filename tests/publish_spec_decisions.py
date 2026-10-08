"""The steps of publish-a-shops-spec for the ledger and the decisions' records. Star-imported by the feature's test
module alone (adrs/0035)."""
import re

from pytest_bdd import given, parsers, then

import spec_shop
from driver import whole
from published_from import markdown


def _file(number, title):
    """The record's name for a title of plain words: lower-cased, a `-` between the words."""
    return f"{number:04d}-{title.lower().replace(' ', '-')}.md"


def _ledger_of_the_shop(env, built):
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
    return "\n\n".join([markdown(env, built.shop), "# Decisions", *entries]) + "\n"


def _record(env, built, index):
    fields = spec_shop.DECISIONS[index]
    blocks = [markdown(env, built.decisions[index]), f"# {fields['number']:04d} {fields['title']}",
              f"{fields['date']}. {fields['title']}, because the shelves need it.", "The shop runs better so."]
    if "supersedes" in fields:
        blocks.append(f"Supersedes {spec_shop.DECISIONS[fields['supersedes']]['number']:04d}.")
    blocks += [f"Extends {spec_shop.DECISIONS[at]['number']:04d}." for at in fields.get("extends", [])]
    return "\n\n".join(blocks[:4]) + ("\n\n" + "\n".join(blocks[4:]) if blocks[4:] else "") + "\n"


@then("that directory holds `spec/decisions.md`")
def _holds_the_ledger(result, target, built):
    assert result.returncode == 0, result.stderr
    assert (target / "spec" / "decisions.md").is_file()


@then("the ledger lists each of the shop's decisions and each decision its capabilities rest on")
def _lists_each_decision(env, result, target, built):
    assert (target / "spec" / "decisions.md").read_text() == _ledger_of_the_shop(env, built)


@then("that directory holds `adrs/<number>-<name>.md` for each of the shop's decisions")
def _holds_each_record(env, result, target, built):
    assert result.returncode == 0, result.stderr
    for index, fields in enumerate(spec_shop.DECISIONS):
        assert (target / "adrs" / _file(fields["number"], fields["title"])).read_text() == _record(env, built, index)


@given(parsers.parse('one of the shop\'s decisions numbered {number:d}, titled "{title}"'), target_fixture="numbered")
def _a_numbered_decision(env, tmp_path, built, number, title):
    return spec_shop.numbered_decision(env, tmp_path, built.shop, number, title), title


@then(parsers.parse("that directory holds `adrs/{file}.md` for that decision"))
def _holds_that_record(result, target, numbered, file):
    assert result.returncode == 0, result.stderr
    _, title = numbered
    heading = (target / "adrs" / f"{file}.md").read_text().splitlines()[2]
    assert heading == f"# {file.split('-')[0]} {title}"


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


@given("the decisions linking to the shop are three, numbered 12, 3 and 7, created in that order")
def _three_numbered_decisions(env, tmp_path, built):
    """Beside the two the shop was built with, numbered 1 and 2: the ledger holds all five, in number order."""
    for number in (12, 3, 7):
        spec_shop.numbered_decision(env, tmp_path, built.shop, number, f"Decision {number}")


@given("another shop of the same product, with a decision linking to it", target_fixture="other")
def _another_shop_with_a_decision(env, tmp_path, built):
    return spec_shop.other_shop_decision(env, tmp_path, built.product, 9, "Aisles are swept")


def _ledger_numbers(target):
    """The number of each decision the ledger lists, in the order it lists them, read from the source it gives."""
    return [int(match) for match in re.findall(r"^source: (?:\S+: )?adrs/(\d+)-", (target / "spec" / "decisions.md").read_text(), re.M)]


@then("the ledger lists the decisions numbered 3, 7 and 12, in that order")
def _lists_in_number_order(target):
    """Numbers 3, 7 and 12 among the lowest to the highest of all the ledger lists."""
    numbers = _ledger_numbers(target)
    assert numbers == sorted(numbers) and [at for at in numbers if at in {3, 7, 12}] == [3, 7, 12], numbers


@then("the ledger does not list the other shop's decision")
def _does_not_list_the_other(target, other):
    assert f"## {other[1]}\n" not in (target / "spec" / "decisions.md").read_text()
