# Pre-tag Implementation Plan: slices 1 and 54 to 63

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `2026-09-23-shop-knowledge-slices.md`; inside a task, follow `shopsystem-bdd:bdd-red-green` scenario by scenario. That skill's stop conditions, hand-back, and checkpoint apply and override any step here that would conflict with them.

**Goal:** Everything kb 0.1 writes to disk or refuses on Init, Create, and Read is pinned before the tag: the start scenario of slice 1 is green again with the store started under a role, and the ten slices between slice 1 and the tag are green, so that the file on disk is in canonical form, the title travels beside the content, the store is found the way git finds a repository, starting a store leaves the first journal entry, and a bad title, bad content, bad name, or missing role is met with a fault and nothing written.

**Architecture:** kb (`/home/vscode/shopsystem-kb`) is a Python package `kb` with a protobuf contract under `kb.contract`, a servicer over a `Store` (one canonical YAML file per artifact under `<root>/kb/`, itself a git repository), and an in-process client with the stub's method names. This plan adds four small modules beside the store: `discovery` (finding the store), `journal` (one file per entry), `locators` (the grammar of a name and a place), and the checks in `content` and `validation`. shop-knowledge (`/home/vscode/shopsystem-knowledge`) is a Python package `shop_knowledge` whose `shop-knol` command builds contract messages and calls kb through the in-process client; it changes only where the contract does (the actor on Init, the title beside the content).

**Provenance:** Every code block in this plan was assembled in scratch copies of both repositories (`/tmp/pretag/kb`, `/tmp/pretag/shop`, with `PYTHONPATH` pointing at their `src/` directories ahead of the editable installs) on 2026-09-24 and run: the 27 kb scenarios of slices 1 and 54 to 63 pass, the two shop-knowledge scenarios of slice 1 pass throughout, and the shell walk-through in the closing section gives the output stated there. The repositories themselves were not touched.

**Tech Stack:** Python 3.11, setuptools (src layout), protobuf + grpcio (generated code committed; grpcio-tools only to regenerate, `make contract`), python-jsonschema (Draft 2020-12), PyYAML, git via subprocess, pytest + pytest-bdd 8, argparse.

**Spec:** `/home/vscode/shopsystem-kb/docs/superpowers/specs/2026-09-23-kb-design.md` (Serialization, The contract, Input safety, Write path) and `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md` (The CLI). Slice plan: `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`. Feature files: `features/` in each repository; the scenarios of each slice carry `@slice-<n>`, so `python -m pytest -q -m slice-<n>` runs a slice.

## Global Constraints

- Feature files are read-only for the implementer. Only `slicing-into-increments` edits a tag line; only `formulating-features` edits a Given, When, or Then. Any diff under `features/` other than what those skills make is a stop condition.
- Code only what a scenario asserts (bdd-red-green). Where the scenarios are silent, the code is silent; the silence goes into the checkpoint entry as an open question. The decisions this plan makes are listed below, each justified by a scenario line.
- kb knows nothing about any domain: "It ships no schemas beyond the metaschema and no renderers." Domain types live in shop-knowledge only.
- kb is exercised through its in-process transport, never mocked (both specs' Testing sections).
- Git is canonical: "Every change goes through the API: validate, write, journal, serialize, commit. Nothing else edits the serialized text." The commit's author comes from the actor.
- Canonical form: "Identity keys first in the order above, then fields in schema order, then `sections`, then part collections in schema order. Every prose body is a literal block scalar, however short. Two-space indent, sequences indented under their key, no line folding at any width, no flow style, no comments, no anchors, no tags. The same tree always serializes to the same bytes."
- The contract: "The identity keys `id`, `type`, `schema_version`, `revision`, and `title` are typed fields of the messages that carry an artifact. `content` is canonical YAML text holding only what the schema defines: fields, sections, and parts. Content that carries an identity key, `title` included, is refused as a violation naming the key." `Create` is "Refused without a title, or when content carries an identity key"; `Read` is "Refused with a fault naming the id when the store does not hold it".
- Input safety: an id matches `<type>/<slug>` with slug `[a-z0-9]+(-[a-z0-9]+)*`; a part path is node names of the same alphabet or a collection name then an item id; "Anything else, including `.`, `..`, `/` in a segment, or an absolute path, is refused as a fault; no file is resolved from it." A slug is minted "by lowercasing, replacing runs of anything outside `[a-z0-9]` with one hyphen, and trimming hyphens. A title that yields nothing is refused." Titles are strings: "2026-09-24" and "yes" are titles. Content is parsed "with a safe loader: no tags, no anchors resolving to code, no documents beyond the first. A section has exactly `title`, `body`, and `sections`; any other key is a violation."
- Finding the store: "from the working directory upward until a directory holding `kb/store.yaml` is met, or `KB_ROOT` names one explicitly. Neither found, the call is refused and says so. `KB_ROOT` naming a directory with no store is its own refusal, naming `KB_ROOT`. The working directory inside one store while `KB_ROOT` names a different one is refused too: nothing is guessed."
- Init: "creates the store as the subdirectory `kb/` of the root and writes the metaschema there, journalled under the actor, supplied through `KB_ACTOR` and required, with the message "initialise store"; the entry is the metaschema write, artifact `schema/schema` at revision 1 with its digest."
- Journal entry: "`id`, `at`, `actor: { role, execution }`, `op`, `artifact`, `path`, `revision`, `schema_version`, `digest` (sha256 of the canonical bytes after the write), `message`, and `batch`: the id of the `Apply` that wrote it, or the entry's own id for a single operation". One file per entry at `journal/<YYYY>/<MM>/<DD>/<timestamp>-<seq>.yaml`.
- Errors are a typed list of `{ artifact, path, rule, message }`; a response that carries faults is a refusal and nothing was written.
- `shop-knol init <root>` "needs an actor but no `-m`, its messages are fixed". `shop-knol create` sends the title beside the content; ids are minted by kb and never supplied by the user.
- Python `>=3.11`. One user-site Python environment serves both checkouts (`pip install -e` lands in `~/.local`); `make dev` in either repo reinstalls after a `pyproject.toml` change, `make contract` in kb regenerates `kb_pb2*.py` after a `kb.proto` change.
- Commits in both repos end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- After every kb task, the shop-knowledge suite's slice 1 must still pass: `cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1` -> `2 passed`.

## Decisions this plan makes (the spec left them open or silent)

1. **What is prose.** The spec says "every prose body is a literal block scalar". This plan writes every string under a key named `body` (a section's body, an item's body, a field named `body`) as a literal block, and every other string plain, quoted only when YAML would otherwise read it as another type. Pinned by slice 54 (four bodies, two of them one short line) and slice 58 (a quoted title).
2. **Title validated as part of the artifact.** The title travels as a field of `CreateRequest`; kb validates `{"title": <the field>, **content}` against the type, so every type, and the metaschema, keep declaring `title` among their properties and may require it, while content carrying `title` is refused before validation. The metaschema does not change. Pinned by slice 55 and by slice 1 staying green.
3. **Journal entry id and time.** `id` is `<YYYYmmddTHHMMSSffffff>Z-<seq>` with `seq` 1 for a change made alone; `at` is ISO 8601 UTC; `execution` is the empty string when the actor has none. `journal.now()` is a module function so slice 9 can set the clock from outside. Pinned by slice 57 (one entry, its role, message, op, artifact, revision, digest).
4. **Discovery lives in the client.** `kb.client.connect()` with no root reads `Path.cwd()` and `os.environ` and finds the store; an explicit root bypasses discovery, so `shop-knol`, which still passes `KB_ROOT` outright, is unchanged until slice 21. A client built over a refusal answers every call with that fault. Pinned by slices 56 and 61.
5. **Fault rules.** `title` (missing, or nothing to make a name from), `identity` (an identity key in content), `content` (a tag, or more than one document), `section` (a key besides title, body, sections), `locator` (a name or place that is not plain), `not-found` (a name the store lacks), `store` (no store found, or two), `actor` (no role on Init). Each message says what the scenario's Then line says and names back what it carried. Pinned by slices 55, 59, 60, 61, 63.
6. **Not-found is a file check on a validated id.** After the locator grammar passes, `Read` refuses when no file sits at the path derived from the id; a kind with no schema falls under the same refusal, since no file can sit there. Pinned by slice 60.
7. **Order of checks on Create.** Parse the content (tags, documents), then the title (present, yields a name), then identity keys in content, then JSON Schema and the section shape together, then write. Each stage returns its faults before the next runs. Pinned by slices 55 and 59; slice 7 later asks that JSON Schema and kb-keyword faults arrive together, which the last stage already does.

## Review Focus

writing-plans asks that each line here get a test in the owning task. In this project tests are scenarios and the feature files are the human gate, so no unit tests are added; each line instead goes into the owning task's checkpoint entry as an open question, or names the later scenario that pins it.

1. **A body with a space at the end of a line, or an empty body** (`body: "Keep prices.  \n"`, `body: ""`): PyYAML refuses block style for such a string and writes it double-quoted, so the file is not in canonical form and a person opening it sees a quoted string among blocks. No scenario pins it. Task 2 logs it.
2. **Content that is not a mapping, or is not YAML at all** (`- a list`, `just words`, `title: [unclosed`): `loads` returns a list or a string, or PyYAML raises, and the client sees a traceback instead of a fault naming the artifact. No scenario pins it. Task 7 logs it.
3. **`sections` that is not a list** (`sections: Purpose`): the section check iterates a string and reports nonsense paths, or raises on an integer, before JSON Schema has its say. No scenario pins it. Task 7 logs it.
4. **`KB_ROOT` set to the empty string**: discovery treats it as naming `.`, so a call from inside a store is refused as "KB_ROOT names a directory that holds no store" when a person expects unset behaviour. No scenario pins it. Task 9 logs it.
5. **`shop-knol read` of a name the store lacks or that is not plain**: kb now refuses with a fault, but the shop command prints an empty artifact and exits 0. Slice 21 pins the shop's discovery refusals ("the command reports failure"); the not-found and bad-name cases have no shop scenario. Task 8 logs it.

---

### Task 1: Slice 1, the client starts a store saying which role it is

**Slice plan entry:** Slice 1, capability, re-opened. Five of its six scenarios pass; the one to make green:

1. kb / start-a-store / The client starts a store

Its When now reads "the client starts a store there, saying which role it is". The store is started under a role, and the role authors the commit. Nothing else in the slice changes.

**Files (kb):**
- Modify: `src/kb/contract/kb.proto` (`InitRequest.actor`), regenerate `kb_pb2*.py` with `make contract`
- Modify: `src/kb/servicer.py` (`Init` commits as the actor)
- Modify: `tests/test_start_a_store.py`, `tests/conftest.py`, `tests/test_create_an_artifact.py`, `tests/test_read_an_artifact.py` (every `Init` in the suite says which role)

**Files (shop-knowledge):**
- Modify: `src/shop_knowledge/cli.py` (`init` passes the actor)
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: everything slice 1 built: `kb.client.connect(root)`, `kb.store.Store`, `tests/calls.py` with `CLIENT = kb_pb2.Actor(role="client")`, `define`, `create`, `read`.
- Produces: `InitRequest{root, actor}`; every later task starts stores with `client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))`.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_starts_a_store 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: When "the client starts a store there, saying which role it is"`.

- [ ] **Step 2: The actor on the request**

In `/home/vscode/shopsystem-kb/src/kb/contract/kb.proto` replace

```proto
message InitRequest {
  string root = 1;
}
```

with

```proto
message InitRequest {
  string root = 1;
  Actor actor = 2;
}
```

Then regenerate:

```bash
cd /home/vscode/shopsystem-kb && make contract
```

- [ ] **Step 3: The step, saying which role**

In `/home/vscode/shopsystem-kb/tests/test_start_a_store.py` change the import and the When:

```python
from calls import CLIENT, define, read
```

```python
@when("the client starts a store there, saying which role it is", target_fixture="client")
def _start_a_store(root):
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))
    return client
