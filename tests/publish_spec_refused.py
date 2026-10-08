"""The steps of publish-a-shops-spec for the spec a shop's publishing refuses. Star-imported by the feature's test
module alone (adrs/0035). Every refusal is shop-knol's own, in plain words, so each Then checks the reason it gives and
the names it gives it for, never the whole line."""
from pytest_bdd import given, parsers, then

import spec_shop
from publish_refusals import capability as _capability, feature_of as _feature_of, lines_naming as _lines_naming
from published_from import markdown


@given("another shop of the same product", target_fixture="other_shop")
def _another_shop(env, tmp_path, built):
    return spec_shop.put(env, tmp_path, "shop", "Aisles", product=built.product, gist="Keeps the aisles.")


@given(parsers.parse('two of the shop\'s capabilities, each with an order of its own, titled "{first}" and "{second}"'),
       target_fixture="refused_for")
def _two_capabilities(env, tmp_path, built, first, second):
    both = [_capability(env, tmp_path, built.shop, title, order) for order, title in ((3, first), (4, second))]
    return ["would share", both]


@then("publishing is rejected because those capabilities would share a file, naming both")
def _rejected_shared_capabilities(result, refused_for):
    _lines_naming(result, *refused_for)


@given(parsers.parse('two of the shop\'s decisions numbered {number:d}, titled "{first}" and "{second}"'), target_fixture="refused_for")
def _two_decisions(env, tmp_path, built, number, first, second):
    both = [spec_shop.numbered_decision(env, tmp_path, built.shop, number, title) for title in (first, second)]
    return ["would share" if first.lower() == second.lower() else "a number names one decision", both]


@then("publishing is rejected because those decisions would share a file, naming both")
def _rejected_shared_decisions(result, refused_for):
    _lines_naming(result, *refused_for)


@then("publishing is rejected because a number names one decision, naming both decisions")
def _rejected_shared_number(result, refused_for):
    _lines_naming(result, *refused_for)


@given("two features that each formulate the same one of the shop's capabilities", target_fixture="refused_for")
def _two_features(env, tmp_path, built):
    capability, first = spec_shop.ordered_capability(env, tmp_path, built.shop, "Wipe the counter")
    return ["would share", [first, _feature_of(env, tmp_path, capability, "Wipe the counter again", {})]]


@then("publishing is rejected because those features would share a file, naming both")
def _rejected_shared_features(result, refused_for):
    _lines_naming(result, *refused_for)


@given("a scenario in a feature formulating one of the shop's capabilities, whose uses points at another of the shop's capabilities",
       target_fixture="refused_for")
def _a_scenario_using_its_own_shop(env, tmp_path, built):
    capability = _capability(env, tmp_path, built.shop, "Mop the floor")
    feature = _feature_of(env, tmp_path, capability, "Mop the floor", {"uses": [built.capabilities[0]]})
    return ["uses only another shop's capability", [feature, "Mop the floor, as the user does it"]]


@then("publishing is rejected because a scenario uses only another shop's capability, naming that scenario")
def _rejected_used(result, refused_for):
    _lines_naming(result, *refused_for)


@given("a scenario in a feature formulating one of the shop's capabilities, whose step's table has a row with fewer cells than its header",
       target_fixture="refused_for")
def _a_scenario_with_a_ragged_table(env, tmp_path, built):
    capability = _capability(env, tmp_path, built.shop, "Shelve the tins")
    steps = [{"keyword": "When", "text": "the user acts", "table": [["tin", "shelf"], ["beans"]]},
             {"keyword": "Then", "text": "the shelf is in order"}]
    feature = _feature_of(env, tmp_path, capability, "Shelve the tins", {"steps": steps})
    return ["must each have one cell per column", [feature, "Shelve the tins, as the user does it"]]


@then("publishing is rejected because a table's rows must each have one cell per column, naming that scenario")
def _rejected_ragged(result, refused_for):
    _lines_naming(result, *refused_for)


@given(
    "a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to another shop of the same product"
)
def _a_directory_holding_an_old_record(env, tmp_path, built, target, kept):
    """The directory is the published one, which holds the old record: a file carrying the published-from line of a
    decision of another shop."""
    _, decision = spec_shop.other_shop_decision(env, tmp_path, built.product, 99, "Old rule")
    _old_record(env, target, kept, decision)


@given("a directory holding `adrs/0099-old-rule.md`, whose published-from line names a decision linking to the other shop")
def _a_directory_holding_the_other_shops_old_record(env, tmp_path, built, target, kept, other_shop):
    """The same, the decision linking to the other shop the scenario already made."""
    _old_record(env, target, kept, spec_shop.numbered_decision(env, tmp_path, other_shop, 99, "Old rule"))


def _old_record(env, target, kept, decision):
    file = target / "adrs" / "0099-old-rule.md"
    file.parent.mkdir()
    file.write_text(f"{markdown(env, decision)}\n\n# 0099 Old rule\n")
    kept[file] = file.read_text()


def _files(target):
    return {file: file.read_text() for file in target.rglob("*") if file.is_file()}


@then("nothing is written to the directory")
def _nothing_written(target, kept):
    """The directory holds what it held before the publish: nothing, or the files the scenario put there."""
    assert _files(target) == kept


@then("`adrs/0099-old-rule.md` is still in that directory")
def _the_old_record_is_still_there(target, kept):
    file = target / "adrs" / "0099-old-rule.md"
    assert file.is_file() and file.read_text() == kept[file]


@given(parsers.re(r"a capability linking to (?P<owner>the shop|the other shop) whose status is retired"), target_fixture="retiree")
def _a_retired_capability_of(env, tmp_path, built, request, owner):
    shop = request.getfixturevalue("other_shop") if owner == "the other shop" else built.shop
    return spec_shop.retired_capability(env, tmp_path, shop, "Old cache")[0]


@given(parsers.parse("a capability linking to the shop whose status is {status} depends on that retired capability"),
       target_fixture="refused_for")
def _a_capability_depending_on_it(env, tmp_path, built, retiree, status):
    lines = [{"title": "Only line", "says": "When asked, it answers."}]
    dependent = spec_shop.put(env, tmp_path, "capability", "Sweep the floor", shop=built.shop, gist="A capability.",
                              behaviour=lines, order="3", status=status)
    spec_shop.depend_on(env, tmp_path, dependent, [retiree])
    return ["a retired capability", [dependent, retiree]]


@then("publishing is rejected because it depends on a retired capability, naming both capabilities")
def _rejected_depending_on_retired(result, refused_for):
    _lines_naming(result, *refused_for)
