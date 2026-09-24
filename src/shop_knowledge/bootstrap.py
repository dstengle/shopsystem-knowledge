"""The shop's types, loaded through Create when a knowledge base starts. kb never learns them any other way."""
from importlib import resources

import yaml
from kb.content import dumps
from kb.contract import kb_pb2

TYPES = ("tag", "decision", "work-item")


def load(client, actor):
    for name in TYPES:
        text = resources.files("shop_knowledge.types").joinpath(f"{name}.yaml").read_text()
        content = yaml.safe_load(text)
        title = content.pop("title")
        client.Create(kb_pb2.CreateRequest(
            type="schema", title=title, content=dumps(content), actor=actor,
            message=f"Define the shop's {title.lower()} type",
        ))
