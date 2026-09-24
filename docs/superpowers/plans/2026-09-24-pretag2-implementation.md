# Pre-tag Implementation Plan, second cut: slices 64 to 70

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `2026-09-23-shop-knowledge-slices.md`; inside a task, follow `shopsystem-bdd:bdd-red-green` scenario by scenario. That skill's stop conditions, hand-back, and checkpoint apply and override any step here that would conflict with them.

**Goal:** The last things kb 0.1 writes or refuses are pinned before the tag: every piece of YAML kb and shop-knol read or write is YAML 1.2; one check of plain reading runs on content coming in and bytes going out; kb's section rules are a JSON Schema fragment composed with the type's schema; every request value is turned into a checked value where it enters kb; a client finds its store on each call; and a title in a user's file reaches kb as the text the user wrote.

**Architecture:** kb (`/home/vscode/shopsystem-kb`) is the Python package `kb`: a protobuf contract under `kb.contract`, a servicer over a `Store` (one canonical YAML file per artifact under `<root>/kb/`, itself a git repository), and an in-process client with the stub's method names. This plan swaps PyYAML for ruamel.yaml's pure-Python YAML 1.2 loader and emitter inside `kb.canonical`, which becomes the one place kb reads or writes YAML and the home of the one plain-reading check. It moves kb's section rules from hand-written code in `kb.validation` into a composed schema. It replaces `kb.locators` and the servicer's string joins with a new boundary module, `kb.values`, whose checked values are all `Store` accepts. And it makes `kb.client` find the store per call instead of once when the client is made. shop-knowledge (`/home/vscode/shopsystem-knowledge`) is the package `shop_knowledge`, whose `shop-knol` command calls kb through the in-process client. It drops PyYAML and reads and writes through `kb.content`.

**Provenance:** Every code block in this plan was put together in scratch copies of both repositories (`/tmp/pretag2/kb`, `/tmp/pretag2/shop`), with ruamel.yaml 0.19.1 installed to `/tmp/pretag2/site` and `PYTHONPATH=/tmp/pretag2/site:/tmp/pretag2/kb/src:/tmp/pretag2/shop/src` ahead of the editable installs, on 2026-09-24. Each task was applied in order and run. The red and green results and the suite counts stated below are what those runs gave, and the shell walk-through at the end printed what it states. The repositories themselves were not touched.

**Tech Stack:** Python 3.11, setuptools (src layout), protobuf + grpcio (generated code committed), python-jsonschema (Draft 2020-12), ruamel.yaml ≥ 0.18 (pure-Python safe loader and emitter, YAML 1.2), git via subprocess, pytest + pytest-bdd 8, argparse.

**Spec:** `/home/vscode/shopsystem-kb/docs/superpowers/specs/2026-09-23-kb-design.md` (Schema language, Serialization, The contract, Discovery and The client and the store, Input safety) and `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md` (The CLI). Slice plan: `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, slices 64 to 70. Feature files: `features/` in each repository. The scenarios of each slice carry `@slice-<n>`, so `python -m pytest -q -m slice-<n>` runs a slice.

## Global Constraints

- Feature files are read-only for the implementer. Only `slicing-into-increments` edits a tag line, and only `formulating-features` edits a Given, When, or Then. Any other diff under `features/` is a stop condition.
- Code only what a scenario asserts (bdd-red-green). Where the scenarios are silent, the code is silent, and the silence goes into the checkpoint entry as an open question. The decisions this plan makes are listed below, each tied to the spec line or scenario that asks for it.
- **Replace, never add beside.** Where the spec says a rule is a composed JSON Schema fragment, a single boundary conversion, or one checker, the task deletes the hand-written check it replaces. `kb.locators` is deleted in Task 4, `validation._section_faults` in Task 3, and the tag and document checks in `kb.content` in Task 2. No PyYAML import remains in kb after Task 1 or in shop-knowledge after Task 7.
- All YAML is 1.2: "All YAML kb reads or writes is YAML 1.2: content arriving over the contract, schema artifacts, files on disk, the journal, and the metaschema. No YAML 1.1 loader or emitter appears anywhere in kb." ruamel.yaml is used as `YAML(typ="safe", pure=True)`. Without `pure=True` it may pick the libyaml C loader, which is YAML 1.1.
- Content: "Content is parsed with a safe YAML 1.2 loader, so `yes`, `on`, and `1:20` are text, not a boolean or a number: no tags, no anchors, no aliases, no documents beyond the first. A section's `body` may be empty; it may not be absent. A section has exactly `title`, `body`, and `sections`; any other key is a violation."
- One checker: "The canonical-form check is one checker, run on content after it is parsed and on the bytes about to be written; a write whose own output fails it is refused, so nothing kb writes can differ from what kb accepts."
- Composed schema: "kb's own structural rules, the section tree with `title` and `body` required and nothing else allowed, part collections whose items carry an `id`, and the identity keys, are JSON Schema fragments that kb composes with the type's schema into one effective schema per artifact, checked by the standard validator in one pass."
- Boundary: "Every request is converted at the boundary into validated values, an id, a locator, a content tree, by one function per kind of value; storage accepts only those values and never a string that came from a request; one function derives a file path from a validated id, and nothing else touches paths."
- The client: "A client is constructed without finding a store. Discovery runs on each call, so a client whose working directory has moved into a different store uses the store it now sits in. `Init` takes its root on the request and skips discovery. Any other call that finds no store is refused with a fault, never an exception."
- Canonical form, unchanged from slice 54: "Every prose body is a literal block scalar, however short. Two-space indent, sequences indented under their key, no line folding at any width, no flow style, no comments, no anchors, no tags. The same tree always serializes to the same bytes."
- shop-knol: "Every file shop-knol reads or writes, on `create`, `write`, `append`, `apply`, and in its own output, is YAML 1.2, read and written the way kb reads content, so a title that looks like a date or a yes is still text when it reaches kb."
- Errors are a typed list of `{ artifact, path, rule, message }`. A response that carries faults is a refusal, and nothing was written.
- kb is exercised through its in-process transport, never mocked. kb ships no domain types.
- One user-site Python environment serves both checkouts. `make dev` in kb reinstalls it (`pip install -e '.[dev]'`) after a `pyproject.toml` change. `make dev` in shop-knowledge reinstalls both.
- Work on `main` in both repositories, not in a worktree: shop-knowledge imports kb from `/home/vscode/shopsystem-kb` as an editable install, and its step driver spawns `python -m shop_knowledge`, so a worktree would test the wrong code.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with the Co-Authored-By line of the model that made the commit, e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
- After every kb task, shop-knowledge's slice 1 must still pass: `cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1` → `2 passed`.
- The kb suite prints pytest-bdd `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.

## Decisions this plan makes (the spec left them open or silent)

