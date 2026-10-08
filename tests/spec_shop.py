"""The small shop that publish-a-shops-spec's scenarios share, built the way a user builds one: a product; a shop with
constraints and sections; decisions linking to the shop; active capabilities linking to the shop, each with an order
of its own, Behaviour and Not yet items, resting on its decisions; and a feature formulating each capability. Imported plainly, never star-imported. `build` returns the
names kb minted, and the content it gave, so a scenario reads what it needs from there instead of spelling it."""
from decision_fields import decided, without_shop
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
        "order": "5",
    },
    {
        "title": "Count the stock",
        "gist": "Know what is on each shelf.",
        "narrator": "the shopkeeper, counting",
        "behaviour": [{"title": "Counted shelf", "says": "When a shelf is counted, its count is kept."}],
        "not_yet": [],
        "rests_on": [0, 1],
        "order": "6",
    },
]
DECISIONS = [
    {"title": "Shelves are filled daily", **without_shop(1)},
    {"title": "Counts are kept weekly", **without_shop(2), "revisit_when": "the shop grows", "supersedes": 0, "extends": [0]},
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


def _decision(env, tmp_path, shop, fields, earlier=()):
    """Record a decision of `shop`; `supersedes` and `extends`, where it has them, are indexes into the `earlier` names."""
    given = {key: value for key, value in fields.items() if key not in {"supersedes", "extends"}} | {"shop": shop}
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
            "formulates": f"{name}#behaviour/{line_id(env, name, capability['behaviour'][0]['title'])}",
            "steps": [{"keyword": "When", "text": "the user acts"}, {"keyword": "Then", "text": "the shelf is in order"}],
        }],
    }, f"Formulate {capability['title']}")


def line_id(env, capability, title):
    """The id kb minted for the Behaviour line of `title` in `capability`, read from the capability held."""
    return next(line["id"] for line in whole(env, capability)["behaviour"] if line["title"] == title)


def build(env, tmp_path) -> Built:
    """Record the whole shop in the knowledge base `env` names, the shop's constraints written once its capabilities
    exist, since they pin to them; its decisions and capabilities link to it."""
    product = record(env, tmp_path, "product", {"title": "Corner shop", "gist": "A shop on the corner.", "sections": [PURPOSE]},
                     "Record the product")
    shop_content = {
        "title": "Shelves", "product": product, "gist": "Keeps the shelves.", "narrator": "the shopkeeper",
        "sections": SHOP_SECTIONS,
    }
    shop = record(env, tmp_path, "shop", shop_content, "Record the shop")
    decisions = []
    for fields in DECISIONS:
        decisions.append(_decision(env, tmp_path, shop, fields, decisions))
    capabilities = []
    for each in CAPABILITIES:
        content = {key: value for key, value in each.items() if key not in {"rests_on", "not_yet"}}
        content |= {"shop": shop, "status": "active", "rests_on": [decisions[index] for index in each["rests_on"]],
                    "not_yet": each["not_yet"], "sections": [PURPOSE]}
        capabilities.append(record(env, tmp_path, "capability", content, f"Record {each['title']}"))
    features = [_feature(env, tmp_path, each, name) for each, name in zip(CAPABILITIES, capabilities)]
    constraints = [
        {"title": each["title"], "says": each["says"], "pinned_in": [capabilities[index] for index in each["pinned"]]}
        for each in CONSTRAINTS
    ]
    complete = {**{key: value for key, value in shop_content.items() if key != "title"}, "constraints": constraints}
    path = tmp_path / "shop-complete.yaml"
    path.write_text(dumps(complete))
    result = knol(env, "write", shop, "--from", str(path), "-m", "Pin the constraints")
    assert result.returncode == 0, result.stderr
    return Built(product, shop, capabilities, decisions, features)


KIND_DEFAULTS = {
    "product": {"sections": [PURPOSE]},
    "shop": {"sections": SHOP_SECTIONS},
    "capability": {"narrator": "the shopkeeper", "order": "1", "status": "active", "sections": [PURPOSE]},
    "decision": {"sections": [PURPOSE, {"title": "Rationale", "body": "The shop runs better so.\n"}]},
}
"""What each kind needs beside its title and the fields a scenario gives: its sections, and a capability's narrator. A
decision's own fields, its shop among them, are the caller's (`decision_fields.decided`)."""


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


def ordered_capability(env, tmp_path, shop, title, order="3"):
    """A capability of `title` linking to `shop`, active and at `order`, and a feature formulating it, recorded as the
    user does; return the capability's name and the feature's."""
    lines = [{"title": "Only line", "says": "When asked, it answers."}]
    capability = put(env, tmp_path, "capability", title, shop=shop, gist="A capability.", behaviour=lines, order=order)
    return capability, _feature(env, tmp_path, {"title": title, "behaviour": lines}, capability)


def _rewritten(env, tmp_path, name, **changed):
    """The artifact `name` written over with `changed` fields beside what it holds."""
    held = whole(env, name)
    complete = {key: value for key, value in held.items() if key not in {"id", "type", "schema_version", "revision", "title"}}
    path = tmp_path / "rewritten.yaml"
    path.write_text(dumps({**complete, **changed}))
    result = knol(env, "write", name, "--from", str(path), "-m", f"Rewrite {name}")
    assert result.returncode == 0, result.stderr


def numbered_decision(env, tmp_path, shop, number, title):
    """A decision of `number` and `title` linking to `shop`; return its name."""
    return put(env, tmp_path, "decision", title, **decided(number, shop))


def other_shop_decision(env, tmp_path, product, number, title):
    """Another shop of `product` and a decision of `number` and `title` linking to it; return the shop's name and the decision's."""
    shop = put(env, tmp_path, "shop", "Aisles", product=product, gist="Keeps the aisles.")
    return shop, numbered_decision(env, tmp_path, shop, number, title)


def deprecate(env, tmp_path, capability):
    """`capability` made deprecated, still in use."""
    _rewritten(env, tmp_path, capability, status="deprecated")


def rest_on(env, tmp_path, capability, decision):
    """`capability` made to rest on `decision` as well as what it rests on."""
    _rewritten(env, tmp_path, capability, rests_on=[*whole(env, capability)["rests_on"], decision])


def retired_capability(env, tmp_path, shop, title):
    """A capability of `title` linking to `shop` whose status is retired, and a feature formulating it; return the
    capability's name and the feature's."""
    lines = [{"title": "Only line", "says": "When asked, it answers."}]
    capability = put(env, tmp_path, "capability", title, shop=shop, gist="A capability.", behaviour=lines, order="9",
                     status="retired")
    return capability, _feature(env, tmp_path, {"title": title, "behaviour": lines}, capability)


def depend_on(env, tmp_path, capability, targets):
    """`capability` made to depend on `targets` (names), beside what it depends on."""
    _rewritten(env, tmp_path, capability, depends_on=[*whole(env, capability).get("depends_on", []), *targets])
