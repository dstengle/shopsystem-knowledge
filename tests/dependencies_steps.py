"""The steps of see-what-a-shop-depends-on. Star-imported by the feature's test module alone (adrs/0035)."""
from pytest_bdd import given, parsers, then, when

import spec_shop
from driver import knol, record


def _rows(datatable):
    return [dict(zip(datatable[0], row)) for row in datatable[1:]]


@given(
    parsers.parse('a shop knowledge base holding the shop "{shop}" with these capabilities, depending on these capabilities'),
    target_fixture="held",
)
def _a_shop_with_dependencies(env, started_shop, tmp_path, datatable, shop):
    """The named shop and the shops of what its capabilities depend on, each capability recorded at the status the table
    gives it, then linked to what it depends on. Returns the shop, and each capability's name by title."""
    product = spec_shop.put(env, tmp_path, "product", "Corner shop", gist="A shop on the corner.")
    rows = _rows(datatable)
    shop_titles = list(dict.fromkeys([shop, *(row["shop of what it depends on"] for row in rows)]))
    shops = {title: spec_shop.put(env, tmp_path, "shop", title, product=product, gist="Keeps the shop.") for title in shop_titles}
    wanted = {}
    for row in rows:
        wanted[row["capability"]] = (shop, row["status"])
        wanted.setdefault(row["depends on"], (row["shop of what it depends on"], row["status of what it depends on"]))
    lines = [{"title": "Only line", "says": "When asked, it answers."}]
    capabilities = {
        title: spec_shop.put(env, tmp_path, "capability", title, shop=shops[of], gist="A capability.", behaviour=lines,
                             order=str(number), status=status)
        for number, (title, (of, status)) in enumerate(wanted.items(), 1)
    }
    for row in rows:
        spec_shop.depend_on(env, tmp_path, capabilities[row["capability"]], [capabilities[row["depends on"]]])
    return {"shop": shops[shop], "capabilities": capabilities, "shops": shops}


@given("these scenarios of the shop's capabilities, using these capabilities")
def _scenarios_using(env, tmp_path, held, datatable):
    """A feature for each capability the table names, holding its scenarios, each using what the table says."""
    rows = _rows(datatable)
    for title in dict.fromkeys(row["capability"] for row in rows):
        capability = held["capabilities"][title]
        line = spec_shop.line_id(env, capability, "Only line")
        scenarios = [
            {
                "title": row["scenario"],
                "formulates": f"{capability}#behaviour/{line}",
                **({} if row["uses"] == "nothing" else {"uses": [held["capabilities"][row["uses"]]]}),
                "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "all is well"}],
            }
            for row in rows if row["capability"] == title
        ]
        record(env, tmp_path, "feature", {"title": title, "formulates": capability, "scenarios": scenarios}, f"Formulate {title}")


@when(parsers.parse('the user asks what the shop "{shop}" depends on'), target_fixture="result")
def _asks(env, held, shop):
    return knol(env, "dependencies", held["shop"])


@then("the user is shown each of these capabilities, with the capability it depends on, that capability's shop and its status, and no other")
def _shown_each(shown, held, datatable):
    wanted = {
        (held["capabilities"][row["capability"]], held["capabilities"][row["depends on"]]):
            (held["shops"][row["shop of what it depends on"]], row["status of what it depends on"])
        for row in _rows(datatable)
    }
    assert len(shown) == len(wanted), shown
    assert {(entry["capability"], entry["depends_on"]): (entry["shop"], entry["status"]) for entry in shown} == wanted, shown


@then("the user is shown, with each of those capabilities, these of its scenarios using what it depends on, and no other")
def _shown_scenarios(shown, held, datatable):
    wanted = {}
    for row in _rows(datatable):
        wanted.setdefault(held["capabilities"][row["capability"]], set()).add(row["scenario"])
    assert {entry["capability"]: set(entry["scenarios"]) for entry in shown} == wanted, shown
    assert sum(len(entry["scenarios"]) for entry in shown) == sum(len(each) for each in wanted.values()), shown


@then("the user is shown no capability depending on a deprecated or retired capability")
def _shown_none(shown):
    assert not shown, shown  # an empty list is printed as an empty value
