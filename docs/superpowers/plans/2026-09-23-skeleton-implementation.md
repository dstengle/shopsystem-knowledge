# Walking Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `2026-09-23-shop-knowledge-slices.md`; inside a task, follow `shopsystem-bdd:bdd-red-green` scenario by scenario. That skill's stop conditions, hand-back, and checkpoint apply and override any step here that would conflict with them.

**Goal:** Both checkouts run their feature suites (slice 0), then a user at a shell starts a shop knowledge base, records a decision from a file, is shown the name kb minted for it, and reads it back at a glance, with the decision on disk as canonical YAML inside a git commit (slice 1).

**Architecture:** kb (`/home/vscode/shopsystem-kb`) is a Python package `kb` with a protobuf contract under `kb.contract`, a servicer that implements the rpcs over a `Store` (one YAML file per artifact under `<root>/kb/`, itself a git repository), and an in-process client with the stub's method names. shop-knowledge (`/home/vscode/shopsystem-knowledge`) is a Python package `shop_knowledge` whose `shop-knol` command builds contract messages, calls kb through the in-process client, and prints YAML. Until kb is tagged 0.1, shop-knowledge installs kb as an editable path dependency from the checkout beside it.

**Provenance:** Every code block in Task 2 was assembled in a scratch directory against copies of both repos' feature files on 2026-09-23 and run: the four kb scenarios and the two shop-knowledge scenarios of slice 1 pass, and the shell walk-through in Scenario 6 Step 6 gives the output stated there. The repos themselves were not touched.

**Tech Stack:** Python 3.11, setuptools (src layout), protobuf + grpcio (generated code committed; grpcio-tools only to regenerate), python-jsonschema (Draft 2020-12), PyYAML, git via subprocess, pytest + pytest-bdd 8, argparse.

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md` (this repo) and `/home/vscode/shopsystem-kb/docs/superpowers/specs/2026-09-23-kb-design.md`. Slice plan: `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`. Feature files: `features/` in each repo; the scenarios of slice 1 carry `@slice-1`.

## Global Constraints

- Feature files are read-only for the implementer. Only `slicing-into-increments` edits a tag line; only `formulating-features` edits a Given, When, or Then. Any diff under `features/` other than what those skills make is a stop condition.
- Code only what a scenario asserts (bdd-red-green). Where the scenarios are silent, the code is silent; the silence goes into the checkpoint entry as an open question. The one exception this plan makes is named in Task 2 (a refused write returns faults instead of writing) and is justified there.
- kb knows nothing about any domain: "It ships no schemas beyond the metaschema and no renderers." Domain types live in shop-knowledge only.
- kb is exercised through its in-process transport, never mocked (both specs' Testing sections).
- Git is canonical: "Every change goes through the API: validate, write, journal, serialize, commit. Nothing else edits the serialized text." The commit's author comes from the actor.
- Canonical form: "Identity keys first in the order above (`id`, `type`, `schema_version`, `revision`, `title`), then fields in schema order, then `sections`, then part collections in schema order. Prose bodies as literal block scalars. Two-space indent, no flow style, no comments, no anchors."
- Ids are minted by kb from titles: "`<type>/<slug>`, minted by kb from the title on create and never supplied by the client." Part item ids likewise, from the item's title.
- The store is `<root>/kb/`, marked by `<root>/kb/store.yaml`, which records the contract version.
- `shop-knol` finds the repository through `KB_ROOT` and the actor through `KB_ACTOR`; every mutating command requires an actor and `-m`. Output is YAML by default.
- Python `>=3.11`. One user-site Python environment serves both checkouts (the machine has no venv tooling; `pip install -e` lands in `~/.local`).
- Commits in both repos end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- The distribution name `shopsystem-knowledge` is already taken in this environment by an older, unrelated package (`knowledge/` in user site, script `shop-knowledge`). This repo's distribution is `shop-knowledge`, its package `shop_knowledge`, its script `shop-knol`. Do not uninstall the old package.

## Decisions this plan makes (the spec left them open or silent)

The kb spec lists "the exact protobuf message shapes" as Open. The slice plan's Needs lines leave composition and id minting to the implementer. These are the calls:

1. **Messages** are the ones in Task 2's `kb.proto`: `Init`, `Create`, `Read` (summary only; no `level` field until slice 20 needs it). Faults travel as `repeated Fault faults` on a response, so the in-process and network shapes are identical and a refusal is a response, not an exception.
2. **Everything is under `<root>/kb/`**: `store.yaml`, `schema/<type>.yaml`, `<type>/<slug>.yaml`. The spec's "Schemas at `<root>/schema/<type>.yaml`" predates the `kb/` subdirectory decision and is read as `<root>/kb/schema/`. Logged as a question.
3. **The git repository is `<root>/kb/` itself**, so "Nothing else in `<root>` is the store's concern" holds and a shell-bearing role can run in `<root>` "where the repository is not". Logged as a question.
4. **Bootstrap types are flat** (no `shop-artifact` base); slice 4 introduces composition. Slice 1 loads `tag`, `decision`, `work-item`; the other four arrive in slice 4.
5. **JSON numbers cross a Struct as doubles.** kb reads a whole-valued double back as an int (`version: 1`, not `1.0`). JSON Schema treats `1.0` as an integer, so validation agrees.
6. **Struct does not preserve key order.** A type's `properties` reach kb in whatever order the Struct yields, so "fields in schema order" is only as canonical as that, and the order of reference stubs in a summary follows it. This already shows in slice 1: the shop's decision type has `supersedes` and `tags`, and a dry run of this plan's code returned the `tags` stub first. The Then lines that say "a stub of each thing it points at" therefore compare as sets, which is what those lines say. Logged as a question for the spec: either the contract carries content as text (YAML or JSON, both ordered) or the schema states field order explicitly.
7. **`init` takes no `-m`**; its bootstrap creates use the `KB_ACTOR` role and the message `Define the shop's <type> type`. Slice 4 and 25 may revisit.
8. **The record-a-decision Given** ("a decision in a file, with … the decision it supersedes") first records the older decision through `shop-knol` so the file names something the shop holds, then writes the file. Reference targets are not checked in slice 1 (slice 24 pins that), but a summary read builds a stub of the target, so it must exist.

## Review Focus

writing-plans asks that each line here get a test in the owning task. In this project tests are scenarios and the feature files are the human gate, so no unit tests are added; each line instead names the later scenario that pins it, or says it is unpinned and must go into the slice-1 checkpoint's Open questions.

1. **A file with no `title`** (`shop-knol create decision --from f`): a person expects a refusal naming the artifact and the place; slice 1 raises `KeyError` in id minting. Pinned by slice 25 "A decision that does not fit the shop's decision type is refused" only if that scenario's file omits the title; otherwise unpinned. Log it.
2. **`shop-knol read` of an id the store does not hold**: a person expects "no such artifact" and a non-zero exit; slice 1 prints a `FileNotFoundError` traceback. No scenario pins it. Log it.
3. **Two artifacts with the same title**: a person expects the second to get `-2`; slice 1 overwrites the first file. Pinned by slice 24 "A second artifact with a title already used gets a name of its own" and slice 27.
4. **A part item without a `title`**: a person expects it named by position; slice 1 raises `KeyError`. Pinned by slice 38 "An item of a kind that carries no title is named by its place".
5. **`KB_ROOT` or `KB_ACTOR` unset**: a person expects to be told which one; slice 1 prints a `KeyError` traceback. `KB_ACTOR` pinned by slice 25 "A decision recorded by nobody is refused"; `KB_ROOT` unpinned. Log it.

---

### Task 1: Slice 0, both checkouts run their feature suites

**Slice plan entry:** Slice 0, enabling. Check: `python -m pytest -q` in `shopsystem-kb` -> 65 failed, every scenario collected and failing for want of steps; `python -m pytest -q` here -> 50 failed, the same; `python -c "import kb"` from this checkout succeeds with kb resolved from the sibling checkout; the protobuf compiler over kb's contract file exits 0 and the generated code imports.

**Files (kb, `/home/vscode/shopsystem-kb`):**
- Create: `pyproject.toml`, `.gitignore`, `Makefile`
- Create: `src/kb/__init__.py`, `src/kb/contract/__init__.py`, `src/kb/contract/kb.proto`
- Create (generated, committed): `src/kb/contract/kb_pb2.py`, `src/kb/contract/kb_pb2_grpc.py`, `src/kb/contract/kb_pb2.pyi`
- Create: `tests/conftest.py`, one `tests/test_<feature>.py` per feature file (15)
- Modify: `README.md` (a "Developing" section)

