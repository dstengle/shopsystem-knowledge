"""The fields the decision type requires beside its title and sections, given by every step that records a decision:
one home for them, imported plainly, never star-imported. The statement says nothing any search scenario looks for,
and each decision of one scenario is given a number of its own. A decision links to its shop, so a step recording one
first records, through `shop_of`, a product and a shop of it in the scenario's own knowledge base."""
from driver import record

STATEMENT = "The shop settled this one way."
DATE = "2026-10-07"
PURPOSE = {"title": "Purpose", "body": "Hold what was decided.\n"}
SHOP_SECTIONS = [PURPOSE, {"title": "Order of building", "body": "One by one.\n"}, {"title": "Testing", "body": "By hand.\n"}]


def without_shop(number: int) -> dict:
    """A decision's statement, date and number, the number as the step gives it: what a decision requires beside its
    title, sections and the shop it links to."""
    return {"statement": STATEMENT, "date": DATE, "number": number}


def decided(number: int, shop: str) -> dict:
    """A decision's required fields with its shop, `shop` the name kb minted."""
    return {**without_shop(number), "shop": shop}


def shop_of(env, tmp_path, title: str = "Front counter") -> str:
    """A product and a shop of it titled `title`, recorded as the user does in the knowledge base `env` reaches; return
    the shop's name, for the scenario's decisions to link to."""
    product = record(env, tmp_path, "product", {"title": "Main street", "gist": "A street of shops.", "sections": [PURPOSE]},
                     "Record the product")
    return record(env, tmp_path, "shop", {"title": title, "product": product, "gist": "Serves who comes in.",
                                          "sections": SHOP_SECTIONS}, "Record the shop")
