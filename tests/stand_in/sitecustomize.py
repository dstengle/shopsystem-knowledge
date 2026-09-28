"""A stand-in for kb at its contract boundary, loaded by every Python process started with this directory on
PYTHONPATH, as the steps start shop-knol through `driver.answering`. It puts itself in front of `kb.client.connect`:
a call the scenario described is answered with the `kb_pb2` message the step wrote, and every other call reaches the
real kb unchanged. Told nothing (no KB_STAND_IN), it answers nothing itself.

KB_STAND_IN names a YAML file the step wrote: a list of answers, each
  call:    the client call it answers, such as Validate or Read
  asking:  optional; request fields the call must carry to be answered, such as {locator: {id: decision/x}}
  answer:  the response message's fields, as the step wrote them
  from_kb: optional; repeated fields of the response taken from the real kb's own answer to the same call
It knows kb only through what kb publishes: `kb.client`, `kb.contract` and `kb.content`."""
import os
from pathlib import Path

import kb.client
from google.protobuf import json_format
from kb.content import loads
from kb.contract import kb_pb2

_real_connect = kb.client.connect


def _described() -> list:
    source = os.environ.get("KB_STAND_IN")
    return loads(Path(source).read_text()) if source else []


def _asks(answer: dict, request) -> bool:
    """Whether the request matches the answer's `asking`: each top-level field `asking` names must equal the
    request's field of that name exactly, so a nested message (`locator`, say) is compared whole, not itself field
    by field. A field `asking` does not name is not compared, and does not keep the answer from matching."""
    asked = json_format.MessageToDict(request, preserving_proto_field_name=True)
    return all(asked.get(field) == value for field, value in answer.get("asking", {}).items())


def _response(rpc: str, answer: dict, real):
    """The message the step described, with any fields it takes from the real kb's answer to the same request."""
    message = json_format.ParseDict(answer["answer"], getattr(kb_pb2, f"{rpc}Response")())
    if answer.get("from_kb"):
        for field in answer["from_kb"]:
            getattr(message, field).extend(getattr(real, field))
    return message


class _StandIn:
    """A client that answers the described calls itself and hands every other call to the real client."""

    def __init__(self, real, answers: list):
        self._real = real
        self._answers = answers

    def __getattr__(self, rpc: str):
        call = getattr(self._real, rpc)
        described = [answer for answer in self._answers if answer["call"] == rpc]
        if not described:
            return call

        def answered(request, timeout=None):
            """The real kb is always asked first: a call it refuses (no store found, say) is refused the same way
            whether or not a step described it, so a described answer never hides a refusal the real kb would give.
            Only when the real kb carries no faults does a matching description answer instead."""
            real = call(request, timeout=timeout)
            if real.faults:
                return real
            for answer in described:
                if _asks(answer, request):
                    return _response(rpc, answer, real)
            return real

        return answered


def connect(root=None, *, clock=None):
    """kb's own client, given the clock the caller gives (kb adrs/0018), behind the stand-in."""
    return _StandIn(_real_connect(root, clock=clock), _described())


kb.client.connect = connect
