"""The steps of use-the-shops-types.feature about the limits the shop's types put on a short line, and the refusal a
record over them meets. Each Then compares what the user is shown with kb's own refusal of the same record, so no
step spells kb's wording. The feature's test module star-imports this and no other does."""
import pytest
from pytest_bdd import parsers, then, when

from spec_attempt import create, refused_as_unfit
from spec_shop import KIND_DEFAULTS, capability_content
LONG, BREAK = "x" * 201, "one\ntwo"
"""A line one character over the 200 a gist or a statement may hold; and one holding a line break."""


@pytest.fixture
def attempted():
    """The kind and the content the scenario's When gave `create`, for the Then to ask kb of the same record."""
    return {}


def _long_or_broken(how):
    return LONG if how == "is 201 characters long" else BREAK


@when(
    parsers.re(
        r"the user records a (?P<kind>product|decision) whose (?P<field>gist|statement) "
        r"(?P<how>is 201 characters long|holds a line break), saying who they are and why"
    ),
    target_fixture="result",
)
def _records_a_bad_summary(env, tmp_path, attempted, kind, field, how):
    base = {"title": "Corner shop", "gist": "A shop on the corner.", **KIND_DEFAULTS["product"]}
    if kind == "decision":
        base = {"title": "Prices are shown", **KIND_DEFAULTS["decision"]}
    return create(env, tmp_path, attempted, kind, {**base, field: _long_or_broken(how)})


@when(
    parsers.re(
        r"the user records a capability with a Behaviour line whose title "
        r"(?P<how>is 81 characters long|holds a line break), saying who they are and why"
    ),
    target_fixture="result",
)
def _records_a_bad_title(env, tmp_path, attempted, how):
    title = "y" * 81 if how == "is 81 characters long" else BREAK
    content = capability_content(env, tmp_path, [{"title": title, "says": "When asked, it is done."}])
    return create(env, tmp_path, attempted, "capability", content)


@then("the change is refused because it does not fit its type")
def _refused_as_unfit(env, result, attempted):
    refused_as_unfit(env, result, attempted)
