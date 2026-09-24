# Pre-tag Implementation Plan, third and last cut: slices 1.18 to 1.28

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `2026-09-23-shop-knowledge-slices.md`. Inside a task, follow `shopsystem-bdd:bdd-red-green` scenario by scenario. That skill's stop conditions, hand-back, and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** The last things kb 0.1 accepts, refuses, or reports are pinned before the tag. A title that arrives as a yes-or-no or a number is text. A stored file that cannot be read is a fault on Read and a violation for a new Validate call, never an exception. Content with a duplicate key or a `%YAML`/`%TAG` directive is refused, naming the place. Init's root is checked like any other input. A kind the store holds no type for is its own fault. shop-knol prints every refusal in plain words with a non-zero exit: on create, on read, and on a new `validate` command.

**Architecture:** kb (`/home/vscode/shopsystem-kb`) is the Python package `kb`. It has a protobuf contract under `kb.contract` and a servicer over a `Store`, which keeps one canonical YAML file per artifact under `<root>/kb/`, itself a git repository. Clients use an in-process client with the stub's method names. `kb.canonical` is the one place kb reads or writes YAML, and it holds the one plain-reading check. `kb.values` holds the boundary conversions. This plan:
- extends `kb.canonical.check` with a directive rule and a duplicate-key rule, both naming the place;
- makes every YAML error `NotCanonical`, and every unreadable stored file a `store.Unreadable` carrying a fault;
- adds `Validate` to the contract;
- adds `values.root` for Init;
- adds `kb.content.text`, the one function that turns a YAML 1.2 value into the text it is written as.

shop-knowledge (`/home/vscode/shopsystem-knowledge`) is the package `shop_knowledge`. Its `shop-knol` command calls kb through the in-process client. It gains one refusal printer and a `validate` command.

**Provenance:** Every code block in this plan was assembled in scratch copies of both repositories (`/tmp/pretag3/kb`, `/tmp/pretag3/shop`) on 2026-09-24, with `PYTHONPATH=/tmp/pretag3/kb/src:/tmp/pretag3/shop/src` ahead of the editable installs. Each task was applied in order and run. The red and green results and the suite counts below are what those runs gave, and the walk-through at the end printed what it states. The repositories themselves were not touched.

**Tech Stack:** Python 3.11, setuptools (src layout), protobuf + grpcio + grpcio-tools (generated code committed, `make contract` regenerates it), python-jsonschema (Draft 2020-12), ruamel.yaml 0.19 (`YAML(typ="safe", pure=True)`, YAML 1.2), git via subprocess, pytest + pytest-bdd 8, argparse.

**Spec:** `/home/vscode/shopsystem-kb/docs/superpowers/specs/2026-09-23-kb-design.md` (The contract, Input safety) and `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md` (The CLI). Slice plan: `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, slices 1.18 to 1.28. Feature files: `features/` in each repository. The scenarios of each slice carry `@slice-<n>`, so `python -m pytest -q -m slice-1.18` runs a slice (the dotted number is a marker name like any other).

## Global Constraints

- Feature files are read-only for the implementer. Only `slicing-into-increments` edits a tag line, and only `formulating-features` edits a Given, When, or Then. Any other diff under `features/` is a stop condition.
- Code only what a scenario asserts (bdd-red-green). Where the scenarios are silent, the code is silent, and the silence goes into the checkpoint entry as an open question. The decisions this plan makes are listed below, each tied to the spec line or scenario that asks for it.
- **Replace, never add beside.** shop-knol's own `_text` is deleted in Task 1 in favour of `kb.content.text`. The parse-error handling of Task 2 sits inside `canonical.check` and `canonical.load`, not in each caller. Init's root goes through `values.root`, the same boundary every other request value goes through.
- Content: "Content is parsed with a safe YAML 1.2 loader using the core schema, so `yes`, `on`, `1:20`, and a bare date are text; only `true`, `false`, `null`, integers, and floats are typed. No tags, no anchors, no aliases, no `%YAML` or `%TAG` directive, no documents beyond the first, and no duplicate keys; each of these is a fault naming the place, never an exception. A title is always text whatever it looks like, `true` and `12` included."
- Init: "`Init`'s root is an input like any other: an absolute or relative path to a directory that exists; empty, missing, or not a directory is refused."
- Unreadable files: "A stored file that fails to parse is reported by load and by `Validate` as a violation naming the file, and `Read` of that artifact is refused with the same fault. Nothing raises."
- Create: "Refused without a title, when content carries an identity key, or, as its own fault, when the type is a plain name that names no schema the store holds".
- Validate: "`Validate` | nothing | every violation as artifact, path, message; stale artifacts listed". Stale listing belongs to slice 43. This plan adds only what slice 1.20 observes.
- shop-knol: "shop-knol never shows a traceback: a file it cannot read, for a tag, an anchor, a directive, a second document, or a duplicate key, is refused the way kb refuses it, naming the place, with a non-zero exit. Errors are printed as returned by kb, with artifact, path, and message, and exit non-zero." `shop-knol validate` maps to Validate.
- Errors are a typed list of `{ artifact, path, rule, message }`. A response that carries faults is a refusal, and nothing was written.
- kb is exercised through its in-process transport, never mocked. kb ships no domain types.
- One user-site Python environment serves both checkouts. `make contract` in kb regenerates `kb_pb2.py`, `kb_pb2.pyi` and `kb_pb2_grpc.py` from `kb.proto`, and all four files are committed together.
- Work on `main` in both repositories, not in a worktree. shop-knowledge imports kb from `/home/vscode/shopsystem-kb` as an editable install, and its step driver spawns `python -m shop_knowledge`, so a worktree would test the wrong code.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with the Co-Authored-By line of the model that made the commit, e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
- After every kb task, shop-knowledge's pre-tag scenarios must still pass: `cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m "slice-1 or slice-1.17"` → `4 passed`.
- The kb suite prints pytest-bdd `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- Baseline before Task 1: kb `84 failed, 34 passed`; shop-knowledge `58 failed, 4 passed`.

## Decisions this plan makes (the spec left them open or silent)

1. **Where a title that is not text becomes text.** The contract carries the title as a `string` field, so a `true` or a `12` cannot reach kb at all until a client turns it into text. kb therefore supplies the one function that does it the YAML 1.2 way: `kb.content.text(value) -> str`, giving `"true"`/`"false"` for a yes-or-no, `""` for nothing, ISO text for a date, and `str()` otherwise. A client uses it when it builds a request, and the steps of slices 1.18 and 1.25 do. shop-knol's own `_text`, which gave `"True"` for `true`, is replaced by it (slice 70's open question). Pinned by slices 1.18 and 1.25.
2. **What "cannot be read" covers.** Any stored file that `canonical.load` refuses: YAML that does not parse, and YAML that parses but breaks the plain-reading check, such as a hand-added anchor (slice 65's open question). Every `ruamel.yaml` error becomes `NotCanonical` inside `canonical.check` and `canonical.load`, with the message `it is not YAML that can be read: <problem> at line <n>`. `Store.load` turns `NotCanonical` into `store.Unreadable`, which carries `Fault(artifact=<id>, rule="unreadable", message="the stored file <kind>/<slug>.yaml cannot be read: …")`. Read answers any `Unreadable` met while it builds its answer with that fault. The same wrapping means content arriving on Create that is not YAML is now a `content` fault, not a `ParserError` (slice 59's open question), with no code of its own.
3. **The Validate call.** `rpc Validate(ValidateRequest) returns (ValidateResponse)`, with `ValidateResponse { repeated Fault violations = 1; repeated Fault faults = 2; }`. `violations` is the answer; `faults` is a refusal (no store found), as on every other call. It loads every artifact file (`*/*.yaml` under the store, schemas included, in path order). A file that cannot be read is a violation, and the check goes on. Every artifact that loads is validated against its type's composed schema, without the four keys the store settles (`id`, `type`, `schema_version`, `revision`). References, required sections by title, and staleness are slice 43's.
4. **Where a content fault stands.** `NotCanonical` gains a `path`. A duplicate key carries the node path of the second entry (`sections/0/body`), and its message names the key and the line: `an entry is named once and only once; 'body' is named again at line 4`. A directive stands before any node, so its fault has no path, and its message names the line: `content is read plainly as written and opens with no declaration of its format; line 1 declares %YAML 1.1`. The duplicate check walks the composed node tree itself, so it names a path where ruamel's own `DuplicateKeyError` gives only a line. The directive check scans tokens, because the document-start event marks the `---` line, not the directive's. `%TAG` is refused by the same rule, with no scenario of its own.
5. **Init's root.** `values.root(text) -> Path` refuses `""` (rule `root`, "…that was named and that exists; no directory was named"), a path that does not exist ("…in a directory that exists; '<text>' does not"), and a path that is not a directory ("…in a directory, and '<text>' is not one"). A relative path stays relative. `KbServicer()` with no root is a servicer that can only start a store, and `InProcessClient.Init` uses it. Refusing a missing directory means kb no longer builds one, so shop-knowledge's `shop` fixture now makes the directory the scenarios start in (Task 9, Step 5).
6. **A kind with no type.** Create checks that the store holds `schema/<kind>` right after the kind is converted, and refuses with `Fault(rule="kind", message="a kind must name a type the store holds; the store holds no type called '<kind>'")` alone, before the content is read, so nothing else stands beside it.
7. **shop-knol's plain words.** One line per fault, `<artifact> at <path>: <message>`, or `<artifact>: <message>` when there is no path, printed on stderr with exit 1. For a user's file shop-knol cannot read, the artifact is the file name as given. `shop-knol validate` prints every violation the same way and exits 1, or prints nothing and exits 0. Slice 44 decides what a sound check says.

