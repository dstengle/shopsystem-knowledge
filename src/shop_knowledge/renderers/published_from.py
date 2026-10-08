"""The line every file of a published spec carries to say it came from the knowledge base and is not to be edited by
hand, naming the artifact it is published from and that artifact's revision: an HTML comment in a markdown file, a `#`
comment in a feature file. The one place the line is worded, and so the one place a line is told to be one."""
import re

_SAID, _UNSAID = "published from the knowledge base: ", "; do not edit by hand"


def _words(name: str, revision: int) -> str:
    return f"{_SAID}{name}@{revision}{_UNSAID}"


def markdown(name: str, revision: int) -> str:
    return f"<!-- {_words(name, revision)} -->"


def gherkin(name: str, revision: int) -> str:
    return f"# {_words(name, revision)}"


_ANY_WORDS = rf"{re.escape(_SAID)}\S+@\d+{re.escape(_UNSAID)}"
_LINE = re.compile(rf"<!-- {_ANY_WORDS} -->|# {_ANY_WORDS}")


def is_line(line: str) -> bool:
    """Whether `line` is the line as `markdown` or `gherkin` words it, for any artifact's name and revision."""
    return _LINE.fullmatch(line) is not None
