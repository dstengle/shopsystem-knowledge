"""The fields the decision type requires beside its title and sections, given by every step that records a decision:
one home for them, imported plainly, never star-imported. The statement says nothing any search scenario looks for,
and each decision of one scenario is given a number of its own."""
STATEMENT = "The shop settled this one way."
DATE = "2026-10-07"


def decided(number: int) -> dict:
    """A decision's statement, date and number, the number as the step gives it."""
    return {"statement": STATEMENT, "date": DATE, "number": number}