## Review Focus

writing-plans asks that each line here get a test in the owning task. In this project tests are scenarios, and the feature files are the human gate, so no unit tests are added. Instead, each line goes into the owning task's checkpoint entry as a `QUESTION FOR THE SPEC`, with the reproduction given here. Each was reproduced in scratch after all eleven tasks.

1. **Reading a sound artifact while a different file is unreadable** (hand-break `decision/two.yaml`, read `decision/one`): Read is refused with `decision/two`'s fault, because the inbound count loads every artifact. A person would expect `decision/one` back, with the broken file reported by Validate. Task 2 logs it.
2. **Creating an artifact of a kind whose schema file is unreadable** (hand-break `schema/work-item.yaml`, create a work item): `store.Unreadable` raises through the client, against "Nothing raises". Task 2 logs it.
3. **`shop-knol init` into a directory that is not there** (`shop-knol init /tmp/none`): kb refuses, but shop-knol ignores the Init response, loads its types into no store, and exits 0. Task 9 logs it.
4. **shop-knol's other tracebacks**: `KB_ACTOR` unset gives `KeyError: 'KB_ACTOR'`, and `create --from` a missing file gives `FileNotFoundError`, both against "shop-knol never shows a traceback". Slice 47 pins the first. Task 7 logs both.
5. **Content that is YAML but not a mapping** (`- a\n` sent as Create content): the servicer raises `TypeError: 'list' object is not a mapping`. Slice 59's question, still open. Task 4 logs it.

---

### Task 1: Slice 1.18, a title that arrives as a yes-or-no is still a title

**Slice plan entry:** Slice 1.18, capability. Unknown: where does a title that arrives as something other than text become the text it would be written as, when the contract carries the title as a text field? Scenario:

1. kb / create-an-artifact / A title given as a yes-or-no is still a title

**Files (kb):**
- Modify: `src/kb/content.py`
- Modify: `tests/test_create_an_artifact.py`

**Files (shop-knowledge):**
- Modify: `src/shop_knowledge/cli.py` (`_text` replaced by `kb.content.text`)
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `tests/calls.py:request(client, type_name, title, content, message)`; the Thens `the name the client is given is made from that text` (slice 1.5) and the Background Given (slice 1).
- Produces: `kb.content.text(value) -> str`. The steps `When the client creates a decision with that title, saying which role and why` (reads fixture `title`, gives `created`) and `Then the title reads back as the text "<text>"`, both reused by Task 8.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.18 2>&1 | tail -3
```

Expected: `1 failed`, a `StepDefinitionNotFoundError` for `Given "a title for a new decision that is the yes-or-no true rather than text"`.

- [ ] **Step 2: The steps**

In `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`, change the import line `from kb import canonical, client as kb_client` to `from kb import canonical, content, client as kb_client`, and append:

```python


@given("a title for a new decision that is the yes-or-no true rather than text", target_fixture="title")
def _a_title_that_is_a_yes_or_no():
    return True


@when("the client creates a decision with that title, saying which role and why", target_fixture="created")
def _create_with_that_title(client, title):
    return request(client, "decision", content.text(title), {"sections": SECTIONS}, message="Record it")


@then(parsers.parse('the title reads back as the text "{text}"'))
def _title_reads_back_as(root, client, created, text):
    assert not created.faults, created.faults
    assert read(client, created.id).title == text
    on_disk = canonical.load((root / "kb" / f"{created.id}.yaml").read_text())
    assert on_disk["title"] == text
```

The client holds a title that is not text and must make it text to put it in the request at all. `CreateRequest(title=True)` raises `TypeError` in protobuf itself. kb's function is how it does that.

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.18 2>&1 | grep -E "^E .*Error|passed|failed"
```

Expected: `AttributeError: module 'kb.content' has no attribute 'text'` and `1 failed`.

- [ ] **Step 3: The function, and shop-knol on it**

Replace the whole of `/home/vscode/shopsystem-kb/src/kb/content.py` with:

```python
"""Artifact content crossing the contract as canonical YAML text, read as YAML 1.2."""
import datetime

from kb import canonical


def dumps(value: dict) -> str:
    """Canonical text: block style, keys in the order given, prose as literal blocks."""
    return canonical.dump(value)


def loads(text: str) -> dict:
    """Read content plainly, by the same check every file kb writes passes. Raises canonical.NotCanonical."""
    return canonical.load(text) or {}


def text(value) -> str:
    """A value as the text YAML 1.2 writes it. A title is text whatever arrived: true is "true", 12 is "12"."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, datetime.date):
        return value.isoformat()
    return str(value)
```

`bool` is tested before anything numeric, since `True` is also an `int`.

In `/home/vscode/shopsystem-knowledge/src/shop_knowledge/cli.py`, change `from kb.content import loads, dumps` to `from kb.content import dumps, loads, text`. Delete the whole function `_text` (the `def _text(title) -> str:` line, its docstring, its four body lines, and the blank lines after it). In `_create`, change `title = _text(content.pop("title", None))` to `title = text(content.pop("title", None))`.

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.18 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m "slice-1 or slice-1.17" 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
```

Expected: `1 passed`; `83 failed, 35 passed`; `4 passed`; `58 failed, 4 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/content.py tests/test_create_an_artifact.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.18: a title that arrives as a yes-or-no is still a title

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
cd /home/vscode/shopsystem-knowledge && git add src/shop_knowledge/cli.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.18: shop-knol makes a title text with kb's function, so true is \"true\"

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.18's Status to `green`. Append at the very end of the log, and check with `tail` that it is last:

```
- <date> slice 1.18 green. Someone can now: create an artifact whose title arrived as true and read it back as the text "true", with the name made from it.
  Assumption "a title that is not text becomes text in the client, through one function kb supplies, since the contract carries text": <held or not>. Evidence: <the real output of: python -c "from kb.content import text; print([text(v) for v in (True, False, None, 12, 12.5)])">.
  Surprised by: <nothing, or what>.
  Open questions: <none, or what arose>. Next: slice 1.19.
```

Commit the plan: `Slice 1.18 green`.

---

### Task 2: Slice 1.19, reading an artifact whose stored file cannot be read is refused

**Slice plan entry:** Slice 1.19, capability. Unknown: can a stored file that fails to parse become a fault naming the file wherever kb loads a stored file, so that nothing kb does raises on it? Scenario:

1. kb / read-an-artifact / Reading an artifact whose stored file cannot be read is refused

**Files (kb):**
- Modify: `src/kb/canonical.py` (`check`, `load`, new `_unreadable`)
- Modify: `src/kb/store.py` (new `Unreadable`, `load`, new `ids`, `artifacts`)
- Modify: `src/kb/servicer.py` (`Read` split, new `_summary`)
- Modify: `tests/test_read_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: the step `When the client reads the decision` (slice 1.15, gives `shown`; with no `readied` client it connects with no root and finds the store from the working directory); `DECISION` in `tests/test_read_an_artifact.py`; the Background (slice 1).
- Produces: `canonical.NotCanonical` for every YAML error; `kb.store.Unreadable(fault)` with `.fault: kb_pb2.Fault` (rule `unreadable`); `Store.ids() -> list[ArtifactId]`; `Store.load` raising `Unreadable`. Task 3 uses all three.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.19 2>&1 | tail -3
```

Expected: `1 failed`, a `StepDefinitionNotFoundError` for `Given "someone edited the decision's file by hand and left it in a shape the store cannot read"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_read_an_artifact.py`:

```python


MANGLED = "title: [a bracket opened by hand and never closed\n"


@given("someone edited the decision's file by hand and left it in a shape the store cannot read")
def _decision_file_mangled_by_hand(root, monkeypatch):
    (root / "kb" / f"{DECISION}.yaml").write_text(MANGLED)
    monkeypatch.chdir(root)
    monkeypatch.delenv("KB_ROOT", raising=False)


@then("the read is rejected because that file cannot be read, and the file is named")
def _rejected_as_unreadable(shown):
    assert [(fault.artifact, fault.rule) for fault in shown.faults] == [(DECISION, "unreadable")]
    assert f"{DECISION}.yaml cannot be read" in shown.faults[0].message


@then("the client is given that fault as it is given any other, the call never breaking off")
def _given_as_any_other_fault(shown):
    assert isinstance(shown, kb_pb2.ReadResponse)
    assert (shown.id, shown.title, shown.content) == ("", "", "")
```

