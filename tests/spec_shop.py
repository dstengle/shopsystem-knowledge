"""The small shop that publish-a-shops-spec's scenarios share, built the way a user builds one: a product; a shop with
constraints, sections, a reading order and decisions; capabilities of the shop with Behaviour and Not yet items resting
on its decisions; and a feature formulating each capability. Imported plainly, never star-imported. `build` returns the
names kb minted, and the content it gave, so a scenario reads what it needs from there instead of spelling it."""
from decision_fields import decided
from driver import knol, record, whole
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
    {"title": "Counts are kept weekly", **decided(2), "revisit_when": "the shop grows", "supersedes": 0, "extends": [0]},
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


def _decision(env, tmp_path, fields, earlier=()):
    """Record a decision; `supersedes` and `extends`, where it has them, are indexes into the `earlier` names."""
    given = {key: value for key, value in fields.items() if key not in {"supersedes", "extends"}}
    if "supersedes" in fields:
        given["supersedes"] = earlier[fields["supersedes"]]
    if "extends" in fields:
        given["extends"] = [earlier[at] for at in fields["extends"]]
    fields = given
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
            "formulates": f"{name}#behaviour/{handle(capability['behaviour'][0]['title'])}",
            "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "the shelf is in order"}],
        }],
    }, f"Formulate {capability['title']}")


def handle(title):
    return title.lower().replace(" ", "-")


def build(env, tmp_path) -> Built:
    """Record the whole shop in the knowledge base `env` names, the shop's reading order and constraints written once
    its capabilities exist, since they link to it and it to them."""
    product = record(env, tmp_path, "product", {"title": "Corner shop", "gist": "A shop on the corner.", "sections": [PURPOSE]},
                     "Record the product")
    decisions = []
    for fields in DECISIONS:
        decisions.append(_decision(env, tmp_path, fields, decisions))
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


KIND_DEFAULTS = {
    "product": {"sections": [PURPOSE]},
    "shop": {"sections": SHOP_SECTIONS},
    "capability": {"narrator": "the shopkeeper", "sections": [PURPOSE]},
    "decision": {**decided(1), "sections": [PURPOSE, {"title": "Rationale", "body": "The shop runs better so.\n"}]},
}
"""What each kind needs beside its title and the fields a scenario gives: its sections, and a capability's narrator."""


def put(env, tmp_path, kind, title, **fields):
    """Record one product, shop, capability or decision of `title` with `fields` over the kind's defaults, as the
    user does, and return the name kb minted. A feature has no defaults: its caller gives every field."""
    content = {"title": title, **KIND_DEFAULTS.get(kind, {}), **fields}
    return record(env, tmp_path, kind, content, f"Record {title}")


def capability_with(env, tmp_path, title, behaviour_titles):
    """A product, a shop and, of that shop, a capability of `title` with a Behaviour line for each of `behaviour_titles`,
    recorded as the user does; return the capability's name."""
    product = put(env, tmp_path, "product", "Corner shop", gist="A shop on the corner.")
    shop = put(env, tmp_path, "shop", "Shelves", product=product, gist="Keeps the shelves.")
    lines = [{"title": each, "says": f"When asked, {each.lower()}."} for each in behaviour_titles]
    return put(env, tmp_path, "capability", title, shop=shop, gist="A capability.", behaviour=lines)


def capability_content(env, tmp_path, lines):
    """What a capability of a new product and shop is recorded with, `lines` its Behaviour items, to be given to
    `create` by the caller; the product and the shop are recorded here."""
    product = put(env, tmp_path, "product", "Corner shop", gist="A shop on the corner.")
    shop = put(env, tmp_path, "shop", "Shelves", product=product, gist="Keeps the shelves.")
    return {"title": "Checkout", "shop": shop, "gist": "A capability.", "behaviour": lines, **KIND_DEFAULTS["capability"]}


def ordered_capability(env, tmp_path, shop, title):
    """A capability of `title` added to `shop`, last in its reading order, and a feature formulating it, recorded as the
    user does; return the capability's name and the feature's."""
    lines = [{"title": "Only line", "says": "When asked, it answers."}]
    capability = put(env, tmp_path, "capability", title, shop=shop, gist="A capability.", behaviour=lines)
    feature = _feature(env, tmp_path, {"title": title, "behaviour": lines}, capability)
    held = whole(env, shop)
    complete = {key: value for key, value in held.items() if key not in {"id", "type", "schema_version", "revision", "title"}}
    complete["reading_order"] = [*held["reading_order"], capability]
    path = tmp_path / "shop-ordered.yaml"
    path.write_text(dumps(complete))
    result = knol(env, "write", shop, "--from", str(path), "-m", "Order the shop's capabilities")
    assert result.returncode == 0, result.stderr
    return capability, feature


def _rewritten(env, tmp_path, name, **changed):
    """The artifact `name` written over with `changed` fields beside what it holds."""
    held = whole(env, name)
    complete = {key: value for key, value in held.items() if key not in {"id", "type", "schema_version", "revision", "title"}}
    path = tmp_path / "rewritten.yaml"
    path.write_text(dumps({**complete, **changed}))
    result = knol(env, "write", name, "--from", str(path), "-m", f"Rewrite {name}")
    assert result.returncode == 0, result.stderr


def reading_order(env, tmp_path, shop, capabilities):
    """`shop` made to order `capabilities`, which link to it and so were recorded after it."""
    _rewritten(env, tmp_path, shop, reading_order=capabilities)


def numbered_decision(env, tmp_path, shop, number, title):
    """A decision of `number` and `title` added to the decisions `shop` names; return its name."""
    decision = put(env, tmp_path, "decision", title, **decided(number))
    _rewritten(env, tmp_path, shop, decisions=[*whole(env, shop).get("decisions", []), decision])
    return decision


def other_shop_decision(env, tmp_path, product, number, title):
    """Another shop of `product` that names a decision of `number` and `title`; return the shop's name and the decision's."""
    shop = put(env, tmp_path, "shop", "Aisles", product=product, gist="Keeps the aisles.")
    return shop, numbered_decision(env, tmp_path, shop, number, title)


def rest_on(env, tmp_path, capability, decision):
    """`capability` made to rest on `decision` as well as what it rests on."""
    _rewritten(env, tmp_path, capability, rests_on=[*whole(env, capability)["rests_on"], decision])
