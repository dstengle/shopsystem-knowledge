"""The steps of publish-a-shops-spec for the links of a shop's capabilities that publishing refuses. Star-imported by
the feature's test module alone (adrs/0035). Each Then checks the reason shop-knol gives and the names it gives it for."""
import pytest
from pytest_bdd import given, parsers, then

import spec_shop
from driver import whole
from publish_refusals import capability, feature_of, lines_naming


@given(parsers.parse('two of the shop\'s capabilities, both active, both at order {order:d}, titled "{first}" and "{second}"'),
       target_fixture="refused_for")
def _two_at_one_order(env, tmp_path, built, order, first, second):
    both = [spec_shop.put(env, tmp_path, "capability", title, shop=built.shop, gist="A capability.", order=str(order),
                          behaviour=[{"title": "Only line", "says": "When asked, it answers."}]) for title in (first, second)]
    return ["an order places one capability", both]


@then("publishing is rejected because an order places one capability, naming both capabilities")
def _rejected_one_order(result, refused_for):
    lines_naming(result, *refused_for)


@pytest.fixture
def other_shop(other):
    """The other shop of a scenario whose Given made it with a decision (`other`: the shop and the decision), for the
    steps that take the other shop as the scenarios that made only a shop give it."""
    return other[0]


@then("publishing is rejected because a capability rests only on its own shop's decisions, naming that capability and that decision")
def _rejected_borrowed(result, built, other):
    lines_naming(result, "a capability rests only on its own shop's decisions", [built.capabilities[0], other[1]])


@pytest.fixture
def formulated():
    """The capability of the shop whose scenario a Given made, kept for the Given that follows."""
    return []


@given("another shop of the same product, with an active capability linking to it", target_fixture="other")
def _another_shop_with_a_capability(env, tmp_path, built):
    shop = spec_shop.put(env, tmp_path, "shop", "Aisles", product=built.product, gist="Keeps the aisles.")
    lines = [{"title": "Only line", "says": "When asked, it answers."}]
    return shop, spec_shop.put(env, tmp_path, "capability", "Stack the crates", shop=shop, gist="A capability.", behaviour=lines)


@given("a scenario in a feature formulating one of the shop's capabilities, whose uses names that other shop's capability",
       target_fixture="refused_for")
def _a_scenario_using_it(env, tmp_path, built, other, formulated):
    formulated.append(capability(env, tmp_path, built.shop, "Mop the floor"))
    feature_of(env, tmp_path, formulated[0], "Mop the floor", {"uses": [other[1]]})
    return ["a scenario uses only what its capability depends on", ["Mop the floor, as the user does it", other[1]]]


@given("the scenario's capability does not depend on that other shop's capability")
def _the_capability_does_not_depend_on_it(env, formulated, other):
    assert other[1] not in whole(env, formulated[0]).get("depends_on", [])


@then("publishing is rejected because a scenario uses only what its capability depends on, naming that scenario and the capability it uses")
def _rejected_undepended(result, refused_for):
    lines_naming(result, *refused_for)
