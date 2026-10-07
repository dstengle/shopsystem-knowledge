"""The steps of use-the-shops-types.feature about a feature's scenarios: what one `uses`, the Behaviour line it
formulates as a link, and its labels as plain words. The feature's test module star-imports this and no other does."""
from kb.content import loads

from pytest_bdd import given, parsers, then, when

from driver import knol, whole
from spec_attempt import create
from spec_shop import put

STEPS = [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "the shelf is in order"}]


@given(parsers.parse('a decision "{name}"'), target_fixture="decided")
def _a_decision(env, tmp_path, name):
    return put(env, tmp_path, "decision", name)


def _line(env, held, line_title):
    """The capability the scenario holds, and the name kb minted for its Behaviour line of `line_title`."""
    capability = next(iter(held.values()))
    line = next(each for each in whole(env, capability)["behaviour"] if each["title"] == line_title)
    return capability, line["id"]


def _attempt_feature(env, tmp_path, attempted, held, line_title, **scenario):
    capability, line = _line(env, held, line_title)
    scenario = {"title": "As the user does it", "formulates": f"{capability}#behaviour/{line}", "steps": STEPS, **scenario}
    content = {"title": "Checkout", "formulates": capability, "scenarios": [scenario]}
    return create(env, tmp_path, attempted, "feature", content)


@when(
    parsers.re(
        r'the user records a feature with a scenario that formulates the Behaviour line "(?P<line>[^"]*)" '
        r'and uses the decision "(?P<decision>[^"]*)", saying who they are and why'
    ),
    target_fixture="result",
)
def _records_a_scenario_using_a_decision(env, tmp_path, attempted, held, decided, line, decision):
    return _attempt_feature(env, tmp_path, attempted, held, line, uses=[decided])


@when(
    parsers.re(
        r'the user records a feature with a scenario (?:labelled "(?P<label>[^"]*)" )?that formulates the Behaviour line '
        r'"(?P<line>[^"]*)", saying who they are and why'
    ),
    target_fixture="result",
)
def _records_a_feature(env, tmp_path, attempted, held, label, line):
    labels = {"labels": [label]} if label else {}
    return _attempt_feature(env, tmp_path, attempted, held, line, **labels)


def _recorded_scenario(env, result):
    assert result.returncode == 0, result.stderr
    return whole(env, loads(result.stdout)["id"])["scenarios"][0]


@then(parsers.re(
    r'the scenario names the Behaviour line "(?P<line>[^"]*)" as a link into the Behaviour lines of "(?P<capability>[^"]*)"'
))
def _names_the_line(env, result, held, line, capability):
    """The link is the capability's name, then the name kb minted for that line, as a whole read of the capability gives it."""
    _, minted = _line(env, held, line)
    assert _recorded_scenario(env, result)["formulates"] == f"{held[capability]}#behaviour/{minted}"


@then(parsers.parse('the label is kept as the plain word "{label}", not as a link to the tag "{tag_title}"'))
def _label_is_plain(env, result, tag, label, tag_title):
    assert _recorded_scenario(env, result)["labels"] == [label]
    glance = loads(knol(env, "read", tag).stdout)
    assert not [each for each in glance["inbound"] if each["type"] == "feature"], glance["inbound"]