```

The old step text ("the client starts a store there") is gone from the feature; delete the old function.

- [ ] **Step 4: The least code: the role authors the commit**

In `/home/vscode/shopsystem-kb/src/kb/servicer.py`, in `Init`, replace

```python
        store.commit([store.dir / "store.yaml", path], "kb", "Start the store")
```

with

```python
        store.commit([store.dir / "store.yaml", path], request.actor.role, "Start the store")
```

- [ ] **Step 5: Every other Init in the suite says which role too**

The shared Given and the two Backgrounds start stores; make them say who, so Task 11's refusal of a role-less Init does not break them later.

`/home/vscode/shopsystem-kb/tests/conftest.py`:

```python
from calls import CLIENT
from kb import client as kb_client
from kb.contract import kb_pb2
```

```python
@given("a store", target_fixture="client")
def _a_store(root):
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))
    return client
```

`/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`: import `CLIENT` (`from calls import CLIENT, DECISION_TYPE, create, define, read`) and in `_store_with_decision_type` write `client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))`.

`/home/vscode/shopsystem-kb/tests/test_read_an_artifact.py`: import `CLIENT` (`from calls import CLIENT, DECISION_TYPE, WORK_ITEM_TYPE, create, define, read`) and in `_store_with_a_linked_decision` write `client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))`.

- [ ] **Step 6: The shop's init says who**

In `/home/vscode/shopsystem-knowledge/src/shop_knowledge/cli.py`, in `_init`:

```python
def _init(args) -> int:
    root = Path(args.root)
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root), actor=_actor()))
    bootstrap.load(client, _actor())
    return 0
```

- [ ] **Step 7: Run it green, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
```

Expected: `4 passed, 96 deselected`; `2 passed, 55 deselected`; `96 failed, 4 passed`.

Then at a shell, the commit's author is the role:

```bash
cd $(mktemp -d) && python -c "
from kb import client as c; from kb.contract import kb_pb2
c.connect('.').Init(kb_pb2.InitRequest(root='.', actor=kb_pb2.Actor(role='client')))" && git -C kb log --format='%an%x09%s'
```

Expected: `client	Start the store`.

- [ ] **Step 8: Commit, both repositories**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/contract src/kb/servicer.py tests && git commit -m "Slice 1: a store is started under a role, which authors the commit

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
cd /home/vscode/shopsystem-knowledge && git add src/shop_knowledge/cli.py && git commit -m "Slice 1: shop-knol init says who starts the store

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 9: Checkpoint**

In `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md` set slice 1's Status back to `green` and append to the log:

```
- <date> slice 1 green again. Someone can now: start a store saying which role they are, and find that role as the author of the store's first commit; the other five scenarios of the skeleton are as they were.
  Surprised by: <what building it turned out to involve that the plan didn't say | nothing>.
  Open questions: none. Next: slice 54.
```

```bash
git add docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git commit -m "Slice 1 green again

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: Slice 54, an artifact's file on disk is in canonical form

**Slice plan entry:** Slice 54, capability. Unknown: can PyYAML's emitter be made to give every prose body as a literal block however short, every sequence indented under its key, no line folded at any width and no tag, or must kb write the form itself? Scenario:

1. kb / look-after-a-store / The operator reads an artifact's file on disk

**Files (kb):**
- Modify: `src/kb/canonical.py` (the dumper)
- Modify: `tests/test_look_after_a_store.py` (from the bare `scenarios(...)` line to the steps)

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.canonical.dump(artifact) -> str`, used by `Store.save`, `content.dumps`, and the journal; `tests/calls.py`.
- Produces: `kb.canonical.Prose(str)`, the marker for a body; `dump` writes every `body` as a literal block, sequences indented two spaces under their key, no folding. Task 5's journal entries and Task 10's byte comparison rest on this.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-54 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: Given "a store holding a decision whose purpose is one short line and which carries a list of options"`.

- [ ] **Step 2: The steps**

Replace `/home/vscode/shopsystem-kb/tests/test_look_after_a_store.py` with:

```python
import re

from pytest_bdd import given, scenarios, then, when

from calls import CLIENT, DECISION_TYPE, create, define
from kb import client as kb_client
from kb.contract import kb_pb2

scenarios("look-after-a-store.feature")

LONG_LINE = (
    "Costs move weekly, and a review that runs once a month lags them by three weeks on average, "
    "which is long enough to lose money on every shelf in the shop."
)


@given(
    "a store holding a decision whose purpose is one short line and which carries a list of options",
    target_fixture="decision_file",
)
def _store_with_a_short_decision(root):
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))
    define(client, DECISION_TYPE)
    created = create(client, "decision", {
        "title": "Price reviews happen weekly",
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": LONG_LINE + "\n"},
        ],
        "options": [
            {"title": "Keep weekly", "body": "Review every Monday."},
            {"title": "Go monthly", "body": "Review on the first of the month."},
        ],
    })
    return root / "kb" / f"{created.id}.yaml"


@when("the operator opens the decision's file", target_fixture="text")
def _open_the_file(decision_file):
    return decision_file.read_text()


@then("every piece of prose stands as a block of its own, however short it is")
def _prose_as_blocks(text):
    bodies = re.findall(r"^\s*body: (.*)$", text, re.M)
    assert len(bodies) == 4, text
    assert all(marker in ("|", "|-") for marker in bodies), text


@then("each list is written beneath the name it belongs to, indented under it")
def _lists_indented(text):
    assert re.search(r"^sections:\n  - title: Purpose$", text, re.M), text
    assert re.search(r"^options:\n  - id: keep-weekly$", text, re.M), text


@then("no line of prose has been broken to fit a width")
def _no_folding(text):
    assert ("\n      " + LONG_LINE + "\n") in text, text


@then("nothing in the file tells a reader how to build a value")
def _no_tags(text):
    assert not re.search(r"\s!\S", text), text
```

Run it: `python -m pytest -q -m slice-54 2>&1 | grep -E '^E  |passed|failed' | head -3`. Expected: the first Then fails, `assert all(marker in ("|", "|-") for marker in bodies)`, because the two option bodies, having no newline, are written plain.

- [ ] **Step 3: The least code: the emitter**

In `/home/vscode/shopsystem-kb/src/kb/canonical.py` replace everything from `class _Dumper` through `def dump(...)` with:

```python
class Prose(str):
    """A prose body. Written as a literal block, however short."""


class _Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        """Sequences sit indented under their key, never flush with it."""
        return super().increase_indent(flow, False)


def _represent_mapping(dumper, mapping):
    """Every value under a `body` key is prose."""
    items = [
        (key, Prose(value) if key == "body" and isinstance(value, str) else value)
        for key, value in mapping.items()
    ]
    return dumper.represent_mapping("tag:yaml.org,2002:map", items)


def _represent_prose(dumper, value):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(value), style="|")


def _represent_str(dumper, value):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_Dumper.add_representer(dict, _represent_mapping)
_Dumper.add_representer(Prose, _represent_prose)
_Dumper.add_representer(str, _represent_str)


def dump(artifact: dict) -> str:
    """Block style, keys in the order given, prose as literal blocks, no line folded at any width."""
    return yaml.dump(
        artifact, Dumper=_Dumper, sort_keys=False, default_flow_style=False,
        allow_unicode=True, width=float("inf"),
    )
```

`load`, `order`, `_section`, `_item`, and `IDENTITY` stay as they are.

- [ ] **Step 4: Run it green, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-54 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `1 passed`; `95 failed, 5 passed`; `2 passed`.

At a shell, a decision's file now reads:

```
id: decision/price-reviews-happen-weekly
type: decision
schema_version: 1
revision: 1
title: Price reviews happen weekly
sections:
  - title: Purpose
    body: |
      Keep prices in step with costs.
  - title: Rationale
    body: |
      Costs move weekly.
options:
  - id: keep-weekly
    title: Keep weekly
    body: |-
      Review every Monday.
```

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/canonical.py tests/test_look_after_a_store.py && git commit -m "Slice 54: the file on disk is in canonical form

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 54's Status to `green` and append to the slice plan's log:

```
- <date> slice 54 green. Someone can now: open any artifact's file and find every body a literal block however short, every list indented under its key, no line folded, and no tag.
  Assumption "PyYAML's emitter can be made to write the canonical form": held. Evidence: <the file from Step 4>. A marker class on `body` values, an `increase_indent` override, and `width=float("inf")` were enough; kb writes no YAML of its own.
  Surprised by: <...>.
  Open questions:
  - QUESTION FOR THE SPEC: a body with a space at the end of a line, or an empty body, cannot be a block scalar in YAML; PyYAML writes it double-quoted. Is such a body refused on the way in, or is a quoted string acceptable in the canonical form? No scenario pins it.
  Next: slice 55.
```

Commit the plan: `git add docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git commit -m "Slice 54 green" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"`.

---

### Task 3: Slice 55, the title travels beside the content, never inside it

