"""The line every file of a published spec carries to say it came from the knowledge base and is not to be edited by
hand, naming the artifact it is published from and that artifact's revision: an HTML comment in a markdown file, a `#`
comment in a feature file."""


def _words(name: str, revision: int) -> str:
    return f"published from the knowledge base: {name}@{revision}; do not edit by hand"


def markdown(name: str, revision: int) -> str:
    return f"<!-- {_words(name, revision)} -->"


def gherkin(name: str, revision: int) -> str:
    return f"# {_words(name, revision)}"