The Given moves into the store because the shared When reads with a client that finds its store from where it works.

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.19 2>&1 | grep -E "^E .*Error|passed|failed"
```

Expected: `ruamel.yaml.parser.ParserError: while parsing a flow sequence` and `1 failed`.

- [ ] **Step 3: Every YAML error a NotCanonical; every unreadable stored file a fault**

In `/home/vscode/shopsystem-kb/src/kb/canonical.py`, add the import line `from ruamel.yaml.error import YAMLError` after `from ruamel.yaml import YAML, events`. In `check`, replace

```python
    parsed = list(_yaml().parse(text))
```

with

```python
    try:
        parsed = list(_yaml().parse(text))
    except YAMLError as error:
        raise NotCanonical(_unreadable(error)) from None
```

and replace the whole function `load` with:

```python
def load(text: str):
    """Plain YAML 1.2: checked, then read. Text that cannot be read raises NotCanonical, never the parser's own error."""
    check(text)
    try:
        return _yaml().load(text)
    except YAMLError as error:
        raise NotCanonical(_unreadable(error)) from None


def _unreadable(error: YAMLError) -> str:
    mark = getattr(error, "problem_mark", None)
    where = f" at line {mark.line + 1}" if mark is not None else ""
    return f"it is not YAML that can be read: {getattr(error, 'problem', None) or error}{where}"
```

In `/home/vscode/shopsystem-kb/src/kb/store.py`, change `from kb.contract import CONTRACT_VERSION` to `from kb.contract import CONTRACT_VERSION, kb_pb2`. Insert above `class Store:`:

```python
class Unreadable(Exception):
    """A stored file that cannot be read. Carries the fault that names it."""

    def __init__(self, fault: kb_pb2.Fault):
        super().__init__(fault.message)
        self.fault = fault


```

Replace `Store.load` with:

```python
    def load(self, artifact_id: ArtifactId) -> dict:
        """The artifact as stored. A file that cannot be read raises Unreadable, naming the file."""
        path = self.path(artifact_id)
        try:
            return canonical.load(path.read_text())
        except canonical.NotCanonical as error:
            raise Unreadable(kb_pb2.Fault(
                artifact=str(artifact_id), rule="unreadable",
                message=f"the stored file {path.relative_to(self.dir)} cannot be read: {error}",
            )) from None
```

and replace `Store.artifacts` with:

```python
    def ids(self) -> list[ArtifactId]:
        """The name of every artifact in the store, schemas included, in path order."""
        return [ArtifactId(Kind(path.parent.name), path.stem) for path in sorted(self.dir.glob("*/*.yaml"))]

    def artifacts(self):
        """Every artifact in the store, schemas included, in path order. A file that cannot be read raises Unreadable."""
        for artifact_id in self.ids():
            yield self.load(artifact_id)
```

In `/home/vscode/shopsystem-kb/src/kb/servicer.py`, change `from kb.store import Store` to `from kb.store import Store, Unreadable`. In `Read`, replace

```python
        artifact = self._store.load(locator.id)
        schema = self._store.schema(locator.id.kind)["schema"]
```

with

```python
        try:
            return self._summary(locator)
        except Unreadable as unreadable:
            return kb_pb2.ReadResponse(faults=[unreadable.fault])

    def _summary(self, locator):
        artifact = self._store.load(locator.id)
        schema = self._store.schema(locator.id.kind)["schema"]
