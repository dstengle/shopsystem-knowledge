"""The steps of publish-a-shops-spec for the spec a shop's publishing refuses. Star-imported by the feature's test
module alone (adrs/0035). Every refusal is shop-knol's own, in plain words, so each Then checks the reason it gives and
the names it gives it for, never the whole line."""
from pytest_bdd import given, parsers, then

import spec_shop
from decision_fields import decided
from driver import record


def _lines_naming(result, reason, names):
    """The refusal is shop-knol's, as one line holding the reason and every one of the names."""
    assert result.returncode == 1 and result.stdout == "", (result.returncode, result.stdout)
    lines = [line for line in result.stderr.splitlines() if reason in line]
    assert any(all(name in line for name in names) for line in lines), result.stderr


def _capability(env, tmp_path, shop, title):
    line = {"title": "Only line", "says": "When asked, it answers."}
    return spec_shop.put(env, tmp_path, "capability", title, shop=shop, gist="A capability.", behaviour=[line])


@given("a capability that names the shop but is not in the shop's reading order", target_fixture="refused_for")
def _a_capability_left_out(env, tmp_path, built):
    return ["is not in the shop's reading order", [_capability(env, tmp_path, built.shop, "Count the bags")]]


@then("publishing is rejected because that capability is not in the shop's reading order, naming that capability")
def _rejected_left_out(result, refused_for):
    _lines_naming(result, *refused_for)


@given("another shop of the same product", target_fixture="other_shop")
def _another_shop(env, tmp_path, built):
    return spec_shop.put(env, tmp_path, "shop", "Aisles", product=built.product, gist="Keeps the aisles.")


@given("a capability that names the other shop is in the shop's reading order", target_fixture="refused_for")
def _a_foreign_capability_in_order(env, tmp_path, built, other_shop):
    foreign = _capability(env, tmp_path, other_shop, "Sweep the aisles")
    spec_shop.reading_order(env, tmp_path, built.shop, [*built.capabilities, foreign])
    return ["belongs to another shop", [foreign]]


@then("publishing is rejected because that capability belongs to another shop, naming that capability")
def _rejected_foreign(result, refused_for):
    _lines_naming(result, *refused_for)


@given(parsers.parse('two of the shop\'s capabilities titled "{first}" and "{second}"'), target_fixture="refused_for")
def _two_capabilities(env, tmp_path, built, first, second):
    both = [_capability(env, tmp_path, built.shop, first), _capability(env, tmp_path, built.shop, second)]
    spec_shop.reading_order(env, tmp_path, built.shop, [*built.capabilities, *both])
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


@given("one of the shop's capabilities rests on a decision that no shop names among its decisions", target_fixture="refused_for")
def _rests_on_an_unnamed_decision(env, tmp_path, built):
    decision = spec_shop.put(env, tmp_path, "decision", "Nobody owns this", **decided(5))
    spec_shop.rest_on(env, tmp_path, built.capabilities[0], decision)
    return ["belongs to no shop", [decision]]


@then("publishing is rejected because that decision belongs to no shop, naming it")
def _rejected_unowned(result, refused_for):
    _lines_naming(result, *refused_for)


def _feature_of(env, tmp_path, capability, title, scenario):
    return record(env, tmp_path, "feature", {"title": title, "formulates": capability, "scenarios": [{
        "title": f"{title}, as the user does it", "formulates": f"{capability}#behaviour/{spec_shop.line_id(env, capability, 'Only line')}",
        "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "the shelf is in order"}], **scenario}]},
        f"Formulate {title}")


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
    spec_shop.reading_order(env, tmp_path, built.shop, [*built.capabilities, capability])
    feature = _feature_of(env, tmp_path, capability, "Mop the floor", {"uses": [built.capabilities[0]]})
    return ["uses only another shop's capability", [feature, "Mop the floor, as the user does it"]]


@then("publishing is rejected because a scenario uses only another shop's capability, naming that scenario")
def _rejected_used(result, refused_for):
    _lines_naming(result, *refused_for)


@given("a scenario in a feature formulating one of the shop's capabilities, whose step's table has a row with fewer cells than its header",
       target_fixture="refused_for")
def _a_scenario_with_a_ragged_table(env, tmp_path, built):
    capability = _capability(env, tmp_path, built.shop, "Shelve the tins")
    spec_shop.reading_order(env, tmp_path, built.shop, [*built.capabilities, capability])
    steps = [{"keyword": "When", "text": "the user acts", "table": [["tin", "shelf"], ["beans"]]},
             {"keyword": "Then", "text": "the shelf is in order"}]
    feature = _feature_of(env, tmp_path, capability, "Shelve the tins", {"steps": steps})
    return ["must each have one cell per column", [feature, "Shelve the tins, as the user does it"]]


@then("publishing is rejected because a table's rows must each have one cell per column, naming that scenario")
def _rejected_ragged(result, refused_for):
    _lines_naming(result, *refused_for)


@then("nothing is written to the directory")
def _nothing_written(target):
    assert list(target.iterdir()) == []