1. **Which YAML 1.2 library.** ruamel.yaml, the one maintained YAML 1.2 implementation for Python, used as `typ="safe", pure=True`. Its safe representer, given the same representers kb has now (every `body` as a literal block, other strings plain unless multi-line, sequences indented with `indent(mapping=2, sequence=4, offset=2)`, width infinite), gives the same bytes PyYAML gave for every tree the suite writes. It writes 1.1-only values as plain text (`title: yes`, not `title: 'yes'`), which is right under 1.2. Pinned by slices 54, 58, 62 staying green and slice 64.
2. **ruamel's 1.2 resolver still reads a bare date as a date.** kb does not write its own resolver. Titles never hit this, because a title crosses the contract as a string field, and ruamel quotes any string that would resolve to something else (`title: '2026-09-24'`). shop-knol, reading a user's file, turns a non-text title back into text (decision 6). A date in a field value is Review Focus 3.
3. **What the one checker checks.** Plain reading: no tag, no anchor or alias, at most one document. It lives in `kb.canonical.check(text)` and runs from `kb.canonical.load` (content coming in, and every file kb reads back) and from `kb.canonical.dump` (every byte kb is about to write). A failed dump in Create is refused with rule `content`, the same rule as content that fails coming in. The emitter's `ignore_aliases` means kb never writes an alias itself. Pinned by slice 65 and slice 59's tag and document scenarios.
4. **What the composed fragment covers now.** The section tree only: an array of objects each requiring `title` and `body` (strings, `""` allowed), with an optional nested `sections`, and `additionalProperties: false`. It is composed as `allOf` beside the type's schema, with kb's shape under `$defs/kb-section`, so the type stays the root and its own `#` references still resolve. The "part items carry an `id`" fragment is not composed here, because kb mints item ids after validation, so incoming content never carries them. Nor are the identity-key fragments: content carrying an identity key is refused before validation (slice 55's `rule="identity"` messages, which name the key and the value back). Both belong to the first slice that validates a stored artifact (slices 10 and 42). Faults from the fragment carry the JSON Schema keyword as their rule, like any other schema fault. Slice 59's step for an extra key in a section is rewritten to match (Task 3, Step 2), and its Then line still holds: the fault names the extra entry.
5. **The boundary values.** `kb.values` holds `Kind`, `ArtifactId`, and `Locator` (frozen dataclasses), one conversion per kind of value (`kind`, `artifact_id`, `locator`, `named`), and `path(store_dir, ArtifactId)`, the one function that makes a file path, which raises `TypeError` for anything but an `ArtifactId`. `Store` takes only these values. A kind that is not plain is refused with rule `kind` before anything is looked up. The conversions raise `values.Refused(faults)`, and the servicer turns that into a response. Content keeps its one conversion, `kb.content.loads`. Pinned by slice 67 and slice 60 staying green.
6. **A title in a user's file.** shop-knol reads the file with `kb.content.loads`. If the title is not text (a date, a number, `true`), shop-knol makes it text with `str()`, and a missing or empty title becomes `""`, which kb refuses for want of a title. Pinned by slice 70. Other non-text titles are Review Focus 2.

## Review Focus

writing-plans asks that each line here get a test in the owning task. In this project tests are scenarios, and the feature files are the human gate, so no unit tests are added. Instead, each line goes into the owning task's checkpoint entry as a `QUESTION FOR THE SPEC`, with the reproduction given here.

1. **A plain kind that names no schema** (`CreateRequest(type="note")` in a store with no `schema/note`): the spec now says this is refused "as its own fault", but no scenario pins it, and Create raises `FileNotFoundError` through the client. Task 4 logs it.
2. **A title in a user's file that YAML 1.2 still reads as something other than text** (`title: true`, `title: 12`, `title: 2026-9-24`): shop-knol's `str()` gives `True`, `12`, and `2026-09-24`, not the text the user wrote. Task 7 logs it.
3. **A field value written as a bare date** (`reviewed: 2026-09-24` in content): ruamel loads a `datetime.date`, which is stored and written back unquoted. A type that declares the field a string refuses it with a `type` fault that the person did not expect. Task 1 logs it.
4. **A file in the store that no longer reads plainly** (a hand-edited `id: &a decision/t`): `canonical.load` now checks every file it reads, so `Read` raises `NotCanonical` through the client instead of answering with a fault. Task 2 logs it.
5. **Content that is not YAML, or not a mapping** (`title: [unclosed`, or `- a\n- b\n`): ruamel raises `ParserError`, or the servicer raises `TypeError` on `{**content}`, through the client. Task 2 logs it (the 2026-09-24 slice-59 question, now reproduced on ruamel).

---

### Task 1: Slice 64, every value is read and written as YAML 1.2

**Slice plan entry:** Slice 64, capability. Unknown: does a YAML 1.2 library, put in PyYAML's place everywhere kb reads or writes YAML, still give the canonical form of slices 54 and 62 byte for byte? Scenario:

1. kb / create-an-artifact / A value that reads as a switch or as a clock time is still the text that was written

**Files (kb):**
- Modify: `pyproject.toml` (`PyYAML>=6` → `ruamel.yaml>=0.18`)
- Modify: `src/kb/canonical.py` (everything above `def order`)
- Modify: `src/kb/content.py`
- Modify: `tests/test_create_an_artifact.py`, `tests/test_start_a_store.py` (read files with `kb.canonical.load`, not PyYAML)

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.canonical.order`, `IDENTITY`, `Prose` (slice 54); `tests/test_create_an_artifact.py:_raw(client, text)` (slice 59).
- Produces: `kb.canonical.dump(tree) -> str`, `kb.canonical.load(text)`, and `kb.canonical.events(text)` (the ruamel parse events, used by `kb.content.loads` until Task 2 replaces it). No module in kb imports `yaml` after this task.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-64 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: When "the client creates a decision carrying one field written "on" and another written "1:20", saying which role and why"`.

- [ ] **Step 2: The steps, and the steps' reading of files moved off PyYAML**

In `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`, delete the line `import yaml`, change `from kb import client as kb_client` to `from kb import canonical, client as kb_client`, and replace each of the three `yaml.safe_load(` calls with `canonical.load(`. Then append:

```python


@when(
    'the client creates a decision carrying one field written "on" and another written "1:20", saying which role and why',
    target_fixture="created",
)
def _create_with_values_yaml_1_1_would_convert(client):
    return _raw(client, (
        "switch: on\n"
        "time: 1:20\n"
        "sections:\n"
        "  - title: Purpose\n    body: Why.\n"
        "  - title: Rationale\n    body: Because.\n"
    ))


@then(
    "both fields read back as the text that was written, the first not as a yes or a no "
    "and the second not as a number"
)
def _both_fields_are_text(root, created):
    assert not created.faults, created.faults
    on_disk = canonical.load((root / "kb" / f"{created.id}.yaml").read_text())
    assert (on_disk["switch"], on_disk["time"]) == ("on", "1:20")
```

The content is sent as raw text through `_raw`, because `dumps` would quote the values. The file is read with kb's own loader, because after this task the file says `switch: on` bare, and a YAML 1.1 reader would make that `True` again.

In `/home/vscode/shopsystem-kb/tests/test_start_a_store.py`, delete `import yaml`, change `from kb import client as kb_client` to `from kb import canonical, client as kb_client`, and replace `yaml.safe_load(` with `canonical.load(`.

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-64 2>&1 | grep -E "^E +Assert|passed|failed"
```

Expected: `AssertionError: assert (True, 80) == ('on', '1:20')` and `1 failed`. `canonical.load` is still PyYAML here, and YAML 1.1 reads `on` as true and `1:20` as the base-60 number 80.

- [ ] **Step 3: ruamel.yaml in PyYAML's place**

In `/home/vscode/shopsystem-kb/pyproject.toml`, replace the dependency line `  "PyYAML>=6",` with `  "ruamel.yaml>=0.18",`. Then:

```bash
cd /home/vscode/shopsystem-kb && make dev 2>&1 | tail -1 && python -c "import ruamel.yaml; print(ruamel.yaml.__version__)"
```

In `/home/vscode/shopsystem-kb/src/kb/canonical.py`, replace everything above `def order(artifact: dict, schema: dict) -> dict:` with the block below. `order`, `_section` and `_item` stay as they are.

```python
"""Canonical YAML: the one serialization kb writes, and the one reading of YAML kb does. YAML 1.2 throughout.

kb is the only writer, so loading needs no round-trip preservation.
"""
import io

from ruamel.yaml import YAML
from ruamel.yaml.representer import SafeRepresenter

IDENTITY = ("id", "type", "schema_version", "revision", "title")


class Prose(str):
    """A prose body. Written as a literal block, however short."""


class _Representer(SafeRepresenter):
    def ignore_aliases(self, data):
        """A value used twice is written out twice, never as an anchor and an alias."""
        return True


def _represent_mapping(representer, mapping):
    """Every value under a `body` key is prose."""
    items = [
        (key, Prose(value) if key == "body" and isinstance(value, str) else value)
        for key, value in mapping.items()
    ]
    return representer.represent_mapping("tag:yaml.org,2002:map", items)


def _represent_prose(representer, value):
    return representer.represent_scalar("tag:yaml.org,2002:str", str(value), style="|")


def _represent_str(representer, value):
    style = "|" if "\n" in value else None
    return representer.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_Representer.add_representer(dict, _represent_mapping)
_Representer.add_representer(Prose, _represent_prose)
_Representer.add_representer(str, _represent_str)


def _yaml() -> YAML:
    """The pure-Python safe loader and emitter, YAML 1.2. Never the C one, which is YAML 1.1."""
    yaml = YAML(typ="safe", pure=True)
    yaml.Representer = _Representer
    yaml.default_flow_style = False
    yaml.allow_unicode = True
    yaml.width = float("inf")
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml


def dump(artifact: dict) -> str:
    """Block style, keys in the order given, prose as literal blocks, sequences indented under their key, no line folded."""
    stream = io.StringIO()
    _yaml().dump(artifact, stream)
    return stream.getvalue()


def load(text: str):
    return _yaml().load(text)


def events(text: str):
    """The YAML 1.2 parse of `text`, as events, for checks that look at how a value is written."""
    return _yaml().parse(text)


```

Replace the whole of `/home/vscode/shopsystem-kb/src/kb/content.py` with:

```python
"""Artifact content crossing the contract as canonical YAML text, read as YAML 1.2."""
from ruamel.yaml import events

from kb import canonical


class ContentFault(ValueError):
    """Content that cannot be read plainly. The message is the fault's."""


def dumps(value: dict) -> str:
    """Canonical text: block style, keys in the order given, prose as literal blocks."""
    return canonical.dump(value)


def loads(text: str) -> dict:
    """Read content plainly: no tags, exactly one document."""
    parsed = list(canonical.events(text))
    if any(getattr(event, "tag", None) is not None for event in parsed):
        raise ContentFault("content is read plainly as written and carries no tags")
    if sum(isinstance(event, events.DocumentStartEvent) for event in parsed) > 1:
        raise ContentFault("content holds exactly one document")
    return canonical.load(text) or {}
```

(This is the same check as before, now on ruamel's events. Task 2 replaces it with the one checker.)

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-64 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q -m "slice-1 or slice-54 or slice-55 or slice-56 or slice-57 or slice-58 or slice-59 or slice-60 or slice-61 or slice-62 or slice-63 or slice-64" 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
grep -rn --include='*.py' "import yaml\|from yaml" /home/vscode/shopsystem-kb/src /home/vscode/shopsystem-kb/tests
```

Expected: `1 passed`; `28 passed, 79 deselected`; `79 failed, 28 passed`; `2 passed`; and the grep prints nothing. Slices 54 and 62 staying green is the evidence the emitter gives the same bytes. If either goes red, the difference is in `_yaml()`'s settings, not in the representers. Look at the file text the Then prints before changing anything else.

For the checkpoint's evidence, print a file:

```bash
cd $(mktemp -d) && python - <<'EOF'
from kb import canonical
print(canonical.dump({"title": "yes", "time": "1:20", "date": "2026-09-24",
    "sections": [{"title": "Purpose", "body": ""}, {"title": "Rationale", "body": "trailing \n"}]}), end="")
EOF
```

Expected:

```
title: yes
time: 1:20
date: '2026-09-24'
sections:
  - title: Purpose
    body: |
  - title: Rationale
    body: |
      trailing 
```

The empty body and the body with a trailing space are literal blocks too, which PyYAML could not write. That answers slice 54's open question about such bodies. Paste the actual output, not this.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add pyproject.toml src/kb/canonical.py src/kb/content.py tests/test_create_an_artifact.py tests/test_start_a_store.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 64: every value is read and written as YAML 1.2

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 64's Status to `green`. Append at the very end of the slice plan's log (check with `tail`):

```
- <date> slice 64 green. Someone can now: create content with values YAML 1.1 would have turned into a yes or a number and read them back as the text written; every file kb writes or reads is YAML 1.2.
  Assumption "a YAML 1.2 library gives the canonical form byte for byte": <held | failed>. Evidence: <the output of Step 4's print, in full, and the 28 passed line>.
  Surprised by: <...>
  Open questions:
  - ANSWERED by the emitter: an empty body and a body with a trailing space are literal blocks (slice 54's question).
  - QUESTION FOR THE SPEC: a field value written as a bare date (`reviewed: 2026-09-24`) loads as a date under ruamel's YAML 1.2 resolver, is stored as one, and fails a type that declares the field a string. Is a date in content text, as a title is? No scenario pins it.
  Next: slice 65.
```

Commit the plan in shop-knowledge: `Slice 64 green`.

---

### Task 2: Slice 65, one check of the canonical form, on what comes in and what goes out

**Slice plan entry:** Slice 65, capability. Unknown: can the one check that refuses content after it is parsed also be run on the bytes kb is about to write, so that a write whose own output fails it is refused? Scenario:

1. kb / create-an-artifact / Content that writes a value once and points back at it elsewhere is refused

Needs: slice 59's tag and document refusals made by the same check, which replaces the one in `kb.content`.

**Files (kb):**
- Modify: `src/kb/canonical.py` (`check`, `NotCanonical`; `dump` and `load` call `check`; `events` removed)
- Modify: `src/kb/content.py` (the hand-written checks and `ContentFault` removed)
- Modify: `src/kb/servicer.py` (catch `canonical.NotCanonical` coming in and going out)
- Modify: `tests/test_create_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.canonical._yaml()` (Task 1).
- Produces: `kb.canonical.NotCanonical(ValueError)`; `kb.canonical.check(text: str) -> None`, which raises `NotCanonical` naming the first rule broken; `kb.canonical.dump` and `kb.canonical.load`, which both run it; `kb.content.loads(text) -> dict`, which raises `NotCanonical`. `kb.content.ContentFault` no longer exists.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-65 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError` for `When "the client creates a decision whose content writes a value once and points back at it from another place instead of writing it again, saying which role and why"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`:

```python


@when(
    "the client creates a decision whose content writes a value once and points back at it from another place "
    "instead of writing it again, saying which role and why",
    target_fixture="refused",
)
def _create_with_an_alias(client):
    return _raw(client, (
        "reviewed: &day Monday\n"
        "decided: *day\n"
        "sections:\n"
        "  - title: Purpose\n    body: Why.\n"
        "  - title: Rationale\n    body: Because.\n"
    ))


@then(
    "the artifact is rejected because content is read exactly as written and nothing in it stands in "
    "for a value written somewhere else"
)
def _rejected_for_an_alias(refused):
    assert (refused.id, refused.revision) == ("", 0)
    assert [(fault.rule, fault.message) for fault in refused.faults] == [
        ("content", "content is read exactly as written and nothing in it stands in for a value written somewhere else"),
    ]
```

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-65 2>&1 | grep -E "^E +Assert|passed|failed"
```

Expected: `AssertionError: assert ('decision/pr...en-weekly', 1) == ('', 0)`, `1 failed`. The alias is loaded, written out twice, and the create goes through.

- [ ] **Step 3: One checker, in and out**

In `/home/vscode/shopsystem-kb/src/kb/canonical.py`, change the import `from ruamel.yaml import YAML` to `from ruamel.yaml import YAML, events`. Then replace the three functions `dump`, `load`, and `events` (from `def dump(` down to just above `def order(`) with:

```python
class NotCanonical(ValueError):
    """YAML that is not read plainly as written. The message says which rule it breaks."""


def check(text: str) -> None:
    """The one check of plain reading, run on content as it arrives and on every file kb is about to write.

    No tags, no anchors or aliases, exactly one document. Raises NotCanonical naming the first rule broken.
    """
    parsed = list(_yaml().parse(text))
    if any(getattr(event, "tag", None) is not None for event in parsed):
        raise NotCanonical("content is read plainly as written and carries no tags")
    if any(getattr(event, "anchor", None) is not None for event in parsed):
        raise NotCanonical(
            "content is read exactly as written and nothing in it stands in for a value written somewhere else"
        )
    if sum(isinstance(event, events.DocumentStartEvent) for event in parsed) > 1:
        raise NotCanonical("content holds exactly one document")


def dump(artifact: dict) -> str:
    """Block style, keys in the order given, prose as literal blocks, sequences indented under their key, no line folded.

    The text is checked before it is handed back, so nothing kb writes can differ from what kb accepts.
    """
    stream = io.StringIO()
    _yaml().dump(artifact, stream)
    text = stream.getvalue()
    check(text)
    return text


def load(text: str):
    """Plain YAML 1.2: checked, then read."""
    check(text)
    return _yaml().load(text)


```

(An anchor always comes with an alias in content that means anything, and the parse gives both the anchor, on the value, and the alias as `AliasEvent.anchor`, so one test catches both.)

Replace the whole of `/home/vscode/shopsystem-kb/src/kb/content.py` with:

```python
"""Artifact content crossing the contract as canonical YAML text, read as YAML 1.2."""
from kb import canonical


def dumps(value: dict) -> str:
    """Canonical text: block style, keys in the order given, prose as literal blocks."""
    return canonical.dump(value)


def loads(text: str) -> dict:
    """Read content plainly, by the same check every file kb writes passes. Raises canonical.NotCanonical."""
    return canonical.load(text) or {}
```

In `/home/vscode/shopsystem-kb/src/kb/servicer.py`, change `from kb.content import ContentFault, loads, dumps` to `from kb.content import loads, dumps`, change `        except ContentFault as fault:` to `        except canonical.NotCanonical as fault:`, and replace

```python
        path = self._store.save(canonical.order(artifact, schema["schema"]))
        self._store.commit([path], request.actor.role, request.message)
```

with

```python
        try:
            path = self._store.save(canonical.order(artifact, schema["schema"]))
        except canonical.NotCanonical as fault:
            return kb_pb2.CreateResponse(faults=[kb_pb2.Fault(artifact=artifact_id, rule="content", message=str(fault))])
        self._store.commit([path], request.actor.role, request.message)
```

(`Store.save` calls `canonical.dump` before it writes the temporary file, so a refused dump leaves nothing on disk.)

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m "slice-65 or slice-59" 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
grep -rn "ContentFault\|yaml.scan\|TagToken" /home/vscode/shopsystem-kb/src /home/vscode/shopsystem-kb/tests
```

Expected: `9 passed, 98 deselected`; `78 failed, 29 passed`; `2 passed`; the grep prints nothing.

The outbound half has no scenario. For the checkpoint's evidence:

```bash
python -c "
from kb import canonical
x = ['a']; print(repr(canonical.dump({'a': x, 'b': x})))
try: canonical.dump({'a': b'hi'})
except canonical.NotCanonical as e: print('refused:', e)
"
```

Expected: `'a:\n  - a\nb:\n  - a\n'` (a shared value written twice, with no anchor) and `refused: content is read plainly as written and carries no tags` (bytes would be written with a `!!binary` tag, so the dump is refused).

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/canonical.py src/kb/content.py src/kb/servicer.py tests/test_create_an_artifact.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 65: one check of plain reading, on content in and bytes out

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 65's Status to `green`. Append at the very end of the log:

```
- <date> slice 65 green. Someone can now: send content that writes a value once and points back at it, and be refused; the same check refuses tags and second documents, and runs on every file kb writes and reads.
  Assumption "the one check that refuses content can run on kb's own output": <held | failed>. Evidence: <Step 4's print, in full>.
  Surprised by: <...>
  Open questions:
  - QUESTION FOR THE SPEC: a file in the store that no longer reads plainly (hand-edited to hold `&a`) now makes Read raise NotCanonical through the client, since load checks every file. Is it a fault on Read, or only a violation for Validate? No scenario pins it.
  - QUESTION FOR THE SPEC (still open from slice 59, now on ruamel): content that is not YAML (`title: [unclosed`) raises ParserError, and content that is not a mapping (`- a`) raises TypeError, through the client.
  Next: slice 66.
```

Commit the plan: `Slice 65 green`.

---

### Task 3: Slice 66, a section missing its title or its body does not fit its type

**Slice plan entry:** Slice 66, capability. Unknown: can kb's own structural rules be written as one schema fragment that the standard validator checks together with the type's schema in one pass? Scenarios:

1. kb / create-an-artifact / A section with no title is refused
2. kb / create-an-artifact / A section with no body is refused

Needs: slice 59's section rule checked by that fragment, in place of `_section_faults`.

**Files (kb):**
- Modify: `src/kb/validation.py` (whole file)
- Modify: `tests/test_create_an_artifact.py` (two Whens and a Then; slice 59's section Then rewritten)

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `tests/test_create_an_artifact.py:request`, `SECTIONS` (slice 1).
- Produces: `kb.validation.SECTION`, `STRUCTURE` (the fragment), `compose(schema: dict) -> dict`, and `validate(artifact_id: str, content: dict, schema: dict) -> list[kb_pb2.Fault]` (same signature as before). A section fault's `rule` is its JSON Schema keyword (`required`, `additionalProperties`, `type`) and its `path` is the section's own place (`sections/0`).

- [ ] **Step 1: Run them red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-66 2>&1 | tail -3
```

Expected: `2 failed`, each a `StepDefinitionNotFoundError` for its When.

- [ ] **Step 2: The steps, and slice 59's section Then as the composed schema reports it**

In `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`, replace

```python
def _rejected_for_an_extra_entry(refused):
    assert [(fault.path, fault.rule) for fault in refused.faults] == [("sections/0/author", "section")]
    assert "author" in refused.faults[0].message
```

with

```python
def _rejected_for_an_extra_entry(refused):
    assert [(fault.path, fault.rule) for fault in refused.faults] == [("sections/0", "additionalProperties")]
    assert "'author'" in refused.faults[0].message
```

That scenario's Then line ("a section holds exactly its title, its body and the sections inside it, and the extra entry is named") is unchanged and still asserted: one fault, at the section, naming `'author'`. Only the rule's name changes, from kb's own to the schema keyword, because the rule now lives in the schema (decision 4). This edit is to a step definition, not a feature file.

Append:

```python


@when(
    "the client creates a decision whose first section carries a body and no title, saying which role and why",
    target_fixture="refused",
)
def _create_with_a_section_without_a_title(client):
    return request(client, "decision", "Price reviews happen weekly", {
        "sections": [{"body": SECTIONS[0]["body"]}, SECTIONS[1]],
    }, message="Record it")


@when(
    "the client creates a decision whose purpose carries a title and no body, saying which role and why",
    target_fixture="refused",
)
def _create_with_a_section_without_a_body(client):
    return request(client, "decision", "Price reviews happen weekly", {
        "sections": [{"title": "Purpose"}, SECTIONS[1]],
    }, message="Record it")


@then(
    "the artifact is rejected because a section carries both a title and a body, and a section without one "
    "does not fit its type like anything else that does not"
)
def _rejected_for_a_section_missing_a_key(refused):
    assert (refused.id, refused.revision) == ("", 0)
    assert [(fault.path, fault.rule) for fault in refused.faults] == [("sections/0", "required")]
    assert "is a required property" in refused.faults[0].message
```

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m "slice-66 or slice-59" 2>&1 | grep -E "^E +(KeyError|At index)|passed|failed"
```

Expected: `KeyError: 'title'` and `KeyError: 'body'` (validation lets the section through and `canonical._section` falls over), slice 59's section scenario failing at `('sections/0/author', 'section') != ('sections/0', 'additionalProperties')`, and `3 failed, 7 passed`.

- [ ] **Step 3: The fragment, composed; the hand-written check gone**

Replace the whole of `/home/vscode/shopsystem-kb/src/kb/validation.py` with:

```python
"""Schema validation: the type's JSON Schema composed with kb's own structural rules, checked in one pass.

The other kb keywords (references, required sections in order, id uniqueness) are checked in code in later slices.
"""
from jsonschema import Draft202012Validator

from kb.contract import kb_pb2

SECTION = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "body": {"type": "string"},
        "sections": {"type": "array", "items": {"$ref": "#/$defs/kb-section"}},
    },
    "required": ["title", "body"],
    "additionalProperties": False,
}