```

The rest of the old `Read` body, from `response = kb_pb2.ReadResponse(` to `return response`, is now `_summary`'s body, unchanged. So any file Read loads, the artifact's own, a reference target's, a schema, or another artifact in the inbound count, answers with its fault rather than raising.

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.19 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m "slice-1 or slice-1.17" 2>&1 | tail -1
```

Expected: `1 passed`; `82 failed, 36 passed`; `4 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/canonical.py src/kb/store.py src/kb/servicer.py tests/test_read_an_artifact.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.19: a stored file that cannot be read is a fault naming it, never an exception

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.19's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.19 green. Someone can now: read an artifact whose file was mangled by hand and be refused with the file named, the call answering like any other refusal.
  Assumption "every YAML error can become NotCanonical in canonical, and every unreadable stored file an Unreadable fault in Store.load": <held or not>. Evidence: <the real output of reading a mangled decision in a scratch store, showing the fault's artifact, rule and message>.
  Surprised by: <nothing, or what>.
  Open questions:
  - QUESTION FOR THE SPEC: reading a sound artifact while a different stored file is unreadable is refused with the other file's fault, because the inbound count loads every artifact. Should the read answer, leaving the broken file to Validate? No scenario pins it. (Review Focus 1)
  - QUESTION FOR THE SPEC: Create of a kind whose schema file is unreadable raises store.Unreadable through the client. No scenario pins it. (Review Focus 2)
  Next: slice 1.20.
```

Commit the plan: `Slice 1.19 green`.

---

### Task 3: Slice 1.20, a check of the store reports a file it cannot read and goes on

**Slice plan entry:** Slice 1.20, capability. Unknown: does kb's first check of a whole store go on past a file that fails to parse, and report it among what it finds in the rest? Needs: the store's check as a call a client makes, as far as this scenario needs it. Scenario:

1. kb / check-the-store / A stored file that cannot be read is reported as a violation

**Files (kb):**
- Modify: `src/kb/contract/kb.proto`; regenerate `src/kb/contract/kb_pb2.py`, `kb_pb2.pyi`, `kb_pb2_grpc.py` with `make contract`
- Modify: `src/kb/client.py` (new `Validate`)
- Modify: `src/kb/servicer.py` (new `Validate`)
- Modify: `tests/test_check_the_store.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `Store.ids()`, `Store.load` raising `Unreadable` (Task 2); `validation.validate(artifact_id: str, content: dict, schema: dict) -> list[Fault]` (slice 1.13); `canonical.IDENTITY`; `tests/calls.py:create`, `define`, `DECISION_TYPE`, `CLIENT`; the `root` fixture (conftest).
- Produces: `kb_pb2.ValidateRequest()`, `kb_pb2.ValidateResponse(violations, faults)`; `InProcessClient.Validate(request)`; `KbServicer.Validate(request, context)`. The step `When the client checks the store` (gives `checked`), which slice 43 reuses. Task 11 calls `Validate` from shop-knol.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.20 2>&1 | tail -3
```

Expected: `1 failed`, a `StepDefinitionNotFoundError` for `Given "a store where someone edited a decision's file by hand and left it in a shape the store cannot read"`.

- [ ] **Step 2: The steps**

Replace the whole of `/home/vscode/shopsystem-kb/tests/test_check_the_store.py` with:

```python
from pytest_bdd import given, scenarios, then, when

from calls import CLIENT, DECISION_TYPE, create, define
from kb import canonical, client as kb_client
from kb.contract import kb_pb2

scenarios("check-the-store.feature")

MANGLED = "title: [a bracket opened by hand and never closed\n"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given(
    "a store where someone edited a decision's file by hand and left it in a shape the store cannot read",
    target_fixture="client",
)
def _store_with_a_file_mangled_by_hand(root):
    """Two decisions edited by hand: one left unreadable, one left readable but without the body of its purpose."""
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))
    define(client, DECISION_TYPE)
    create(client, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS})
    create(client, "decision", {"title": "Prices are reviewed monthly", "sections": SECTIONS})
    (root / "kb" / "decision" / "price-reviews-happen-weekly.yaml").write_text(MANGLED)
    monthly = root / "kb" / "decision" / "prices-are-reviewed-monthly.yaml"
    held = canonical.load(monthly.read_text())
    del held["sections"][0]["body"]
    monthly.write_text(canonical.dump(held))
    return client


@when("the client checks the store", target_fixture="checked")
def _check_the_store(client):
    return client.Validate(kb_pb2.ValidateRequest())


@then("that file is reported as a violation, naming the file")
def _reported_as_unreadable(checked):
    unreadable = [fault for fault in checked.violations if fault.rule == "unreadable"]
    assert [fault.artifact for fault in unreadable] == ["decision/price-reviews-happen-weekly"]
    assert "decision/price-reviews-happen-weekly.yaml cannot be read" in unreadable[0].message


@then("everything else in the store is checked and reported alongside it")
def _the_rest_checked_alongside(checked):
    assert [(fault.artifact, fault.path, fault.rule) for fault in checked.violations] == [
        ("decision/price-reviews-happen-weekly", "", "unreadable"),
        ("decision/prices-are-reviewed-monthly", "sections/0", "required"),
    ]


@then("the check comes back with its answer rather than breaking off")
def _answers(checked):
    assert isinstance(checked, kb_pb2.ValidateResponse)
    assert not checked.faults, checked.faults
```

The second decision is the evidence that the check went on: it sits after the broken file in path order, and its own fault is found. It is broken in a way the composed schema already catches (a section without a body, slice 1.13). kb's required-sections-by-title keyword is not checked yet (slice 43).

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.20 2>&1 | grep -E "^E .*Error|passed|failed"
```

Expected: `AttributeError: 'InProcessClient' object has no attribute 'Validate'` and `1 failed`.

- [ ] **Step 3: Validate in the contract, the client, and the servicer**

In `/home/vscode/shopsystem-kb/src/kb/contract/kb.proto`, add after `  rpc Read(ReadRequest) returns (ReadResponse);`:

```proto
  rpc Validate(ValidateRequest) returns (ValidateResponse);
```

and append at the end of the file:

```proto

message ValidateRequest {
}

// Every violation the store holds, each a fault naming the artifact, the
// place and the rule; a stored file that cannot be read is one of them.
// With faults, a refusal: no store found.
message ValidateResponse {
  repeated Fault violations = 1;
  repeated Fault faults = 2;
}
```

Regenerate, and check that only the new call and messages were added:

```bash
cd /home/vscode/shopsystem-kb && make contract && git diff --stat src/kb/contract
```

Expected: the four files under `src/kb/contract/` changed, `kb_pb2_grpc.py` by about 43 added lines and no removed ones.

In `/home/vscode/shopsystem-kb/src/kb/client.py`, add after `Read`:

```python

    def Validate(self, request, timeout=None):
        servicer, refusal = self._servicer()
        if refusal is not None:
            return kb_pb2.ValidateResponse(faults=[refusal])
        return servicer.Validate(request, None)
```

In `/home/vscode/shopsystem-kb/src/kb/servicer.py`, add above `def _stub(self, field, target_id: ArtifactId):`:

```python
    def Validate(self, request, context):
        """Every artifact checked against its type; a file that cannot be read is reported and the check goes on."""
        violations = []
        for artifact_id in self._store.ids():
            try:
                artifact = self._store.load(artifact_id)
                schema = self._store.schema(artifact_id.kind)["schema"]
            except Unreadable as unreadable:
                violations.append(unreadable.fault)
                continue
            content = {key: value for key, value in artifact.items() if key not in canonical.IDENTITY[:4]}
            violations += validation.validate(str(artifact_id), content, schema)
        return kb_pb2.ValidateResponse(violations=violations)

```

`IDENTITY[:4]` is `id`, `type`, `schema_version`, `revision`. The title stays, because every type declares it.

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.20 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m "slice-1 or slice-1.17" 2>&1 | tail -1
```

Expected: `1 passed`; `81 failed, 37 passed`; `4 passed`. Slice 43's four scenarios now fail on their Givens instead of on the When.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/contract src/kb/client.py src/kb/servicer.py tests/test_check_the_store.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.20: Validate reports a file it cannot read and checks the rest

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.20's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.20 green. Someone can now: check a whole store and be told of a file that cannot be read and of every artifact that does not fit its type, the check going on past the broken file.
  Assumption "the first check of a whole store goes on past an unreadable file": <held or not>. Evidence: <the real violations list from the scenario's store, printed as (artifact, path, rule)>.
  Surprised by: <nothing, or what>.
  Open questions: <none, or what arose>. Next: slice 1.21.
```

Commit the plan: `Slice 1.20 green`.

---

### Task 4: Slice 1.21, content naming the same entry twice is refused

**Slice plan entry:** Slice 1.21, capability. Unknown: can the place of the second of two entries with the same name be given in the form the contract gives places in, when the reader stops at it knowing only a line and a column? Scenario:

1. kb / create-an-artifact / Content naming the same entry twice is refused

**Files (kb):**
- Modify: `src/kb/canonical.py` (`NotCanonical` gains `path`; `check` calls new `_named_once`)
- Modify: `src/kb/servicer.py` (Create's content fault carries the path)
- Modify: `tests/test_create_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `tests/test_create_an_artifact.py:_raw(client, text)` (slice 1.6); `canonical.check` and `_unreadable` (Task 2).
- Produces: `canonical.NotCanonical(message, path="")` with `.path: str`; the steps `When the client creates a decision from that content, saying which role and why` (reads fixture `written`, gives `created`), reused by Tasks 5 and 8. Task 7 relies on `.path` being the node path of the second entry.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.21 2>&1 | tail -3
```

Expected: `1 failed`, a `StepDefinitionNotFoundError` for `Given "content for a decision that names the same entry twice in the same place"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`:

```python


@given("content for a decision that names the same entry twice in the same place", target_fixture="written")
def _content_naming_an_entry_twice():
    return (
        "sections:\n"
        "  - title: Purpose\n"
        "    body: Keep prices in step with costs.\n"
        "    body: Keep prices low.\n"
        "  - title: Rationale\n"
        "    body: Because.\n"
    )


@when("the client creates a decision from that content, saying which role and why", target_fixture="created")
def _create_from_that_content(client, written):
    return _raw(client, written)


@then("the artifact is rejected because an entry is named once and only once, and the place the second one stands is named")
def _rejected_for_an_entry_named_twice(created):
    assert (created.id, created.revision) == ("", 0)
    assert [(fault.path, fault.rule) for fault in created.faults] == [("sections/0/body", "content")]
    assert created.faults[0].message.startswith("an entry is named once and only once")
    assert "line 4" in created.faults[0].message
```

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.21 2>&1 | grep -E "^E  +assert|^E .*Error|passed|failed"
```

Expected: `AssertionError: assert [('', 'content')] == [('sections/0...', 'content')]` and `1 failed`. Since Task 2, ruamel's `DuplicateKeyError` is already a `content` fault, but it names no place.

- [ ] **Step 3: The check finds a repeated entry itself, by walking the nodes**

In `/home/vscode/shopsystem-kb/src/kb/canonical.py`, change `from ruamel.yaml import YAML, events` to `from ruamel.yaml import YAML, events, nodes`. Replace the class `NotCanonical` with:

```python
class NotCanonical(ValueError):
    """YAML that is not read plainly as written. The message says which rule it breaks; `path` names the place, if any."""

    def __init__(self, message: str, path: str = ""):
        super().__init__(message)
        self.path = path
```

In `check`, after the last rule

```python
    if sum(isinstance(event, events.DocumentStartEvent) for event in parsed) > 1:
        raise NotCanonical("content holds exactly one document")
```

add the line `    _named_once(_yaml().compose(text), ())`, and add below `check`:

```python


def _named_once(node, place: tuple) -> None:
    """Every entry of every mapping is named once and only once. Raises NotCanonical at the second of a pair."""
    if isinstance(node, nodes.MappingNode):
        seen = set()
        for key, value in node.value:
            if key.value in seen:
                raise NotCanonical(
                    f"an entry is named once and only once; {key.value!r} is named again at line {key.start_mark.line + 1}",
                    "/".join((*place, str(key.value))),
                )
            seen.add(key.value)
            _named_once(value, (*place, str(key.value)))
    elif isinstance(node, nodes.SequenceNode):
        for index, item in enumerate(node.value):
            _named_once(item, (*place, str(index)))
```

Composing builds nodes without constructing values, so a repeated key is still there to be found, with its mark. Aliases and extra documents are refused before this line, so `compose` sees one plain document. An empty text composes to `None` and passes.

Update the docstring of `check` to read:

```python
    """The one check of plain reading, run on content as it arrives and on every file kb is about to write.

    No tags, no anchors or aliases, exactly one document, every entry named once. Raises NotCanonical naming the
    first rule broken.
    """
```

In `/home/vscode/shopsystem-kb/src/kb/servicer.py`, in `Create`, replace the first

```python
        except canonical.NotCanonical as fault:
            return kb_pb2.CreateResponse(faults=[kb_pb2.Fault(artifact=at, rule="content", message=str(fault))])
```

(the one after `content = loads(request.content)`) with

```python
        except canonical.NotCanonical as fault:
            return kb_pb2.CreateResponse(faults=[kb_pb2.Fault(
                artifact=at, path=fault.path, rule="content", message=str(fault),
            )])
```

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.21 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m "slice-1 or slice-1.17" 2>&1 | tail -1
```

Expected: `1 passed`; `80 failed, 38 passed`; `4 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/canonical.py src/kb/servicer.py tests/test_create_an_artifact.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.21: an entry named twice is refused at the place of the second

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.21's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.21 green. Someone can now: send content naming an entry twice and be refused with the node path and the line of the second.
  Assumption "the place of a repeated entry can be given as a node path": <held or not>. Evidence: <the real output of: python -c "from kb import canonical
for t in ['a: 1\na: 2\n', 'x:\n  - {b: 1, b: 2}\n']:
    try: canonical.load(t)
    except canonical.NotCanonical as e: print(repr(e.path), e)">.
  Surprised by: <nothing, or what>.
  Open questions:
  - QUESTION FOR THE SPEC (slice 59's, still open): content that is YAML but not a mapping (`- a`) raises TypeError through the client. (Review Focus 5)
  Next: slice 1.22.
```

Commit the plan: `Slice 1.21 green`.

---

### Task 5: Slice 1.22, content cannot declare the format it is read by

**Slice plan entry:** Slice 1.22, capability. Unknown: can the one check of plain reading see a directive, and where it stands, before the reader has taken it up and changed how the rest is read? Scenario:

1. kb / create-an-artifact / Content that opens by declaring the format it is written in is refused

**Files (kb):**
- Modify: `src/kb/canonical.py` (`check` calls new `_no_directive` first)
- Modify: `tests/test_create_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `When the client creates a decision from that content, saying which role and why` (Task 4, fixture `written`); `NotCanonical` (Task 4).
- Produces: nothing later tasks call.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.22 2>&1 | tail -3
```

Expected: `1 failed`, a `StepDefinitionNotFoundError` for `Given "content for a decision that opens with a line declaring which version of the writing format the rest is in"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`:

```python


@given(
    "content for a decision that opens with a line declaring which version of the writing format the rest is in",
    target_fixture="written",
)
def _content_opening_with_a_directive():
    return (
        "%YAML 1.1\n"
        "---\n"
        "switch: on\n"
        "sections:\n"
        "  - title: Purpose\n    body: Why.\n"
        "  - title: Rationale\n    body: Because.\n"
    )


@then(
    "the artifact is rejected because content is read plainly as written and opens with no declaration of its format, "
    "and the place the declaration stands is named"
)
def _rejected_for_a_directive(created):
    assert (created.id, created.revision) == ("", 0)
    assert [fault.rule for fault in created.faults] == ["content"]
    assert created.faults[0].message == (
        "content is read plainly as written and opens with no declaration of its format; "
        "line 1 declares %YAML 1.1"
    )
```

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.22 2>&1 | grep -E "^E  +assert|passed|failed"
```

Expected: `AssertionError: assert ('decision/pr...en-weekly', 1) == ('', 0)` and `1 failed`. The content was accepted, and under the directive `switch: on` was stored as YAML 1.1 reads it.

- [ ] **Step 3: The directive rule, first in the check**

In `/home/vscode/shopsystem-kb/src/kb/canonical.py`, change `from ruamel.yaml import YAML, events, nodes` to `from ruamel.yaml import YAML, events, nodes, tokens`. In `check`, replace

```python
    try:
        parsed = list(_yaml().parse(text))
```

with

```python
    try:
        _no_directive(text)
        parsed = list(_yaml().parse(text))
```

and change the docstring's rule list to `No directive, no tags, no anchors or aliases, exactly one document, every entry named once.` Add above `def _named_once`:

```python
def _no_directive(text: str) -> None:
    """Content cannot choose the rules it is read by: a %YAML or %TAG line is refused before anything reads past it."""
    for token in _yaml().scan(text):
        if isinstance(token, tokens.DirectiveToken):
            value = ".".join(map(str, token.value)) if token.name == "YAML" else " ".join(token.value)
            raise NotCanonical(
                "content is read plainly as written and opens with no declaration of its format; "
                f"line {token.start_mark.line + 1} declares %{token.name} {value}"
            )
        if not isinstance(token, (tokens.StreamStartToken, tokens.DirectiveToken)):
            return


```

Tokens are scanned, not parsed, so the directive is met before any reader acts on it. The document-start event would give the `---` line instead of the directive's. The scan stops at the first token that is not a directive, since directives can only open a document. A directive before a second document is refused by the one-document rule.

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.22 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m "slice-1 or slice-1.17" 2>&1 | tail -1
```

Expected: `1 passed`; `79 failed, 39 passed`; `4 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/canonical.py tests/test_create_an_artifact.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.22: content that declares its own format is refused, naming the line

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.22's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.22 green. Someone can now: send content opening with a %YAML or %TAG line and be refused with the line named, so content cannot switch kb's reader.
  Assumption "the check sees a directive before the reader takes it up": <held or not>. Evidence: <the real output of: python -c "from kb import canonical
for t in ['%TAG !e! tag:example.com,2000:\n---\na: 1\n', '# note\n%YAML 1.2\n---\na: 1\n', 'a: \"%YAML\"\n']:
    try: print(canonical.load(t))
    except canonical.NotCanonical as e: print(e)">.
  Surprised by: <nothing, or what>.
  Open questions: <none, or what arose>. Next: slice 1.23.
```

Commit the plan: `Slice 1.22 green`.

---

### Task 6: Slice 1.23, starting a store without naming a directory is refused

**Slice plan entry:** Slice 1.23, capability. Unknown: can the directory a store is started in become a checked value where it enters kb, like every other value a request carries, when it may be relative and no store exists yet? Scenario:

1. kb / start-a-store / Starting a store without naming a directory at all is refused

**Files (kb):**
- Modify: `src/kb/values.py` (new `root`)
- Modify: `src/kb/servicer.py` (`__init__` takes no root; `Init` converts the root)
- Modify: `src/kb/client.py` (`Init`)
- Modify: `tests/test_start_a_store.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `values.Refused` (slice 1.14); `_everything_under(directory)` in `tests/test_start_a_store.py` (slice 1.16).
- Produces: `values.root(text: str) -> Path`, raising `Refused` with rule `root`, which Task 9 completes; `KbServicer(root=None)`.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.23 2>&1 | tail -3
```

Expected: `1 failed`, a `StepDefinitionNotFoundError` for `Given "the client has nothing at all to name as the directory to start a store in"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_start_a_store.py`:

```python


@given("the client has nothing at all to name as the directory to start a store in", target_fixture="here")
def _nothing_to_name(tmp_path, monkeypatch):
    """The client works in an empty directory, so a store made where it works, for want of a name, would show."""
    here = tmp_path / "here"
    here.mkdir()
    monkeypatch.chdir(here)
    monkeypatch.delenv("KB_ROOT", raising=False)
    return {"before": _everything_under(tmp_path)}


@when("the client starts a store naming nothing, saying which role it is", target_fixture="started")
def _start_a_store_naming_nothing():
    return kb_client.connect().Init(kb_pb2.InitRequest(root="", actor=CLIENT))


@then("starting the store is rejected because a store is started in a directory that was named and that exists")
def _rejected_as_named_nothing(started):
    assert [(fault.rule, fault.message) for fault in started.faults] == [
        ("root", "a store is started in a directory that was named and that exists; no directory was named"),
    ]


@then("no store is made anywhere")
def _no_store_anywhere(here, tmp_path):
    assert _everything_under(tmp_path) == here["before"]
```

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.23 2>&1 | grep -E "^E  +assert|passed|failed"
```

Expected: `AssertionError: assert [] == [('root', 'a ...y was named')]` and `1 failed`. `Path("")` is `.`, so a store was started in the working directory.

- [ ] **Step 3: The root, converted at the boundary**

In `/home/vscode/shopsystem-kb/src/kb/values.py`, add above `def slug(title: str) -> str:`:

```python
def root(text: str) -> Path:
    """The directory a store is started in, as the request names it; relative names stay relative."""
    if not text:
        raise Refused([kb_pb2.Fault(
            rule="root",
            message="a store is started in a directory that was named and that exists; no directory was named",
        )])
    return Path(text)


```

In `/home/vscode/shopsystem-kb/src/kb/servicer.py`, replace

```python
    def __init__(self, root):
        self._store = Store(root)
```

with

```python
    def __init__(self, root=None):
        """Over the store at root; with none, a servicer that can only start a store, taking its root from the request."""
        self._store = Store(root) if root is not None else None
```

and in `Init` replace

```python
        store = Store(request.root)
        store.start()
```

with

```python
        try:
            store = Store(values.root(request.root))
        except values.Refused as refused:
            return kb_pb2.InitResponse(faults=refused.faults)
        store.start()
```

In `/home/vscode/shopsystem-kb/src/kb/client.py`, in `Init`, change `return KbServicer(Path(request.root)).Init(request, None)` to `return KbServicer().Init(request, None)`. The request's root is then turned into a path in one place, `values.root`.

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.23 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m "slice-1 or slice-1.17" 2>&1 | tail -1
```

Expected: `1 passed`; `78 failed, 40 passed`; `4 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/values.py src/kb/servicer.py src/kb/client.py tests/test_start_a_store.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.23: Init's root is a checked value; naming none is refused

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.23's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.23 green. Someone can now: start a store naming no directory and be refused, with nothing made where they work.
  Assumption "Init's root can be a checked value at the boundary": <held or not>. Evidence: <the real faults of connect().Init(InitRequest(root="", actor=...)) and the grep for "Store(request" over src/kb printing nothing>.
  Surprised by: <nothing, or what>.
  Open questions: <none, or what arose>. Next: slice 1.24.
```

Commit the plan: `Slice 1.23 green`.

---

### Task 7: Slice 1.24, shop-knol refuses a file it cannot read in plain words

**Slice plan entry:** Slice 1.24, capability. Unknown: how does shop-knol give every refusal, kb's and its own reading of the user's file alike, as plain words and a non-zero exit, so that no traceback reaches the user? Scenario:

1. shop-knowledge / record-a-decision / A file naming the same entry twice is refused

**Files (shop-knowledge):**
- Modify: `src/shop_knowledge/cli.py` (module docstring, new `_plain` and `_refuse`, `_create`)
- Modify: `tests/driver.py` (new `refused_plainly`, `reported_failure`)
- Modify: `tests/test_record_a_decision.py`
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.canonical.NotCanonical` with `.path` (Task 4); the step `When the user records that file as a decision, saying who they are and why` (slice 1, fixture `decision_file`, gives `recorded`, a `CompletedProcess`).
- Produces: `shop_knowledge.cli._plain(fault) -> str` and `_refuse(faults) -> int`, used by Tasks 10 and 11; `driver.refused_plainly(result)` and `driver.reported_failure(result)`, used by Tasks 10 and 11.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1.24 2>&1 | tail -3
```

Expected: `1 failed`, a `StepDefinitionNotFoundError` for `Given "a decision in a file that names the same entry twice in the same place"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-knowledge/tests/driver.py`:

```python


def refused_plainly(result):
    """Refused in plain words: something said on stderr, no traceback anywhere, nothing on stdout."""
    assert result.stderr.strip(), "nothing was said"
    assert "Traceback" not in result.stderr + result.stdout, result.stderr
    assert result.stdout == ""


def reported_failure(result):
    assert result.returncode != 0, result.stdout
```

In `/home/vscode/shopsystem-knowledge/tests/test_record_a_decision.py`, change `from driver import knol, record` to `from driver import knol, record, refused_plainly, reported_failure`, and append:

```python


@given("a decision in a file that names the same entry twice in the same place", target_fixture="decision_file")
def _decision_in_a_file_naming_an_entry_twice(tmp_path):
    path = tmp_path / "twice.yaml"
    path.write_text(
        "title: Price reviews happen weekly\n"
        "sections:\n"
        "  - title: Purpose\n"
        "    body: Keep prices in step with costs.\n"
        "    body: Keep prices low.\n"
        "  - title: Rationale\n"
        "    body: Costs move weekly.\n"
    )
    return path


@then("the decision is rejected because an entry is named once and only once, naming the place in the file")
def _rejected_for_an_entry_named_twice(recorded, decision_file):
    assert recorded.stderr.splitlines() == [
        f"{decision_file} at sections/0/body: an entry is named once and only once; 'body' is named again at line 5",
    ]


@then("the user is shown that fault in plain words, never a traceback")
def _shown_in_plain_words(recorded):
    refused_plainly(recorded)


@then("the command reports failure to whatever ran it")
def _reports_failure(recorded):
    reported_failure(recorded)
```

The two shared Thens are helpers in `driver.py`, not conftest steps, because each feature's When gives its result under its own fixture name.

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1.24 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: `At index 0 diff: 'Traceback (most recent call last):' != "…twice.yaml at sections/0/body: …"` and `1 failed`.

- [ ] **Step 3: One printer for every refusal**

In `/home/vscode/shopsystem-knowledge/src/shop_knowledge/cli.py`, replace the head of the file, from the docstring through `from kb import client as kb_client`, with:

```python
"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting.

Every file it reads and everything it prints is YAML 1.2, read and written by kb's own reading and writing of content.
A refusal, kb's or its own, is printed in plain words on stderr, one fault a line, with a non-zero exit; never a traceback.
"""
import argparse
import os
import sys
from pathlib import Path

from kb import canonical, client as kb_client
```

Add above `def _init(args) -> int:`:

```python
def _plain(fault: kb_pb2.Fault) -> str:
    """One fault as a line a person reads: where, then what is wrong."""
    where = f"{fault.artifact} at {fault.path}" if fault.path else fault.artifact
    return f"{where}: {fault.message}"


def _refuse(faults) -> int:
    for fault in faults:
        print(_plain(fault), file=sys.stderr)
    return 1


```

Replace the body of `_create` with:

```python
    try:
        content = loads(Path(args.source).read_text())
    except canonical.NotCanonical as fault:
        return _refuse([kb_pb2.Fault(artifact=args.source, path=fault.path, rule="content", message=str(fault))])
    title = text(content.pop("title", None))
    response = _client().Create(kb_pb2.CreateRequest(
        type=args.type, title=title, content=dumps(content), actor=_actor(), message=args.message,
    ))
    if response.faults:
        return _refuse(response.faults)
    _show({"id": response.id, "revision": response.revision})
    return 0
```

A file shop-knol cannot read is refused the way kb refuses content, as a fault with the file's name as its artifact, printed by the same function as kb's own faults.

- [ ] **Step 4: Run it green, and the suite**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1.24 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
```

Expected: `1 passed`; `57 failed, 5 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-knowledge && git add src/shop_knowledge/cli.py tests/driver.py tests/test_record_a_decision.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.24: shop-knol refuses a file it cannot read in plain words, never a traceback

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.24's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.24 green. Someone can now: record a file that names an entry twice and be told in plain words where, with a non-zero exit and no traceback; any fault kb returns on create is printed the same way.
  Assumption "one printer serves kb's faults and shop-knol's own reading of a file": <held or not>. Evidence: <the real stderr and exit status of shop-knol create decision --from <a file with a repeated key> in a scratch shop>.
  Surprised by: <nothing, or what>.
  Open questions:
  - QUESTION FOR THE SPEC: shop-knol still shows a traceback with KB_ACTOR unset (KeyError) and for --from a file that is not there (FileNotFoundError); the spec says never. (Review Focus 4)
  Next: slice 1.25.
```

Commit the plan: `Slice 1.24 green`.

---

### Task 8: Slice 1.25, Create refuses a kind with no type, keeps typed values typed, and takes a number as a title

**Slice plan entry:** Slice 1.25, capability, no unknown. Scenarios:

1. kb / create-an-artifact / A kind the store holds no type for is refused
2. kb / create-an-artifact / Values written as a yes-or-no, as nothing and as a number keep those meanings
3. kb / create-an-artifact / A title given as a number is still a title

**Files (kb):**
- Modify: `src/kb/servicer.py` (`Create`)
- Modify: `tests/test_create_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `When the client creates an artifact of the kind "<kind>", with a title and both required sections, saying which role and why` (slice 1.14, gives `attempt`, a dict of `response`, `before`, `after`); `When the client creates a decision from that content, …` (Task 4); `When the client creates a decision with that title, …` and `Then the title reads back as the text "<text>"` (Task 1); `Then the name the client is given is made from that text` (slice 1.5).
- Produces: nothing later tasks call.

- [ ] **Step 1: Run them red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.25 2>&1 | tail -3
```

Expected: `3 failed`, each a `StepDefinitionNotFoundError` for its Given.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`:

```python


@given(parsers.parse('a store that holds no type called "{kind}"'))
def _no_type_called(client, kind):
    assert read(client, f"schema/{kind}").faults


@then("the artifact is rejected because a kind must name a type the store holds, and the kind asked for is given back")
def _rejected_as_an_unknown_kind(attempt):
    refused = attempt["response"]
    assert (refused.id, refused.revision) == ("", 0)
    assert refused.faults[0].rule == "kind"
    assert refused.faults[0].message == "a kind must name a type the store holds; the store holds no type called 'invoice'"


@then("that fault stands on its own, apart from anything wrong with the content")
def _the_kind_fault_alone(attempt):
    assert [(fault.path, fault.rule) for fault in attempt["response"].faults] == [("", "kind")]


@then("nothing is written anywhere in the store")
def _nothing_written_in_the_store(attempt):
    assert attempt["after"] == attempt["before"]


@given(
    'content for a decision carrying one field written "true", one field left as nothing, and one field written "12.5"',
    target_fixture="written",
)
def _content_with_typed_values():
    return (
        "urgent: true\n"
        "owner:\n"
        "weight: 12.5\n"
        "sections:\n"
        "  - title: Purpose\n    body: Why.\n"
        "  - title: Rationale\n    body: Because.\n"
    )


@then("the first field reads back as a yes-or-no, the second as nothing at all, and the third as a number")
def _typed_values_read_back(root, created):
    assert not created.faults, created.faults
    on_disk = canonical.load((root / "kb" / f"{created.id}.yaml").read_text())
    assert (on_disk["urgent"], on_disk["owner"], on_disk["weight"]) == (True, None, 12.5)


@then("none of the three reads back as text")
def _none_of_them_text(root, created):
    on_disk = canonical.load((root / "kb" / f"{created.id}.yaml").read_text())
    assert not any(isinstance(on_disk[name], str) for name in ("urgent", "owner", "weight"))


@given("a title for a new decision that is the number 12 rather than text", target_fixture="title")
def _a_title_that_is_a_number():
    return 12
```

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.25 2>&1 | grep -E "^E .*Error|^FAILED|passed|failed"
```

Expected: `FileNotFoundError: … store/kb/schema/invoice.yaml`, `FAILED tests/test_create_an_artifact.py::test_a_kind_the_store_holds_no_type_for_is_refused`, and `1 failed, 2 passed`. The typed values and the number title pass on their step definitions alone: ruamel's YAML 1.2 loader has typed `true`, `null` and `12.5` since slice 1.11, and `content.text(12)` is `"12"` since Task 1. That is not bdd-red-green's first stop condition, since nothing passed before the steps existed, but the checkpoint says so plainly. If either fails on a Then instead, stop and hand back.

- [ ] **Step 3: The kind's type looked for before anything else**

In `/home/vscode/shopsystem-kb/src/kb/servicer.py`, in `Create`, replace

```python
        except values.Refused as refused:
            return kb_pb2.CreateResponse(faults=refused.faults)
        at = f"{kind.name}/{values.slug(request.title)}"
```

with

```python
        except values.Refused as refused:
            return kb_pb2.CreateResponse(faults=refused.faults)
        if not self._store.holds(ArtifactId(Kind("schema"), kind.name)):
            return kb_pb2.CreateResponse(faults=[kb_pb2.Fault(
                rule="kind", message=f"a kind must name a type the store holds; the store holds no type called {kind.name!r}",
            )])
        at = f"{kind.name}/{values.slug(request.title)}"
```

- [ ] **Step 4: Run them green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.25 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m "slice-1 or slice-1.17" 2>&1 | tail -1
```

Expected: `3 passed`; `75 failed, 43 passed`; `4 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/servicer.py tests/test_create_an_artifact.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.25: a kind with no type is its own fault; typed values and a number title hold

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.25's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.25 green. Someone can now: create an artifact of a kind the store holds no type for and be refused with that alone and nothing written; send true, nothing and 12.5 and read them back typed; give 12 as a title and read back "12".
  Surprised by: <nothing, or: two of the three scenarios went green on their step definitions, as the task predicted>.
  Open questions: <none, or what arose>. Next: slice 1.26.
```

Commit the plan: `Slice 1.25 green`.

---

### Task 9: Slice 1.26, starting a store where no directory stands is refused

**Slice plan entry:** Slice 1.26, capability, no unknown. Scenarios:

1. kb / start-a-store / Starting a store in a directory that is not there is refused
2. kb / start-a-store / Starting a store where a file sits instead of a directory is refused

**Files (kb):**
- Modify: `src/kb/values.py` (`root`)
- Modify: `tests/test_start_a_store.py` (the shared When gives the response; `client` becomes a fixture)

**Files (shop-knowledge):**
- Modify: `tests/conftest.py` (the `shop` fixture makes its directory)
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `values.root` (Task 6); the step `When the client starts a store there, saying which role it is` (slice 1), whose Thens (slices 1, 1.4) read the store through `client` and `root`.
- Produces: that When now gives `started` (the `InitResponse`), and `client` is a module fixture over `root`.

- [ ] **Step 1: Run them red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.26 2>&1 | tail -3
```

Expected: `2 failed`, each a `StepDefinitionNotFoundError` for its Given.

- [ ] **Step 2: The shared When gives what Init answered**

In `/home/vscode/shopsystem-kb/tests/test_start_a_store.py`, add `import pytest` above `from pytest_bdd import given, parsers, scenarios, then, when`, and replace

```python
@when("the client starts a store there, saying which role it is", target_fixture="client")
def _start_a_store(root):
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))
    return client
```

with

```python
@pytest.fixture
def client(root):
    """A client over the store at root, for the steps that go on to use the store a scenario started."""
    return kb_client.connect(root)


@when("the client starts a store there, saying which role it is", target_fixture="started")
def _start_a_store(client, root):
    return client.Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))
```

A client is readied without finding a store (slice 1.15), so readying it before the store exists changes nothing for slice 1's Thens.

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q tests/test_start_a_store.py -m "slice-1 or slice-1.4 or slice-1.10 or slice-1.16 or slice-1.23" 2>&1 | tail -1
```

Expected: `5 passed, 5 deselected`. The five scenarios of start-a-store that were green stay green; slice 45's three and slice 1.26's two are the ones deselected.

- [ ] **Step 3: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_start_a_store.py`:

```python


@given("a place on the disk where no directory exists", target_fixture="root")
def _a_place_with_no_directory(tmp_path):
    return tmp_path / "nowhere" / "store"


@then("starting the store is rejected because a store is started in a directory that exists")
def _rejected_as_not_there(started, root):
    assert [(fault.rule, fault.message) for fault in started.faults] == [
        ("root", f"a store is started in a directory that exists; {str(root)!r} does not"),
    ]


@then("nothing is made at that place")
def _nothing_made_there(root):
    assert not root.parent.exists()


FILE_TEXT = b"notes the store must not write through\n"


@given("a place on the disk holding a file rather than a directory", target_fixture="root")
def _a_place_holding_a_file(tmp_path):
    root = tmp_path / "store"
    root.write_bytes(FILE_TEXT)
    return root


@then("starting the store is rejected because a store is started in a directory, and what was named is not one")
def _rejected_as_not_a_directory(started, root):
    assert [(fault.rule, fault.message) for fault in started.faults] == [
        ("root", f"a store is started in a directory, and {str(root)!r} is not one"),
    ]


@then("that file is left as it was")
def _file_left_as_it_was(root):
    assert root.read_bytes() == FILE_TEXT
```

The missing place is two levels down, so a store that built its way there would show in the parent.

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.26 2>&1 | grep -E "^E  +assert|^E .*Error|passed|failed"
```

Expected: `assert [] == [('root', "a ...e' does not")]`, `NotADirectoryError: [Errno 20] Not a directory: '…/store/kb'`, and `2 failed`.

- [ ] **Step 4: The rest of the root's check**

In `/home/vscode/shopsystem-kb/src/kb/values.py`, in `root`, replace the last line `    return Path(text)` with:

```python
    named = Path(text)
    if not named.exists():
        raise Refused([kb_pb2.Fault(
            rule="root", message=f"a store is started in a directory that exists; {text!r} does not",
        )])
    if not named.is_dir():
        raise Refused([kb_pb2.Fault(
            rule="root", message=f"a store is started in a directory, and {text!r} is not one",
        )])
    return named
```

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1.26 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q 2>&1 | tail -1
```

Expected: `2 passed`; `73 failed, 45 passed`; and shop-knowledge `61 failed, 1 passed`. The shop's steps start its knowledge base in `tmp_path / "shop"`, which nothing made, and kb no longer builds it.

- [ ] **Step 5: The shop starts where a directory is**

Every shop scenario that starts a knowledge base starts it in a directory that is there ("One command in an empty directory", "a directory holding other work of the shop's"). In `/home/vscode/shopsystem-knowledge/tests/conftest.py`, replace the `shop` fixture's body

```python
    """The directory the shop's knowledge base is started in; the store is its kb/ subdirectory."""
    return tmp_path / "shop"
```

with

```python
    """The directory the shop's knowledge base is started in, there before it starts; the store is its kb/ subdirectory."""
    shop = tmp_path / "shop"
    shop.mkdir()
    return shop
```

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q 2>&1 | tail -1
```

Expected: `57 failed, 5 passed`.

- [ ] **Step 6: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/values.py tests/test_start_a_store.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.26: a store is started only in a directory that is there

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
cd /home/vscode/shopsystem-knowledge && git add tests/conftest.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.26: the shop's scenarios start in a directory that is there

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 7: Checkpoint**

Set slice 1.26's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.26 green. Someone can now: start a store at a place with no directory, or where a file sits, and be refused with nothing made and the file untouched.
  Surprised by: <nothing, or: shop-knowledge's fixture had started every knowledge base in a directory that did not exist, and kb had built it>.
  Open questions:
  - QUESTION FOR THE SPEC: shop-knol init into a directory that is not there exits 0 having started nothing; it ignores kb's refusal and loads its types into no store. Slice 47 pins what the user sees on init. (Review Focus 3)
  Next: slice 1.27.
```

Commit the plan: `Slice 1.26 green`.

---

### Task 10: Slice 1.27, reading a decision whose file the shop cannot read is refused in plain words

**Slice plan entry:** Slice 1.27, capability, no unknown. Needs: the shop's read reporting a refusal kb returns, where today it prints an empty artifact and succeeds. Scenario:

1. shop-knowledge / read-back-what-the-shop-knows / Reading something whose file the shop cannot read is refused

**Files (shop-knowledge):**
- Modify: `src/shop_knowledge/cli.py` (`_read`)
- Modify: `tests/test_read_back_what_the_shop_knows.py` (the shared When gives the process; `shown` becomes a fixture)
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `_refuse` (Task 7); `driver.refused_plainly`, `driver.reported_failure` (Task 7); Read's `unreadable` fault (Task 2); the Background (slice 1, gives `decision_id`, and the `shop` fixture is the knowledge base's directory).
- Produces: the step `When the user reads the decision` now gives `result` (the `CompletedProcess`), and `shown` is a fixture that asserts success and loads stdout. Slice 22's scenarios will reuse both.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1.27 2>&1 | tail -3
```

Expected: `1 failed`, a `StepDefinitionNotFoundError` for `Given "someone edited the decision's file by hand and left it in a shape the shop cannot read"`.

- [ ] **Step 2: The steps**

In `/home/vscode/shopsystem-knowledge/tests/test_read_back_what_the_shop_knows.py`, replace the import lines

```python
from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start
```

with

```python
import pytest
from kb.content import loads
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, refused_plainly, reported_failure, start
```

and replace

```python
@when("the user reads the decision", target_fixture="shown")
def _read_the_decision(env, decision_id):
    result = knol(env, "read", decision_id)
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)
```

with

```python
@when("the user reads the decision", target_fixture="result")
def _read_the_decision(env, decision_id):
    return knol(env, "read", decision_id)


@pytest.fixture
def shown(result):
    """What the user is shown, for the steps that expect the read to succeed."""
    assert result.returncode == 0, result.stderr
    return loads(result.stdout)
```

Slice 1's three Thens take `shown` as before and are unchanged. Append:

```python


@given("someone edited the decision's file by hand and left it in a shape the shop cannot read")
def _decision_file_mangled_by_hand(shop):
    (shop / "kb" / f"{DECISION}.yaml").write_text("title: [a bracket opened by hand and never closed\n")


@then("the command is rejected because that file cannot be read, naming the file")
def _rejected_as_unreadable(result):
    assert result.stderr.startswith(f"{DECISION}: the stored file {DECISION}.yaml cannot be read: ")


@then("the user is shown that fault in plain words, never a traceback")
def _shown_in_plain_words(result):
    refused_plainly(result)


@then("the command reports failure to whatever ran it")
def _reports_failure(result):
    reported_failure(result)
```

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1.27 2>&1 | grep -E "^E  |passed|failed" | head -4
python -m pytest -q -m slice-1 tests/test_read_back_what_the_shop_knows.py 2>&1 | tail -1
```

Expected: the startswith assertion fails on `''` with `stdout="id: ''\ntype: ''\nschema_version: 0\n…"` (an empty artifact, exit 0), and `1 failed`; slice 1's read still `1 passed`.

- [ ] **Step 3: The shop's read reports a refusal**

In `/home/vscode/shopsystem-knowledge/src/shop_knowledge/cli.py`, in `_read`, add after `response = _client().Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=args.locator)))`:

```python
    if response.faults:
        return _refuse(response.faults)