**Slice plan entry:** Slice 55, capability. Unknown: when the title travels beside the content as a field of the message, what becomes of the title every type, and the type that describes types, declares among its content, while the file on disk still carries the title among its identity keys? Needs: the shop's record command lifting the title out of the user's file, so slice 1's record scenario stays green. Scenario:

1. kb / create-an-artifact / Content carrying a title of its own is refused

**Files (kb):**
- Modify: `src/kb/contract/kb.proto` (`CreateRequest.title`), regenerate with `make contract`
- Modify: `src/kb/servicer.py` (`Create`)
- Modify: `tests/calls.py` (`request`, `create`, `define`), `tests/test_create_an_artifact.py`

**Files (shop-knowledge):**
- Modify: `src/shop_knowledge/cli.py` (`_create`), `src/shop_knowledge/bootstrap.py` (`load`)
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `CreateRequest{type, content, actor, message}`, `kb.canonical.IDENTITY`, `kb.store.slug`.
- Produces: `CreateRequest{type, content, actor, message, title}`. In `tests/calls.py`: `request(client, type_name, title, content, message="Create an artifact") -> CreateResponse` (no assertion on faults), `create(client, type_name, content, message=...)` (lifts `title` out of the dict, asserts no faults), `define(client, type_content)` (a `create` of type `schema`). Every later task's refusal steps use `request`.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-55 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: When "the client creates a decision whose content carries a title as well as the title given alongside it, saying which role and why"`.

- [ ] **Step 2: The title on the request**

In `/home/vscode/shopsystem-kb/src/kb/contract/kb.proto` replace the `CreateRequest` message with:

```proto
// The title travels here, never inside the content.
message CreateRequest {
  string type = 1;
  string content = 2;  // canonical YAML: fields, sections, parts
  Actor actor = 3;
  string message = 4;
  string title = 5;
}
```

```bash
cd /home/vscode/shopsystem-kb && make contract
```

- [ ] **Step 3: The helpers send the title beside the content**

In `/home/vscode/shopsystem-kb/tests/calls.py` replace `define` and `create` with:

```python
def request(client, type_name, title, content, message="Create an artifact"):
    """A Create as the client sends it: the title beside the content. Returns the response, faults and all."""
    return client.Create(kb_pb2.CreateRequest(
        type=type_name, title=title, content=dumps(content), actor=CLIENT, message=message,
    ))


def create(client, type_name, content, message="Create an artifact"):
    """Create from a dict written the way a user writes a file, title inside; the title is lifted out and sent beside."""
    content = dict(content)
    title = content.pop("title", "")
    response = request(client, type_name, title, content, message)
    assert not response.faults, response.faults
    return response


def define(client, type_content):
    """Define a type: a Create of type `schema`."""
    return create(client, "schema", type_content, message=f"Define {type_content['title']}")
```

`read` stays.

- [ ] **Step 4: The step**

In `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py` change the import to `from calls import CLIENT, DECISION_TYPE, create, define, read, request` and append:

```python


@when(
    "the client creates a decision whose content carries a title as well as the title given alongside it, "
    "saying which role and why",
    target_fixture="refused",
)
def _create_with_a_title_inside(client):
    return request(client, "decision", "Price reviews happen weekly", {
        "title": "Price reviews, weekly",
        "sections": SECTIONS,
    }, message="Move price reviews to weekly")


@then(
    "the artifact is rejected because a title is given alongside the content, never inside it, "
    "and the title the content carried is named back"
)
def _rejected_for_a_title_inside(refused):
    assert (refused.id, refused.revision) == ("", 0)
    assert [(fault.path, fault.rule) for fault in refused.faults] == [("title", "identity")]
    assert "Price reviews, weekly" in refused.faults[0].message
```

- [ ] **Step 5: The least code: Create takes the title from the request**

In `/home/vscode/shopsystem-kb/src/kb/servicer.py` replace the top of `Create`, from `content = loads(request.content)` through the first `return kb_pb2.CreateResponse(faults=faults)`, with:

```python
    def Create(self, request, context):
        content = loads(request.content)
        schema = self._store.schema(request.type)
        artifact_id = f"{request.type}/{slug(request.title)}"
        if "title" in content:
            return kb_pb2.CreateResponse(faults=[kb_pb2.Fault(
                artifact=artifact_id, path="title", rule="identity",
                message=f"a title is given alongside the content, never inside it; the content carried the title {content['title']!r}",
            )])
        faults = validation.validate(artifact_id, {"title": request.title, **content}, schema["schema"])
        if faults:
            return kb_pb2.CreateResponse(faults=faults)
```

and, further down in the same method, put the title on the artifact:

```python
        artifact = {
            **content,
            "id": artifact_id, "type": request.type,
            "schema_version": schema["version"], "revision": 1, "title": request.title,
        }
```

The metaschema and the type definitions keep `title` among their properties: the artifact is validated with its title in place (decision 2).

- [ ] **Step 6: The shop lifts the title out of the file**

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/cli.py`, `_create`:

```python
def _create(args) -> int:
    content = yaml.safe_load(Path(args.source).read_text())
    title = content.pop("title", "")
    response = _client().Create(kb_pb2.CreateRequest(
        type=args.type, title=title, content=dumps(content), actor=_actor(), message=args.message,
    ))
    _show({"id": response.id, "revision": response.revision})
    return 0
```

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/bootstrap.py`, the loop body of `load`:

```python
        content = yaml.safe_load(text)
        title = content.pop("title")
        client.Create(kb_pb2.CreateRequest(
            type="schema", title=title, content=dumps(content), actor=actor,
            message=f"Define the shop's {title.lower()} type",
        ))
```

The type files under `shop_knowledge/types/` do not change: their `title:` line is the one lifted out.

- [ ] **Step 7: Run it green, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-55 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `1 passed`; `94 failed, 6 passed`; `2 passed`.

- [ ] **Step 8: Commit, both repositories**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/contract src/kb/servicer.py tests/calls.py tests/test_create_an_artifact.py && git commit -m "Slice 55: the title travels beside the content, and a title inside is refused

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
cd /home/vscode/shopsystem-knowledge && git add src/shop_knowledge/cli.py src/shop_knowledge/bootstrap.py && git commit -m "Slice 55: shop-knol sends the title beside the content

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 9: Checkpoint**

Set slice 55's Status to `green` and append to the log:

```
- <date> slice 55 green. Someone can now: create an artifact giving its title beside its content, and is refused, with the title named back, when the content carries one too; shop-knol lifts the title out of the user's file.
  Assumption "the title as a message field leaves the types and the metaschema as they are": held. Evidence: kb validates the artifact with its title in place, so every type's `title` property and `required: [title]` still hold, and `schema/decision.yaml` on disk is unchanged but for the emitter.
  Surprised by: <...>.
  Open questions: none. Next: slice 56.
```

Commit the plan as before: `Slice 55 green`.

---

### Task 4: Slice 56, the store is found above where the client works

**Slice plan entry:** Slice 56, capability. Unknown: how does a client's call find the store from the folder it works in, upward like git, when the store is marked only by a file inside its own subdirectory and the folder may be any depth below? Scenario:

1. kb / read-an-artifact / The client works in a folder inside the store

**Files (kb):**
- Create: `src/kb/discovery.py`
- Modify: `src/kb/client.py` (`connect` with no root)
- Modify: `tests/test_read_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.client.connect(root) -> InProcessClient`, `tests/calls.py:read`.
- Produces: `kb.discovery.MARKER = Path("kb") / "store.yaml"`, `kb.discovery.find_above(start: Path) -> Path | None`; `kb.client.connect(root=None)`, which with no root finds the store above `Path.cwd()`. Task 9 extends both. The step `When the client reads the decision` (`_read_the_decision_from_here`, fixture `shown`) is shared with Task 9's four scenarios.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-56 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: Given "the client is working in a folder deep inside the directory the store sits in"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_read_an_artifact.py`:

```python


@given("the client is working in a folder deep inside the directory the store sits in")
def _working_deep_inside_the_store(root, monkeypatch):
    deep = root / "shelves" / "pricing" / "notes"
    deep.mkdir(parents=True)
    monkeypatch.chdir(deep)
    monkeypatch.delenv("KB_ROOT", raising=False)


@when("the client reads the decision", target_fixture="shown")
def _read_the_decision_from_here():
    return read(kb_client.connect(), DECISION)


@then("the client is given the decision, from the store found above where it is working")
def _from_the_store_above(shown):
    assert (shown.id, shown.title) == (DECISION, "Price reviews happen weekly")
```

The `delenv` is the Given's "having named no store": a developer's shell may export `KB_ROOT`, and this scenario is about finding the store without it.

Run it: expected `TypeError: connect() missing 1 required positional argument: 'root'`.

- [ ] **Step 3: The least code: walk upward**

Create `/home/vscode/shopsystem-kb/src/kb/discovery.py`:

```python
"""Finding the store the way git finds a repository: upward from the working directory."""
from pathlib import Path

MARKER = Path("kb") / "store.yaml"


def find_above(start: Path) -> Path | None:
    """The nearest directory at or above `start` with a store inside it, or None."""
    for directory in (start, *start.parents):
        if (directory / MARKER).is_file():
            return directory
    return None
```

In `/home/vscode/shopsystem-kb/src/kb/client.py` add `from kb import discovery` after the `pathlib` import and replace `connect`:

```python
def connect(root=None) -> InProcessClient:
    """A client over the store at <root>/kb/, in this process; with no root, over the store found above the working directory."""
    if root is None:
        root = discovery.find_above(Path.cwd())
    return InProcessClient(KbServicer(Path(root)))
```

No store above is not handled here; slice 61 (Task 9) says what happens then.

- [ ] **Step 4: Run it green, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-56 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `1 passed`; `93 failed, 7 passed`; `2 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/discovery.py src/kb/client.py tests/test_read_an_artifact.py && git commit -m "Slice 56: the store is found above the working directory

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 56's Status to `green` and append to the log:

```
- <date> slice 56 green. Someone can now: work in any folder inside the directory a store sits in and have a client's call go to that store without naming it.
  Assumption "a walk upward from the working directory to the first directory holding kb/store.yaml finds the store at any depth": held. Evidence: <the scenario, three folders down>.
  Surprised by: <...>.
  Open questions:
  - Slice 50's unknown (how a directory is known to sit inside a store) is this walk; slicing decides at the next re-plan whether 50 is spent.
  Next: slice 57.
