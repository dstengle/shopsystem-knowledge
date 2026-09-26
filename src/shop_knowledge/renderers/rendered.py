"""What every renderer gives back: the files to write, by path under the directory asked for, or the faults that stop
it. It carries its faults the way kb's answers do, so the command line refuses both the one way it refuses anything."""
from typing import NamedTuple

from kb.contract import kb_pb2


class Rendered(NamedTuple):
    files: dict[str, str]
    faults: list[kb_pb2.Fault]


def refused(faults) -> Rendered:
    return Rendered({}, list(faults))