STRUCTURE = {"properties": {"sections": {"type": "array", "items": {"$ref": "#/$defs/kb-section"}}}}


def compose(schema: dict) -> dict:
    """One effective schema: the type's, with kb's structural rules beside it under allOf.

    The type stays the root, so its own `#` references still resolve; kb's shapes sit under `$defs/kb-*`.
    """
    return {
        **schema,
        "allOf": [*schema.get("allOf", []), STRUCTURE],
        "$defs": {**schema.get("$defs", {}), "kb-section": SECTION},
    }


def validate(artifact_id: str, content: dict, schema: dict) -> list[kb_pb2.Fault]:
    """Every violation, as artifact, path, rule, message."""
    return [
        kb_pb2.Fault(
            artifact=artifact_id,
            path="/".join(str(step) for step in error.absolute_path),
            rule=error.validator,
            message=error.message,
        )
        for error in Draft202012Validator(compose(schema)).iter_errors(content)
    ]
```

- [ ] **Step 4: Run them green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m "slice-66 or slice-59" 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
grep -rn "_section_faults\|SECTION_KEYS" /home/vscode/shopsystem-kb/src
```

Expected: `10 passed, 97 deselected`; `76 failed, 31 passed`; `2 passed`; the grep prints nothing.

For the checkpoint's evidence:

```bash
python -c "
from kb import validation
print(validation.validate('d/x', {'title': 't', 'sections': [{'title': 'P', 'body': ''}]}, {'type': 'object'}))
print([(f.path, f.rule) for f in validation.validate('d/x', {'title': 't', 'sections': [{'title': 'P', 'body': 'b', 'sections': [{'title': 'Q'}]}]}, {'type': 'object'})])
print([(f.path, f.rule) for f in validation.validate('d/x', {'title': 't', 'sections': 'Purpose'}, {'type': 'object'})])
"
```

Expected: `[]` (an empty body fits), `[('sections/0/sections/0', 'required')]` (a nested section is held to the same rule), and `[('sections', 'type')]` (sections that are not a list are refused plainly, which answers slice 59's second open question).

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/validation.py tests/test_create_an_artifact.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 66: the section rules are a schema fragment composed with the type's

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 66's Status to `green`. Append at the very end of the log:

```
- <date> slice 66 green. Someone can now: create a decision with a section missing its title or its body and be refused the way any content that does not fit its type is; an empty body still fits.
  Assumption "kb's structural rules can be one fragment checked with the type's schema in one pass": <held | failed>. Evidence: <Step 4's print, in full>.
  Surprised by: <...>
  Open questions:
  - ANSWERED by the composed schema: `sections` that is not a list is refused as a `type` fault at `sections` (slice 59's question).
  - The part-item id and identity-key fragments are not composed yet: kb mints item ids after validation, and content carrying an identity key is refused before it. They arrive with the first slice that validates a stored artifact (slice 10 or 42).
  Next: slice 67.
```

Commit the plan: `Slice 66 green`.

---

### Task 4: Slice 67, a kind that is not a plain name is refused like any other input

**Slice plan entry:** Slice 67, capability. Unknown: can every value a request carries be turned into a checked value where it enters kb, so that storage is handed nothing else and no path is made from anything but a checked name? Scenario:

1. kb / create-an-artifact / A kind that is not a plain name is refused

Needs: slice 60's name and place checks made by the same conversion, in place of `kb.locators`.

**Files (kb):**
- Create: `src/kb/values.py`
- Delete: `src/kb/locators.py`
- Modify: `src/kb/store.py` (takes `ArtifactId` and `Kind` only; `slug` moves to `values`)
- Modify: `src/kb/servicer.py` (whole file)
- Modify: `tests/test_create_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.canonical.NotCanonical`, `load`, `dump` (Task 2); `kb.validation.validate` (Task 3); `kb.journal.write` (slice 57).
- Produces, in `kb.values`: `Refused(faults: list[kb_pb2.Fault])`; frozen dataclasses `Kind(name)`, `ArtifactId(kind: Kind, slug)` with `str()` → `"<kind>/<slug>"`, `Locator(id: ArtifactId, place: tuple[str, ...])`; `kind(text) -> Kind`, `artifact_id(text) -> ArtifactId`, `locator(pb: kb_pb2.Locator) -> Locator`, `named(kind: Kind, title: str) -> ArtifactId`, each raising `Refused`; `slug(title) -> str`; `path(store_dir: Path, artifact_id: ArtifactId) -> Path`. In `kb.store.Store`: `path(ArtifactId)`, `save(ArtifactId, artifact: dict)`, `holds(ArtifactId) -> bool`, `load(ArtifactId)`, `schema(Kind)`. `kb.store.slug` and `kb.locators` no longer exist.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-67 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError` for `When "the client creates an artifact of the kind "../schema/decision", with a title and both required sections, saying which role and why"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`:

```python


def _everything_under(directory):
    """Every file below a directory, with its bytes, so a step can tell whether anything was written."""
    return {path: path.read_bytes() for path in sorted(directory.rglob("*")) if path.is_file()}


@when(
    parsers.parse(
        'the client creates an artifact of the kind "{kind}", with a title and both required sections, '
        "saying which role and why"
    ),
    target_fixture="attempt",
)
def _create_of_a_kind(client, tmp_path, kind):
    before = _everything_under(tmp_path)
    response = request(client, kind, "Price reviews happen weekly", {"sections": SECTIONS}, message="Record it")
    return {"response": response, "before": before, "after": _everything_under(tmp_path)}


@then("the artifact is rejected because a kind is a plain name of lower-case letters, digits and single hyphens, never a path")
def _rejected_as_not_a_plain_kind(attempt):
    refused = attempt["response"]
    assert (refused.id, refused.revision) == ("", 0)
    assert [fault.rule for fault in refused.faults] == ["kind"]
    assert "never a path" in refused.faults[0].message
    assert "../schema/decision" in refused.faults[0].message


@then("nothing is looked up or written anywhere, inside the store or outside it")
def _nothing_written_anywhere(attempt):
    assert attempt["after"] == attempt["before"]
```

`tmp_path` holds the store's root and everything around it, so comparing every file beneath it, the store's git repository included, covers "inside the store or outside it".

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-67 2>&1 | grep -E "^E +subprocess|passed|failed" | cut -c1-160
```

Expected: `subprocess.CalledProcessError: Command '['git', '-C', '.../store/kb', 'add', '--', '../schema/decision/price-reviews-happen...` and `1 failed`. The kind is joined into a path, the schema is found at `kb/schema/../schema/decision.yaml`, the file is written outside `kb/`, and git refuses to add it.

- [ ] **Step 3: The boundary**

Create `/home/vscode/shopsystem-kb/src/kb/values.py`:

```python
"""The boundary: every value a request carries is turned here into a checked value, or refused with a fault.

Storage takes only these values, never a string that came from a request, and `path` is the one place a file
path is made from a name.
"""
import re
from dataclasses import dataclass
from pathlib import Path

from kb.contract import kb_pb2

PLAIN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class Refused(ValueError):
    """A request value that does not convert. Carries every fault found."""

    def __init__(self, faults: list[kb_pb2.Fault]):
        super().__init__(faults)
        self.faults = faults


@dataclass(frozen=True)
class Kind:
    name: str


@dataclass(frozen=True)
class ArtifactId:
    kind: Kind
    slug: str

    def __str__(self) -> str:
        return f"{self.kind.name}/{self.slug}"


@dataclass(frozen=True)
class Locator:
    id: ArtifactId
    place: tuple[str, ...]


def kind(text: str) -> Kind:
    if not PLAIN.fullmatch(text):
        raise Refused([kb_pb2.Fault(
            rule="kind",
            message=f"a kind is a plain name of lower-case letters, digits and single hyphens, never a path; {text!r} is not",
        )])
    return Kind(text)


def artifact_id(text: str) -> ArtifactId:
    kind_name, _, slug = text.partition("/")
    if not (PLAIN.fullmatch(kind_name) and PLAIN.fullmatch(slug)):
        raise Refused([_not_a_plain_name(text)])
    return ArtifactId(Kind(kind_name), slug)


def locator(request: kb_pb2.Locator) -> Locator:
    """A locator's name and its place, each checked; both faults when both fail."""
    faults = []
    try:
        converted = artifact_id(request.id)
    except Refused as refused:
        faults += refused.faults
    place = tuple(request.path.split("/")) if request.path else ()
    if not all(PLAIN.fullmatch(part) for part in place):
        faults.append(kb_pb2.Fault(
            artifact=request.id, path=request.path, rule="locator",
            message=f"a place inside an artifact is named by parts of the same plain alphabet, or a collection and an item in it; {request.path!r} is not",
        ))
    if faults:
        raise Refused(faults)
    return Locator(converted, place)


def named(kind: Kind, title: str) -> ArtifactId:
    """The name kb gives an artifact of this kind from its title. A title is required and must leave a name."""
    at = f"{kind.name}/{slug(title)}"
    if not title:
        raise Refused([kb_pb2.Fault(artifact=at, path="title", rule="title",
                                    message="an artifact cannot be created without a title")])
    if not slug(title):
        raise Refused([kb_pb2.Fault(artifact=at, path="title", rule="title",
                                    message=f"a title must leave something to make a name from; {title!r} leaves nothing")])
    return ArtifactId(kind, slug(title))


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def path(store_dir: Path, artifact_id: ArtifactId) -> Path:
    """The one function that makes a file path from a name."""
    if not isinstance(artifact_id, ArtifactId):
        raise TypeError(f"a path is made only from a checked name, not {artifact_id!r}")
    return store_dir / artifact_id.kind.name / f"{artifact_id.slug}.yaml"


def _not_a_plain_name(text: str) -> kb_pb2.Fault:
    return kb_pb2.Fault(
        artifact=text, rule="locator",
        message=f"a name is a kind and a plain name of lower-case letters, digits and single hyphens, never a path; {text!r} is not",
    )
```

The messages of `artifact_id` and `locator` are word for word those of `kb.locators`, so slice 60's Thens hold unchanged. Delete the old module:

```bash
cd /home/vscode/shopsystem-kb && git rm -q src/kb/locators.py
```

In `/home/vscode/shopsystem-kb/src/kb/store.py`:

- replace the imports `import os`, `import re`, `import subprocess`, `from pathlib import Path`, `from kb import canonical`, `from kb.contract import CONTRACT_VERSION` with

```python
import os
import subprocess
from pathlib import Path

from kb import canonical, values
from kb.contract import CONTRACT_VERSION
from kb.values import ArtifactId, Kind
```

- replace `path`:

```python
    def path(self, artifact_id: ArtifactId) -> Path:
        return values.path(self.dir, artifact_id)
```

- change `save`'s signature and first line to

```python
    def save(self, artifact_id: ArtifactId, artifact: dict) -> Path:
        """Serialize canonically to a temp file and rename into place."""
        path = self.path(artifact_id)
```

- replace `load` and `schema` with

```python
    def holds(self, artifact_id: ArtifactId) -> bool:
        return self.path(artifact_id).is_file()

    def load(self, artifact_id: ArtifactId) -> dict:
        return canonical.load(self.path(artifact_id).read_text())

    def schema(self, kind: Kind) -> dict:
        """The schema artifact of a kind; its JSON Schema is under `schema`."""
        return self.load(ArtifactId(Kind("schema"), kind.name))
```

- delete the module function `slug` (it now lives in `kb.values`).

Replace the whole of `/home/vscode/shopsystem-kb/src/kb/servicer.py` with:

```python
"""The contract's servicer: every rpc, over one store. Hosted in-process today; grpc.server can host it later.

Each rpc first turns what the request carries into checked values (kb.values); nothing past that point sees a
string that came from the request.
"""
from kb import canonical, journal, validation, values
from kb.content import loads, dumps
from kb.contract import kb_pb2, kb_pb2_grpc
from kb.metaschema import METASCHEMA
from kb.store import Store
from kb.values import ArtifactId, Kind

METASCHEMA_ID = ArtifactId(Kind("schema"), "schema")


class KbServicer(kb_pb2_grpc.KbServicer):
    def __init__(self, root):
        self._store = Store(root)

    def Init(self, request, context):
        if not request.actor.role:
            return kb_pb2.InitResponse(faults=[kb_pb2.Fault(
                rule="actor", message="a store can only be started under a role",
            )])
        store = Store(request.root)
        store.start()
        metaschema = {"id": str(METASCHEMA_ID), "type": "schema", "schema_version": 1, "revision": 1, **METASCHEMA}
        path = store.save(METASCHEMA_ID, canonical.order(metaschema, METASCHEMA["schema"]))
        entry = journal.write(
            store.dir, actor=request.actor, op="create", artifact=str(METASCHEMA_ID), path="",
            revision=1, schema_version=1, written=path, message="initialise store",
        )
        store.commit([store.dir / "store.yaml", path, entry], request.actor.role, "initialise store")
        return kb_pb2.InitResponse()

    def Create(self, request, context):
        try:
            kind = values.kind(request.type)
        except values.Refused as refused:
            return kb_pb2.CreateResponse(faults=refused.faults)
        at = f"{kind.name}/{values.slug(request.title)}"
        try:
            content = loads(request.content)
        except canonical.NotCanonical as fault:
            return kb_pb2.CreateResponse(faults=[kb_pb2.Fault(artifact=at, rule="content", message=str(fault))])
        faults = _identity_faults(at, content)
        try:
            artifact_id = values.named(kind, request.title)
        except values.Refused as refused:
            faults = refused.faults + faults
        if faults:
            return kb_pb2.CreateResponse(faults=faults)
        schema = self._store.schema(kind)
        faults = validation.validate(at, {"title": request.title, **content}, schema["schema"])
        if faults:
            return kb_pb2.CreateResponse(faults=faults)
        for collection in schema["schema"].get("parts", {}):
            for item in content.get(collection, []):
                item["id"] = values.slug(item["title"])
        artifact = {
            **content,
            "id": str(artifact_id), "type": kind.name,
            "schema_version": schema["version"], "revision": 1, "title": request.title,
        }
        try:
            path = self._store.save(artifact_id, canonical.order(artifact, schema["schema"]))
        except canonical.NotCanonical as fault:
            return kb_pb2.CreateResponse(faults=[kb_pb2.Fault(artifact=at, rule="content", message=str(fault))])
        self._store.commit([path], request.actor.role, request.message)
        return kb_pb2.CreateResponse(id=str(artifact_id), revision=1)

    def Read(self, request, context):
        try:
            locator = values.locator(request.locator)
        except values.Refused as refused:
            return kb_pb2.ReadResponse(faults=refused.faults)
        if not self._store.holds(locator.id):
            return kb_pb2.ReadResponse(faults=[kb_pb2.Fault(
                artifact=str(locator.id), rule="not-found",
                message=f"the store holds nothing by the name {str(locator.id)!r}",
            )])
        artifact = self._store.load(locator.id)
        schema = self._store.schema(locator.id.kind)["schema"]
        response = kb_pb2.ReadResponse(
            id=artifact["id"], type=artifact["type"],
            schema_version=artifact["schema_version"], revision=artifact["revision"],
            title=artifact["title"],
            content=dumps(_summary_fields(artifact, schema)),
        )
        for field in _reference_fields(schema):
            for target_id in _as_list(artifact.get(field)):
                response.references.append(self._stub(field, values.artifact_id(target_id)))
        for collection in schema.get("parts", {}):
            for item in artifact.get(collection, []):
                response.parts.append(kb_pb2.PartStub(collection=collection, id=item["id"], title=item["title"]))
        for (type_name, field), count in self._inbound(str(locator.id)).items():
            response.inbound.append(kb_pb2.InboundCount(type=type_name, field=field, count=count))
        return response

    def _stub(self, field, target_id: ArtifactId):
        target = self._store.load(target_id)
        schema = self._store.schema(target_id.kind)["schema"]
        return kb_pb2.Stub(
            field=field, id=target["id"], type=target["type"], title=target["title"],
            fields=dumps(_summary_fields(target, schema)),
        )

    def _inbound(self, artifact_id: str):
        """How many artifacts point at this one, by their type and the field they use."""
        counts = {}
        for other in self._store.artifacts():
            schema = self._store.schema(values.kind(other["type"]))["schema"]
            for field in _reference_fields(schema):
                if artifact_id in _as_list(other.get(field)):
                    key = (other["type"], field)
                    counts[key] = counts.get(key, 0) + 1
        return counts


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


def _summary_fields(artifact, schema):
    return {name: artifact[name] for name in schema.get("summary", []) if name in artifact}


def _reference_fields(schema):
    return [name for name, field in schema.get("properties", {}).items() if "ref" in field]


def _as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]
```

The order of Create's checks is the one slice 59 settled (decision 7 of the first pre-tag plan), with the kind ahead of everything: kind; then content read plainly; then the title and the identity keys together, title faults first; then the composed schema; then the write. `_title_faults` is gone, because `values.named` makes those faults.

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m "slice-67 or slice-60 or slice-59 or slice-55" 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
grep -rn "locators\|store import.*slug\|f\"{request\.\|f\"schema/{" /home/vscode/shopsystem-kb/src
```

Expected: `14 passed, 93 deselected`; `75 failed, 32 passed`; `2 passed`; the grep prints nothing.

For the checkpoint's evidence, and Review Focus 1:

```bash
python -c "
from pathlib import Path
from kb import values
try: values.path(Path('/s'), 'decision/x')
except TypeError as e: print('TypeError:', e)
print(values.path(Path('/s'), values.artifact_id('decision/x')))
"
```

Expected: `TypeError: a path is made only from a checked name, not 'decision/x'` and `/s/decision/x.yaml`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add -A src/kb tests/test_create_an_artifact.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 67: every request value is checked where it enters kb; a kind that is not plain is refused

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 67's Status to `green`. Append at the very end of the log:

```
- <date> slice 67 green. Someone can now: create an artifact of a kind that is not a plain name and be refused with nothing looked up or written; every name and place a request carries is checked in one module, and only a checked name makes a path.
  Assumption "every request value can become a checked value at the boundary, storage taking nothing else": <held | failed>. Evidence: <Step 4's print, and the grep's empty output>.
  Surprised by: <...>
  Open questions:
  - QUESTION FOR THE SPEC: the spec says Create refuses, as its own fault, a plain kind that names no schema; with no scenario, `CreateRequest(type="note")` in a store without `schema/note` still raises FileNotFoundError through the client.
  Next: slice 68.
```

Commit the plan: `Slice 67 green`.

---

### Task 5: Slice 68, a client readied before there was a store finds it once it is started

**Slice plan entry:** Slice 68, capability. Unknown: can finding the store move from when a client is readied to each call it makes, while starting a store still takes its directory from the request? Scenario:

1. kb / read-an-artifact / A client readied before there was a store finds the store started since

Needs: slice 61's refusals given on the call that finds no store, in place of a client readied over a refusal.

**Files (kb):**
- Modify: `src/kb/client.py` (whole file)
- Modify: `tests/test_read_an_artifact.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.discovery.locate(cwd, env) -> (root | None, Fault | None)` (slice 56/61); `KbServicer(root)` (Task 4).
- Produces: `kb.client.InProcessClient(root: Path | None = None)`; `kb.client.connect(root=None) -> InProcessClient`, which finds nothing when called; each call but `Init` finds its store as it is made; `Init` always serves `request.root`. The step `When the client reads the decision` now takes a `readied` fixture (default `None`).

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-68 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError` for `Given "the client was readied to call a store while working where there was none and nothing named one"`.

- [ ] **Step 2: The steps**

In `/home/vscode/shopsystem-kb/tests/test_read_an_artifact.py`:

- add `import pytest` as the first line;
- split the Background's body into a helper that any Given can start a store with, by replacing

```python
def _store_with_a_linked_decision(root):
    client = kb_client.connect(root)
```

with

```python
def _store_with_a_linked_decision(root):
    return _start_with_a_linked_decision(root)


def _start_with_a_linked_decision(root):
    """Start a store at root holding the decision, what it supersedes, and two work items pointing at it."""
    client = kb_client.connect(root)
```

- let the shared When use a client a scenario readied beforehand, by replacing

```python
@when("the client reads the decision", target_fixture="shown")
def _read_the_decision_from_here():
    return read(kb_client.connect(), DECISION)
```

with

```python
@pytest.fixture
def readied():
    """The client a scenario readied before it read, if one did; otherwise the read readies its own."""
    return None


@when("the client reads the decision", target_fixture="shown")
def _read_the_decision_from_here(readied):
    if readied is None:
        return read(kb_client.connect(), DECISION)
    readied["used"] = readied["client"]
    return read(readied["client"], DECISION)
```

- and append:

```python


@given(
    "the client was readied to call a store while working where there was none and nothing named one",
    target_fixture="readied",
)
def _readied_where_there_is_no_store(tmp_path, monkeypatch):
    here = tmp_path / "shop"
    here.mkdir()
    monkeypatch.chdir(here)
    monkeypatch.delenv("KB_ROOT", raising=False)
    return {"client": kb_client.connect(), "store_there": (here / "kb").exists(), "here": here}


@given("a store holding the decision has since been started where the client is working")
def _store_started_since(readied):
    _start_with_a_linked_decision(readied["here"])


@then("the client is given the decision")
def _given_the_decision(shown):
    assert not shown.faults, shown.faults
    assert (shown.id, shown.title) == (DECISION, "Price reviews happen weekly")


@then("the client was never readied again after the store appeared")
def _never_readied_again(readied):
    assert readied["store_there"] is False
    assert readied["used"] is readied["client"]
```

The Background's store at `root` stays where it is. The store this scenario reads from is a second one, started where the client works after the client was readied.

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-68 2>&1 | grep -E "^E +(message|AssertionError)|passed|failed" | head -3
```

Expected: `AssertionError: [rule: "store"` with `message: "no store was found, neither above .../shop nor named outright"`, `1 failed`. The client was built over the refusal it met when readied, and it keeps answering with it.

- [ ] **Step 3: Finding the store on each call**

Replace the whole of `/home/vscode/shopsystem-kb/src/kb/client.py` with:

```python
"""Transports. In-process: an object with the stub's method names that calls the servicer directly."""
import os
from pathlib import Path

from kb import discovery
from kb.contract import kb_pb2
from kb.servicer import KbServicer


class InProcessClient:
    """Same method names, requests and responses as kb_pb2_grpc.KbStub, with no channel between.

    Readied without finding a store. Each call but Init finds its store as it is made, from the root the client
    was given or, with none, the way git finds a repository; a call that finds none answers with that fault and
    touches nothing. Init takes its root from the request and finds nothing.
    """

    def __init__(self, root: Path | None = None):
        self._root = root

    def _servicer(self) -> tuple[KbServicer | None, kb_pb2.Fault | None]:
        if self._root is not None:
            return KbServicer(self._root), None
        root, refusal = discovery.locate(Path.cwd(), os.environ)
        if refusal is not None:
            return None, refusal
        return KbServicer(root), None

    def Init(self, request, timeout=None):
        return KbServicer(Path(request.root)).Init(request, None)

    def Create(self, request, timeout=None):
        servicer, refusal = self._servicer()
        if refusal is not None:
            return kb_pb2.CreateResponse(faults=[refusal])
        return servicer.Create(request, None)

    def Read(self, request, timeout=None):
        servicer, refusal = self._servicer()
        if refusal is not None:
            return kb_pb2.ReadResponse(faults=[refusal])
        return servicer.Read(request, None)


def connect(root=None) -> InProcessClient:
    """A client over the store at <root>/kb/, in this process; with no root, over whichever store each call finds."""
    return InProcessClient(Path(root) if root is not None else None)
```

`KbServicer(root)` only makes a `Store` object, which does no I/O until it is used, so making one per call costs nothing that matters.

- [ ] **Step 4: Run it green, and both suites**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m "slice-68 or slice-61 or slice-56" 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `6 passed, 101 deselected`; `74 failed, 33 passed`; `2 passed`.

For the checkpoint's evidence, the whole-branch review's `connect().Init` crash:

```bash
cd /tmp && python -c "
from kb import client
from kb.contract import kb_pb2
print(client.connect().Init(kb_pb2.InitRequest(root='/tmp/slice68-probe', actor=kb_pb2.Actor(role='x'))))
import os; print(os.path.exists('/tmp/slice68-probe/kb/store.yaml'))
" && rm -rf /tmp/slice68-probe
```

Expected: an empty line (an `InitResponse` with no faults) and `True`.

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add src/kb/client.py tests/test_read_an_artifact.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 68: a client finds its store on each call, not when it is readied

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 68's Status to `green`. Append at the very end of the log:

```
- <date> slice 68 green. Someone can now: ready a client where there is no store, start one there, and read from it with the same client; a client readied anywhere can start a store.
  Assumption "finding the store can move to each call, Init still taking its root from the request": <held | failed>. Evidence: <Step 4's print>.
  Surprised by: <...>
  Open questions:
  - ANSWERED: connect() with no store, then Init, no longer raises (the whole-branch review's question on slice 61).
  Next: slice 69.
```

Commit the plan: `Slice 68 green`.

---

### Task 6: Slice 69, a store is started where the client says, not where it works

**Slice plan entry:** Slice 69, capability, no unknown. Scenario:

1. kb / start-a-store / Where a store is started is settled by the directory named, not by where the client is working

**Files (kb):**
- Modify: `tests/test_start_a_store.py`

**Files (shop-knowledge):**
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.client.connect()` with no root, and `Init` serving `request.root` (Task 5); `tests/calls.py:CLIENT`.
- Produces: the Givens `the client is working inside a store` (fixture `working_in`) and `an empty directory elsewhere that sits inside no store` (fixture `root`).

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-69 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: Given "the client is working inside a store"`.

- [ ] **Step 2: The steps**

Append to `/home/vscode/shopsystem-kb/tests/test_start_a_store.py`:

```python


def _everything_under(directory):
    """Every file below a directory, with its bytes, the store's git repository included."""
    return {path: path.read_bytes() for path in sorted(directory.rglob("*")) if path.is_file()}


@given("the client is working inside a store", target_fixture="working_in")
def _working_inside_a_store(tmp_path, monkeypatch):
    working_in = tmp_path / "shop"
    working_in.mkdir()
    kb_client.connect(working_in).Init(kb_pb2.InitRequest(root=str(working_in), actor=CLIENT))
    monkeypatch.chdir(working_in)
    monkeypatch.delenv("KB_ROOT", raising=False)
    return {"root": working_in, "held": _everything_under(working_in)}


@given("an empty directory elsewhere that sits inside no store", target_fixture="root")
def _empty_directory_elsewhere(tmp_path):
    root = tmp_path / "elsewhere"
    root.mkdir()
    return root


@when("the client starts a store in that empty directory, saying which role it is", target_fixture="started")
def _start_a_store_in_the_named_directory(root):
    return kb_client.connect().Init(kb_pb2.InitRequest(root=str(root), actor=CLIENT))


@then("the store is made in the directory the client named")
def _made_where_named(started, root):
    assert not started.faults, started.faults
    assert (root / "kb" / "store.yaml").is_file()
    assert (root / "kb" / "schema" / "schema.yaml").is_file()


@then("the store the client was working in is left as it was")
def _working_store_unchanged(working_in):
    assert _everything_under(working_in["root"]) == working_in["held"]
```

The When readies its client with no root, from inside the store it works in, which is the case the scenario is about.

- [ ] **Step 3: Run it**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-69 2>&1 | tail -1
```

Expected: `1 passed`, with no production code in this task. `Init` has served `request.root` since slice 1, and since Task 5 it does so whether or not the client found a store. In the scratch run the scenario also passed on its steps with Task 5 left out. It failed for want of steps, not on a Then. That is not bdd-red-green's first stop condition (nothing passed before the steps existed), but the checkpoint says so plainly. If instead a Then fails, stop and hand back: the fix would be in `InProcessClient.Init`, and Task 5 said it takes its root from the request.

Then both suites:

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `73 failed, 34 passed`; `2 passed`.

- [ ] **Step 4: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add tests/test_start_a_store.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 69: a store is started where the client says, not where it works

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 5: Checkpoint**

Set slice 69's Status to `green`. Append at the very end of the log:

```
- <date> slice 69 green. Someone can now: start a store in a directory they name while working inside another store, and find the other store as it was.
  Surprised by: <nothing, or: the scenario went green on its step definitions, as the task predicted>.
  Open questions: <none, or what arose>. Next: slice 70.
```

Commit the plan: `Slice 69 green`.

---

### Task 7: Slice 70, a title in a user's file reaches kb as the text the user wrote

**Slice plan entry:** Slice 70, capability, no unknown. Scenarios:

1. shop-knowledge / record-a-decision / A title in a file that reads as a date is still a title
2. shop-knowledge / record-a-decision / A title in a file that reads as a yes is still a title

Needs: every file shop-knol reads, the shop's own type files included, and everything it prints, read and written through `kb.content`, in place of PyYAML.

**Files (shop-knowledge):**
- Modify: `pyproject.toml` (PyYAML dependency removed)
- Modify: `src/shop_knowledge/cli.py`
- Modify: `src/shop_knowledge/bootstrap.py`
- Modify: `tests/driver.py`, `tests/test_record_a_decision.py`, `tests/test_read_back_what_the_shop_knows.py`
- Modify: the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.content.loads(text) -> dict` and `kb.content.dumps(tree) -> str` (Tasks 1 and 2); the step `When the user records that file as a decision, saying who they are and why` (slice 1, fixture `decision_file`, gives `recorded`).
- Produces: `shop_knowledge.cli._text(title) -> str`; the Given `a decision in a file whose title is written "<title>"` (fixture `decision_file`); the Then `the name the decision was given is made from that text`. After this task, no module in shop-knowledge imports `yaml`.

- [ ] **Step 1: Run them red**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-70 2>&1 | tail -3
```

Expected: `2 failed`, each a `StepDefinitionNotFoundError` for `Given "a decision in a file whose title is written "..."`.

- [ ] **Step 2: The steps, and the tests' own YAML moved to kb's**

In `/home/vscode/shopsystem-knowledge/tests/driver.py`, delete `import yaml`, add `from kb.content import dumps, loads` after `import sys` (with a blank line between), replace `yaml.safe_dump(content, sort_keys=False, allow_unicode=True)` with `dumps(content)`, and replace `yaml.safe_load(` with `loads(`.

In `/home/vscode/shopsystem-knowledge/tests/test_read_back_what_the_shop_knows.py`, replace `import yaml` with `from kb.content import loads`, and replace `yaml.safe_load(` with `loads(`.

In `/home/vscode/shopsystem-knowledge/tests/test_record_a_decision.py`, replace the first two lines

```python
import yaml
from pytest_bdd import given, scenarios, then, when
```

with

```python
from kb.content import dumps, loads
from pytest_bdd import given, parsers, scenarios, then, when
```

replace `yaml.safe_dump(WEEKLY, sort_keys=False)` with `dumps(WEEKLY)`, replace each `yaml.safe_load(` with `loads(`, and append:

```python


@given(parsers.parse('a decision in a file whose title is written "{title}"'), target_fixture="decision_file")
def _decision_in_a_file_titled(tmp_path, title):
    """The title is written bare, as a person types it, so YAML is free to read it as something else."""
    path = tmp_path / "titled.yaml"
    path.write_text(
        f"title: {title}\n"
        "sections:\n"
        "  - title: Purpose\n    body: Keep prices in step with costs.\n"
        "  - title: Rationale\n    body: Costs move weekly.\n"
    )
    return path


def _title_read_back(env, recorded, decision_file):
    """The title as the shop reads it back under the name the decision was given, and the title as written."""
    assert recorded.returncode == 0, recorded.stderr
    result = knol(env, "read", loads(recorded.stdout)["id"])
    assert result.returncode == 0, result.stderr
    written = decision_file.read_text().splitlines()[0].removeprefix("title: ")
    return loads(result.stdout)["title"], written


@then("the shop reads the title back as the text that was written, not as a date")
def _title_is_text_not_a_date(env, recorded, decision_file):
    shown, written = _title_read_back(env, recorded, decision_file)
    assert shown == written == "2026-09-24"


@then("the shop reads the title back as the text that was written, not as a yes or a no")
def _title_is_text_not_a_bool(env, recorded, decision_file):
    shown, written = _title_read_back(env, recorded, decision_file)
    assert shown == written == "yes"


@then("the name the decision was given is made from that text")
def _name_from_that_text(recorded, decision_file):
    written = decision_file.read_text().splitlines()[0].removeprefix("title: ")
    assert loads(recorded.stdout)["id"] == f"decision/{written}"
```

The Thens take the written title from the file, because pytest-bdd does not give a parsed step argument to later steps as a fixture. The output is read with kb's loader: after this task, shop-knol prints `title: yes` bare.

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m slice-70 2>&1 | grep -E "TypeError|passed|failed" | head -3
```

Expected: `2 failed`. Each create exits non-zero with a traceback, because shop-knol's PyYAML reads the title as a `datetime.date` or `True`, and `CreateRequest(title=...)` raises `TypeError`.

- [ ] **Step 3: shop-knol on kb's reading and writing**

In `/home/vscode/shopsystem-knowledge/pyproject.toml`, delete the dependency line `  "PyYAML>=6",`.

In `/home/vscode/shopsystem-knowledge/src/shop_knowledge/cli.py`:

- make the module docstring

```python
"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting.

Every file it reads and everything it prints is YAML 1.2, read and written by kb's own reading and writing of content.
"""
```

- delete `import yaml`;
- replace `_show` with

```python
def _show(document: dict) -> None:
    print(dumps(document), end="")


def _text(title) -> str:
    """A title is text. YAML 1.2 still reads a bare date as a date, so a title that is not text is turned back into it."""
    if title is None:
        return ""
    return title if isinstance(title, str) else str(title)
```

- in `_create`, replace

```python
    content = yaml.safe_load(Path(args.source).read_text())
    title = content.pop("title", "")
```

with

```python
    content = loads(Path(args.source).read_text())
    title = _text(content.pop("title", None))
```

In `/home/vscode/shopsystem-knowledge/src/shop_knowledge/bootstrap.py`, replace `import yaml` and `from kb.content import dumps` with the one line `from kb.content import dumps, loads`, and replace `content = yaml.safe_load(text)` with `content = loads(text)`.

```bash
cd /home/vscode/shopsystem-knowledge && make dev 2>&1 | tail -1
```

- [ ] **Step 4: Run them green, and both suites**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -m "slice-70 or slice-1" 2>&1 | tail -1
cd /home/vscode/shopsystem-knowledge && python -m pytest -q 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -1
grep -rn --include='*.py' "import yaml\|from yaml" /home/vscode/shopsystem-knowledge/src /home/vscode/shopsystem-knowledge/tests; grep -n PyYAML /home/vscode/shopsystem-knowledge/pyproject.toml
```

Expected: `4 passed, 55 deselected`; `55 failed, 4 passed`; `73 failed, 34 passed`; both greps print nothing (the generated `*.egg-info` under `src/` may still name PyYAML until `make dev` rewrites it; it is not source).

- [ ] **Step 5: Commit**

```bash
cd /home/vscode/shopsystem-knowledge && git add pyproject.toml src/shop_knowledge/cli.py src/shop_knowledge/bootstrap.py tests/driver.py tests/test_record_a_decision.py tests/test_read_back_what_the_shop_knows.py && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -m "Slice 70: shop-knol reads and writes YAML 1.2 through kb, so a title stays the text written

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 6: Checkpoint**

Set slice 70's Status to `green`. Append at the very end of the log:

```
- <date> slice 70 green. Someone can now: record a decision from a file whose title is written 2026-09-24 or yes and read that title back as text, with the name made from it.
  Surprised by: <...>
  Open questions:
  - QUESTION FOR THE SPEC: a title in a file that YAML 1.2 still reads as something other than text (`title: true`, `title: 12`, `title: 2026-9-24`) reaches kb as `True`, `12`, `2026-09-24`, not as the text written. No scenario pins it.
  Next: tag kb 0.1, pin it here, then slicing moves the kb-only slices to kb's own plan.
```

Commit the plan: `Slice 70 green`.

---

## After slice 70: tag kb 0.1, pin it, split the plans

Not a slice. Run the section "After slice 63: tag kb 0.1, pin it, split the plans" of `2026-09-24-pretag-implementation.md` now, in full, instead of after slice 63: the slice plan's log entry of 2026-09-24 moved the tag behind slices 64 to 70. Its walk-through gives the same file as it states there, and the whole-branch review before the tag covers slices 1 and 54 to 70. One addition to that walk-through, run in the same directory before tagging:

```bash
printf 'title: yes\nsections:\n  - title: Purpose\n    body: Keep prices in step with costs.\n  - title: Rationale\n    body: Costs move weekly.\n' > yes.yaml && shop-knol create decision --from yes.yaml -m "Record it" && shop-knol read decision/yes && cat shop/kb/decision/yes.yaml
```

Expected: `id: decision/yes` and `revision: 1`; the read shows `title: yes` among `id`, `type`, `schema_version`, `revision`, then `references: []`, `parts: []`, `inbound: []`; and the file reads

```
id: decision/yes
type: decision
schema_version: 1
revision: 1
title: yes
sections:
  - title: Purpose
    body: |-
      Keep prices in step with costs.
  - title: Rationale
    body: |-
      Costs move weekly.
```