```

Commit the plan: `Slice 56 green`.

---

### Task 5: Slice 57, starting a store is recorded in its history

**Slice plan entry:** Slice 57, capability. Unknown: what does the first entry in a store's history hold and how is it read back, when it is written for the type that describes types before any other type exists? Needs: the journal entry the metaschema write leaves, inside the commit that starts the store. Scenario:

1. kb / start-a-store / Starting a store is recorded in the store's history

**Files (kb):**
- Create: `src/kb/journal.py`
- Modify: `src/kb/servicer.py` (`Init`)
- Modify: `tests/test_start_a_store.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.canonical.dump`, `Store.save`, `Store.commit(paths, role, message)`.
- Produces: `kb.journal.now() -> datetime` (UTC; a module function slice 9 can replace), `kb.journal.digest(path: Path) -> str` (sha256 hex of the file's bytes), `kb.journal.write(store_dir: Path, *, actor, op: str, artifact: str, path: str, revision: int, schema_version: int, written: Path, message: str, seq: int = 1) -> Path` (the entry's file, under `journal/<YYYY>/<MM>/<DD>/`). Slice 9 will call `write` from every operation.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-57 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: Then "the store's history holds one entry, under that role, with the message "initialise store""`.

- [ ] **Step 2: The steps**

In `/home/vscode/shopsystem-kb/tests/test_start_a_store.py` make the imports:

```python
import hashlib
import subprocess
from pathlib import Path

import yaml
from pytest_bdd import given, parsers, scenarios, then, when
```

The existing Then "the store holds no other type and no content" lists every file under the store; the journal is neither a type nor content, so its files are left out of that listing:

```python
@then("the store holds no other type and no content")
def _holds_nothing_else(root):
    store = root / "kb"
    files = sorted(p.relative_to(store) for p in store.rglob("*") if p.is_file() and ".git" not in p.parts)
    assert [f for f in files if f.parts[0] != "journal"] == [Path("schema/schema.yaml"), Path("store.yaml")]
```

Then append:

```python


@then(
    parsers.parse('the store\'s history holds one entry, under that role, with the message "{message}"'),
    target_fixture="entry",
)
def _one_entry_under_the_role(root, message):
    entries = sorted((root / "kb" / "journal").rglob("*.yaml"))
    assert len(entries) == 1, entries
    entry = yaml.safe_load(entries[0].read_text())
    assert (entry["actor"]["role"], entry["message"]) == ("client", message)
    log = subprocess.run(
        ["git", "-C", str(root / "kb"), "log", "--format=%an%x09%s"], capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    assert log == [f"client\t{message}"]
    return entry


@then(
    "that entry is the writing of the one type that describes what a type is, at its first version, "
    "with a fingerprint of what was written"
)
def _the_entry_is_the_metaschema_write(root, entry):
    assert (entry["op"], entry["artifact"], entry["path"], entry["revision"]) == ("create", "schema/schema", "", 1)
    assert entry["digest"] == hashlib.sha256((root / "kb" / "schema" / "schema.yaml").read_bytes()).hexdigest()
```

Run it: expected `FileNotFoundError` on the `journal` directory, or `assert len(entries) == 1`.

- [ ] **Step 3: The least code: the journal**

Create `/home/vscode/shopsystem-kb/src/kb/journal.py`:

```python
"""The journal: one file per entry under <store>/journal/<YYYY>/<MM>/<DD>/, written inside the commit that made the change."""
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from kb import canonical


def now() -> datetime:
    """The clock entries are stamped with. A module function so a later slice can set it from outside."""
    return datetime.now(timezone.utc)


def digest(path: Path) -> str:
    """The fingerprint of what was written: sha256 of the file's bytes after the write."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(store_dir: Path, *, actor, op: str, artifact: str, path: str, revision: int,
          schema_version: int, written: Path, message: str, seq: int = 1) -> Path:
    """Write one entry and return its file. A change made alone names itself as its batch."""
    at = now()
    entry_id = f"{at.strftime('%Y%m%dT%H%M%S%fZ')}-{seq}"
    entry = {
        "id": entry_id,
        "at": at.isoformat(),
        "actor": {"role": actor.role, "execution": actor.execution},
        "op": op,
        "artifact": artifact,
        "path": path,
        "revision": revision,
        "schema_version": schema_version,
        "digest": digest(written),
        "message": message,
        "batch": entry_id,
    }
    target = store_dir / "journal" / at.strftime("%Y") / at.strftime("%m") / at.strftime("%d") / f"{entry_id}.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(canonical.dump(entry))
    return target
```

In `/home/vscode/shopsystem-kb/src/kb/servicer.py` make the first import `from kb import canonical, journal, validation` and replace the end of `Init`:

```python
        path = store.save(canonical.order(metaschema, METASCHEMA["schema"]))
        entry = journal.write(
            store.dir, actor=request.actor, op="create", artifact="schema/schema", path="",
            revision=1, schema_version=1, written=path, message="initialise store",
        )
        store.commit([store.dir / "store.yaml", path, entry], request.actor.role, "initialise store")
        return kb_pb2.InitResponse()
```

Only Init journals here: slice 9 asks for an entry from every operation, and nothing in this slice asserts on a Create's entry.

- [ ] **Step 4: Run it green, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-57 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `1 passed`; `92 failed, 8 passed`; `2 passed`.

At a shell, after an Init, `cat kb/journal/*/*/*/*.yaml` reads like:

```
id: 20260924T154144795952Z-1
at: '2026-09-24T15:41:44.795952+00:00'
actor:
  role: client
  execution: ''
op: create
artifact: schema/schema
path: ''
revision: 1
schema_version: 1
digest: 47fd035f39bc977175f29de65c91a585d451112a907b7e67a0c195d89d1bbaa0
message: initialise store
batch: 20260924T154144795952Z-1
```

and `git -C kb show --stat --format='%an %s' HEAD` lists the entry, `schema/schema.yaml`, and `store.yaml` under `client initialise store`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/journal.py src/kb/servicer.py tests/test_start_a_store.py && git commit -m "Slice 57: starting a store leaves the first journal entry, inside the commit

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 57's Status to `green` and append to the log:

```
- <date> slice 57 green. Someone can now: start a store and find, in its history, one entry under their role with the message "initialise store", being the metaschema write at revision 1 with the digest of the file, inside the commit that started the store.
  Assumption "the first entry is written like any later one, one file under journal/<date>/, read back from disk": held. Evidence: <the entry file and git show from Step 4>. The step reads the file; the Journal rpc arrives with slice 9.
  Surprised by: <...>.
  Open questions: none. Next: slice 58.
```

Commit the plan: `Slice 57 green`.

---

### Task 6: Slice 58, a title that reads as a date is still a title

**Slice plan entry:** Slice 58, capability. Unknown: does a title YAML would read as a date survive the trip to disk and back as text, when the file is written by kb's emitter and loaded by a YAML parser? Scenario:

1. kb / create-an-artifact / A title that reads as a date is still a title

**Files (kb):**
- Modify: `tests/test_create_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `tests/calls.py:request`, `read`; `CreateRequest.title` (Task 3); `kb.canonical.dump` (Task 2).
- Produces: the step `When the client creates a decision titled "<title>", saying which role and why` (`_create_titled`, fixture `created`), shared with three scenarios of Task 7 and one of slice 24; the step `Then the name the client is given is made from that text`, shared with Task 7's "yes" scenario.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-58 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: When "the client creates a decision titled "2026-09-24", saying which role and why"`.

- [ ] **Step 2: The steps**

In `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py` make the pytest-bdd import `from pytest_bdd import given, parsers, scenarios, then, when` and append:

```python


@when(parsers.parse('the client creates a decision titled "{title}", saying which role and why'), target_fixture="created")
def _create_titled(client, title):
    return request(client, "decision", title, {"sections": SECTIONS}, message="Record it")


@then("the title reads back as the text that was written, not as a date")
def _title_is_text_not_a_date(root, client, created):
    assert read(client, created.id).title == "2026-09-24"
    on_disk = yaml.safe_load((root / "kb" / f"{created.id}.yaml").read_text())
    assert on_disk["title"] == "2026-09-24"


@then("the name the client is given is made from that text")
def _name_from_that_text(client, created):
    assert created.id == f"decision/{read(client, created.id).title}"
```

The on-disk assertion is the one that matters: `yaml.safe_load` gives a `datetime.date` for an unquoted `2026-09-24`, and `==` against the string fails. (pytest-bdd here does not offer a parsed step argument as a fixture to later steps, so the last Then reads the title back rather than taking `title`.)

- [ ] **Step 3: Run it**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-58 2>&1 | tail -1
```

Expected: `1 passed`, with no production code in this task. The title arrives as a string field since Task 3, and PyYAML's emitter writes a string that would otherwise resolve to a date or a bool in single quotes (`title: '2026-09-24'`), so a YAML parser reads it back as text. The scenario failed for want of steps, not on its Then, and goes green on the steps alone; that is not bdd-red-green's first stop condition (nothing passed before the steps existed), but the checkpoint says so plainly. If instead the Then fails, the fix belongs in `kb.canonical._represent_str` (quote a string whose plain form resolves to another type), and nowhere else.

Then both suites:

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `91 failed, 9 passed`; `2 passed`.

- [ ] **Step 4: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add tests/test_create_an_artifact.py && git commit -m "Slice 58: a title that reads as a date is text on disk and back

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 5: Checkpoint**

Set slice 58's Status to `green` and append to the log:

```
- <date> slice 58 green. Someone can now: create an artifact titled "2026-09-24" and read that title back as text, from the store and from the file, with the name made from it.
  Assumption "a title YAML would read as a date survives as text": held with no code of this slice's own. Evidence: the file carries `title: '2026-09-24'`; the emitter quotes any string whose plain form resolves to another type, and the title has been a string field since slice 55.
  Surprised by: the unknown was spent by slices 54 and 55 together; the scenario went green on its step definitions.
  Open questions: none. Next: slice 59.