**Files (shop-knowledge, `/home/vscode/shopsystem-knowledge`):**
- Create: `pyproject.toml`, `.gitignore`, `Makefile`
- Create: `src/shop_knowledge/__init__.py`
- Create: `tests/conftest.py`, one `tests/test_<feature>.py` per feature file (14)
- Modify: `README.md`, `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md` (Status and Log only, per bdd-red-green's checkpoint)

**Interfaces:**
- Consumes: nothing.
- Produces: importable package `kb` with `kb.contract.CONTRACT_VERSION: str = "0.1"` and generated modules `kb.contract.kb_pb2`, `kb.contract.kb_pb2_grpc`; importable package `shop_knowledge`; `make contract` in kb regenerates the contract; `make dev` in either repo installs it editable; pytest in either repo collects every scenario, with `@slice-<n>` registered as marker `slice-<n>` so `python -m pytest -q -m slice-1` selects a slice.

- [ ] **Step 1: Run the check and see it fail for the right reason**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q
cd /home/vscode/shopsystem-knowledge && python -m pytest -q
python -c "import kb"
```

Expected: `no tests ran` twice, then `ModuleNotFoundError: No module named 'kb'`. If any of these already gives the slice's stated result, stop: that is bdd-red-green's second stop condition.

- [ ] **Step 2: kb packaging**

`/home/vscode/shopsystem-kb/pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "shopsystem-kb"
version = "0.1"
description = "A schema-typed, graph-oriented artifact store behind one versioned contract"
requires-python = ">=3.11"
dependencies = [
  "protobuf>=5",
  "grpcio>=1.60",
  "jsonschema>=4.18",
  "PyYAML>=6",
]

[project.optional-dependencies]
dev = [
  "pytest>=8",
  "pytest-bdd>=8",
  "grpcio-tools>=1.60",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
kb = ["contract/*.proto"]

[tool.pytest.ini_options]
testpaths = ["tests"]
bdd_features_base_dir = "features"
```

`/home/vscode/shopsystem-kb/.gitignore`:

```
__pycache__/
*.egg-info/
.pytest_cache/
build/
dist/
```

`/home/vscode/shopsystem-kb/Makefile` (recipe lines start with a tab):

```make
.PHONY: dev contract

dev:
	pip install -e '.[dev]'

contract:
	python -m grpc_tools.protoc -I src --python_out=src --grpc_python_out=src --pyi_out=src src/kb/contract/kb.proto
```

`/home/vscode/shopsystem-kb/src/kb/__init__.py`:

```python
"""kb: a schema-typed, graph-oriented artifact store behind one versioned contract."""
```

`/home/vscode/shopsystem-kb/src/kb/contract/__init__.py`:

```python
"""The contract: kb.proto and the code generated from it. Clients pin CONTRACT_VERSION."""

CONTRACT_VERSION = "0.1"
```

`/home/vscode/shopsystem-kb/src/kb/contract/kb.proto` (slice 0 proves the pipeline; slice 1 fills the service):

```proto
// kb contract, version 0.1. Regenerate with `make contract`.
syntax = "proto3";

package kb;

service Kb {}
```

Append to `/home/vscode/shopsystem-kb/README.md`:

```markdown

## Developing

Python 3.11. `make dev` installs kb editable with its test and build tools.
`make contract` regenerates `src/kb/contract/kb_pb2*.py` from `kb.proto`;
the generated files are committed. `python -m pytest -q` runs the feature
suite; `python -m pytest -q -m slice-1` runs one slice.
```

- [ ] **Step 3: Install kb editable and generate the contract**

```bash
cd /home/vscode/shopsystem-kb && make dev && make contract
ls src/kb/contract
python -c "from kb.contract import kb_pb2, kb_pb2_grpc, CONTRACT_VERSION; print(CONTRACT_VERSION, kb_pb2_grpc.KbServicer)"
```

Expected: `make contract` exits 0; the directory lists `kb_pb2.py`, `kb_pb2_grpc.py`, `kb_pb2.pyi`; the import prints `0.1 <class 'kb.contract.kb_pb2_grpc.KbServicer'>`. The generated grpc module imports `from kb.contract import kb_pb2 ...` because protoc ran with `-I src` and the proto sits inside the package. If pip refuses with "externally-managed-environment", add `--user` to the Makefile's pip line.

- [ ] **Step 4: kb test wiring, one module per feature, no steps**

`/home/vscode/shopsystem-kb/tests/conftest.py`:

```python
"""Suite wiring. Step definitions live beside the scenarios they serve; shared Givens are added here by slice 1."""
import re
from pathlib import Path


def pytest_configure(config):
    """Register every @slice-<n> tag in the feature files as a marker, so -m slice-<n> selects a slice."""
    tags = set()
    for feature in Path(config.rootpath, "features").glob("*.feature"):
        tags.update(re.findall(r"@(slice-\d+)", feature.read_text()))
    for tag in sorted(tags):
        config.addinivalue_line("markers", f"{tag}: scenario of that slice in the plan")
```

One module per feature file, holding only the binding:

```bash
cd /home/vscode/shopsystem-kb
for f in features/*.feature; do
  name=$(basename "$f" .feature)
  printf 'from pytest_bdd import scenarios\n\nscenarios("%s.feature")\n' "$name" > "tests/test_${name//-/_}.py"
done
ls tests
```

Expected: 15 `test_*.py` files plus `conftest.py`, e.g. `tests/test_start_a_store.py` containing:

```python
from pytest_bdd import scenarios

scenarios("start-a-store.feature")
```

- [ ] **Step 5: Run the kb check**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q 2>&1 | tail -3
python -m pytest -q --strict-markers 2>&1 | tail -1
python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `65 failed in …` with every failure a `StepDefinitionNotFoundError`; the same under `--strict-markers`; `4 failed, 61 deselected` for slice 1. Zero passed. If anything passes, stop (bdd-red-green stop condition). `PytestRemovedIn10Warning` lines come from pytest-bdd 8.1 under pytest 9 and are not ours.

- [ ] **Step 6: Commit kb**

```bash
cd /home/vscode/shopsystem-kb && git add -A && git status --short
git commit -m "Slice 0: package, contract pipeline, feature suite collected

setuptools src layout; kb.proto with an empty service generates and
imports; every scenario collected and failing for want of steps.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

Check `git status --short` before committing shows nothing under `.pytest_cache/` or `*.egg-info/`.

- [ ] **Step 7: shop-knowledge packaging**

`/home/vscode/shopsystem-knowledge/pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "shop-knowledge"
version = "0.1.0"
description = "The shop's interface to its knowledge base: types, seed content, renderers, and the shop-knol command line"
requires-python = ">=3.11"
dependencies = [
  "shopsystem-kb",
  "PyYAML>=6",
]

[project.optional-dependencies]
dev = [
  "pytest>=8",
  "pytest-bdd>=8",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
bdd_features_base_dir = "features"
```

`/home/vscode/shopsystem-knowledge/.gitignore`: same five lines as kb's.

`/home/vscode/shopsystem-knowledge/Makefile` (recipe line starts with a tab; pip resolves a relative editable path against the working directory, not a requirements file, which is why this is a make target run from the repo root):

```make
.PHONY: dev

KB ?= ../shopsystem-kb

dev:
	pip install -e $(KB) -e '.[dev]'
```

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/__init__.py`:

```python
"""shop-knowledge: the shop's only interface to its knowledge base, a client of kb."""
```

Replace `/home/vscode/shopsystem-knowledge/README.md` with:

```markdown
# shopsystem-knowledge

The shop's interface to its knowledge base: the artifact types, the seed
content, the renderers, and the `shop-knol` command line. A client of
[kb](https://github.com/dstengle/shopsystem-kb).

Design: `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`.

## Developing

Python 3.11, with `shopsystem-kb` checked out beside this repository.
`make dev` installs kb editable from that checkout and this package editable
(`KB=<path> make dev` if it lives elsewhere). `python -m pytest -q` runs the
feature suite; `python -m pytest -q -m slice-1` runs one slice.
```

- [ ] **Step 8: shop-knowledge test wiring**

`/home/vscode/shopsystem-knowledge/tests/conftest.py`: identical to kb's conftest from Step 4 (the same `pytest_configure`).

```bash
cd /home/vscode/shopsystem-knowledge
for f in features/*.feature; do
  name=$(basename "$f" .feature)
  printf 'from pytest_bdd import scenarios\n\nscenarios("%s.feature")\n' "$name" > "tests/test_${name//-/_}.py"
done
ls tests
```

Expected: 14 `test_*.py` files plus `conftest.py`.

- [ ] **Step 9: Install both editable from this checkout and run the check**

```bash
cd /home/vscode/shopsystem-knowledge && make dev
python -c "import kb, shop_knowledge; print(kb.__file__); print(shop_knowledge.__file__)"
pip show shopsystem-kb | grep -i -E '^(Location|Editable)'
python -m pytest -q 2>&1 | tail -3
python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: the two paths are `/home/vscode/shopsystem-kb/src/kb/__init__.py` and `/home/vscode/shopsystem-knowledge/src/shop_knowledge/__init__.py`; pip reports an editable project location under `shopsystem-kb`; `50 failed in …`, all `StepDefinitionNotFoundError`; `2 failed, 48 deselected`.

- [ ] **Step 10: Commit shop-knowledge, then the checkpoint**

```bash
cd /home/vscode/shopsystem-knowledge && git add -A && git status --short
git commit -m "Slice 0: package, kb as an editable path dependency, feature suite collected

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

Then follow bdd-red-green's checkpoint: in `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md` set slice 0's Status to `green` and append to its Log:

```
- 2026-09-23 slice 0 green. Someone can now: run the feature suite in either checkout and see every scenario collected and failing for want of steps, and import kb from this checkout as an editable path dependency of the sibling checkout. Surprised by: <what the run turned up | nothing>. Open questions: <none | list>. Next: slice 1.
```

```bash
git add docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md
git commit -m "Slice 0 green

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: Slice 1, record a decision and read it back

**Slice plan entry:** Slice 1, capability. Scenarios, in this order:

1. kb / start-a-store / The client starts a store
2. kb / define-a-type / The client defines a type
3. kb / create-an-artifact / The client creates an artifact
4. kb / read-an-artifact / The client reads a summary
5. shop-knowledge / record-a-decision / The user records a decision
6. shop-knowledge / read-back-what-the-shop-knows / The user reads a decision at a glance

Run the cycle per scenario: run it red, write only its steps, write the least code, run the suite, commit. Runs use `-k` with the scenario name in snake case, e.g. `-k the_client_starts_a_store`.

**Files (kb):**
- Modify: `src/kb/contract/kb.proto` (the slice's messages), regenerate `kb_pb2*.py`
- Create: `src/kb/content.py`, `src/kb/canonical.py`, `src/kb/metaschema.py`, `src/kb/validation.py`, `src/kb/store.py`, `src/kb/servicer.py`, `src/kb/client.py`
- Create: `tests/calls.py` (helpers and type definitions the steps share)
- Modify: `tests/conftest.py` (the shared `Given a store`), `tests/test_start_a_store.py`, `tests/test_define_a_type.py`, `tests/test_create_an_artifact.py`, `tests/test_read_an_artifact.py`

**Files (shop-knowledge):**
- Modify: `pyproject.toml` (the `shop-knol` script and type package data)
- Create: `src/shop_knowledge/__main__.py`, `src/shop_knowledge/cli.py`, `src/shop_knowledge/bootstrap.py`, `src/shop_knowledge/types/__init__.py`, `src/shop_knowledge/types/tag.yaml`, `src/shop_knowledge/types/decision.yaml`, `src/shop_knowledge/types/work-item.yaml`
- Create: `tests/driver.py`
- Modify: `tests/conftest.py`, `tests/test_record_a_decision.py`, `tests/test_read_back_what_the_shop_knows.py`, the slice plan (checkpoint)

**Interfaces:**
- Consumes: `kb.contract.CONTRACT_VERSION`, the generated `kb_pb2` / `kb_pb2_grpc` modules from Task 1.
- Produces (kb, used by shop-knowledge and by every later slice):
  - `kb.client.connect(root: str | Path) -> InProcessClient`; `InProcessClient.Init(request, timeout=None)`, `.Create(...)`, `.Read(...)`, same names and message types as `kb_pb2_grpc.KbStub`.
  - `kb.content.to_struct(value: dict) -> google.protobuf.struct_pb2.Struct`; `kb.content.from_struct(struct) -> dict` (whole-valued doubles become ints).
  - Messages: `Actor{role, execution}`, `Locator{id, path}`, `Fault{artifact, path, rule, message}`, `InitRequest{root}`, `InitResponse{}`, `CreateRequest{type, content, actor, message}`, `CreateResponse{id, revision, faults}`, `ReadRequest{locator}`, `ReadResponse{id, type, schema_version, revision, title, content, references, parts, inbound}`, `Stub{field, id, type, title, fields}`, `PartStub{collection, id, title}`, `InboundCount{type, field, count}`.
  - `kb.store.Store(root)` with `.dir`, `.path(id)`, `.start()`, `.save(artifact) -> Path`, `.load(id) -> dict`, `.schema(type) -> dict`, `.commit(paths, role, message)`, `.artifacts()`; `kb.store.slug(title) -> str`.
  - `kb.canonical.dump(artifact) -> str`, `.load(text) -> dict`, `.order(artifact, schema) -> dict`, `IDENTITY`.
  - `kb.validation.validate(artifact_id, content, schema) -> list[kb_pb2.Fault]`.
  - `kb.metaschema.METASCHEMA: dict` (the content of `schema/schema`).
- Produces (shop-knowledge): `shop_knowledge.cli.main(argv=None) -> int` behind `shop-knol` and `python -m shop_knowledge`; `shop_knowledge.bootstrap.TYPES` and `.load(client, actor)`; the type files under `shop_knowledge/types/`.

#### Scenario 1: kb / start-a-store / The client starts a store

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_starts_a_store 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: Given "an empty directory"`.

- [ ] **Step 2: The contract for the slice**

Replace `/home/vscode/shopsystem-kb/src/kb/contract/kb.proto` with the messages every scenario in this slice needs. The whole slice's contract is written once here because the contract is one file and a message is not behaviour; the servicer grows scenario by scenario.

```proto
// kb contract, version 0.1. Regenerate with `make contract`.
//
// Artifact content crosses as google.protobuf.Struct beside the fixed
// identity fields, since content shape is schema-defined at runtime.
// Errors are a typed list of faults on the response; a response that
// carries faults is a refusal and nothing was written.
syntax = "proto3";

package kb;

import "google/protobuf/struct.proto";

service Kb {
  rpc Init(InitRequest) returns (InitResponse);
  rpc Create(CreateRequest) returns (CreateResponse);
  rpc Read(ReadRequest) returns (ReadResponse);
}

message Actor {
  string role = 1;
  string execution = 2;
}

// An artifact root when path is empty; a node inside it otherwise.
message Locator {
  string id = 1;
  string path = 2;
}

message Fault {
  string artifact = 1;
  string path = 2;
  string rule = 3;
  string message = 4;
}

message InitRequest {
  string root = 1;
}

message InitResponse {}

message CreateRequest {
  string type = 1;
  google.protobuf.Struct content = 2;
  Actor actor = 3;
  string message = 4;
}

message CreateResponse {
  string id = 1;
  int32 revision = 2;
  repeated Fault faults = 3;
}

message ReadRequest {
  Locator locator = 1;
}

// A summary: identity, the fields the type shows at a glance, a stub of
// each reference target and of each part, and inbound counts.
message ReadResponse {
  string id = 1;
  string type = 2;
  int32 schema_version = 3;
  int32 revision = 4;
  string title = 5;
  google.protobuf.Struct content = 6;
  repeated Stub references = 7;
  repeated PartStub parts = 8;
  repeated InboundCount inbound = 9;
}

message Stub {
  string field = 1;
  string id = 2;
  string type = 3;
  string title = 4;
  google.protobuf.Struct fields = 5;
}

message PartStub {
  string collection = 1;
  string id = 2;
  string title = 3;
}

message InboundCount {
  string type = 1;
  string field = 2;
  int32 count = 3;
}
```

```bash
cd /home/vscode/shopsystem-kb && make contract && python -c "from kb.contract import kb_pb2; print(kb_pb2.ReadResponse.DESCRIPTOR.fields_by_name.keys())"
```

Expected: exits 0 and lists the nine field names.

- [ ] **Step 3: Step definitions for the scenario**

`/home/vscode/shopsystem-kb/tests/calls.py`, the client's side of the contract as the steps use it:

```python
"""How the steps call the contract: one helper per rpc, plus the types the Backgrounds define."""
from kb.content import to_struct
from kb.contract import kb_pb2

CLIENT = kb_pb2.Actor(role="client")

DECISION_TYPE = {
    "title": "Decision",
    "version": 1,
    "schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "supersedes": {
                "type": "string",
                "ref": {"targets": ["decision"], "cardinality": "one", "parts": False, "on_delete": "refuse"},
            },
        },
        "required": ["title"],
        "sections": [{"title": "Purpose"}, {"title": "Rationale"}],
        "parts": {
            "options": {
                "items": {
                    "type": "object",
                    "properties": {"title": {"type": "string"}, "body": {"type": "string"}},
                    "required": ["title"],
                }
            }
        },
        "summary": ["supersedes"],
    },
}

WORK_ITEM_TYPE = {
    "title": "Work item",
    "version": 1,
    "schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "decisions": {
                "type": "array",
                "items": {"type": "string"},
                "ref": {"targets": ["decision"], "cardinality": "many", "parts": False, "on_delete": "refuse"},
            },
        },
        "required": ["title"],
        "summary": ["decisions"],
    },
}


def define(client, type_content):
    """Define a type: a Create of type `schema`."""
    return client.Create(kb_pb2.CreateRequest(
        type="schema", content=to_struct(type_content), actor=CLIENT,
        message=f"Define {type_content['title']}",
    ))


def create(client, type_name, content, message="Create an artifact"):
    return client.Create(kb_pb2.CreateRequest(
        type=type_name, content=to_struct(content), actor=CLIENT, message=message,
    ))


def read(client, artifact_id):
    return client.Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=artifact_id)))
```

Replace `/home/vscode/shopsystem-kb/tests/test_start_a_store.py`:

```python
from pathlib import Path

from pytest_bdd import given, scenarios, then, when

from calls import create, define, read
from kb import client as kb_client
from kb.contract import kb_pb2

scenarios("start-a-store.feature")


@given("an empty directory", target_fixture="root")
def _empty_directory(tmp_path):
    root = tmp_path / "store"
    root.mkdir()
    return root


@when("the client starts a store there", target_fixture="client")
def _start_a_store(root):
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root)))
    return client


@then("the store holds the one type that describes what a type is")
def _holds_the_metaschema(client):
    schema = read(client, "schema/schema")
    assert schema.id == "schema/schema"
    assert schema.type == "schema"


@then("the store holds no other type and no content")
def _holds_nothing_else(root):
    store = root / "kb"
    files = sorted(p.relative_to(store) for p in store.rglob("*") if p.is_file() and ".git" not in p.parts)
    assert files == [Path("schema/schema.yaml"), Path("store.yaml")]


@then("the client can define its own types straight away")
def _can_define_a_type(client):
    defined = define(client, {
        "title": "Note",
        "version": 1,
        "schema": {"type": "object", "properties": {"title": {"type": "string"}}, "required": ["title"]},
    })
    assert defined.id == "schema/note"
    assert defined.revision == 1
```

The second Then looks at the disk because the contract has no List until slice 32; the store's "no other type and no content" is only observable there in this slice.

- [ ] **Step 4: Run it, red on the code now**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_starts_a_store 2>&1 | tail -3
```

Expected: `1 failed`, `ModuleNotFoundError: No module named 'kb.client'` (or `kb.content`, whichever import runs first).

- [ ] **Step 5: The least kb that starts a store, defines a type, and reads identity back**

`/home/vscode/shopsystem-kb/src/kb/content.py`:

```python
"""Artifact content crossing the contract as google.protobuf.Struct."""
from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Struct


def to_struct(value: dict) -> Struct:
    struct = Struct()
    struct.update(value)
    return struct


def from_struct(struct: Struct) -> dict:
    return _integral(MessageToDict(struct))


def _integral(value):
    """JSON numbers cross a Struct as doubles; a whole-valued double reads back as an int."""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, dict):
        return {key: _integral(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_integral(item) for item in value]
    return value
```

`/home/vscode/shopsystem-kb/src/kb/canonical.py`:

```python
"""Canonical YAML: the one serialization kb writes. kb is the only writer, so loading needs no round-trip preservation."""
import yaml

IDENTITY = ("id", "type", "schema_version", "revision", "title")


class _Dumper(yaml.SafeDumper):
    pass


def _represent_str(dumper, value):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_Dumper.add_representer(str, _represent_str)


def dump(artifact: dict) -> str:
    return yaml.dump(artifact, Dumper=_Dumper, sort_keys=False, default_flow_style=False, allow_unicode=True)


def load(text: str) -> dict:
    return yaml.safe_load(text)


def order(artifact: dict, schema: dict) -> dict:
    """Identity keys first, then fields in schema order, then anything else as given."""
    ordered = {key: artifact[key] for key in IDENTITY}
    for name in schema.get("properties", {}):
        if name in artifact and name not in ordered:
            ordered[name] = artifact[name]
    for name, value in artifact.items():
        if name not in ordered:
            ordered[name] = value
    return ordered
```

`/home/vscode/shopsystem-kb/src/kb/metaschema.py`:

```python
"""The one type a new store holds: the type that describes what a type is.

A schema artifact carries the type's human name as its title, an integer
version, and under `schema` a JSON Schema 2020-12 document plus the kb
keywords (`ref`, `parts`, `sections`, `summary`), which the JSON Schema
metaschema lets through as annotations.
"""

METASCHEMA = {
    "title": "Schema",
    "version": 1,
    "schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "version": {"type": "integer"},
            "schema": {"$ref": "https://json-schema.org/draft/2020-12/schema"},
        },
        "required": ["title", "version", "schema"],
    },
}
```

`/home/vscode/shopsystem-kb/src/kb/validation.py`:

```python
"""Schema validation: JSON Schema 2020-12 over an artifact's content. The kb keywords are checked in later slices."""
from jsonschema import Draft202012Validator

from kb.contract import kb_pb2


def validate(artifact_id: str, content: dict, schema: dict) -> list[kb_pb2.Fault]:
    """Every violation, as artifact, path, rule, message."""
    return [
        kb_pb2.Fault(
            artifact=artifact_id,
            path="/".join(str(step) for step in error.absolute_path),
            rule=error.validator,
            message=error.message,
        )
        for error in Draft202012Validator(schema).iter_errors(content)
    ]
```

`/home/vscode/shopsystem-kb/src/kb/store.py`:

```python
"""The store on disk: <root>/kb/, one canonical YAML file per artifact, itself a git repository."""
import re
import subprocess
from pathlib import Path

from kb import canonical
from kb.contract import CONTRACT_VERSION


class Store:
    def __init__(self, root):
        self.root = Path(root)
        self.dir = self.root / "kb"

    def path(self, artifact_id: str) -> Path:
        return self.dir / f"{artifact_id}.yaml"

    def start(self) -> None:
        """Make the store directory, its git repository, and its marker file."""
        self.dir.mkdir(parents=True)
        _git("init", "-q", "-b", "main", str(self.dir))
        (self.dir / "store.yaml").write_text(canonical.dump({"contract": CONTRACT_VERSION}))

    def save(self, artifact: dict) -> Path:
        """Serialize canonically to a temp file and rename into place."""
        path = self.path(artifact["id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(path.name + ".tmp")
        temp.write_text(canonical.dump(artifact))
        temp.replace(path)
        return path

    def load(self, artifact_id: str) -> dict:
        return canonical.load(self.path(artifact_id).read_text())

    def schema(self, type_name: str) -> dict:
        """The schema artifact of a type; its JSON Schema is under `schema`."""
        return self.load(f"schema/{type_name}")

    def commit(self, paths: list, role: str, message: str) -> None:
        """One commit of the given files, message from the request, author from the actor."""
        relative = [str(Path(path).relative_to(self.dir)) for path in paths]
        _git("-C", str(self.dir), "add", "--", *relative)
        _git(
            "-C", str(self.dir),
            "-c", f"user.name={role}", "-c", f"user.email={role}@kb", "-c", "commit.gpgsign=false",
            "commit", "-q", "-m", message,
        )


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _git(*args):
    subprocess.run(["git", *args], check=True, capture_output=True, text=True)
```

`/home/vscode/shopsystem-kb/src/kb/servicer.py`:

```python
"""The contract's servicer: every rpc, over one store. Hosted in-process today; grpc.server can host it later."""
from kb import canonical, validation
from kb.content import from_struct
from kb.contract import kb_pb2, kb_pb2_grpc
from kb.metaschema import METASCHEMA
from kb.store import Store, slug


class KbServicer(kb_pb2_grpc.KbServicer):
    def __init__(self, root):
        self._store = Store(root)

    def Init(self, request, context):
        store = Store(request.root)
        store.start()
        metaschema = {"id": "schema/schema", "type": "schema", "schema_version": 1, "revision": 1, **METASCHEMA}
        path = store.save(canonical.order(metaschema, METASCHEMA["schema"]))
        store.commit([store.dir / "store.yaml", path], "kb", "Start the store")
        return kb_pb2.InitResponse()

    def Create(self, request, context):
        content = from_struct(request.content)
        schema = self._store.schema(request.type)
        artifact_id = f"{request.type}/{slug(content['title'])}"
        faults = validation.validate(artifact_id, content, schema["schema"])
        if faults:
            return kb_pb2.CreateResponse(faults=faults)
        artifact = {
            "id": artifact_id, "type": request.type,
            "schema_version": schema["version"], "revision": 1,
            **content,
        }
        path = self._store.save(canonical.order(artifact, schema["schema"]))
        self._store.commit([path], request.actor.role, request.message)
        return kb_pb2.CreateResponse(id=artifact_id, revision=1)

    def Read(self, request, context):
        artifact = self._store.load(request.locator.id)
        return kb_pb2.ReadResponse(
            id=artifact["id"], type=artifact["type"],
            schema_version=artifact["schema_version"], revision=artifact["revision"],
            title=artifact["title"],
        )
```

The `if faults` branch is the one exception to "code only what a scenario asserts": the slice's Unknown names schema validation as a layer the round trip must pass through, and a validation that cannot refuse is not a layer. Slices 7, 24, 25 and 26 pin what a refusal looks like. In-process, `InitRequest.root` and the servicer's root coincide; the request carries it because the contract says Init takes a root path.

`/home/vscode/shopsystem-kb/src/kb/client.py`:

```python
"""Transports. In-process: an object with the stub's method names that calls the servicer directly."""
from pathlib import Path

from kb.servicer import KbServicer


class InProcessClient:
    """Same method names, requests and responses as kb_pb2_grpc.KbStub, with no channel between."""

    def __init__(self, servicer: KbServicer):
        self._servicer = servicer

    def Init(self, request, timeout=None):
        return self._servicer.Init(request, None)

    def Create(self, request, timeout=None):
        return self._servicer.Create(request, None)

    def Read(self, request, timeout=None):
        return self._servicer.Read(request, None)


def connect(root) -> InProcessClient:
    """A client over the store at <root>/kb/, in this process."""
    return InProcessClient(KbServicer(Path(root)))
```

- [ ] **Step 6: Run it green, then the suite**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_starts_a_store 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
cat /tmp/pytest-of-$USER/pytest-current/*/store/kb/schema/schema.yaml 2>/dev/null | head -8
```

Expected: `1 passed`; `1 passed, 64 failed`. The metaschema file starts `id: schema/schema`, `type: schema`, `schema_version: 1`, `revision: 1`, `title: Schema`, `version: 1`, `schema:`.

- [ ] **Step 7: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add -A && git commit -m "Slice 1: the client starts a store

Init makes <root>/kb/ as a git repository with store.yaml and the
metaschema; Create validates against the type's JSON Schema, mints the id
from the title, writes canonical YAML and commits as the actor; Read
returns identity. In-process client over the servicer.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

#### Scenario 2: kb / define-a-type / The client defines a type

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_defines_a_type 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: Given "a store"`.

- [ ] **Step 2: The shared Given and the scenario's steps**

Append to `/home/vscode/shopsystem-kb/tests/conftest.py` (keep the existing `pytest_configure`):

```python
import pytest
from pytest_bdd import given

from kb import client as kb_client
from kb.contract import kb_pb2


@pytest.fixture
def root(tmp_path):
    """The directory a store is started in; the store is its kb/ subdirectory."""
    root = tmp_path / "store"
    root.mkdir()
    return root


@given("a store", target_fixture="client")
def _a_store(root):
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root)))
    return client
```

Replace `/home/vscode/shopsystem-kb/tests/test_define_a_type.py`:

```python
from pytest_bdd import scenarios, then, when

from calls import create, define, read

scenarios("define-a-type.feature")

NOTE_TYPE = {
    "title": "Note",
    "version": 1,
    "schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "body": {"type": "string"},
            "relates_to": {
                "type": "string",
                "ref": {"targets": ["note"], "cardinality": "one", "parts": False, "on_delete": "refuse"},
            },
        },
        "required": ["title"],
        "sections": [{"title": "Context"}, {"title": "Outcome"}],
        "parts": {
            "attachments": {
                "items": {
                    "type": "object",
                    "properties": {"title": {"type": "string"}, "url": {"type": "string"}},
                    "required": ["title"],
                }
            }
        },
        "summary": ["relates_to"],
    },
}


@when(
    "the client defines a type whose artifacts carry a title, a body, a link to another artifact "
    "of the same type, two required sections in order, and a collection of parts",
    target_fixture="defined",
)
def _define_note(client):
    return define(client, NOTE_TYPE)


@then("the type is an artifact the client can read back like any other")
def _read_back_like_any_other(client, defined):
    assert defined.id == "schema/note"
    note_type = read(client, defined.id)
    assert (note_type.id, note_type.type, note_type.title) == ("schema/note", "schema", "Note")
    assert note_type.revision == 1


@then("artifacts of that type can be created")
def _create_a_note(client):
    note = create(client, "note", {
        "title": "First note",
        "body": "A note to start with.\n",
        "sections": [
            {"title": "Context", "body": "Why the note exists.\n"},
            {"title": "Outcome", "body": "What came of it.\n"},
        ],
        "attachments": [{"title": "Sketch", "url": "https://example.test/sketch"}],
    })
    assert note.id == "note/first-note"
    assert note.revision == 1
```

- [ ] **Step 3: Run it, then the suite**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_defines_a_type 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
```

Expected: `1 passed`; `2 passed, 63 failed`. No production change is expected: scenario 1's code already defines a type and creates an artifact of it. This is not a stop condition, because the scenario failed for want of steps before its steps were written and passes only with them.

- [ ] **Step 4: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add -A && git commit -m "Slice 1: the client defines a type

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

#### Scenario 3: kb / create-an-artifact / The client creates an artifact

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_creates_an_artifact 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError` for the Background Given `"a store holding a decision type whose artifacts require a purpose then a rationale, may link to the decision they supersede, and may carry a collection of options"`.

- [ ] **Step 2: Steps**

Replace `/home/vscode/shopsystem-kb/tests/test_create_an_artifact.py`:

```python
import yaml
from pytest_bdd import given, scenarios, then, when

from calls import DECISION_TYPE, create, define, read
from kb import client as kb_client
from kb.contract import kb_pb2

scenarios("create-an-artifact.feature")

SECTIONS = [
    {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
    {"title": "Rationale", "body": "Costs move weekly, so a monthly review lags them.\n"},
]
OPTIONS = [
    {"title": "Keep weekly", "body": "Review every Monday."},
    {"title": "Go monthly", "body": "Review on the first of the month."},
]


@given(
    "a store holding a decision type whose artifacts require a purpose then a rationale, "
    "may link to the decision they supersede, and may carry a collection of options",
    target_fixture="client",
)
def _store_with_decision_type(root):
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root)))
    define(client, DECISION_TYPE)
    return client


@when(
    "the client creates a decision with a title, both required sections and two options, saying which role and why",
    target_fixture="created",
)
def _create_decision(client):
    return create(client, "decision", {
        "title": "Price reviews happen weekly",
        "sections": SECTIONS,
        "options": OPTIONS,
    }, message="Move price reviews to weekly")


@then("the client is given the name the artifact keeps for life and its first version")
def _given_name_and_first_version(created):
    assert created.id == "decision/price-reviews-happen-weekly"
    assert created.revision == 1


@then("the artifact records the version of the type it was checked against")
def _records_schema_version(client, created):
    assert read(client, created.id).schema_version == 1


@then("reading it back gives what was written, in the order the type declares")
def _read_back_in_declared_order(root, client, created):
    stubs = read(client, created.id).parts
    assert [(stub.collection, stub.id, stub.title) for stub in stubs] == [
        ("options", "keep-weekly", "Keep weekly"),
        ("options", "go-monthly", "Go monthly"),
    ]
    on_disk = yaml.safe_load((root / "kb" / "decision" / "price-reviews-happen-weekly.yaml").read_text())
    assert list(on_disk) == ["id", "type", "schema_version", "revision", "title", "sections", "options"]
    assert on_disk["sections"] == SECTIONS
    assert on_disk["options"] == [
        {"id": "keep-weekly", **OPTIONS[0]},
        {"id": "go-monthly", **OPTIONS[1]},
    ]
```

The last Then reads the file on disk for the order and the sections: a whole read arrives in slice 20, and the order the type declares is only observable in the canonical file until then. Part stubs come through the contract.

- [ ] **Step 3: Run it, red on the code**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_creates_an_artifact 2>&1 | grep -E "^E|passed|failed" | head -5
```

Expected: `1 failed`, an `AssertionError` on the part stubs (`[] == [...]`), since Read returns no parts yet.

- [ ] **Step 4: Mint part ids; order sections and parts canonically; return part stubs**

In `/home/vscode/shopsystem-kb/src/kb/canonical.py`, replace `order` and add the two helpers below it:

```python
def order(artifact: dict, schema: dict) -> dict:
    """Identity keys first, then fields in schema order, then sections, then part collections in schema order."""
    parts = schema.get("parts", {})
    ordered = {key: artifact[key] for key in IDENTITY}
    for name in schema.get("properties", {}):
        if name in artifact and name not in ordered:
            ordered[name] = artifact[name]
    for name, value in artifact.items():
        if name not in ordered and name != "sections" and name not in parts:
            ordered[name] = value
    if "sections" in artifact:
        ordered["sections"] = [_section(section) for section in artifact["sections"]]
    for name in parts:
        if name in artifact:
            ordered[name] = [_item(item, parts[name]["items"]) for item in artifact[name]]
    return ordered


def _section(section: dict) -> dict:
    ordered = {"title": section["title"], "body": section["body"]}
    if "sections" in section:
        ordered["sections"] = [_section(child) for child in section["sections"]]
    return ordered


def _item(item: dict, item_schema: dict) -> dict:
    """An item's id first, then its fields in the item schema's order."""
    ordered = {"id": item["id"]}
    for name in item_schema.get("properties", {}):
        if name in item and name not in ordered:
            ordered[name] = item[name]
    for name, value in item.items():
        if name not in ordered:
            ordered[name] = value
    return ordered
```

In `/home/vscode/shopsystem-kb/src/kb/servicer.py`, in `Create`, between the `if faults:` return and the `artifact = {` line, mint the item ids:

```python
        for collection in schema["schema"].get("parts", {}):
            for item in content.get(collection, []):
                item["id"] = slug(item["title"])
```

and replace `Read` with:

```python
    def Read(self, request, context):
        artifact = self._store.load(request.locator.id)
        schema = self._store.schema(artifact["type"])["schema"]
        response = kb_pb2.ReadResponse(
            id=artifact["id"], type=artifact["type"],
            schema_version=artifact["schema_version"], revision=artifact["revision"],
            title=artifact["title"],
        )
        for collection in schema.get("parts", {}):
            for item in artifact.get(collection, []):
                response.parts.append(kb_pb2.PartStub(collection=collection, id=item["id"], title=item["title"]))
        return response
```

- [ ] **Step 5: Run it green, then the suite**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_creates_an_artifact 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
```

Expected: `1 passed`; `3 passed, 62 failed`.

- [ ] **Step 6: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add -A && git commit -m "Slice 1: the client creates an artifact

Part item ids minted from titles; canonical order puts sections after
fields and part collections last, item ids first; summary read lists parts.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

#### Scenario 4: kb / read-an-artifact / The client reads a summary

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_reads_a_summary 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError` for the Background Given `"a store holding a decision that supersedes an older decision, has a purpose and a rationale, carries two options, and is pointed at by two work items"`.

- [ ] **Step 2: Steps**

Replace `/home/vscode/shopsystem-kb/tests/test_read_an_artifact.py`:

```python
from pytest_bdd import given, scenarios, then, when

from calls import DECISION_TYPE, WORK_ITEM_TYPE, create, define, read
from kb import client as kb_client
from kb.content import from_struct
from kb.contract import kb_pb2

scenarios("read-an-artifact.feature")

OLDER = "decision/prices-are-reviewed-monthly"
DECISION = "decision/price-reviews-happen-weekly"


@given(
    "a store holding a decision that supersedes an older decision, has a purpose and a rationale, "
    "carries two options, and is pointed at by two work items",
    target_fixture="client",
)
def _store_with_a_linked_decision(root):
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root)))
    define(client, DECISION_TYPE)
    define(client, WORK_ITEM_TYPE)
    create(client, "decision", {
        "title": "Prices are reviewed monthly",
        "sections": [
            {"title": "Purpose", "body": "Keep prices current.\n"},
            {"title": "Rationale", "body": "Monthly was enough once.\n"},
        ],
    })
    create(client, "decision", {
        "title": "Price reviews happen weekly",
        "supersedes": OLDER,
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
        "options": [
            {"title": "Keep weekly", "body": "Review every Monday."},
            {"title": "Go monthly", "body": "Review on the first of the month."},
        ],
    })
    create(client, "work-item", {"title": "Move the review to Mondays", "decisions": [DECISION]})
    create(client, "work-item", {"title": "Tell the pricing team", "decisions": [DECISION]})
    return client


