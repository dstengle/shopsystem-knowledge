"""The steps of follow-the-links that follow the links into a capability. Star-imported by the feature's test module
alone (adrs/0035)."""
from pytest_bdd import given, parsers, then, when

import spec_shop
from driver import knol, record


@given(parsers.parse('the shops "{first}" and "{second}" of the product "{product}"'), target_fixture="built")
def _two_shops(env, tmp_path, first, second, product):
    """The product and its two shops, and (as capabilities are recorded) the names kb minted for them."""
    made = spec_shop.put(env, tmp_path, "product", product, gist="A product.")
    return {"shops": {each: spec_shop.put(env, tmp_path, "shop", each, product=made, gist="Keeps the shop.") for each in (first, second)},
            "capabilities": {}}


@given(parsers.re(r'the capability "(?P<title>[^"]+)" of the shop "(?P<shop>[^"]+)"(?:, depending on "(?P<target>[^"]+)")?$'))
def _a_capability(env, tmp_path, built, title, shop, target):
    """A capability recorded in the shop, depending on the one named where it says so."""
    lines = [{"title": "Only line", "says": "When asked, it answers."}]
    made = spec_shop.put(env, tmp_path, "capability", title, shop=built["shops"][shop], gist="A capability.", behaviour=lines)
    built["capabilities"][title] = made
    if target:
        spec_shop.depend_on(env, tmp_path, made, [built["capabilities"][target]])


@given(parsers.parse('a feature formulating "{title}", with a scenario whose uses name "{target}"'))
def _a_feature(env, tmp_path, built, title, target):
    capability = built["capabilities"][title]
    line = spec_shop.line_id(env, capability, "Only line")
    scenario = {
        "title": "The capability is used", "formulates": f"{capability}#behaviour/{line}", "uses": [built["capabilities"][target]],
        "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "all is well"}],
    }
    built["feature"] = record(env, tmp_path, "feature", {"title": title, "formulates": capability, "scenarios": [scenario]}, f"Formulate {title}")


@when(parsers.parse('the user follows the links into the capability "{title}"'), target_fixture="result")
def _follow_into(env, built, title):
    return knol(env, "refs", built["capabilities"][title], "--inbound")


@then(parsers.parse('the user sees the capabilities "{first}" and "{second}"'))
def _sees_capabilities(shown, built, first, second):
    assert {entry["id"] for entry in shown if entry["id"].startswith("capability/")} == {built["capabilities"][first], built["capabilities"][second]}


@then(parsers.parse('the user sees the feature formulating "{title}"'))
def _sees_feature(shown, built, title):
    assert built["feature"] in {entry["id"] for entry in shown}