```

Commit the plan: `Slice 58 green`.

---

### Task 7: Slice 59, Create refuses what it cannot name or hold, and names plainly what it can

**Slice plan entry:** Slice 59, capability, no unknown. Scenarios, in feature-file order:

1. kb / create-an-artifact / An artifact created without a title is refused
2. kb / create-an-artifact / Content that settles what only the store settles is refused
3. kb / create-an-artifact / A title with capitals and punctuation gives a plain name
4. kb / create-an-artifact / A title that leaves nothing to make a name from is refused
5. kb / create-an-artifact / A title that reads as yes is still a title
6. kb / create-an-artifact / Content telling the store how to build a value is refused
7. kb / create-an-artifact / Content holding more than one document is refused
8. kb / create-an-artifact / A section carrying anything besides its title, its body and its own sections is refused

Run the cycle per scenario, in this order. Scenarios 3 and 5 are expected green on their steps alone (the slug has minted plain names since slice 1; the quoting is slice 58's); the other six go red on their Then line.

**Files (kb):**
- Modify: `src/kb/content.py` (`ContentFault`, `loads`)
- Modify: `src/kb/servicer.py` (`Create`, `_title_faults`, `_identity_faults`)
- Modify: `src/kb/validation.py` (`SECTION_KEYS`, `_section_faults`)
- Modify: `tests/test_create_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `request`, `create`, `read` from `tests/calls.py`; `_create_titled` from Task 6; `kb.canonical.IDENTITY`; `kb.store.slug`.
- Produces: `kb.content.ContentFault(ValueError)`; `kb.content.loads(text) -> dict` raising it for a tag or a second document; `kb.validation.validate(artifact_id, content, schema) -> list[Fault]` now including section-shape faults with rule `section`; in the servicer, module functions `_title_faults(artifact_id, title) -> list[Fault]` and `_identity_faults(artifact_id, content) -> list[Fault]`, which slices 22 and 38 will reuse for Write and Append.

- [ ] **Step 1: Scenario 1, run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k an_artifact_created_without_a_title 2>&1 | tail -3
```

Expected: `StepDefinitionNotFoundError ... When "the client creates a decision with both required sections and no title, saying which role and why"`.

- [ ] **Step 2: Scenario 1, steps**

Append to `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`:

```python


@when(
    "the client creates a decision with both required sections and no title, saying which role and why",
    target_fixture="refused",
)
def _create_without_a_title(client):
    return request(client, "decision", "", {"sections": SECTIONS}, message="Record it")


@then("the artifact is rejected because an artifact cannot be created without a title")
def _rejected_without_a_title(refused):
    assert [(fault.path, fault.rule, fault.message) for fault in refused.faults] == [
        ("title", "title", "an artifact cannot be created without a title"),
    ]
```

Run it: expected the Then fails (`[] == [...]`), the create having gone through with the id `decision/`.

- [ ] **Step 3: Scenario 1, the least code**

In `/home/vscode/shopsystem-kb/src/kb/servicer.py` add, above `_summary_fields`:

```python
def _title_faults(artifact_id, title):
    """A title is required, and must leave something to make a name from."""
    if not title:
        return [kb_pb2.Fault(artifact=artifact_id, path="title", rule="title",
                             message="an artifact cannot be created without a title")]
    if not slug(title):
        return [kb_pb2.Fault(artifact=artifact_id, path="title", rule="title",
                             message=f"a title must leave something to make a name from; {title!r} leaves nothing")]
    return []
```

and in `Create`, after `artifact_id = ...` and before the `if "title" in content:` block from Task 3:

```python
        faults = _title_faults(artifact_id, request.title)
        if faults:
            return kb_pb2.CreateResponse(faults=faults)
```

(The second branch of `_title_faults` is scenario 4's; it is written here because the function is one thought, and scenario 4 will show it red-then-green through its own Then.)

Run scenario 1 green, then `python -m pytest -q 2>&1 | tail -1` (expected `90 failed, 10 passed`). Commit: `Slice 59: a create without a title is refused`.

- [ ] **Step 4: Scenario 2, run it red, steps, code**

```bash
python -m pytest -q -k content_that_settles_what_only_the_store_settles 2>&1 | tail -3
```

Expected: undefined When. Append:

```python


@when(
    "the client creates a decision whose content carries a name and a version for the artifact itself, "
    "saying which role and why",
    target_fixture="refused",
)
def _create_with_identity_inside(client):
    return request(client, "decision", "Price reviews happen weekly", {
        "id": "decision/a-name-of-my-own",
        "revision": 7,
        "sections": SECTIONS,
    }, message="Record it")


@then(
    "the artifact is rejected because content holds only what the type declares, "
    "and each thing it carried that only the store settles is named back"
)
def _rejected_for_identity_inside(refused):
    assert (refused.id, refused.revision) == ("", 0)
    assert [(fault.path, fault.rule) for fault in refused.faults] == [("id", "identity"), ("revision", "identity")]
    assert all(fault.path in fault.message for fault in refused.faults)
```

Run it: the Then fails; today kb overwrites the keys it mints and reports nothing. The least code generalises Task 3's title check to every identity key. In `servicer.py` add, under `_title_faults`:

```python
def _identity_faults(artifact_id, content):
    """Content holds only what the type declares; the identity keys are the store's, the title travels beside."""
    faults = []
    for key in canonical.IDENTITY:
        if key not in content:
            continue
        if key == "title":
            message = f"a title is given alongside the content, never inside it; the content carried the title {content[key]!r}"
        else:
            message = f"content holds only what the type declares; {key} is settled by the store, and the content carried {key}: {content[key]!r}"
        faults.append(kb_pb2.Fault(artifact=artifact_id, path=key, rule="identity", message=message))
    return faults
```

and in `Create` replace the `if "title" in content:` block and the title-faults lines with one gate:

```python
        faults = _title_faults(artifact_id, request.title) + _identity_faults(artifact_id, content)
        if faults:
            return kb_pb2.CreateResponse(faults=faults)
```

Run scenario 2 green; run `-m slice-55` (still green, its message unchanged); suite `89 failed, 11 passed`. Commit: `Slice 59: an identity key in content is refused and named back`.

- [ ] **Step 5: Scenario 3, run it, steps**

```bash
python -m pytest -q -k a_title_with_capitals_and_punctuation 2>&1 | tail -3
```

Expected: undefined Then (the When is Task 6's `_create_titled`). Append:

```python


@then(
    "the name the client is given is that title in lower case, with each run of anything that is not "
    "a letter or a digit turned into a single hyphen, and no hyphen at either end"
)
def _plain_name(created):
    assert not created.faults, created.faults
    assert created.id == "decision/price-reviews-weekly-from-now-on"
```

Run it: expected `1 passed` with no code, since `slug` has done this since slice 1. Suite `88 failed, 12 passed`. Commit: `Slice 59: a title with capitals and punctuation gives a plain name`.

- [ ] **Step 6: Scenario 4, run it red, steps**

```bash
python -m pytest -q -k a_title_that_leaves_nothing 2>&1 | tail -3
```

Expected: undefined Then. Append:

```python


@then("the artifact is rejected because a title must leave something to make a name from")
def _rejected_for_an_empty_name(created):
    assert (created.id, created.revision) == ("", 0)
    assert [(fault.path, fault.rule) for fault in created.faults] == [("title", "title")]
    assert "leave something to make a name from" in created.faults[0].message
```

Run it: expected `1 passed`, the second branch of `_title_faults` (Step 3) answering. If it is red instead, that branch is what to write. Suite `87 failed, 13 passed`. Commit: `Slice 59: a title that leaves nothing to make a name from is refused`.

- [ ] **Step 7: Scenario 5, run it, steps**

```bash
python -m pytest -q -k a_title_that_reads_as_yes 2>&1 | tail -3
```

Expected: undefined Then. Append:

```python


@then("the title reads back as the text that was written, not as a yes or a no")
def _title_is_text_not_a_bool(root, client, created):
    assert read(client, created.id).title == "yes"
    on_disk = yaml.safe_load((root / "kb" / f"{created.id}.yaml").read_text())
    assert on_disk["title"] == "yes"
```

Run it: expected `1 passed` with no code (the emitter writes `title: 'yes'`). Suite `86 failed, 14 passed`. Commit: `Slice 59: a title that reads as yes is text`.

- [ ] **Step 8: Scenario 6, run it red, steps, code**

```bash
python -m pytest -q -k content_telling_the_store_how_to_build 2>&1 | tail -3
```

Expected: undefined When. Append:

```python


def _raw(client, text):
    """A Create whose content is sent as written, so the text can carry what dumps never writes."""
    return client.Create(kb_pb2.CreateRequest(
        type="decision", title="Price reviews happen weekly", content=text, actor=CLIENT, message="Record it",
    ))


@when("the client creates a decision whose content carries a tag on one of its values, saying which role and why", target_fixture="refused")
def _create_with_a_tag(client):
    return _raw(client, "sections:\n  - title: Purpose\n    body: !!binary aGVsbG8=\n  - title: Rationale\n    body: Why.\n")


@then("the artifact is rejected because content is read plainly as written and carries no tags")
def _rejected_for_a_tag(refused):
    assert [(fault.rule, fault.message) for fault in refused.faults] == [
        ("content", "content is read plainly as written and carries no tags"),
    ]
```

Run it: today `yaml.safe_load` builds the `!!binary` into bytes, the JSON Schema check refuses the body's type, and the Then fails on the rule. Replace `/home/vscode/shopsystem-kb/src/kb/content.py` with:

```python
"""Artifact content crossing the contract as canonical YAML text."""
import yaml

from kb import canonical


class ContentFault(ValueError):
    """Content that cannot be read plainly. The message is the fault's."""


def dumps(value: dict) -> str:
    """Canonical text: block style, keys in the order given, prose as literal blocks."""
    return canonical.dump(value)


def loads(text: str) -> dict:
    """Read content plainly: no tags, exactly one document."""
    if any(isinstance(token, yaml.TagToken) for token in yaml.scan(text)):
        raise ContentFault("content is read plainly as written and carries no tags")
    documents = list(yaml.safe_load_all(text))
    if len(documents) > 1:
        raise ContentFault("content holds exactly one document")
    return (documents[0] if documents else None) or {}
```

In `servicer.py` make the content import `from kb.content import ContentFault, loads, dumps` and make the top of `Create`:

```python
    def Create(self, request, context):
        artifact_id = f"{request.type}/{slug(request.title)}"
        try:
            content = loads(request.content)
        except ContentFault as fault:
            return kb_pb2.CreateResponse(faults=[kb_pb2.Fault(artifact=artifact_id, rule="content", message=str(fault))])
        faults = _title_faults(artifact_id, request.title) + _identity_faults(artifact_id, content)
        if faults:
            return kb_pb2.CreateResponse(faults=faults)
        schema = self._store.schema(request.type)
        faults = validation.validate(artifact_id, {"title": request.title, **content}, schema["schema"])
        if faults:
            return kb_pb2.CreateResponse(faults=faults)