@when("the client reads the decision at a glance", target_fixture="summary")
def _read_at_a_glance(client):
    return read(client, DECISION)


@then("the client is given its name, its kind, its title and the few fields the type shows at a glance")
def _identity_and_summary_fields(summary):
    assert (summary.id, summary.type, summary.title) == (DECISION, "decision", "Price reviews happen weekly")
    assert from_struct(summary.content) == {"supersedes": OLDER}


@then("a stub of each thing it points at and of each of its parts")
def _stubs(summary):
    assert {(stub.field, stub.id, stub.type, stub.title) for stub in summary.references} == {
        ("supersedes", OLDER, "decision", "Prices are reviewed monthly"),
    }
    assert [(stub.collection, stub.id, stub.title) for stub in summary.parts] == [
        ("options", "keep-weekly", "Keep weekly"),
        ("options", "go-monthly", "Go monthly"),
    ]


@then("how many things point at it, counted by their kind and by the link they use")
def _inbound_counts(summary):
    assert [(count.type, count.field, count.count) for count in summary.inbound] == [
        ("work-item", "decisions", 2),
    ]
```

- [ ] **Step 3: Run it, red on the code**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_reads_a_summary 2>&1 | grep -E "^E|passed|failed" | head -5
```

Expected: `1 failed`, `AssertionError` on the summary fields (`{} == {'supersedes': ...}`).

