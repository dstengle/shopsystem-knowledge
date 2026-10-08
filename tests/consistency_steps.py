"""The steps of check-the-knowledge-base for a scenario using what its capability does not depend on. Star-imported by
the feature's test module alone (adrs/0035). The fault is shop-knol's own, in plain words, so the Then checks the
artifact, the place and the capability used it names, never the whole line."""
from pytest_bdd import given, parsers, then

import spec_shop
from driver import record, whole

LINES = [{"title": "Only line", "says": "When asked, it answers."}]


@given("a knowledge base holding the shop and another shop", target_fixture="held")
def _the_shop_and_another(env, started_shop, tmp_path):
    product = spec_shop.put(env, tmp_path, "product", "Corner shop", gist="A shop on the corner.")
    shops = {each: spec_shop.put(env, tmp_path, "shop", title, product=product, gist="Keeps the shop.")
             for each, title in (("the shop", "Shelves"), ("the other shop", "Aisles"))}
    return {"shops": shops}


@given(parsers.parse('a capability of {owner} that does not depend on the capability "{used}"'))
def _a_capability_not_depending(env, tmp_path, held, owner, used):
    """The capability used, in the other shop, and the capability that does not depend on it, in `owner`'s."""
    held["used"] = spec_shop.put(env, tmp_path, "capability", used.capitalize(), shop=held["shops"]["the other shop"],
                                 gist="A capability.", behaviour=LINES, order="1")
    held["capability"] = spec_shop.put(env, tmp_path, "capability", "Sweep the floor", shop=held["shops"][owner],
                                       gist="A capability.", behaviour=LINES, order="2")


@given(parsers.parse('a scenario of that capability whose uses names "{used}"'))
def _a_scenario_using_it(env, tmp_path, held, used):
    capability = held["capability"]
    held["feature"] = record(env, tmp_path, "feature", {"title": "Sweep the floor", "formulates": capability, "scenarios": [{
        "title": "The floor is swept", "formulates": f"{capability}#behaviour/{spec_shop.line_id(env, capability, 'Only line')}",
        "uses": [held["used"]],
        "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "the floor is clean"}]}]},
        "Formulate Sweep the floor")
    held["scenario"] = whole(env, held["feature"])["scenarios"][0]["id"]


@then("that scenario is listed as a fault")
def _listed(result, held):
    """One line names the feature, the scenario's place in it and the capability it uses."""
    place = f"{held['feature']} at scenarios/{held['scenario']}"
    assert any(line.startswith(place) and held["used"] in line for line in result.stderr.splitlines()), result.stderr