```

(The schema lookup moves below the cheap checks; nothing else in `Create` changes.) Run scenario 6 green; suite `85 failed, 15 passed`. Commit: `Slice 59: content carrying a tag is refused`.

- [ ] **Step 9: Scenario 7, run it red, steps**

```bash
python -m pytest -q -k content_holding_more_than_one_document 2>&1 | tail -3
```

Expected: undefined When. Append:

```python


@when(
    "the client creates a decision from content holding two documents one after the other, saying which role and why",
    target_fixture="refused",
)
def _create_from_two_documents(client):
    one = "sections:\n  - title: Purpose\n    body: Why.\n  - title: Rationale\n    body: Because.\n"
    return _raw(client, one + "---\n" + one)


@then("the artifact is rejected because content holds exactly one document")
def _rejected_for_two_documents(refused):
    assert [(fault.rule, fault.message) for fault in refused.faults] == [
        ("content", "content holds exactly one document"),
    ]
```

Run it: expected `1 passed`, the second check in `loads` (Step 8) answering; if red, that check is what to write. Suite `84 failed, 16 passed`. Commit: `Slice 59: content holding two documents is refused`.

- [ ] **Step 10: Scenario 8, run it red, steps, code**

```bash
python -m pytest -q -k a_section_carrying_anything_besides 2>&1 | tail -3
```

Expected: undefined When. Append:

```python


@when(
    "the client creates a decision whose purpose carries an extra entry of its own besides its title, its body "
    "and the sections inside it, saying which role and why",
    target_fixture="refused",
)
def _create_with_an_extra_entry_in_a_section(client):
    return request(client, "decision", "Price reviews happen weekly", {
        "sections": [{**SECTIONS[0], "author": "shopkeeper"}, SECTIONS[1]],
    }, message="Record it")


@then(
    "the artifact is rejected because a section holds exactly its title, its body and the sections inside it, "
    "and the extra entry is named"
)
def _rejected_for_an_extra_entry(refused):
    assert [(fault.path, fault.rule) for fault in refused.faults] == [("sections/0/author", "section")]
    assert "author" in refused.faults[0].message
```

Run it: the Then fails; today the extra key is silently dropped on write. Replace `/home/vscode/shopsystem-kb/src/kb/validation.py` with:

```python
"""Schema validation: JSON Schema 2020-12 over an artifact, then the shape of its sections. The other kb keywords are checked in later slices."""
from jsonschema import Draft202012Validator

from kb.contract import kb_pb2

SECTION_KEYS = ("title", "body", "sections")


def validate(artifact_id: str, content: dict, schema: dict) -> list[kb_pb2.Fault]:
    """Every violation, as artifact, path, rule, message."""
    faults = [
        kb_pb2.Fault(
            artifact=artifact_id,
            path="/".join(str(step) for step in error.absolute_path),
            rule=error.validator,
            message=error.message,
        )
        for error in Draft202012Validator(schema).iter_errors(content)
    ]
    return faults + _section_faults(artifact_id, content.get("sections", []), "sections")


def _section_faults(artifact_id: str, sections: list, at: str) -> list[kb_pb2.Fault]:
    """A section holds exactly its title, its body and the sections inside it."""
    faults = []
    for index, section in enumerate(sections):
        here = f"{at}/{index}"
        for key in section:
            if key not in SECTION_KEYS:
                faults.append(kb_pb2.Fault(
                    artifact=artifact_id, path=f"{here}/{key}", rule="section",
                    message=f"a section holds exactly its title, its body and the sections inside it; {key} is none of these",
                ))
        faults += _section_faults(artifact_id, section.get("sections", []), f"{here}/sections")
    return faults
```

Run scenario 8 green.

- [ ] **Step 11: The slice, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-59 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `8 passed`; `83 failed, 17 passed`; `2 passed`.

- [ ] **Step 12: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/content.py src/kb/servicer.py src/kb/validation.py tests/test_create_an_artifact.py && git commit -m "Slice 59: a section carrying anything besides title, body and sections is refused

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 13: Checkpoint**

Set slice 59's Status to `green` and append to the log:

```
- <date> slice 59 green. Someone can now: create an artifact and be refused, with the cause named, for no title, a title that yields no name, an identity key in the content, a tag on a value, a second document, or a stray key in a section; a title with capitals and punctuation gives a plain hyphenated name, and "yes" reads back as text.
  Surprised by: <...>.
  Open questions:
  - QUESTION FOR THE SPEC: content that is not a mapping (a list, a bare scalar) or is not YAML at all raises through to the client instead of coming back as a fault. What is shown? No scenario pins it.
  - QUESTION FOR THE SPEC: `sections` that is not a list (a string, a number) reaches the section check before JSON Schema has refused it, and the check reports nonsense paths or raises. No scenario pins it.
  Next: slice 60.
```

Commit the plan: `Slice 59 green`.

---

### Task 8: Slice 60, a read of a name the store lacks, or of a name or place that is not plain, is refused

**Slice plan entry:** Slice 60, capability, no unknown. Scenarios, in feature-file order:

1. kb / read-an-artifact / Reading something the store does not hold is refused
2. kb / read-an-artifact / A name that is not a plain name is refused
3. kb / read-an-artifact / A name that begins at the root of the disk is refused
4. kb / read-an-artifact / A place inside an artifact that is not a plain place is refused

**Files (kb):**
- Modify: `src/kb/contract/kb.proto` (`ReadResponse.faults`), regenerate with `make contract`
- Create: `src/kb/locators.py`
- Modify: `src/kb/servicer.py` (`Read`)
- Modify: `tests/test_read_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `Store.path(id) -> Path`, `Locator{id, path}`, `read` from `tests/calls.py`.
- Produces: `ReadResponse.faults: repeated Fault` (field 10); `kb.locators.PLAIN`, `ID`, `PLACE` (compiled patterns) and `kb.locators.faults(locator) -> list[Fault]` with rule `locator`; `Read` refuses a missing artifact with rule `not-found`. Slices 22, 38, and 40 reuse `locators.faults` and the not-found check for Write, Append, and Delete.

- [ ] **Step 1: Scenario 1, run it red, steps**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k reading_something_the_store_does_not_hold 2>&1 | tail -3
```

Expected: undefined When. Append to `/home/vscode/shopsystem-kb/tests/test_read_an_artifact.py` (and make the pytest-bdd import `from pytest_bdd import given, parsers, scenarios, then, when`):

```python


@when("the client reads an artifact by a name the store holds nothing under", target_fixture="refused")
def _read_a_name_the_store_lacks(client):
    return read(client, "decision/nothing-of-the-sort")


@then("the read is rejected because the store holds nothing by that name, and the name asked for is given back")
def _rejected_as_not_held(refused):
    assert [(fault.artifact, fault.rule) for fault in refused.faults] == [("decision/nothing-of-the-sort", "not-found")]
    assert "decision/nothing-of-the-sort" in refused.faults[0].message
```

Run it: expected `FileNotFoundError` from the When (today a missing file is a traceback).

- [ ] **Step 2: Scenario 1, the least code**

In `/home/vscode/shopsystem-kb/src/kb/contract/kb.proto` add a field to `ReadResponse` and say why in its comment:

```proto
// A summary: identity, the fields the type shows at a glance, a stub of
// each reference target and of each part, and inbound counts. With faults,
// a refusal: a bad locator, a name the store lacks, or no store found.
message ReadResponse {
  string id = 1;
  string type = 2;
  int32 schema_version = 3;
  int32 revision = 4;
  string title = 5;
  string content = 6;  // canonical YAML
  repeated Stub references = 7;
  repeated PartStub parts = 8;
  repeated InboundCount inbound = 9;
  repeated Fault faults = 10;
}
```

`make contract`. Then in `servicer.py`, at the top of `Read`:

```python
    def Read(self, request, context):
        if not self._store.path(request.locator.id).is_file():
            return kb_pb2.ReadResponse(faults=[kb_pb2.Fault(
                artifact=request.locator.id, rule="not-found",
                message=f"the store holds nothing by the name {request.locator.id!r}",
            )])
        artifact = self._store.load(request.locator.id)
```

Run scenario 1 green; suite `82 failed, 18 passed`. Commit: `Slice 60: a read of a name the store lacks is refused`.

- [ ] **Step 3: Scenario 2, run it red, steps, code**

```bash
python -m pytest -q -k a_name_that_is_not_a_plain_name 2>&1 | tail -3
```

Expected: undefined When. Append:

```python


@when(parsers.parse('the client reads an artifact by the name "{name}"'), target_fixture="refused")
def _read_by_the_name(client, name):
    return read(client, name)


@then("the read is rejected because a name is a kind and a plain name of lower-case letters, digits and single hyphens")
def _rejected_as_not_a_plain_name(refused):
    assert [fault.rule for fault in refused.faults] == ["locator"]
    assert "plain name" in refused.faults[0].message


@then("no content comes back, from inside the store or outside it")
def _no_content_at_all(refused):
    assert (refused.id, refused.title, refused.content) == ("", "", "")
    assert not refused.references and not refused.parts and not refused.inbound
```

Run it: the Then fails on the rule (`not-found`, since `kb/decision/../elsewhere.yaml` is resolved and found missing; the file was looked for, which the spec forbids). Create `/home/vscode/shopsystem-kb/src/kb/locators.py`:

```python
"""What a locator may say: a kind and a plain name, and a plain place inside it. Checked before any file is resolved."""
import re

from kb.contract import kb_pb2

PLAIN = r"[a-z0-9]+(?:-[a-z0-9]+)*"
ID = re.compile(rf"^{PLAIN}/{PLAIN}$")
PLACE = re.compile(rf"^(?:{PLAIN}(?:/{PLAIN})*)?$")


def faults(locator) -> list[kb_pb2.Fault]:
    """Every way the locator fails the grammar; empty when it is plain."""
    found = []
    if not ID.match(locator.id):
        found.append(kb_pb2.Fault(
            artifact=locator.id, rule="locator",
            message=f"a name is a kind and a plain name of lower-case letters, digits and single hyphens, never a path; {locator.id!r} is not",
        ))
    if not PLACE.match(locator.path):
        found.append(kb_pb2.Fault(
            artifact=locator.id, path=locator.path, rule="locator",
            message=f"a place inside an artifact is named by parts of the same plain alphabet, or a collection and an item in it; {locator.path!r} is not",
        ))
    return found
```

In `servicer.py` make the first import `from kb import canonical, journal, locators, validation` and put the grammar check first in `Read`:

```python
    def Read(self, request, context):
        faults = locators.faults(request.locator)
        if faults:
            return kb_pb2.ReadResponse(faults=faults)
        if not self._store.path(request.locator.id).is_file():