- [ ] **Step 4: Summary fields, reference stubs, inbound counts**

Add to `/home/vscode/shopsystem-kb/src/kb/store.py`, inside `Store`:

```python
    def artifacts(self):
        """Every artifact in the store, schemas included, in path order."""
        for path in sorted(self.dir.glob("*/*.yaml")):
            yield canonical.load(path.read_text())
```

In `/home/vscode/shopsystem-kb/src/kb/servicer.py`, change the content import to `from kb.content import from_struct, to_struct`, replace `Read`, and add the helpers:

```python
    def Read(self, request, context):
        artifact = self._store.load(request.locator.id)
        schema = self._store.schema(artifact["type"])["schema"]
        response = kb_pb2.ReadResponse(
            id=artifact["id"], type=artifact["type"],
            schema_version=artifact["schema_version"], revision=artifact["revision"],
            title=artifact["title"],
            content=to_struct(_summary_fields(artifact, schema)),
        )
        for field in _reference_fields(schema):
            for target_id in _as_list(artifact.get(field)):
                response.references.append(self._stub(field, target_id))
        for collection in schema.get("parts", {}):
            for item in artifact.get(collection, []):
                response.parts.append(kb_pb2.PartStub(collection=collection, id=item["id"], title=item["title"]))
        for (type_name, field), count in self._inbound(artifact["id"]).items():
            response.inbound.append(kb_pb2.InboundCount(type=type_name, field=field, count=count))
        return response

    def _stub(self, field, target_id):
        target = self._store.load(target_id)
        schema = self._store.schema(target["type"])["schema"]
        return kb_pb2.Stub(
            field=field, id=target["id"], type=target["type"], title=target["title"],
            fields=to_struct(_summary_fields(target, schema)),
        )

    def _inbound(self, artifact_id):
        """How many artifacts point at this one, by their type and the field they use."""
        counts = {}
        for other in self._store.artifacts():
            schema = self._store.schema(other["type"])["schema"]
            for field in _reference_fields(schema):
                if artifact_id in _as_list(other.get(field)):
                    key = (other["type"], field)
                    counts[key] = counts.get(key, 0) + 1
        return counts


def _summary_fields(artifact, schema):
    return {name: artifact[name] for name in schema.get("summary", []) if name in artifact}


def _reference_fields(schema):
    return [name for name, field in schema.get("properties", {}).items() if "ref" in field]


def _as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]
```

