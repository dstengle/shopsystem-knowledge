"""A shop's decisions as files: the ledger, `spec/decisions.md`, and a record for each of the shop's own decisions,
`adrs/<number>-<name>.md`. The shop's own are those its `decisions` names; the others are those its capabilities rest on
that the shop does not name, each listed with the shop whose `decisions` names it."""
from typing import NamedTuple

from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.renderers import names, published_from, sections, source


class Decision(NamedTuple):
    id: str
    title: str
    content: dict
    shop: str | None = None
    revision: int = 0

    @property
    def number(self) -> str:
        """The number padded with zeros to four digits, written in full where it is longer."""
        return padded(self.content["number"])

    @property
    def path(self) -> str:
        return f"adrs/{self.number}-{names.from_title(self.title)}.md"


def padded(number: int) -> str:
    return f"{number:04d}"


def files(client, shop: kb_pb2.Artifact, shop_content: dict, capabilities: list[dict]):
    """The ledger and the records by path, or the faults of the first read that was refused."""
    own, faults = read(client, shop_content.get("decisions", []))
    if faults:
        return {}, faults
    others, faults = _others(client, resting_on(capabilities, shop_content.get("decisions", [])))
    if faults:
        return {}, faults
    records, faults = _records(client, sorted(own, key=_by_number))
    if faults:
        return {}, faults
    ledger = _ledger(shop, sorted(own, key=_by_number) + sorted(others, key=lambda each: (each.shop, _by_number(each))))
    return {"spec/decisions.md": ledger, **records}, []


def _by_number(decision: Decision) -> int:
    return decision.content["number"]


def resting_on(capabilities: list[dict], own: list[str]) -> list[str]:
    """The decisions the capabilities rest on that the shop does not name, each once."""
    resting = [id for content in capabilities for id in content.get("rests_on", [])]
    return [id for id in dict.fromkeys(resting) if id not in own]


def read(client, ids: list[str]):
    """Each decision read whole, or the faults of the first read that was refused."""
    decisions = []
    for id in ids:
        read = source.whole(client, id)
        if faults := source.faults(read):
            return [], faults
        decisions.append(Decision(id, read.result.title, loads(read.result.content), revision=read.result.revision))
    return decisions, []


def _others(client, ids: list[str]):
    """Each decision with the shop whose `decisions` names it."""
    decisions, faults = read(client, ids)
    if faults:
        return [], faults
    held = []
    for decision in decisions:
        owners, faults = owners_of(client, decision.id)
        if faults:
            return [], faults
        held.append(decision._replace(shop=owners[0]))
    return held, []


def owners_of(client, id: str):
    """The shops whose `decisions` name the decision, or the faults of the question that was refused."""
    followed = client.Follow(kb_pb2.FollowRequest(
        locator=kb_pb2.Locator(id=id), depth=1, direction=kb_pb2.FollowRequest.IN, via="decisions", kind="shop"))
    return [each.stub.id for each in followed.result.reached], list(followed.refusal.faults)


def _ledger(shop: kb_pb2.Artifact, decisions: list[Decision]) -> str:
    return "\n\n".join([published_from.markdown(shop.id, shop.revision), "# Decisions", *(_entry(each) for each in decisions)]) + "\n"


def _entry(decision: Decision) -> str:
    content = decision.content
    lines = [f"date: {content['date']}"]
    if "revisit_when" in content:
        lines.append(f"revisit_when: {content['revisit_when']}")
    if "supersedes" in content:
        lines.append(f"supersedes: {content['supersedes']}")
    lines.append(f"source: {decision.path}" if decision.shop is None else f"source: {decision.shop}: {decision.path}")
    return "\n\n".join([sections.heading(2, decision.id), content["statement"], "\n".join(lines)])


def _records(client, decisions: list[Decision]):
    records = {}
    for decision in decisions:
        numbers, faults = _numbers(client, decision.content)
        if faults:
            return {}, faults
        records[decision.path] = _record(decision, numbers)
    return records, []


def _numbers(client, content: dict):
    """The numbers of the decisions this one supersedes and extends, as they are written in its record."""
    named = [*([content["supersedes"]] if "supersedes" in content else []), *content.get("extends", [])]
    decisions, faults = read(client, named)
    return {each.id: each.number for each in decisions}, faults


def _record(decision: Decision, numbers: dict[str, str]) -> str:
    content = decision.content
    held = {section["title"]: section.get("body", "").rstrip() for section in content.get("sections", [])}
    blocks = [published_from.markdown(decision.id, decision.revision), sections.heading(1, f"{decision.number} {decision.title}"),
              f"{content['date']}. {held.get('Purpose', '')}", held.get("Rationale", "")]
    links = [f"Supersedes {numbers[content['supersedes']]}."] if "supersedes" in content else []
    links += [f"Extends {numbers[id]}." for id in content.get("extends", [])]
    if links:
        blocks.append("\n".join(links))
    return "\n\n".join(blocks) + "\n"
