"""The steps of use-the-shops-types.feature about the spec's kinds of thing at a glance, and about a part's name
minted from its title. The feature's test module star-imports this and no other does."""
import re

from pytest_bdd import given, parsers, then, when

from driver import knol, start, whole
from kb.content import dumps, loads
from spec_shop import capability_content, capability_with, put

NOT_FIELDS = {"id", "type", "schema_version", "revision", "title", "references", "parts", "inbound"}
"""What a glance shows that is not a field of the artifact: its identity, and what it points at and holds."""


@given(
    parsers.re(
        r'a shop knowledge base holding a product "(?P<product>[^"]*)", a shop "(?P<shop_title>[^"]*)" of "[^"]*", '
        r'a capability "(?P<capability>[^"]*)" of "[^"]*" and a decision "(?P<decision>[^"]*)" of "[^"]*"'
    ),
    target_fixture="held",
)
def _a_base_holding_the_kinds(env, shop, tmp_path, product, shop_title, capability, decision):
    """The base the glance scenarios start from; every thing is named by its title, and `held` maps each title to the
    name kb minted for it."""
    start(env, shop)
    decided = put(env, tmp_path, "decision", decision)
    made = {product: put(env, tmp_path, "product", product, gist="A product.")}
    made[shop_title] = put(env, tmp_path, "shop", shop_title, product=made[product], gist="A shop.", decisions=[decided])
    made[capability] = put(env, tmp_path, "capability", capability, shop=made[shop_title], gist="A capability.")
    made[decision] = decided
    return made


def _quoted(text, label):
    return re.search(rf'{label} "([^"]*)"', text).group(1)


def _given_fields(held, kind, recorded_with):
    """The fields a scenario's "recorded with" gives, links as the names kb minted for the titles it names."""
    fields = {}
    if gist := re.search(r'gist "([^"]*)"', recorded_with):
        fields["gist"] = gist.group(1)
    if statement := re.search(r'statement "([^"]*)"', recorded_with):
        fields["statement"] = statement.group(1)
        fields["date"] = re.search(r"date (\S+?),", recorded_with).group(1)
        fields["supersedes"] = held[_quoted(recorded_with, "superseding")]
    if kind == "shop":
        fields["product"] = held[_quoted(recorded_with, "product")]
    if kind == "capability":
        fields["shop"] = held[_quoted(recorded_with, "shop")]
    if kind == "feature":
        fields["formulates"] = held[_quoted(recorded_with, "capability")]
    return fields


@given(parsers.re(r'the user has recorded a (?P<kind>\w+) "(?P<name>[^"]*)" (?P<recorded_with>.*)'), target_fixture="recorded")
def _recorded(env, tmp_path, held, kind, name, recorded_with):
    fields = _given_fields(held, kind, recorded_with)
    return {"id": put(env, tmp_path, kind, name, **fields), "fields": fields}


@when(parsers.re(r'the user reads the (?P<kind>\w+) "(?P<name>[^"]*)" at a glance'), target_fixture="glanced")
def _reads_at_a_glance(env, kind, name):
    result = knol(env, "read", f"{kind}/{name}")
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)


@then("each field it shows is one short line or a link, as it was recorded")
def _short_lines_as_recorded(glanced, recorded):
    shown = {key: value for key, value in glanced.items() if key not in NOT_FIELDS}
    for key, value in shown.items():
        assert isinstance(value, str) and "\n" not in value and len(value) <= 200, (key, value)
    assert recorded["fields"].items() <= shown.items(), (recorded["fields"], shown)


def _titles(text):
    return re.findall(r'"([^"]*)"', text)


@given(
    parsers.re(r'a shop knowledge base holding a capability "(?P<name>[^"]*)" with (?:a )?Behaviour lines? titled (?P<titles>.*)'),
    target_fixture="held",
)
def _a_base_holding_a_capability(env, shop, tmp_path, name, titles):
    start(env, shop)
    return {name: capability_with(env, tmp_path, name, _titles(titles))}


@given(
    parsers.re(r'a capability "(?P<name>[^"]*)" with a Behaviour line titled (?P<titles>.*)'),
    target_fixture="held",
)
def _a_capability(env, tmp_path, name, titles):
    """In the base the scenario's own Given started."""
    return {name: capability_with(env, tmp_path, name, _titles(titles))}


@then("each of its Behaviour lines is shown by its title")
def _lines_shown_by_title(env, glanced):
    """The glance's parts are the capability's Behaviour lines as a whole read gives them, each with its own title."""
    lines = whole(env, glanced["id"])["behaviour"]
    shown = [(part["id"], part["title"]) for part in glanced["parts"] if part["collection"] == "behaviour"]
    assert shown == [(line["id"], line["title"]) for line in lines], (shown, lines)


@when(
    parsers.re(r'the user records a capability with a Behaviour line titled "(?P<title>[^"]*)", saying who they are and why'),
    target_fixture="result",
)
def _records_a_capability_with_a_line(env, tmp_path, title):
    content = capability_content(env, tmp_path, [{"title": title, "says": "When asked, it is done."}])
    path = tmp_path / "capability.yaml"
    path.write_text(dumps(content))
    return knol(env, "create", "capability", "--from", str(path), "-m", "Record a capability")


@then(parsers.parse('the Behaviour line\'s name is minted from its title "{title}"'))
def _name_minted(env, result, title):
    """The name kb gives the line, in a whole read and in a glance alike, is made of its title's words; the step does
    not say how kb makes it, and the user gave no name (the file holds none)."""
    assert result.returncode == 0, result.stderr
    made = loads(result.stdout)["id"]
    line = whole(env, made)["behaviour"][0]
    in_a_glance = [part["id"] for part in loads(knol(env, "read", made).stdout)["parts"] if part["collection"] == "behaviour"]
    assert line["title"] == title and in_a_glance == [line["id"]]
    assert all(word in line["id"] for word in title.lower().split()), line["id"]
