"""The steps of see-what-is-formulated. Star-imported by the feature's test module alone (adrs/0035)."""
from pytest_bdd import given, parsers, then, when

import spec_shop
from driver import knol, record


@given(
    parsers.parse('a shop knowledge base holding the shop "{shop}" with these Behaviour lines, formulated by these scenarios'),
    target_fixture="held",
)
def _a_shop_with_lines(env, started_shop, tmp_path, datatable, shop):
    """The shop and its capabilities, in the order the table first names them, each with its lines; a feature formulating
    the capability holds a scenario for each time the table says a line is formulated. Returns each line's link, by
    capability title and line title."""
    product = spec_shop.put(env, tmp_path, "product", "Corner shop", gist="A shop on the corner.")
    shop_id = spec_shop.put(env, tmp_path, "shop", shop, product=product, gist="Keeps the shop.")
    rows = [dict(zip(datatable[0], row)) for row in datatable[1:]]
    titles = list(dict.fromkeys(row["capability"] for row in rows))
    capabilities = {}
    for order, title in enumerate(titles, 1):
        lines = [{"title": row["line"], "says": f"When asked, {row['line'].lower()}."} for row in rows if row["capability"] == title]
        capabilities[title] = spec_shop.put(env, tmp_path, "capability", title, shop=shop_id, gist="A capability.", behaviour=lines,
                                              order=str(order))
    ids = {(row["capability"], row["line"]): spec_shop.line_id(env, capabilities[row["capability"]], row["line"]) for row in rows}
    for title, capability in capabilities.items():
        scenarios = [
            {
                "title": f"{row['line']}, number {number}",
                "formulates": f"{capability}#behaviour/{ids[(row['capability'], row['line'])]}",
                "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "all is well"}],
            }
            for row in rows if row["capability"] == title
            for number in range(int(row["scenarios formulating it"]))
        ]
        if scenarios:
            record(env, tmp_path, "feature", {"title": title, "formulates": capability, "scenarios": scenarios}, f"Formulate {title}")
    return {"shop": shop_id, "link": {
        (row["capability"], row["line"]): f"{capabilities[row['capability']]}#behaviour/{ids[(row['capability'], row['line'])]}" for row in rows
    }}


@when(parsers.parse('the user asks what is formulated in the shop "{shop}"'), target_fixture="result")
def _asks(env, held, shop):
    return knol(env, "coverage", held["shop"])


def _listed(shown, key, held, table):
    """The lines shown under `key` are those of the table, each by its link with its capability's and its own title."""
    wanted = {held["link"][(row[0], row[1])]: (row[0], row[1]) for row in table[1:]}
    assert {entry["link"] for entry in shown[key]} == set(wanted), shown
    for entry in shown[key]:
        assert (entry["capability"], entry["line"]) == wanted[entry["link"]], entry


@then("the user is shown as formulated by no scenario each of these lines, by its link, and no other")
def _unformulated(shown, held, datatable):
    _listed(shown, "unformulated", held, datatable)


@then("the user is shown as formulated by more than one scenario each of these lines, by its link, and no other")
def _twice(shown, held, datatable):
    _listed(shown, "formulated_twice", held, datatable)


@then("the user is shown that no line is formulated by no scenario")
def _none_unformulated(shown):
    assert shown["unformulated"] == []


@then("the user is shown that no line is formulated by more than one scenario")
def _none_twice(shown):
    assert shown["formulated_twice"] == []