- [ ] **Step 5: Run it green, then the suite and the slice's kb half**

```bash
cd /home/vscode/shopsystem-kb && python -m pytest -q -k the_client_reads_a_summary 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `1 passed`; `4 passed, 61 failed`; `4 passed, 61 deselected`.

- [ ] **Step 6: Commit**

```bash
cd /home/vscode/shopsystem-kb && git add -A && git commit -m "Slice 1: the client reads a summary

Summary fields from the type's summary keyword, a stub of each reference
target and each part, inbound counts by type and field.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

#### Scenario 5: shop-knowledge / record-a-decision / The user records a decision

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -k the_user_records_a_decision 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError: Step definition is not found: Given "a shop knowledge base holding the shop's types"`.

- [ ] **Step 2: The driver and the steps**

`/home/vscode/shopsystem-knowledge/tests/driver.py`, how the steps use the shop's real entry point:

```python
"""Drive shop-knol the way a user does: a subprocess per command, YAML in files and on stdout."""
import subprocess
import sys

import yaml


def knol(env, *args):
    return subprocess.run(
        [sys.executable, "-m", "shop_knowledge", *args],
        env=env, capture_output=True, text=True,
    )


def start(env, shop):
    result = knol(env, "init", str(shop))
    assert result.returncode == 0, result.stderr