```

- [ ] **Step 4: Run it green, and the suite**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1.27 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
```

Expected: `1 passed`; `56 failed, 6 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-knowledge && git add src/shop_knowledge/cli.py tests/test_read_back_what_the_shop_knows.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.27: shop-knol read reports kb's refusal in plain words

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.27's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.27 green. Someone can now: read a decision whose file was mangled by hand and be told in plain words which file cannot be read, with a non-zero exit; any refusal kb gives a read is printed the same way (slice 60's open question on the shop's read of a refused name).
  Surprised by: <nothing, or what>.
  Open questions: <none, or what arose>. Next: slice 1.28.
```

Commit the plan: `Slice 1.27 green`.

---

### Task 11: Slice 1.28, a check of the shop's knowledge lists a file it cannot read

**Slice plan entry:** Slice 1.28, capability, no unknown. Needs: the shop's check command, as far as listing what kb's check reports; slice 44 extends it. Scenario:

1. shop-knowledge / check-the-shops-knowledge-is-sound / The user checks a knowledge base holding a file the shop cannot read

**Files (shop-knowledge):**
- Modify: `src/shop_knowledge/cli.py` (the `validate` command, new `_validate`)
- Modify: `tests/test_check_the_shops_knowledge_is_sound.py`
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `InProcessClient.Validate`, `ValidateResponse(violations, faults)` (Task 3); `_refuse` (Task 7); `driver.start`, `record`, `refused_plainly`, `reported_failure`; the `env` and `shop` fixtures.
- Produces: `shop-knol validate`; the step `When the user checks the shop's knowledge` (gives `checked`), which slice 44 reuses.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1.28 2>&1 | tail -3
```

Expected: `1 failed`, a `StepDefinitionNotFoundError` for its Given.

- [ ] **Step 2: The steps**

Replace the whole of `/home/vscode/shopsystem-knowledge/tests/test_check_the_shops_knowledge_is_sound.py` with:

```python
from kb import canonical
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, refused_plainly, reported_failure, start

