"""The names a published spec's files are given: a title made into a name, the one rule the spec's files share."""
import re

_APOSTROPHES = re.compile("['’]")
_OTHER = re.compile("[^a-z0-9]+")


def from_title(title: str) -> str:
    """The title lower-cased, every straight and curly apostrophe dropped, every run of characters other than the
    unaccented letters a to z and the digits 0 to 9 made one `-`, and no `-` at either end."""
    return _OTHER.sub("-", _APOSTROPHES.sub("", title.lower())).strip("-")
