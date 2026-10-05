"""The shop's types, loaded through Create when a knowledge base starts. kb never learns them any other way."""
from importlib import resources

from kb.content import dumps, loads
from kb.contract import kb_pb2

TYPES = ("shop-artifact", "tag", "decision", "work-item", "feature", "role", "step", "process")
BASE = "shop-artifact"
"""The one entry of TYPES that is no type of the shop's: the common fields the seven build on."""
SHOP_TYPES = tuple(name for name in TYPES if name != BASE)


def load(client, signed: kb_pb2.Signature):
    """Each type's Create answer, as it is made, signed by the role and piece of work that started the knowledge base,
    with a message of its own: the next Create is made only when the caller asks for the next answer."""
    for name in TYPES:
        text = resources.files("shop_knowledge.types").joinpath(f"{name}.yaml").read_text()
        content = loads(text)
        title = content.pop("title")
        signature = kb_pb2.Signature(
            role=signed.role, execution=signed.execution, message=f"Define the shop's {title.lower()} type",
        )
        yield client.Create(kb_pb2.CreateRequest(kind="schema", title=title, content=dumps(content), signature=signature))
