"""The small shop that publish-a-shops-spec's scenarios share, built the way a user builds one: a product; a shop with
constraints, sections, a reading order and decisions; capabilities of the shop with Behaviour and Not yet items resting
on its decisions; and a feature formulating each capability. Imported plainly, never star-imported. `build` returns the
names kb minted, and the content it gave, so a scenario reads what it needs from there instead of spelling it."""
from decision_fields import decided
from driver import knol, record
from kb.content import dumps

PURPOSE = {"title": "Purpose", "body": "Keep the shelves full.\n"}
SHOP_SECTIONS = [
    PURPOSE,
    {"title": "Order of building", "body": "Stock first, then counts.\n"},
    {"title": "Testing", "body": "Count what is on the shelf.\n"},
]
CAPABILITIES = [
    {
        "title": "Restock the shelves",
        "gist": "Keep every shelf filled.",
        "narrator": "the shopkeeper, filling the shelves",
        "behaviour": [{"title": "Short shelf", "says": "When a shelf is short, it is filled."}],
        "not_yet": [{"title": "Night orders", "defers": "Ordering at night.", "trigger": "the shop opens at night"}],
        "rests_on": [0],
    },
    {
        "title": "Count the stock",
        "gist": "Know what is on each shelf.",
        "narrator": "the shopkeeper, counting",
        "behaviour": [{"title": "Counted shelf", "says": "When a shelf is counted, its count is kept."}],
        "not_yet": [],
        "rests_on": [0, 1],
    },
]
DECISIONS = [
    {"title": "Shelves are filled daily", **decided(1)},
    {"title": "Counts are kept weekly", **decided(2)},
]
CONSTRAINTS = [
    {"title": "Shelves stay full", "says": "No shelf is left empty.", "pinned": [0, 1]},
    {"title": "Counts are honest", "says": "A count is what was counted.", "pinned": [1]},
]


class Built:
    """What kb minted for the shop, in the order written here: `shop`, `product`, `capabilities`, `decisions` and
    `features` (each a list of names), beside the content given for each."""

    def __init__(self, product, shop, capabilities, decisions, features):
        self.product, self.shop = product, shop
        self.capabilities, self.decisions, self.features = capabilities, decisions, features


def _decision(env, tmp_path, fields):
    sections = [
        {"title": "Purpose", "body": f"{fields['title']}, because the shelves need it.\n"},
        {"title": "Rationale", "body": "The shop runs better so.\n"},
    ]
    return record(env, tmp_path, "decision", {**fields, "sections": sections}, f"Record: {fields['title']}")


def _feature(env, tmp_path, capability, name):
    return record(env, tmp_path, "feature", {
        "title": capability["title"],
        "formulates": name,
        "scenarios": [{
            "title": f"{capability['title']}, as the user does it",
            "formulates": f"{name}#behaviour/{_handle(capability['behaviour'][0]['title'])}",
            "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "the shelf is in order"}],
        }],
    }, f"Formulate {capability['title']}")


def _handle(title):
    return title.lower().replace(" ", "-")


def build(env, tmp_path) -> Built:
    """Record the whole shop in the knowledge base `env` names, the shop's reading order and constraints written once
    its capabilities exist, since they link to it and it to them."""
    product = record(env, tmp_path, "product", {"title": "Corner shop", "gist": "A shop on the corner.", "sections": [PURPOSE]},
                     "Record the product")
    decisions = [_decision(env, tmp_path, fields) for fields in DECISIONS]
    shop_content = {
        "title": "Shelves", "product": product, "gist": "Keeps the shelves.", "narrator": "the shopkeeper",
        "decisions": decisions, "sections": SHOP_SECTIONS,
    }
    shop = record(env, tmp_path, "shop", shop_content, "Record the shop")
    capabilities = []
    for each in CAPABILITIES:
        content = {key: value for key, value in each.items() if key not in {"rests_on", "not_yet"}}
        content |= {"shop": shop, "rests_on": [decisions[index] for index in each["rests_on"]],
                    "not_yet": each["not_yet"], "sections": [PURPOSE]}
        capabilities.append(record(env, tmp_path, "capability", content, f"Record {each['title']}"))
    features = [_feature(env, tmp_path, each, name) for each, name in zip(CAPABILITIES, capabilities)]
    constraints = [
        {"title": each["title"], "says": each["says"], "pinned_in": [capabilities[index] for index in each["pinned"]]}
        for each in CONSTRAINTS
    ]
    complete = {**{key: value for key, value in shop_content.items() if key != "title"}, "reading_order": capabilities, "constraints": constraints}
    path = tmp_path / "shop-complete.yaml"
    path.write_text(dumps(complete))
    result = knol(env, "write", shop, "--from", str(path), "-m", "Order the shop's capabilities")
    assert result.returncode == 0, result.stderr
    return Built(product, shop, capabilities, decisions, features)