scenarios("check-the-shops-knowledge-is-sound.feature")

WEEKLY = "decision/price-reviews-happen-weekly"
MONTHLY = "decision/prices-are-reviewed-monthly"
SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly.\n"},
]


@given(
    "a shop knowledge base where someone edited a decision's file by hand and left it in a shape the shop cannot read"
)
def _shop_with_a_file_mangled_by_hand(env, shop, tmp_path):
    """Two decisions edited by hand: one left unreadable, one left readable but without the body of its purpose."""
    start(env, shop)
    record(env, tmp_path, "decision", {"title": "Price reviews happen weekly", "sections": SECTIONS}, "Record weekly")
    record(env, tmp_path, "decision", {"title": "Prices are reviewed monthly", "sections": SECTIONS}, "Record monthly")
    (shop / "kb" / f"{WEEKLY}.yaml").write_text("title: [a bracket opened by hand and never closed\n")
    monthly = shop / "kb" / f"{MONTHLY}.yaml"
    held = canonical.load(monthly.read_text())
    del held["sections"][0]["body"]
    monthly.write_text(canonical.dump(held))


@when("the user checks the shop's knowledge", target_fixture="checked")
def _check(env):
    return knol(env, "validate")


@then("that file is listed as a fault, naming the file")
def _unreadable_listed(checked):
    assert checked.stderr.splitlines()[0].startswith(f"{WEEKLY}: the stored file {WEEKLY}.yaml cannot be read: ")


