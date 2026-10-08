"""The steps of use-the-shops-types.feature about what a capability carries beside its words: the capabilities it
depends on, its status and its order. The feature's test module star-imports this and no other does; the `attempted`
fixture the refusal Then reads is types_spec_limits's."""
from pytest_bdd import given, parsers, then, when

from driver import knol, start, whole
from kb.content import dumps, loads
from spec_attempt import create
from spec_shop import KIND_DEFAULTS, put


@given(
    parsers.re(
        r'a shop knowledge base holding a product "(?P<product>[^"]*)" and a shop "(?P<shop_title>[^"]*)" of "[^"]*"'
    ),
    target_fixture="held",
)
def _a_base_with_a_shop(env, shop, tmp_path, product, shop_title):
    """`held` maps each title to the name kb minted for it."""
    start(env, shop)
    made = {product: put(env, tmp_path, "product", product, gist="A product.")}
    made[shop_title] = put(env, tmp_path, "shop", shop_title, product=made[product], gist="A shop.")
    return made


def _capability_of(env, tmp_path, held, title, shop_title, **fields):
    return put(env, tmp_path, "capability", title, shop=held[shop_title], gist="A capability.", **fields)


@given(
    parsers.re(
        r'a shop knowledge base holding a product "(?P<product>[^"]*)", shops "(?P<first>[^"]*)" and "(?P<second>[^"]*)" '
        r'of "[^"]*", a capability "(?P<mine>[^"]*)" of "[^"]*" and a capability "(?P<yours>[^"]*)" of "[^"]*"'
    ),
    target_fixture="held",
)
def _a_base_with_two_shops(env, shop, tmp_path, product, first, second, mine, yours):
    start(env, shop)
    made = {product: put(env, tmp_path, "product", product, gist="A product.")}
    for title in (first, second):
        made[title] = put(env, tmp_path, "shop", title, product=made[product], gist="A shop.")
    made[mine] = _capability_of(env, tmp_path, made, mine, first, order="1")
    made[yours] = _capability_of(env, tmp_path, made, yours, second, order="1")
    return made


@when(
    parsers.re(
        r'the user records a capability "(?P<title>[^"]*)" of the shop "(?P<shop_title>[^"]*)" that depends on '
        r'"(?P<first>[^"]*)" and "(?P<second>[^"]*)", saying who they are and why'
    ),
    target_fixture="result",
)
def _records_a_dependent(env, tmp_path, held, title, shop_title, first, second):
    content = {"title": title, "shop": held[shop_title], "gist": "A capability.", "depends_on": [held[first], held[second]],
               **KIND_DEFAULTS["capability"]}
    path = tmp_path / "dependent.yaml"
    path.write_text(dumps(content))
    return knol(env, "create", "capability", "--from", str(path), "-m", "Record a capability")


@then(parsers.parse('the capability "{title}" names "{first}" and "{second}" as the capabilities it depends on'))
def _names_what_it_depends_on(env, result, held, first, second):
    """Named in the whole read, and shown at a glance as links to those capabilities: a field the type does not declare
    as a link is kept but pointed at nothing."""
    assert result.returncode == 0, result.stderr
    made = loads(result.stdout)["id"]
    wanted = [held[first], held[second]]
    assert whole(env, made)["depends_on"] == wanted
    glance = loads(knol(env, "read", made).stdout)
    assert [stub["id"] for stub in glance["references"] if stub["field"] == "depends_on"] == wanted, glance


def _attempt(env, tmp_path, attempted, held, shop_title, **fields):
    content = {"title": "Apply a code", "shop": held[shop_title], "gist": "A capability.", **KIND_DEFAULTS["capability"], **fields}
    return create(env, tmp_path, attempted, "capability", content)


@when(
    parsers.re(r'the user records a capability of the shop "(?P<shop_title>[^"]*)" with the status "(?P<status>[^"]*)", saying who they are and why'),
    target_fixture="result",
)
def _records_with_a_status(env, tmp_path, attempted, held, shop_title, status):
    return _attempt(env, tmp_path, attempted, held, shop_title, status=status, order="1")


@when(
    parsers.re(r'the user records a capability of the shop "(?P<shop_title>[^"]*)" with the order "(?P<order>[^"]*)", saying who they are and why'),
    target_fixture="result",
)
def _records_with_an_order(env, tmp_path, attempted, held, shop_title, order):
    return _attempt(env, tmp_path, attempted, held, shop_title, status="active", order=order)