def record(env, tmp_path, type_name, content, message):
    """Write content to a file, record it, and return the id the user is shown."""
    path = tmp_path / f"{content['title']}.yaml"
    path.write_text(yaml.safe_dump(content, sort_keys=False, allow_unicode=True))
    result = knol(env, "create", type_name, "--from", str(path), "-m", message)
    assert result.returncode == 0, result.stderr
    return yaml.safe_load(result.stdout)["id"]
```

Append to `/home/vscode/shopsystem-knowledge/tests/conftest.py` (keep `pytest_configure`):

```python
import os

import pytest
from pytest_bdd import given

from driver import start


@pytest.fixture
def shop(tmp_path):
    """The directory the shop's knowledge base is started in; the store is its kb/ subdirectory."""
    return tmp_path / "shop"


@pytest.fixture
def env(shop):
    return {**os.environ, "KB_ROOT": str(shop), "KB_ACTOR": "shopkeeper"}


@given("a shop knowledge base holding the shop's types")
def _shop_knowledge_base(env, shop):
    start(env, shop)
```

Replace `/home/vscode/shopsystem-knowledge/tests/test_record_a_decision.py`:

```python
import yaml
from pytest_bdd import given, scenarios, then, when

from driver import knol, record

scenarios("record-a-decision.feature")