@then("everything else the shop knows is checked and listed alongside it")
def _the_rest_listed(checked):
    assert checked.stderr.splitlines()[1:] == [f"{MONTHLY} at sections/0: 'body' is a required property"]


@then("the user is shown that fault in plain words, never a traceback")
def _shown_in_plain_words(checked):
    refused_plainly(checked)


@then("the command reports failure to whatever ran it")
def _reports_failure(checked):
    reported_failure(checked)
```

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1.28 2>&1 | grep -E "^E  |passed|failed" | head -3
```

Expected: the startswith assertion fails on `'usage: shop-knol [-h] {init,create,read} ...'`, and `1 failed`.

- [ ] **Step 3: shop-knol validate**

In `/home/vscode/shopsystem-knowledge/src/shop_knowledge/cli.py`, in `main`, replace

```python
    args = parser.parse_args(argv)
    return {"init": _init, "create": _create, "read": _read}[args.command](args)
```

with

```python
    commands.add_parser("validate", help="check everything the shop knows; lists every fault, exits non-zero if any")

    args = parser.parse_args(argv)
    return {"init": _init, "create": _create, "read": _read, "validate": _validate}[args.command](args)
```

and append at the end of the file:

```python


def _validate(args) -> int:
    response = _client().Validate(kb_pb2.ValidateRequest())
    return _refuse([*response.faults, *response.violations]) if response.faults or response.violations else 0
```

