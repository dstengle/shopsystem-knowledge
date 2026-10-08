"""A shop's decisions as files: the ledger, `spec/decisions.md`, and a record for each of the shop's own decisions,
`adrs/<number>-<name>.md`. The shop's decisions are those linking to it."""
from typing import NamedTuple

from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.renderers import names, published_from, sections, source


class Decision(NamedTuple):
    id: str
    title: str
    content: dict
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


def files(client, shop: kb_pb2.Artifact):
    """The ledger and the records by path, or the faults of the first read that was refused."""
    own, faults = of(client, shop.id)
    if faults:
        return {}, faults
    own = sorted(own, key=_by_number)
    records, faults = _records(client, own)
    if faults:
        return {}, faults
    return {"spec/decisions.md": _ledger(shop, own), **records}, []


def _by_number(decision: Decision) -> int:
    return decision.content["number"]


def of(client, shop: str):
    """The decisions linking to the shop, each read whole, or the faults of the list or read that was refused."""
    listed = client.List(kb_pb2.ListRequest(kind="decision", fields={"shop": shop}, form=kb_pb2.ListRequest.IDS))
    if faults := list(listed.refusal.faults):
        return [], faults
    return read(client, list(listed.result.ids))


def read(client, ids: list[str]):
    """Each decision read whole, or the faults of the first read that was refused."""
    decisions = []
    for id in ids:
        read = source.whole(client, id)
        if faults := source.faults(read):
            return [], faults
        decisions.append(Decision(id, read.result.title, loads(read.result.content), revision=read.result.revision))
    return decisions, []


def _ledger(shop: kb_pb2.Artifact, decisions: list[Decision]) -> str:
    return "\n\n".join([published_from.markdown(shop.id, shop.revision), "# Decisions", *(_entry(each) for each in decisions)]) + "\n"


def _entry(decision: Decision) -> str:
    content = decision.content
    lines = [f"date: {content['date']}"]
    if "revisit_when" in content:
        lines.append(f"revisit_when: {content['revisit_when']}")
    if "supersedes" in content:
        lines.append(f"supersedes: {content['supersedes']}")
    lines.append(f"source: {decision.path}")
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
