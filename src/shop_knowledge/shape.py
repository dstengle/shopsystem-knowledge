"""The shape of each file a user gives, held as JSON Schema under shapes/ and checked with the validator kb checks a
type with, so a violation comes out in kb's words: the file, the place, the keyword and the message."""
from importlib import resources

from jsonschema import Draft202012Validator
from kb.content import loads
from kb.contract import kb_pb2


def violations(document, shape: str, source: str) -> list[kb_pb2.Fault]:
    """The faults on the file `source` where `document` is not the named shape; none when it is."""
    text = resources.files("shop_knowledge.shapes").joinpath(f"{shape}.yaml").read_text()
    return [
        kb_pb2.Fault(
            artifact=source,
            place="/".join(str(part) for part in error.absolute_path),
            rule=error.validator,
            message=error.message,
        )
        for error in Draft202012Validator(loads(text)).iter_errors(document)
    ]