OLDER = {
    "title": "Prices are reviewed monthly",
    "sections": [
        {"title": "Purpose", "body": "Keep prices current.\n"},
        {"title": "Rationale", "body": "Monthly was enough once.\n"},
    ],
}
WEEKLY = {
    "title": "Price reviews happen weekly",
    "supersedes": "decision/prices-are-reviewed-monthly",
    "sections": [
        {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
        {"title": "Rationale", "body": "Costs move weekly, so a monthly review lags them.\n"},
    ],
}


@given(
    "a decision in a file, with a title, a purpose, a rationale and the decision it supersedes",
    target_fixture="decision_file",
)
def _decision_in_a_file(env, tmp_path):
    record(env, tmp_path, "decision", OLDER, "Record the monthly review")
    path = tmp_path / "weekly.yaml"
    path.write_text(yaml.safe_dump(WEEKLY, sort_keys=False))
    return path


@when("the user records that file as a decision, saying who they are and why", target_fixture="recorded")
def _record_it(env, decision_file):
    return knol(env, "create", "decision", "--from", str(decision_file), "-m", "Move price reviews to weekly")


@then("the user is shown the name the decision was given, which the user did not choose")
def _shown_the_name(recorded, decision_file):
    assert recorded.returncode == 0, recorded.stderr
    assert yaml.safe_load(recorded.stdout)["id"] == "decision/price-reviews-happen-weekly"
    assert "id" not in yaml.safe_load(decision_file.read_text())


@then("the shop holds the decision under that name and reads it back by it", target_fixture="read_back")
def _reads_back_by_name(env, recorded):
    name = yaml.safe_load(recorded.stdout)["id"]
    result = knol(env, "read", name)
    assert result.returncode == 0, result.stderr
    shown = yaml.safe_load(result.stdout)
    assert shown["id"] == name
    assert shown["title"] == "Price reviews happen weekly"
    return shown


@then("the decision is at its first version")
def _first_version(read_back):
    assert read_back["revision"] == 1
```

- [ ] **Step 3: Run it, red on the code**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -k the_user_records_a_decision 2>&1 | grep -E "^E|passed|failed" | head -4
```

Expected: `1 failed`, `AssertionError` from `start` with stderr `No module named shop_knowledge.__main__`.

- [ ] **Step 4: The command line, the bootstrap, and the decision type**

In `/home/vscode/shopsystem-knowledge/pyproject.toml` add, after `[project.optional-dependencies]`:

```toml
[project.scripts]
shop-knol = "shop_knowledge.cli:main"
```

and after `[tool.setuptools.packages.find]`:

```toml
[tool.setuptools.package-data]
"shop_knowledge.types" = ["*.yaml"]
```

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/__main__.py`:

```python
from shop_knowledge.cli import main

raise SystemExit(main())
```

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/types/__init__.py`:

```python
"""The shop's types: one schema artifact per file, loaded through Create when a knowledge base starts."""
```

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/types/decision.yaml`:

```yaml
title: Decision
version: 1
schema:
  type: object
  properties:
    title:
      type: string
    supersedes:
      type: string
      ref:
        targets: [decision]
        cardinality: one
        parts: false
        on_delete: refuse
    tags:
      type: array
      items:
        type: string
      ref:
        targets: [tag]
        cardinality: many
        parts: false
        on_delete: refuse
  required: [title]
  sections:
    - title: Purpose
    - title: Rationale
  summary: [supersedes, tags]
```

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/bootstrap.py`:

```python
"""The shop's types, loaded through Create when a knowledge base starts. kb never learns them any other way."""
from importlib import resources

import yaml
from kb.content import to_struct
from kb.contract import kb_pb2

TYPES = ("decision",)


def load(client, actor):
    for name in TYPES:
        text = resources.files("shop_knowledge.types").joinpath(f"{name}.yaml").read_text()
        content = yaml.safe_load(text)
        client.Create(kb_pb2.CreateRequest(
            type="schema", content=to_struct(content), actor=actor,
            message=f"Define the shop's {content['title'].lower()} type",
        ))
```

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/cli.py`:

```python
"""shop-knol: the shop's command line over kb. KB_ROOT finds the repository, KB_ACTOR says who is acting."""
import argparse
import os
from pathlib import Path

import yaml
from kb import client as kb_client
from kb.content import from_struct, to_struct
from kb.contract import kb_pb2

from shop_knowledge import bootstrap


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="shop-knol")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="start a shop knowledge base at <root>/kb/ with the shop's types")
    init.add_argument("root")

    create = commands.add_parser("create", help="record an artifact from a YAML file; prints the id kb chose")
    create.add_argument("type")
    create.add_argument("--from", dest="source", required=True, metavar="FILE")
    create.add_argument("-m", dest="message", required=True, help="why")

    read = commands.add_parser("read", help="read an artifact at a glance")
    read.add_argument("locator")

    args = parser.parse_args(argv)
    return {"init": _init, "create": _create, "read": _read}[args.command](args)


def _actor() -> kb_pb2.Actor:
    return kb_pb2.Actor(role=os.environ["KB_ACTOR"])


def _client():
    return kb_client.connect(Path(os.environ["KB_ROOT"]))


def _show(document: dict) -> None:
    print(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), end="")


def _init(args) -> int:
    root = Path(args.root)
    client = kb_client.connect(root)
    client.Init(kb_pb2.InitRequest(root=str(root)))
    bootstrap.load(client, _actor())
    return 0


def _create(args) -> int:
    content = yaml.safe_load(Path(args.source).read_text())
    response = _client().Create(kb_pb2.CreateRequest(
        type=args.type, content=to_struct(content), actor=_actor(), message=args.message,
    ))
    _show({"id": response.id, "revision": response.revision})
    return 0


def _read(args) -> int:
    response = _client().Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=args.locator)))
    _show({
        "id": response.id,
        "type": response.type,
        "schema_version": response.schema_version,
        "revision": response.revision,
        "title": response.title,
        **from_struct(response.content),
        "references": [
            {"field": stub.field, "id": stub.id, "type": stub.type, "title": stub.title, **from_struct(stub.fields)}
            for stub in response.references
        ],
        "parts": [{"collection": stub.collection, "id": stub.id, "title": stub.title} for stub in response.parts],
        "inbound": [{"type": count.type, "field": count.field, "count": count.count} for count in response.inbound],
    })
    return 0
```

`create` prints nothing for a refusal and exits 0 in this slice; slice 25 pins what a refusal prints and how the command reports failure. Reading from `-`, the `#path` part of a locator, `role:execution` in `KB_ACTOR`: slices 27 and 20.

Reinstall so the `shop-knol` script and the type package data are registered:

```bash
cd /home/vscode/shopsystem-knowledge && make dev && which shop-knol
```

Expected: `/home/vscode/.local/bin/shop-knol`.