```

Run scenario 2 green; suite `81 failed, 19 passed`. Commit: `Slice 60: a name that is not plain is refused before any file is resolved`.

- [ ] **Step 4: Scenario 3, run it red, steps**

```bash
python -m pytest -q -k a_name_that_begins_at_the_root 2>&1 | tail -3
```

Expected: undefined When. Append:

```python


@when("the client reads an artifact by a name that begins at the root of the disk", target_fixture="refused")
def _read_by_an_absolute_name(client, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.yaml").write_text("title: Not for the store\n")
    return read(client, str(outside / "secret"))


@then("the read is rejected because a name is a kind and a plain name, never a path")
def _rejected_as_a_path(refused):
    assert [fault.rule for fault in refused.faults] == ["locator"]
    assert "never a path" in refused.faults[0].message
```

The file planted outside the store is the point: before Step 3, `Store.path` joined an absolute id onto `kb/` and `pathlib` gave back the absolute path, so `Read` would have opened it. Run it: expected `1 passed`, the grammar of Step 3 refusing it; if red, `ID` is what to fix. Suite `80 failed, 20 passed`. Commit: `Slice 60: a name that begins at the root of the disk is refused`.

- [ ] **Step 5: Scenario 4, run it red, steps**

```bash
python -m pytest -q -k a_place_inside_an_artifact_that_is_not 2>&1 | tail -3
```

Expected: undefined When. Append:

```python


@when(parsers.parse('the client reads the place "{place}" inside the decision'), target_fixture="refused")
def _read_a_place_inside(client, place):
    return client.Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=DECISION, path=place)))


@then(
    "the read is rejected because a place inside an artifact is named by parts of the same plain alphabet, "
    "or a collection and an item in it"
)
def _rejected_as_not_a_plain_place(refused):
    assert [(fault.artifact, fault.path, fault.rule) for fault in refused.faults] == [(DECISION, "sections/../..", "locator")]
    assert "plain alphabet" in refused.faults[0].message
```

Run it: expected `1 passed`, the `PLACE` check of Step 3 answering; if red, that is what to fix.

- [ ] **Step 6: The slice, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-60 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `4 passed`; `79 failed, 21 passed`; `2 passed`.

- [ ] **Step 7: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/contract src/kb/locators.py src/kb/servicer.py tests/test_read_an_artifact.py && git commit -m "Slice 60: a place that is not plain is refused

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 8: Checkpoint**

Set slice 60's Status to `green` and append to the log:

```
- <date> slice 60 green. Someone can now: read by a name the store lacks and be told so with the name given back, and read by a name or a place that is not plain and be refused before any file, inside the store or outside it, is opened.
  Surprised by: <...>.
  Open questions:
  - shop-knol read of a refused name prints an empty artifact and exits 0; slice 21 pins the shop's discovery refusals, but a not-found or not-plain name has no shop scenario. QUESTION FOR THE SPEC, or a scenario for slice 21.
  Next: slice 61.
```

Commit the plan: `Slice 60 green`.

---

### Task 9: Slice 61, the store KB_ROOT names is used, and a store that cannot be found or is named twice is refused

**Slice plan entry:** Slice 61, capability, no unknown. Scenarios, in feature-file order:

1. kb / read-an-artifact / The client names the store instead of working inside it
2. kb / read-an-artifact / A call with no store to be found is refused
3. kb / read-an-artifact / Naming a store that is not there is refused
4. kb / read-an-artifact / Working in one store while naming another is refused

**Files (kb):**
- Modify: `src/kb/discovery.py` (`locate`)
- Modify: `src/kb/client.py` (a client over a refusal)
- Modify: `tests/test_read_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `discovery.find_above`, `connect(root=None)` from Task 4; `ReadResponse.faults` from Task 8; the shared When `_read_the_decision_from_here`.
- Produces: `kb.discovery.locate(cwd: Path, env: Mapping[str, str]) -> tuple[Path | None, Fault | None]`; `InProcessClient(servicer, refusal=None)`, whose `Create` and `Read` answer with the refusal when it has one; `connect(root=None)` returning such a client when no store is found or two disagree. Slice 21 will route `shop-knol` through `connect()` with no root.

- [ ] **Step 1: Scenario 1, run it red, steps**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_names_the_store_instead 2>&1 | tail -3
```

Expected: undefined Given. Append to `tests/test_read_an_artifact.py`:

```python


@given("the client is working outside any store, with KB_ROOT naming this one")
def _outside_with_kb_root_naming_this_one(root, tmp_path, monkeypatch):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    monkeypatch.setenv("KB_ROOT", str(root))


@then("the client is given the decision, from the store KB_ROOT names")
def _from_the_store_kb_root_names(shown):
    assert (shown.id, shown.title) == (DECISION, "Price reviews happen weekly")
```

Run it: expected `TypeError` from `Path(None)`, since `connect()` walks upward from a directory with no store above it and ignores `KB_ROOT`.

- [ ] **Step 2: Scenarios 1 to 4, the code**

The four scenarios are one decision table, so the code is written once and each scenario then shows its own row red-then-green through its steps. Replace `/home/vscode/shopsystem-kb/src/kb/discovery.py` with:

```python
"""Finding the store the way git finds a repository: upward from the working directory, or named by KB_ROOT."""
from pathlib import Path
from typing import Mapping

from kb.contract import kb_pb2

MARKER = Path("kb") / "store.yaml"


def find_above(start: Path) -> Path | None:
    """The nearest directory at or above `start` with a store inside it, or None."""
    for directory in (start, *start.parents):
        if (directory / MARKER).is_file():
            return directory
    return None


def locate(cwd: Path, env: Mapping[str, str]) -> tuple[Path | None, kb_pb2.Fault | None]:
    """The store a call goes to, or the fault that refuses it. Nothing is guessed at."""
    above = find_above(cwd)
    if "KB_ROOT" not in env:
        if above is None:
            return None, kb_pb2.Fault(
                rule="store", message=f"no store was found, neither above {cwd} nor named outright",
            )
        return above, None
    named = Path(env["KB_ROOT"])
    if not (named / MARKER).is_file():
        return None, kb_pb2.Fault(
            rule="store", message=f"KB_ROOT names a directory that holds no store: {named}",
        )
    if above is not None and above.resolve() != named.resolve():
        return None, kb_pb2.Fault(
            rule="store",
            message=f"KB_ROOT names a store other than the one {cwd} is working in: KB_ROOT is {named}, "
                    f"the working directory is inside {above}; neither is guessed at",
        )
    return named, None
```

Replace `/home/vscode/shopsystem-kb/src/kb/client.py` with:

```python
"""Transports. In-process: an object with the stub's method names that calls the servicer directly."""
import os
from pathlib import Path

from kb import discovery
from kb.contract import kb_pb2
from kb.servicer import KbServicer


class InProcessClient:
    """Same method names, requests and responses as kb_pb2_grpc.KbStub, with no channel between.

    Built over a refusal instead of a servicer, every call answers with that fault and touches nothing.
    """

    def __init__(self, servicer: KbServicer | None, refusal: kb_pb2.Fault | None = None):
        self._servicer = servicer
        self._refusal = refusal

    def Init(self, request, timeout=None):
        return self._servicer.Init(request, None)

    def Create(self, request, timeout=None):
        if self._refusal:
            return kb_pb2.CreateResponse(faults=[self._refusal])
        return self._servicer.Create(request, None)

    def Read(self, request, timeout=None):
        if self._refusal:
            return kb_pb2.ReadResponse(faults=[self._refusal])
        return self._servicer.Read(request, None)


def connect(root=None) -> InProcessClient:
    """A client over the store at <root>/kb/, in this process.

    With no root, over the store found the way git finds a repository: above the working directory, or
    named by KB_ROOT; none found, or the two disagreeing, and the client refuses every call.
    """
    if root is not None:
        return InProcessClient(KbServicer(Path(root)))
    root, refusal = discovery.locate(Path.cwd(), os.environ)
    if refusal is not None:
        return InProcessClient(None, refusal)
    return InProcessClient(KbServicer(root))
```

`Init` takes its root on the request and never goes through discovery, so it has no refusal branch. Run scenario 1 green and `-m slice-56` (still green); suite `78 failed, 22 passed`. Commit: `Slice 61: KB_ROOT names the store when the client works outside one`.

- [ ] **Step 3: Scenario 2, run it red, steps**

```bash
python -m pytest -q -k a_call_with_no_store_to_be_found 2>&1 | tail -3
```

Expected: undefined Given. Append:

```python


@given("the client is working outside any store and nothing names one", target_fixture="elsewhere")
def _outside_with_nothing_naming_one(tmp_path, monkeypatch):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    monkeypatch.delenv("KB_ROOT", raising=False)
    return elsewhere


@then("the read is rejected because no store was found, neither above where it is working nor named outright")
def _rejected_with_no_store_found(shown, elsewhere):
    assert [fault.rule for fault in shown.faults] == ["store"]
    assert "no store was found" in shown.faults[0].message
    assert str(elsewhere) in shown.faults[0].message
```

Run it: expected `1 passed` (Step 2's first row). Suite `77 failed, 23 passed`. Commit: `Slice 61: a call with no store to be found is refused`.

- [ ] **Step 4: Scenario 3, run it red, steps**

```bash
python -m pytest -q -k naming_a_store_that_is_not_there 2>&1 | tail -3
```

Expected: undefined Given. Append:

```python


@given("the client is working outside any store, with KB_ROOT naming a directory that holds no store", target_fixture="empty")
def _outside_with_kb_root_naming_nothing(tmp_path, monkeypatch):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.chdir(elsewhere)
    monkeypatch.setenv("KB_ROOT", str(empty))
    return empty


@then("the read is rejected because KB_ROOT names a directory that holds no store")
def _rejected_as_kb_root_holds_no_store(shown, empty):
    assert [fault.rule for fault in shown.faults] == ["store"]
    assert "KB_ROOT names a directory that holds no store" in shown.faults[0].message
    assert str(empty) in shown.faults[0].message


@then("no content comes back")
def _no_content(shown):
    assert (shown.id, shown.title, shown.content) == ("", "", "")
```

Run it: expected `1 passed`. Suite `76 failed, 24 passed`. Commit: `Slice 61: KB_ROOT naming a directory with no store is refused`.

- [ ] **Step 5: Scenario 4, run it red, steps**

```bash
python -m pytest -q -k working_in_one_store_while_naming_another 2>&1 | tail -3
```

Expected: undefined Given. Append:

```python


