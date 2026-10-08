"""The steps of use-the-shops-types.feature about retiring a capability others still depend on. The feature's test module
star-imports this and no other does."""
from pytest_bdd import given, parsers, then, when

import spec_shop
from driver import knol, record, start, whole
from kb.content import dumps

LINE = {"title": "Only line", "says": "When asked, it answers."}


@given(
    parsers.re(
        r'a shop knowledge base holding a product "(?P<product>[^"]*)", shops "(?P<first>[^"]*)" and "(?P<second>[^"]*)" '
        r'of "[^"]*", and a capability "(?P<title>[^"]*)" of "[^"]*" with the status (?P<status>\w+)'
    ),
    target_fixture="held",
)
def _a_base_with_a_capability_in_use(env, shop, tmp_path, product, first, second, title, status):
    start(env, shop)
    made = {product: spec_shop.put(env, tmp_path, "product", product, gist="A product.")}
    for each in (first, second):
        made[each] = spec_shop.put(env, tmp_path, "shop", each, product=made[product], gist="A shop.")
    made[title] = spec_shop.put(env, tmp_path, "capability", title, shop=made[first], gist="A capability.", behaviour=[LINE],
                                order="1", status=status)
    return made


def _dependent(env, tmp_path, held, shop_title, **fields):
    return spec_shop.put(env, tmp_path, "capability", "Dependent", shop=held[shop_title], gist="A capability.", behaviour=[LINE],
                         order="2", **fields)


@given(parsers.re(r'the knowledge base holds a capability of the shop "(?P<shop_title>[^"]*)" that depends on "(?P<used>[^"]*)"'))
def _a_capability_depending_on(env, tmp_path, held, shop_title, used):
    _dependent(env, tmp_path, held, shop_title, depends_on=[held[used]])


@given(parsers.re(r'the knowledge base holds a scenario of a capability of the shop "(?P<shop_title>[^"]*)" that uses "(?P<used>[^"]*)"'))
def _a_scenario_using(env, tmp_path, held, shop_title, used):
    capability = _dependent(env, tmp_path, held, shop_title)
    line = spec_shop.line_id(env, capability, LINE["title"])
    record(env, tmp_path, "feature", {"title": "Dependent", "formulates": capability, "scenarios": [{
        "title": "Dependent, as the user does it", "formulates": f"{capability}#behaviour/{line}", "uses": [held[used]],
        "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "all is well"}],
    }]}, "Formulate Dependent")


@when(parsers.parse('the user sets the status of the capability "{title}" to retired, saying who they are and why'),
      target_fixture="result")
def _retires(env, tmp_path, held, title):
    held_fields = whole(env, held[title])
    complete = {key: value for key, value in held_fields.items()
                if key not in {"id", "type", "schema_version", "revision", "title"}}
    path = tmp_path / "retired.yaml"
    path.write_text(dumps({**complete, "status": "retired"}))
    return knol(env, "write", held[title], "--from", str(path), "-m", f"Retire {title}")


@then(parsers.parse('the capability "{title}" is recorded as retired'))
def _is_retired(env, result, held, title):
    assert result.returncode == 0, result.stderr
    assert whole(env, held[title])["status"] == "retired"