- [ ] **Step 5: Run it green, then the suite; look at the round trip on disk**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -k the_user_records_a_decision 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
store=$(ls -d /tmp/pytest-of-$USER/pytest-current/*/shop/kb | head -1)
git -C "$store" log --format='%an: %s'
cat "$store/decision/price-reviews-happen-weekly.yaml"
```

Expected: `1 passed`; `1 passed, 49 failed`; the log shows four commits, oldest last: `kb: Start the store`, then `shopkeeper: Define the shop's decision type`, then the shopkeeper's two records; the file starts with the five identity keys, then `supersedes`, then `sections` with `|` bodies.

- [ ] **Step 6: Commit**

```bash
cd /home/vscode/shopsystem-knowledge && git add -A && git commit -m "Slice 1: the user records a decision

shop-knol init, create, read over kb's in-process client; the decision
type loaded through Create at init; YAML out.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

#### Scenario 6: shop-knowledge / read-back-what-the-shop-knows / The user reads a decision at a glance

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -k the_user_reads_a_decision_at_a_glance 2>&1 | tail -3
```

Expected: `1 failed`, `StepDefinitionNotFoundError` for the Background Given.

- [ ] **Step 2: Steps**

Replace `/home/vscode/shopsystem-knowledge/tests/test_read_back_what_the_shop_knows.py`:

```python
import yaml
from pytest_bdd import given, scenarios, then, when

from driver import knol, record, start

scenarios("read-back-what-the-shop-knows.feature")

OLDER = "decision/prices-are-reviewed-monthly"
DECISION = "decision/price-reviews-happen-weekly"


@given(
    'a shop knowledge base holding a decision with a purpose and a rationale, tagged "pricing", '
    "superseding an older decision, and pointed at by two work items",
    target_fixture="decision_id",
)
def _shop_with_a_linked_decision(env, shop, tmp_path):
    start(env, shop)
    record(env, tmp_path, "tag", {"title": "pricing", "description": "How the shop sets prices.\n"}, "Add the pricing tag")
    record(env, tmp_path, "decision", {
        "title": "Prices are reviewed monthly",
        "sections": [
            {"title": "Purpose", "body": "Keep prices current.\n"},
            {"title": "Rationale", "body": "Monthly was enough once.\n"},
        ],
    }, "Record the monthly review")
    decision_id = record(env, tmp_path, "decision", {
        "title": "Price reviews happen weekly",
        "supersedes": OLDER,
        "tags": ["tag/pricing"],
        "sections": [
            {"title": "Purpose", "body": "Keep prices in step with costs.\n"},
            {"title": "Rationale", "body": "Costs move weekly.\n"},
        ],
    }, "Move price reviews to weekly")
    record(env, tmp_path, "work-item", {"title": "Move the review to Mondays", "decisions": [DECISION]}, "Plan the move")
    record(env, tmp_path, "work-item", {"title": "Tell the pricing team", "decisions": [DECISION]}, "Plan the telling")
    return decision_id


@when("the user reads the decision", target_fixture="shown")
def _read_the_decision(env, decision_id):
    result = knol(env, "read", decision_id)
    assert result.returncode == 0, result.stderr
    return yaml.safe_load(result.stdout)


@then("the user sees its name, its title and the few fields the shop shows for a decision")
def _name_title_and_fields(shown):
    assert shown["id"] == DECISION
    assert shown["title"] == "Price reviews happen weekly"
    assert shown["supersedes"] == OLDER
    assert shown["tags"] == ["tag/pricing"]


@then("the user sees a stub of each thing it points at")
def _stubs(shown):
    stubs = {(stub["field"], stub["id"], stub["type"], stub["title"]) for stub in shown["references"]}
    assert stubs == {
        ("supersedes", OLDER, "decision", "Prices are reviewed monthly"),
        ("tags", "tag/pricing", "tag", "pricing"),
    }


@then("the user sees how many things point back at it, and of what kind")
def _inbound(shown):
    assert shown["inbound"] == [{"type": "work-item", "field": "decisions", "count": 2}]
```

- [ ] **Step 3: Run it, red on the code**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -k the_user_reads_a_decision_at_a_glance 2>&1 | grep -E "^E|passed|failed" | head -4
```

Expected: `1 failed`, `AssertionError` from `record` of the tag, stderr ending `FileNotFoundError: ... kb/schema/tag.yaml` (the shop has no tag type yet).

- [ ] **Step 4: The tag and work-item types**

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/types/tag.yaml`:

```yaml
title: Tag
version: 1
schema:
  type: object
  properties:
    title:
      type: string
    description:
      type: string
  required: [title, description]
  summary: []
```

`/home/vscode/shopsystem-knowledge/src/shop_knowledge/types/work-item.yaml`:

```yaml
title: Work item
version: 1
schema:
  type: object
  properties:
    title:
      type: string
    decisions:
      type: array
      items:
        type: string
      ref:
        targets: [decision]
        cardinality: many
        parts: false
        on_delete: refuse
  required: [title]
  summary: [decisions]
```

In `/home/vscode/shopsystem-knowledge/src/shop_knowledge/bootstrap.py`, tag before the types that point at it:

```python
TYPES = ("tag", "decision", "work-item")
```

- [ ] **Step 5: Run it green, then the suite and the slice**

```bash
cd /home/vscode/shopsystem-knowledge && python -m pytest -q -k the_user_reads_a_decision_at_a_glance 2>&1 | tail -1
python -m pytest -q 2>&1 | tail -1
python -m pytest -q -m slice-1 2>&1 | tail -1
cd /home/vscode/shopsystem-kb && python -m pytest -q -m slice-1 2>&1 | tail -1
```

Expected: `1 passed`; `2 passed, 48 failed`; `2 passed, 48 deselected`; `4 passed, 61 deselected`.

- [ ] **Step 6: See the observable at a shell, as the slice states it**

```bash
cd /tmp && rm -rf skeleton && mkdir skeleton && export KB_ROOT=/tmp/skeleton KB_ACTOR=shopkeeper
shop-knol init /tmp/skeleton
printf 'title: Price reviews happen weekly\nsections:\n- title: Purpose\n  body: |\n    Keep prices in step with costs.\n- title: Rationale\n  body: |\n    Costs move weekly.\n' > /tmp/weekly.yaml
shop-knol create decision --from /tmp/weekly.yaml -m "Move price reviews to weekly"
shop-knol read decision/price-reviews-happen-weekly
git -C /tmp/skeleton/kb log --format='%an: %s'
```

Expected: `create` prints `id: decision/price-reviews-happen-weekly` and `revision: 1`; `read` prints identity, empty `references`, `parts`, `inbound`; the log shows the shopkeeper's commit on top of the four bootstrap commits.

- [ ] **Step 7: Commit, then the checkpoint**

```bash
cd /home/vscode/shopsystem-knowledge && git add -A && git commit -m "Slice 1: the user reads a decision at a glance

Tag and work-item types join decision at init.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

Follow bdd-red-green's checkpoint in `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`: set slice 1's Status to `green` and append the entry. Its Open questions must carry the decisions this plan made that the spec did not (numbered 2, 3, 6, 7 under "Decisions this plan makes") and the unpinned Review Focus lines (1, 2, 5), each as a `QUESTION FOR THE SPEC:` line:

```
- 2026-09-23 slice 1 green. Someone can now: start a shop knowledge base, record a decision from a file saying who and why, be shown the name kb gave it, and read it back at a glance with stubs and inbound counts, the decision on disk as canonical YAML inside a commit by the actor.
  Surprised by: <what building it turned out to involve that the plan didn't say | nothing>.
  Open questions:
  - QUESTION FOR THE SPEC: schemas and journal under <root>/kb/ (as built) or <root>/ (as the Layout paragraph still says)?
  - QUESTION FOR THE SPEC: is the git repository <root>/kb/ itself (as built), or <root>?
  - QUESTION FOR THE SPEC: google.protobuf.Struct preserves neither key order nor int-ness; "fields in schema order" needs the order carried explicitly, or content as text on the wire.
  - QUESTION FOR THE SPEC: init's bootstrap creates use KB_ACTOR and a fixed message; does init take -m?
  - QUESTION FOR THE SPEC: a create without a title, a read of an id the store lacks, KB_ROOT unset: what is shown?
  Next: tag kb 0.1, pin it here, then slicing moves the kb-only slices to kb's own plan.
```

```bash
git add docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md
git commit -m "Slice 1 green

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

## After slice 1: tag kb, pin it, split the plans

Not a slice; the close of the one-effort phase both specs describe. Do it right after the slice-1 checkpoint, then stop: later slices get their tasks from a fresh run of `slicing-into-increments` and `writing-plans`.

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

Expected: `2 passed, 48 deselected`.

- [ ] **Hand the slice plan back to slicing-into-increments** to move the slices made only of kb scenarios into a plan in `shopsystem-kb`, as the slice plan's preamble says. writing-plans then runs once per repo for the slices that follow.