@given("the client is working inside a store, with KB_ROOT naming a different store", target_fixture="other")
def _inside_one_store_with_kb_root_naming_another(root, tmp_path, monkeypatch):
    other = tmp_path / "other"
    other.mkdir()
    kb_client.connect(other).Init(kb_pb2.InitRequest(root=str(other), actor=CLIENT))
    deep = root / "shelves"
    deep.mkdir()
    monkeypatch.chdir(deep)
    monkeypatch.setenv("KB_ROOT", str(other))
    return other


@then(
    "the read is rejected because KB_ROOT names a store other than the one it is working in, "
    "and neither of the two is guessed at"
)
def _rejected_as_two_stores(shown, root, other):
    assert [fault.rule for fault in shown.faults] == ["store"]
    assert "KB_ROOT names a store other than the one" in shown.faults[0].message
    assert str(root) in shown.faults[0].message and str(other) in shown.faults[0].message


@then("no content comes back, from either store")
def _no_content_from_either(shown):
    assert (shown.id, shown.title, shown.content) == ("", "", "")
    assert not shown.references and not shown.parts and not shown.inbound
```

Run it: expected `1 passed`.

- [ ] **Step 6: The slice, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-61 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `4 passed`; `75 failed, 25 passed`; `2 passed`.

At a shell, from a directory with no store above it and `KB_ROOT` unset:

```bash
cd /tmp && python -c "
from kb import client as c; from kb.contract import kb_pb2
print(c.connect().Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id='decision/x'))))"
```

Expected:

```
faults {
  rule: "store"
  message: "no store was found, neither above /tmp nor named outright"
}
```

- [ ] **Step 7: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/discovery.py src/kb/client.py tests/test_read_an_artifact.py && git commit -m "Slice 61: working in one store while KB_ROOT names another is refused

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 8: Checkpoint**

Set slice 61's Status to `green` and append to the log:

```
- <date> slice 61 green. Someone can now: name the store with KB_ROOT from anywhere, and be refused, told which, when no store can be found, when KB_ROOT names a directory with none, or when they work inside one store while KB_ROOT names another.
  Surprised by: <...>.
  Open questions:
  - QUESTION FOR THE SPEC: KB_ROOT set but empty is taken as naming the working directory, and refused as holding no store. Is an empty KB_ROOT "unset"? No scenario pins it.
  - shop-knol still passes KB_ROOT to connect() outright and so never walks upward nor sees these refusals; slice 21 changes that.
  Next: slice 62.
```

Commit the plan: `Slice 61 green`.

---

### Task 10: Slice 62, the same content always lands on disk as the same bytes

**Slice plan entry:** Slice 62, capability, no unknown. Scenario:

1. kb / look-after-a-store / The same content always lands on disk as the same bytes

**Files (kb):**
- Modify: `tests/test_look_after_a_store.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.canonical.dump` as Task 2 left it; `define`, `create`, `CLIENT`, `DECISION_TYPE` from `tests/calls.py`.
- Produces: nothing new.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-62 2>&1 | tail -3
```

Expected: `StepDefinitionNotFoundError ... Given "two stores each given the same decision by the same client"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_look_after_a_store.py`:

```python


SAME_DECISION = {
    "title": "Price reviews happen weekly",
    "sections": [
        {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
        {"title": "Rationale", "body": "Costs move weekly.\n"},
    ],
    "options": [{"title": "Keep weekly", "body": "Review every Monday."}],
}


@given("two stores each given the same decision by the same client", target_fixture="files")
def _two_stores_with_the_same_decision(tmp_path):
    files = []
    for name in ("one", "two"):
        root = tmp_path / name
        root.mkdir()
        client = kb_client.connect(root)
        client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))
        define(client, DECISION_TYPE)
        created = create(client, "decision", SAME_DECISION)
        files.append(root / "kb" / f"{created.id}.yaml")
    return files


@when("the operator compares the two decision files", target_fixture="comparison")
def _compare_the_files(files):
    return [path.read_bytes() for path in files]


@then("the two files are the same, byte for byte")
def _the_same_bytes(comparison):
    assert comparison[0] == comparison[1]
    assert len(comparison[0]) > 0
```

- [ ] **Step 3: Run it, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-62 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `1 passed` with no production code (the artifact file carries nothing that varies between runs: the time and the actor live in the journal and the commit); `74 failed, 26 passed`; `2 passed`. If it is red, the difference between the two files is the finding, and it goes in the checkpoint before anything is changed.

- [ ] **Step 4: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add tests/test_look_after_a_store.py && git commit -m "Slice 62: the same content lands on disk as the same bytes

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 5: Checkpoint**

Set slice 62's Status to `green` and append to the log:

```
- <date> slice 62 green. Someone can now: write the same decision into two stores and diff the files to nothing.
  Surprised by: the scenario went green on its step definitions; the canonical emitter of slice 54 is deterministic and the file carries no time or actor.
  Open questions: none. Next: slice 63.
```

Commit the plan: `Slice 62 green`.

---

### Task 11: Slice 63, starting a store without saying which role is refused

**Slice plan entry:** Slice 63, capability, no unknown. Scenario:

1. kb / start-a-store / Starting a store without saying which role is refused

**Files (kb):**
- Modify: `src/kb/contract/kb.proto` (`InitResponse.faults`), regenerate with `make contract`
- Modify: `src/kb/servicer.py` (`Init`)
- Modify: `tests/test_start_a_store.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `InitRequest{root, actor}` from Task 1.
- Produces: `InitResponse.faults: repeated Fault` (field 1); `Init` refuses with rule `actor` before touching the disk. Slices 50, 51, and 44 add the other Init refusals to the same field.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-63 2>&1 | tail -3
```

Expected: `StepDefinitionNotFoundError ... When "the client starts a store there without saying which role it is"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_start_a_store.py`:

```python


@when("the client starts a store there without saying which role it is", target_fixture="refused")
def _start_a_store_without_a_role(root):
    return kb_client.connect(root).Init(kb_pb2.InitRequest(root=str(root)))


@then("starting the store is rejected because a store can only be started under a role")
def _rejected_without_a_role(refused):
    assert [(fault.rule, fault.message) for fault in refused.faults] == [
        ("actor", "a store can only be started under a role"),
    ]


@then("that directory holds no store")
def _no_store_there(root):
    assert not (root / "kb").exists()
    assert list(root.iterdir()) == []
```

Run it: expected `subprocess.CalledProcessError` from the When, git refusing a commit with an empty author name after the store directory was already made.

- [ ] **Step 3: The least code**

In `/home/vscode/shopsystem-kb/src/kb/contract/kb.proto` replace `message InitResponse {}` with:

```proto
// With faults, a refusal: no role, or a store already there.
message InitResponse {
  repeated Fault faults = 1;
}
```

`make contract`. In `servicer.py`, at the top of `Init`, before `store = Store(request.root)`:

```python
    def Init(self, request, context):
        if not request.actor.role:
            return kb_pb2.InitResponse(faults=[kb_pb2.Fault(
                rule="actor", message="a store can only be started under a role",
            )])
        store = Store(request.root)
```

- [ ] **Step 4: Run it green, then both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-63 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1 && python -m pytest -q 2>&1 | tail -1
```

Expected: `1 passed`; `73 failed, 27 passed`; `2 passed`; `55 failed, 2 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/contract src/kb/servicer.py tests/test_start_a_store.py && git commit -m "Slice 63: starting a store without a role is refused and nothing is made

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 63's Status to `green` and append to the log:

```
- <date> slice 63 green. Someone can now: try to start a store without saying which role they are and be refused, the directory left empty.
  Surprised by: <...>.
  Open questions:
  - shop-knol init with KB_ACTOR unset raises KeyError before reaching kb; slice 52 pins what the user sees.
  Next: tag kb 0.1, pin it here, then slicing moves the kb-only slices to kb's own plan.
```

Commit the plan: `Slice 63 green`.

---

## After slice 63: tag kb 0.1, pin it, split the plans

Not a slice; the close of the one-effort phase both specs describe, moved here from the skeleton plan's "After slice 1" by the slice plan's log entry of 2026-09-24. Do it right after the slice-63 checkpoint, then stop: later slices get their tasks from a fresh run of `slicing-into-increments` and `writing-plans`.

- [ ] **The shell walk-through, once, before tagging**

```bash
cd $(mktemp -d) && export KB_ACTOR=shopkeeper && shop-knol init shop && cat > weekly.yaml <<'EOF'
title: Price reviews happen weekly
sections:
  - title: Purpose
    body: Keep prices in step with costs.
  - title: Rationale
    body: Costs move weekly, so a monthly review lags them.
EOF
export KB_ROOT=$PWD/shop && shop-knol create decision --from weekly.yaml -m "Move price reviews to weekly" && cat shop/kb/decision/price-reviews-happen-weekly.yaml && git -C shop/kb log --format='%an%x09%s' && ls shop/kb/journal/*/*/*/
```

Expected: the create prints `id: decision/price-reviews-happen-weekly` and `revision: 1`; the file reads

```
id: decision/price-reviews-happen-weekly
type: decision
schema_version: 1
revision: 1
title: Price reviews happen weekly
sections:
  - title: Purpose
    body: |-
      Keep prices in step with costs.
  - title: Rationale
    body: |-
      Costs move weekly, so a monthly review lags them.
```

and the log shows `shopkeeper	Move price reviews to weekly` above the three `shopkeeper	Define the shop's ... type` commits and `shopkeeper	initialise store`, with one entry file under the journal.

- [ ] **Tag kb 0.1**

```bash
cd /home/vscode/shopsystem-kb && git tag -a 0.1 -m "kb 0.1: the contract's first version, Init, Create, summary Read" && git tag
```

- [ ] **Pin it here**

In `/home/vscode/shopsystem-knowledge/pyproject.toml` change `"shopsystem-kb"` to `"shopsystem-kb==0.1"`. The editable path install still satisfies the pin because kb's `pyproject.toml` says `version = "0.1"`.

```bash
cd /home/vscode/shopsystem-knowledge && make dev && python -m pytest -q -m slice-1 2>&1 | tail -1
git add pyproject.toml && git commit -m "Pin kb 0.1

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

Expected: `2 passed, 55 deselected`.

- [ ] **Hand the slice plan back to slicing-into-increments** to move the slices made only of kb scenarios into a plan in `shopsystem-kb`, as the slice plan's preamble says, and to decide whether slice 50's unknown was spent by slice 56. writing-plans then runs once per repo for the slices that follow.
