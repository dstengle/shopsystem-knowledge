from kb import canonical
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("check-the-shops-knowledge-is-sound.feature")

WEEKLY = "decision/price-reviews-happen-weekly"
MONTHLY = "decision/prices-are-reviewed-monthly"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given(
    "a shop knowledge base where someone edited a decision's file by hand and left it in a shape the shop cannot read"
)
def _shop_with_a_file_mangled_by_hand(env, shop, tmp_path):
    """Two decisions edited by hand: one left unreadable, one left readable but without the body of its purpose."""
    start(env, shop)
    record(env, tmp_path, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly")
    record(env, tmp_path, "decision", {"title": "Prices are reviewed monthly", "sections": SECTIONS}, "Record monthly")
    (shop / "kb" / f"{WEEKLY}.yaml").write_text("title: [a bracket opened by hand and never closed\n")
    monthly = shop / "kb" / f"{MONTHLY}.yaml"
    held = canonical.load(monthly.read_text())
    del held["sections"][0]["body"]
    monthly.write_text(canonical.dump(held))


@when("the user checks the shop's knowledge", target_fixture="result")
def _check(env):
    return knol(env, "validate")


@then("that file is listed as a fault, naming the file")
def _unreadable_listed(result):
    assert result.stderr.splitlines()[0].startswith(f"{WEEKLY}: the stored file {WEEKLY}.yaml cannot be read: ")


@then("everything else the shop knows is checked and listed alongside it")
def _the_rest_listed(result):
    assert result.stderr.splitlines()[1:] == [f"{MONTHLY} at sections/0: 'body' is a required property"]
