"""The shop's types, loaded through Create when a knowledge base starts. kb never learns them any other way."""
from importlib import resources

from kb.content import dumps, loads
from kb.contract import kb_pb2

TYPES = ("shop-artifact", "tag", "decision", "work-item", "feature", "role", "step", "process")


def load(client, actor):
    """Each type's Create answer, as it is made: the next Create is made only when the caller asks for the next answer."""
    for name in TYPES:
        text = resources.files("shop_knowledge.types").joinpath(f"{name}.yaml").read_text()
        content = loads(text)
        title = content.pop("title")
        yield client.Create(kb_pb2.CreateRequest(
            type="schema", title=title, content=dumps(content), actor=actor,
            message=f"Define the shop's {title.lower()} type",
        ))