A check's violations are errors as kb returns them, so they are printed by the same function as a refusal.

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1.28 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
```

Expected: `1 passed`; `55 failed, 7 passed`; `73 failed, 45 passed`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-knowledge && git add src/shop_knowledge/cli.py tests/test_check_the_shops_knowledge_is_sound.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 1.28: shop-knol validate lists a file it cannot read beside every other fault

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 1.28's Status to `green`. Append at the very end of the log:

```
- <date> slice 1.28 green. Someone can now: check the shop's knowledge and see a file mangled by hand listed as a fault in plain words, beside every other fault, with a non-zero exit.
  Surprised by: <nothing, or what>.
  Open questions: <none, or what arose>.
  Next: the tag, kb 0.1 (the section after the last task of 2026-09-24-pretag3-implementation.md).
```

Commit the plan: `Slice 1.28 green`.

---

## After slice 1.28: tag kb 0.1, pin it, split the plans

Not a slice. Run the section "After slice 63: tag kb 0.1, pin it, split the plans" of `2026-09-24-pretag-implementation.md` now, in full, with the addition of `2026-09-24-pretag2-implementation.md`'s "After slice 70" section. The whole-branch review before the tag covers slices 1 and 1.1 to 1.28. The slice numbers in those two sections are the old ones: 54 to 70 are now 1.1 to 1.17 (the slice plan's log of 2026-09-24 gives the map). Three corrections to those sections, each checked in scratch:

- The walk-through's first line starts the shop in a directory it has not made, which kb refuses since slice 1.26, and shop-knol ignores the refusal (Review Focus 3). Make it first: `cd $(mktemp -d) && export KB_ACTOR=shopkeeper && mkdir shop && shop-knol init shop && …`. With that, the walk-through prints what it states.
- After the pin, `python -m pytest -q -m slice-1` gives `2 passed, 60 deselected`. Check the whole pre-tag set with `python -m pytest -q -m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28"`, which gives `7 passed, 55 deselected`.
- Its last step asks slicing to decide whether slice 50's unknown was spent. That is done: the re-plan of 2026-09-24 bundled it into slice 45.

Before tagging, in the same directory as those walk-throughs, also run:

```bash
printf 'title: Price reviews happen weekly\nsections:\n  - title: Purpose\n    body: Keep prices in step with costs.\n    body: Keep prices low.\n  - title: Rationale\n    body: Costs move weekly.\n' > twice.yaml && shop-knol create decision --from twice.yaml -m "Record it"; echo "exit=$?"
printf 'title: true\nsections:\n  - title: Purpose\n    body: a\n  - title: Rationale\n    body: b\n' > t.yaml && shop-knol create decision --from t.yaml -m "Record it"
echo 'title: [' > shop/kb/decision/true.yaml && shop-knol read decision/true; echo "exit=$?"; shop-knol validate; echo "exit=$?"
```

Expected:

```
twice.yaml at sections/0/body: an entry is named once and only once; 'body' is named again at line 5
exit=1
id: decision/true
revision: 1
decision/true: the stored file decision/true.yaml cannot be read: it is not YAML that can be read: expected the node content, but found '<stream end>' at line 2
exit=1
decision/true: the stored file decision/true.yaml cannot be read: it is not YAML that can be read: expected the node content, but found '<stream end>' at line 2
exit=1
```

This is the last batch before the tag. Every finding from here on, the whole-branch review's included, is placed by the slicing skill among slices 2 onward, never ahead of them.
