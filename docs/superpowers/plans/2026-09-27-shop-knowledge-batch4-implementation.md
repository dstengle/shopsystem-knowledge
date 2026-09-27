# shop-knowledge batch 4: slices 19.2 to 30

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is one slice of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`. A capability task follows `shopsystem-bdd:bdd-red-green` over its scenarios. An enabling task is done when its check gives the required result. bdd-red-green's stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** Nine slices in plan order. The renderers read what they publish one way (19.2). Anything can be published as markdown (20). No file or directory a user names ends in a traceback (20.1). What the user is shown is shaped apart from the command line (20.2). Then a decision can be read at every depth, as JSON, from wherever the user works (22), revised whole or in part (24), refused when it has no actor, no message or the wrong shape (26), recorded from a pipe, under a piece of work or with a title already used (28), and listed (30).

**Architecture:** shop-knowledge is the Python package `shop_knowledge`. Its `shop-knol` command (`cli.py`) calls kb through `kb.client.connect` with `kb.contract.kb_pb2` messages, and reads and prints YAML 1.2 through `kb.content`. kb is `shopsystem-kb` v0.2.0, installed from its git tag into this checkout's `.venv`. It is never edited here. `CLAUDE.md` is the shape the code is held to. Its module map says where each change lands, and each task names the rule it implements once.

**This plan carries no code** (adrs/0011). The implementer writes every step definition and every line under `src/` red-green in the execution session. What each task gives instead:
- the slice and its scenarios or check;
- why each is red today, found by running it in this checkout;
- where the change lands, and which rule it implements once;
- the decisions the spec leaves open, each resting on a passage;
- what existing steps and fixtures to reuse, by name;
- the commands, with counts taken from the tags;
- the checkpoint to log.

**Tech Stack:** Python 3.11, setuptools (src layout), kb v0.2.0 (protobuf contract, in-process client), pytest 8 + pytest-bdd 8, `jsonschema` (already installed as kb's dependency; slice 20.1 declares it).

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`, sections The CLI, Renderers and What use will tell us. `CLAUDE.md`. Slice plan `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, slices 19.2 to 30, including the 19.1 review entry at the end of its log, which states what 19.2, 20.1 and 20.2 are for. kb's contract: `.venv/lib/python3.11/site-packages/kb/contract/kb.proto`.

## Global Constraints

- Feature files are read-only. Any diff under `features/` is a stop condition.
- Code only what a scenario asserts (bdd-red-green). Where a scenario is silent, the code is silent too, and the silence goes into the checkpoint as an open question.
- kb is v0.2.0 in `.venv` and is never edited here. "shop-knowledge never touches kb's files or git. It calls the contract through the in-process client." A kb change a slice needs is not coded. It is logged in the slice plan as a request to bump the pin, and the slice stops. The probes for this plan found that none of these slices needs one.
- Every rule in `CLAUDE.md` holds at the end of every task, and each is implemented once:
  - a kb answer and a renderer's `Rendered` are refused only through `cli._answered`;
  - a refusal is printed only by `main`, through the one printer, from a `Refused`;
  - a user's file is read only in `cli._document`;
  - files are written only by `cli._write`;
  - no module runs over 250 lines. If a task would take one past 250, stop and hand back. Splitting it is a refactor, which is a slice of its own, not something the task improvises.
- "shop-knol never shows a traceback." "Errors are printed as returned by kb, with artifact, path, and message, and exit non-zero." "Every mutating command requires an actor and `-m`." "Output is YAML by default and `--json` for the same structure."
- Work on `main` in this checkout (adrs/0009). `make test` runs the suite in `.venv`. While scenarios are red, its last line is make's own `Error 1`, so read pytest's summary line above it. Every command below runs from the checkout's root.
- Scratch files for checks go under `.superpowers/batch4/`. `.superpowers/` is in `.git/info/exclude`.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`. The message ends with the Co-Authored-By line of the model that made the commit, e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`. Each task makes one commit, holding the slice's code, its steps and its checkpoint.
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- **Counts.** The suite has 62 scenarios. `pytest --collect-only -q -m slice-N` selects 1 for slice 20, 10 for 22, 2 for 24, 3 for 26, 3 for 28, 3 for 30, and none for the enabling slices 19.2, 20.1 and 20.2. So, failed/passed after each task:

  | after | failed | passed |
  |---|---|---|
  | before Task 1 | 49 | 13 |
  | 19.2 | 49 | 13 |
  | 20 | 48 | 14 |
  | 20.1 | 48 | 14 |
  | 20.2 | 48 | 14 |
  | 22 | 38 | 24 |
  | 24 | 36 | 26 |
  | 26 | 33 | 29 |
  | 28 | 30 | 32 |
  | 30 | 27 | 35 |

  After Task 9, the 27 left are exactly those tagged 32 or later (`-m "slice-32 or slice-34 or slice-36 or slice-38 or slice-40 or slice-42 or slice-44 or slice-47 or slice-48 or slice-49 or slice-50"` collects 27).
- **GREEN**, the slices green before this batch: `-m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28 or slice-4 or slice-15 or slice-16 or slice-17 or slice-18 or slice-19"`, 13 scenarios. Each task below adds its own tag to the expression, and every scenario it selects must pass.
- **The shape check**, run at the end of every task:

  ```bash
  grep -c "_refuse(" src/shop_knowledge/cli.py; grep -c "if response.faults:" src/shop_knowledge/cli.py; grep -c "read_text" src/shop_knowledge/cli.py; find src -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'; grep -lE "print\(|open\(|write_text" src/shop_knowledge/renderers/*.py
  ```

  Expected (as on 2026-09-27): `2` (the printer's definition and `main`'s one call), `1` (`_answered`), `1` (`_document`, the one reader of a user's file; from slice 28 it also reads standard input, and nothing else in `cli.py` does), no module over 250 lines, and no renderer listed. Slice 42.2 moves Validate's refusal into `_answered`. Until then, `_validate` raising its own `Refused` is the one exception CLAUDE.md names.

## Decisions that hold across the batch

1. **A user's file has a shape, and the shapes are data** (slice 20.1, from the 19.1 review). The shapes live as JSON Schema files under `src/shop_knowledge/shapes/`, as the types do under `types/`. `_document` checks each file against its shape where it reads it, with the same validator kb checks a type with (`jsonschema`'s Draft 2020-12). So a violation comes out in kb's words: the file as the artifact, the place as the path, the keyword as the rule, and jsonschema's message.
2. **An operating system's refusal of a path is a fault naming it.** `main` catches `OSError` next to `Refused` and prints one line: the path the error names, then its reason. That covers a file not there, a directory given as a file, and `--to` naming a file. A file that is not UTF-8 is a content problem, not a path problem, so `_document` refuses it the way it refuses `NotCanonical`. A catch-all over `Exception` is not taken. Its words would be Python's, and it would hide a defect as a refusal (the 19.1 review).
3. **One fault, one line.** The printer prints `artifact at path: message`. It leaves out ` at path` when there is no path, and prints the message alone when the fault names no artifact. A message spanning several lines is joined into one: each line stripped, then joined with a single space.
4. **The store is found by kb, not by shop-knol** (slice 22). "The store is found the way git finds a repository, upward from the working directory to a directory holding `kb/store.yaml`, or through `KB_ROOT` when set." `kb.client.connect()` with no root does exactly this on every call, and refuses in the three ways the spec lists (probed, below). So `cli._client` connects with no root, and kb's words pass through as every kb fault does. `init` keeps connecting to the root it is given.
5. **Answers are shaped in one module** (slice 20.2). Turning a kb answer into the document the user is shown moves out of `cli.py` into `answers.py`, and slices 22, 24 and 30 add their shapes there, not to `cli.py`. `cli.py` keeps the arguments, the handlers, the environment, and printing (`_show` and the printer).
6. **A step that changes where the user works** (slice 22). The Givens that work in another directory, or with `KB_ROOT` unset or pointed elsewhere, change the scenario's `env` dict in place, since it is one fixture instance for the whole scenario. They give the directory as a fixture `workdir`, which defaults to `None`, meaning pytest's own working directory. `tests/driver.py`'s `knol` gains two keyword arguments:
   - `cwd`, the directory the subprocess runs in;
   - `input`, the text piped to it (slice 28).

   Nothing else in the driver changes.

## Review Focus

writing-plans asks for a test in the owning task for each line here. In this project tests are scenarios, and feature files are the human gate, so no test is added. Each line instead goes into the owning task's checkpoint as a `QUESTION FOR THE SPEC`, with the reproduction given, run after that task.

1. **argparse still refuses in its own way** (owner: Task 3, slice 20.1, which makes rule 4 hold for files and paths but not for arguments). A usage error prints argparse's usage on stderr and exits 2, where rule 4 says one fault line and exit 1. Reproductions: `shop-knol read decision/x --resolve two` after Task 5; `shop-knol list` with no `--type` after Task 9; `shop-knol nosuch`. A user would expect one plain line and exit 1. No scenario pins any argument error.
2. **`--json` is on `read` alone** (owner: Task 5). The spec says output is "YAML by default and `--json` for the same structure", for every command, but only the read scenario asks for it, so only `read` takes it. Reproduction after Task 9: `shop-knol list --type decision --json` is a usage error. A user would expect JSON from every command that answers.
3. **`list --ids` is YAML, not bare lines** (owner: Task 9). Everything printed goes through `kb.content`, which writes a top-level sequence indented two spaces (`  - decision/a`). So `shop-knol list --type decision --ids | xargs -n1 shop-knol read` passes `-` as a name. The scenario says "names only, to feed another command". A user would expect one name to a line, or a `--json` array.
4. **"Superseded" is a status the user writes, not the link** (owner: Task 9). kb's List narrows by an artifact's own fields, so the superseded decision is the one whose `status` says `superseded`. A decision that another decision's `supersedes` points at, but which is not marked so, is not listed by `--where status=superseded`. Reproduction after Task 9: record two decisions, the second superseding the first, neither with a status, then `shop-knol list --type decision --where status=superseded` answers an empty sequence. A user would expect the link to count.
5. **Parts as tables are not pinned** (owner: Task 2). The markdown scenario publishes the role, and the shop's role type has no part collection, so nothing the scenario checks is a part. The renderer lays out only what the role holds (Task 2, decision 3). Reproduction after Task 2: `shop-knol render markdown process/restock-a-shelf --to out` shows the steps as a nested list of fields, not a table. A user would expect the table the scenario's title promises.

---

### Task 1: Slice 19.2, a renderer offers only its render, and every renderer reads what it publishes one way

**Slice plan entry:** enabling. Check:
- `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort` gives the same 49 failing scenarios as before (49 failed, 13 passed);
- `grep -nE "^def [a-z]" src/shop_knowledge/renderers/skill.py src/shop_knowledge/renderers/diagram.py` gives the two `render` lines and nothing else;
- `grep -rl "ReadRequest.WHOLE" src/shop_knowledge/renderers` gives one module;
- `grep -rc 'split("/", 1)' src/shop_knowledge | grep -v ":0"` gives one line, a count of 1.

**Observable:** The markdown renderer of slice 20 and the agent renderer of slice 50 read the artifact they publish, and name it without its kind, the same way the skill and diagram renderers do. A renderer's module shows the command line only the function it calls.

**Why the check fails today** (run on 2026-09-27):
- the `def` grep also lists `skill.py:35 def body` and `diagram.py:20 def flowchart`;
- the `WHOLE` grep lists both `renderers/diagram.py` and `renderers/skill.py`, since `skill._whole` and `diagram.render` each build the whole read;
- the `split` grep gives `diagram.py:1` and `skill.py:1`.

**Where it lands:**
- A new module `src/shop_knowledge/renderers/source.py` holds the two things every renderer does to what it publishes:
  - reading an artifact whole through the contract, at a depth that defaults to 0 (links left as names);
  - an artifact's name without its kind.
- `skill.py` and `diagram.py` call it. The skill renderer reads the process, and each step it reuses, through the whole read.
- `body` and `flowchart` become private (`_body`, `_flowchart`).
- `CLAUDE.md` gets a row for `renderers/source.py`: it owns reading the artifact a renderer publishes, and its name without its kind; it never holds rendering or writing.
- Rule implemented once: rule 6's read side. A renderer reads through the contract one way.

**Decisions:**
- The module's name is `source`. It is the source a renderer publishes from. That keeps it apart from `cli._read`, which is the command.
- The whole read's refusal stays the renderer's to hand back as `Rendered` faults, as today. `source` returns kb's answer and decides nothing.

**Reuse:** nothing new in `tests/`. The slice 17, 18 and 19 scenarios are the guard.

- [ ] **Step 1: Record the baseline.** `mkdir -p .superpowers/batch4 && .venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch4/failing-19.1.txt; wc -l < .superpowers/batch4/failing-19.1.txt`. Expected: `49`. Run the three greps above and see them fail as described.
- [ ] **Step 2: Make the change.**
- [ ] **Step 3: Check.** Run `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort | diff - .superpowers/batch4/failing-19.1.txt && echo same 49`. Expected: `same 49`. Then:
  - `make test`: pytest's line reads `49 failed, 13 passed`;
  - GREEN: `13 passed`;
  - the three greps give the required results;
  - the shape check passes.
- [ ] **Step 4: Checkpoint.** Set slice 19.2's Status to `green` and append at the very end of the slice plan's log (check with `tail`): `- 2026-09-27 slice 19.2 green. <what changed, one sentence>. Check: <the diff's output>, <pytest's summary line>, <each grep's real output>.` Then `Surprised by:` and `Next: slice 20.` Commit.

---

### Task 2: Slice 20, publish anything as markdown

**Slice plan entry:** capability. Observable: a user publishes a role into a directory and finds a page with its identity as a heading, its fields as a list, its sections at their levels, and its parts as tables. Unknown: can the page be laid out from the type alone, so the renderer knows nothing about any one type? Scenario: publish-what-the-shop-knows / "The user publishes anything as markdown" (`@slice-20`, 1 scenario).

**Why it is red today:** `StepDefinitionNotFoundError` for When "the user publishes the role as markdown into a directory". Underneath that, `shop-knol render markdown ...` is refused by argparse (`invalid choice: 'markdown'`, exit 2), since `RENDERERS` names only `diagram` and `skill`.

**Where it lands:**
- A new `src/shop_knowledge/renderers/markdown.py`, named `markdown` in `RENDERERS`. It reads through `source` (Task 1) and gives back a `Rendered`.
- `cli.py` is not touched: `_render`, `_answered` and `_write` serve it as they do the other two.
- `CLAUDE.md`'s `renderers/` row already covers it.
- Rules implemented, each once:
  - rule 5, types are data. This is the one renderer that names no field of any type;
  - rule 6, renderers only read.

**What the probe shows:** kb's whole read of the Background's role (`role/stock-keeper`, depth 0) gives, in this order: `harness` (`name`, `description`, `tools: [Read]`), then `shop` (`responsible_for`), then `sections` (one, "How it works", body `Counts, then orders.` with a trailing newline). kb orders a whole read as identity, fields in schema order, sections, then part collections (`kb/settled.py`).

**Decisions:**
1. **The file is `<name>.md`**, the artifact's name without its kind (`stock-keeper.md`), as the diagram is `<name>.mmd`. The spec names no file for markdown.
2. **The page's shape**, resting on "`markdown` for any type: identity as heading, fields as a definition list, sections at their levels, parts as tables":
   - The heading is `# <title>`.
   - The fields are a Markdown list, one item per field in the order kb gives them, each written `- **<field>**: <value>`, with the field's name as it is stored.
   - A field holding a mapping (a field group, such as `harness`) is `- **<field>**`, with its own fields as a nested list indented two spaces.
   - A list of plain values is written joined with `, `.
   - A link is its name, since the read is at depth 0.
   - Each section is a heading one level below its holder: `##` for a top-level section, `###` for a section inside it, and so on down kb's nested `sections`. Its body follows, with trailing whitespace stripped.
   - A blank line separates the heading, the field list and each section.
   - The Then pins the page's exact lines.
3. **Parts: not coded.** The scenario's Then names "the parts as tables", but the role it publishes holds no part collection, since the shop's role type declares none. So no line of the page a scenario can check is a part, and bdd-red-green codes nothing no scenario asserts. So the renderer tells only `sections` apart from everything else. Every other entry is a field. It reads no schema. That is kb's content model (every type's prose is under `sections`), not knowledge of any one type. The checkpoint logs the missing table as Review Focus 5.
4. **The unknown's answer** goes in the checkpoint: the page is laid out from kb's content model, the whole read's own order and its `sections`, with no schema read and no type named. Whether parts can be told apart without the schema is left open by decision 3.
5. **Depth 0.** The spec says renderers read "the resolved whole artifact". A page for a person shows what the artifact points at by name, so the markdown renderer reads at depth 0, as the diagram does.

**Reuse:** in `tests/test_publish_what_the_shop_knows.py`:
- the Background Given (it records `ROLE` as `role/stock-keeper`; the role's name is known from that constant, since the Background returns `process_name` only);
- the fixture `target`;
- the pattern of `_publish_as_a_diagram` / `_a_diagram`: the When gives `result`, and the Then asserts the directory listing and then the file's exact lines.

- [ ] **Step 1: Red.** `.venv/bin/python -m pytest -q -m slice-20 2>&1 | tail -1`. Expected: `1 failed, 61 deselected`, from the missing When.
- [ ] **Step 2: Steps, then red again for the right reason**: the When runs `render markdown role/stock-keeper --to <target>` and argparse refuses `markdown`.
- [ ] **Step 3: The renderer.** Green: `1 passed, 61 deselected`.
- [ ] **Step 4: Suite.** `make test`: `48 failed, 14 passed`. GREEN plus `slice-20`: `14 passed`. The shape check passes, and `grep -nE "harness|shop|role" src/shop_knowledge/renderers/markdown.py` prints nothing.
- [ ] **Step 5: Checkpoint and commit.** Use the capability form the log uses:
  - `- 2026-09-27 slice 20 green. A user can now: ...`;
  - `Assumption "the page can be laid out from the type alone": held/failed. Evidence:` followed by the page the scenario publishes, complete;
  - `Surprised by:`;
  - `Open questions:` holding Review Focus 5 with its reproduction's real output;
  - `Next: slice 20.1.`

---

### Task 3: Slice 20.1, no file or directory a user names ends in a traceback

**Slice plan entry:** enabling. Unknown: can the shape of every file a user gives be checked where it is read, in the words kb uses for a violation, with the shapes held as data as the shop's types are? Check:
- the same 48 failing scenarios as before (48 failed, 14 passed);
- each case in Step 1's table, run in a started knowledge base, prints exactly one line on stderr with no `Traceback`, nothing on stdout, and exits 1.

**Why the check fails today:** each case reproduced on 2026-09-27 in a started knowledge base:

| case | today |
|---|---|
| `apply` of `changes: [{delete: tag/pricing}]` | 22 lines, `KeyError: 'content'`, exit 1 |
| `apply` of a file with no `changes` | 16 lines, `KeyError: 'changes'` |
| `apply` where `changes: 3` | 16 lines, `TypeError: 'int' object is not iterable` |
| `apply` of a file that is a list (`- a`) | 16 lines, `TypeError: list indices must be integers or slices, not str` |
| `create` from a file that is a list | 13 lines, `TypeError: pop expected at most 1 argument, got 2` |
| `create` from a path not there | 22 lines, `FileNotFoundError` |
| `create` from a directory | 22 lines, `IsADirectoryError` |
| `create` from a file that is not text (bytes `ff fe 00`) | `UnicodeDecodeError` traceback |
| `create` from the first 50 bytes of `/bin/ls` | two lines: `bin.yaml: it is not YAML that can be read: unacceptable character #x007f: special characters are not allowed` then `  in "<unicode string>", position 0` |
| `render skill ... --to` a file | `NotADirectoryError: [Errno 20] Not a directory: 'afile/p'` |
| `render diagram ... --to` a file | `FileExistsError: [Errno 17] File exists: 'afile'` |
| `create nosuch` | one line with a leading colon: `: a kind must name a type the store holds; the store holds no type called 'nosuch'` |

**Spike (throwaway, not kept):** the batch shape below, checked with `jsonschema.Draft202012Validator`, gives exactly one violation for each of the four bad batches:
- `changes/0 oneOf: {'delete': 'tag/pricing'} is not valid under any of the given schemas`;
- `required: 'changes' is a required property`;
- `changes type: 3 is not of type 'array'`;
- `type: ['a'] is not of type 'object'`.

It gives none for a good batch. `jsonschema` 4.26.0 is installed as kb's dependency, and kb's own `validation.py` uses the same validator class.

**Where it lands:**
- New data `src/shop_knowledge/shapes/`: an empty `__init__.py`, as `types/` has, plus `content.yaml` and `batch.yaml`.
- A new module `src/shop_knowledge/shape.py`: the violations of a document against a named shape, as faults on the file.
- `cli._document` takes the shape its caller names, and refuses the violations through `Refused`:
  - `create` names `content`;
  - `apply` names `batch`.

  It also refuses a file that is not UTF-8.
- `main` catches `OSError` as in decision 2.
- The printer follows decision 3.
- `pyproject.toml`:
  - `jsonschema` in `dependencies`;
  - `"shop_knowledge.shapes" = ["*.yaml"]` in package-data.

  The editable install needs no reinstall, since `jsonschema` is already in `.venv`.
- `CLAUDE.md`:
  - rows for `shape.py` (owns checking a user's file against its shape, and wording the violations as kb words a type's; never reads files or makes kb calls) and for `shapes/*.yaml` (the shape of each file a user gives, as JSON Schema; never code);
  - the Size and shape line on `_document` says the file is checked there against its shape;
  - rule 1 notes that `jsonschema` is imported by `shape.py` alone.
- Rule implemented once: rule 4, "never a traceback", for every file and path a user names, where it is read and in `main`, rather than per command.

**Decisions:**
1. **The shapes, in words.** Whoever writes them must match these, since the check's "exactly one line" depends on them:
   - `content`: an object.
   - `batch`: an object that requires `changes`, an array. Each item is an object whose `create` and `write`, if present, are strings and whose `content` is an object. Each item must satisfy exactly one of two required-lists, `[create, content]` or `[write, content]` (a `oneOf`). A separate `required: [content]` next to the `oneOf` would give two lines for the first case.
   - No `additionalProperties: false` anywhere. The spike shows it adds a second line to the first two cases.
   - `batch.operations` then assumes the shape. `batch.py` stays as it is apart from that.
2. **The fault's fields:**
   - artifact: the file as the user named it;
   - path: the violation's place, its path parts joined with `/`, empty at the top;
   - rule: the JSON Schema keyword;
   - message: jsonschema's.

   Printed through decision 3, a top-level violation reads `list.yaml: ['a'] is not of type 'object'`.
3. **Not UTF-8:** a fault on the file with rule `content` and a message beginning `it is not text that can be read:`, followed by Python's reason. That parallels kb's own `it is not YAML that can be read:`.
4. **"Behaviour does not change"** (the 19.1 review's call, kept): every scenario gives the same answer, and every stdout and exit status is as it was. The only change is that a traceback, or a line broken in two or opening with a colon, becomes one plain line.

**Reuse:** the 1.24 and 1.27 scenarios guard `_document`'s existing refusals. The 15 scenario guards `apply`.

- [ ] **Step 1: Record the baseline and set up the check's knowledge base.**

  ```bash
  .venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch4/failing-20.txt; wc -l < .superpowers/batch4/failing-20.txt
  rm -rf .superpowers/batch4/c201 && mkdir -p .superpowers/batch4/c201/shop .superpowers/batch4/c201/adir && cd .superpowers/batch4/c201
  export KB_ROOT=$PWD/shop KB_ACTOR=shopkeeper; k() { ../../../.venv/bin/python -m shop_knowledge "$@"; }
  k init shop
  printf 'changes:\n  - delete: tag/pricing\n' > nocontent.yaml; printf 'other: 1\n' > nochanges.yaml; printf 'changes: 3\n' > notalist.yaml; printf -- '- a\n' > list.yaml
  printf '\xff\xfe\x00' > nottext.yaml; touch afile
  printf 'title: Say hello\nsteps:\n  - title: Greet\n    does: Say hello.\n' > p.yaml; k create process --from p.yaml -m "Describe greeting"
  printf 'title: T\n' > t.yaml
  ```

  Expected: `48`, then `id: process/say-hello`. Then run each case, each as `k ... >out 2>err; echo "exit $? stdout $(wc -c <out) stderr $(wc -l <err)"; grep -c Traceback err`:

  | # | case |
  |---|---|
  | 1 | `k apply --from nocontent.yaml -m x` |
  | 2 | `k apply --from nochanges.yaml -m x` |
  | 3 | `k apply --from notalist.yaml -m x` |
  | 4 | `k apply --from list.yaml -m x` |
  | 5 | `k create decision --from list.yaml -m x` |
  | 6 | `k create decision --from nope.yaml -m x` |
  | 7 | `k create decision --from adir -m x` |
  | 8 | `k create decision --from nottext.yaml -m x` |
  | 9 | `k render skill process/say-hello --to afile` |
  | 10 | `k render diagram process/say-hello --to afile` |
  | 11 | `k create nosuch --from t.yaml -m x`, then `cat err` |

  Today they fail as in the table above.
- [ ] **Step 2: Make the change.**
- [ ] **Step 3: Check.** Re-run Step 1's cases in the same directory. Required for each: `exit 1 stdout 0 stderr 1` and `0` tracebacks. Case 11's line begins `a kind must name`. Then, from the checkout's root:
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort | diff - .superpowers/batch4/failing-20.txt && echo same 48`: `same 48`;
  - `make test`: `48 failed, 14 passed`;
  - GREEN plus `slice-20`: `14 passed`;
  - the shape check passes.
- [ ] **Step 4: Checkpoint and commit.** `- 2026-09-27 slice 20.1 green.` Then:
  - one sentence on what changed;
  - `Assumption "the shape of every file a user gives can be checked where it is read, in kb's words, with the shapes held as data": held/failed. Evidence:` followed by the eleven stderr lines, verbatim;
  - `Check: same 48, <pytest's summary line>`;
  - `Surprised by:`;
  - `Open questions:` holding Review Focus 1 with its reproduction (`shop-knol nosuch`: argparse's usage, exit 2);
  - `Next: slice 20.2.`

---

### Task 4: Slice 20.2, what the user is shown is shaped apart from the command line

**Slice plan entry:** enabling. Check:
- the same 48 failing scenarios (48 failed, 14 passed);
- `grep -cE "def _glance|def _change" src/shop_knowledge/cli.py` gives 0;
- `wc -l < src/shop_knowledge/cli.py` is under 200;
- the module that now shapes answers holds no `print`, no `Request` and no `connect`.

**Why the check fails today:** the grep gives `2`, and `cli.py` is 208 lines before Task 3 and more after it.

**Where it lands:**
- A new module `src/shop_knowledge/answers.py` takes every function that turns a kb answer into the document shown:
  - `_glance` (a summary read);
  - `_change` (a history entry) and the history's wrapper;
  - the create answer (`id`, `revision`);
  - the apply answer (`batch`, `results`);
  - the render answer (`written`).
- `cli.py` handlers call it and print through `_show`.
- `CLAUDE.md` gets a row for `answers.py`: it owns each kb answer as the document the user is shown; it never holds printing, kb calls or arguments.
- The `cli.py` row drops nothing it still does. It keeps "printing".
- Rule implemented once: the module map's "a new concern gets a new module". Shaping an answer is one concern, and slices 22, 24 and 30 add to it there.

**Decisions:**
- The public names in `answers.py` read as what they give, e.g. `glance`, `change`, `created`, `applied`, `written`. They are public because `cli.py` calls them.
- They take kb's response messages, or plain values, and return plain dicts. `kb_pb2` is imported only for type hints, if at all.

**Reuse:** nothing new in `tests/`. Slices 1, 15, 16, 17 and 19 guard every moved shape.

- [ ] **Step 1: Baseline.** `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort > .superpowers/batch4/failing-20.1.txt; wc -l < .superpowers/batch4/failing-20.1.txt`: `48`. Run the grep and `wc`.
- [ ] **Step 2: Move.**
- [ ] **Step 3: Check.**
  - the diff against `failing-20.1.txt`: `same 48`;
  - `make test`: `48 failed, 14 passed`;
  - the grep gives `0`;
  - `wc -l` is under 200;
  - `grep -cE "print|Request|connect" src/shop_knowledge/answers.py` gives `0`;
  - the shape check passes.
- [ ] **Step 4: Checkpoint and commit.** `- 2026-09-27 slice 20.2 green.` Then what moved, `Check:` with each output, `Surprised by:` and `Next: slice 22.`

---

### Task 5: Slice 22, read a decision at every depth, as text or JSON, from wherever the user works

**Slice plan entry:** capability, no unknown. Observable: a user reads a decision whole with its links as names, or one section, or with its links filled in one step or two, and as JSON; the store is found above where they work or through `KB_ROOT`, and the three ways of not finding one are refused. Scenarios, all in read-back-what-the-shop-knows (`@slice-22`, 10):
1. The user reads the whole decision
2. The user reads one section of a decision
3. The user reads a decision with the things it points at filled in
4. The user takes the same answer as JSON
5. The user asks for the links to be followed two steps
6. The user reads from a folder inside the shop's knowledge
7. The user reads while working elsewhere, having named the knowledge base
8. Reading where no knowledge base can be found is refused
9. Reading with KB_ROOT naming somewhere that holds no knowledge base is refused
10. Reading from inside one knowledge base while KB_ROOT names another is refused

**Why each is red today:** every one stops at `StepDefinitionNotFoundError`:
- 1: When "the user reads the whole decision";
- 2: When "the user reads the rationale of the decision";
- 3: When "... filled in, without saying how far";
- 4: When "... asking for JSON";
- 5: Given "the older decision is tagged "seasonal"";
- 6 to 10: their Givens.

Underneath that, run by hand on 2026-09-27:
- `read --whole`, `read --section Rationale` and `read --json` are each refused by argparse (`unrecognized arguments`, exit 2);
- with `KB_ROOT` unset, `read` from inside the shop's directory, or from outside any, gives `KeyError: 'KB_ROOT'`, a traceback. `cli._client` reads `os.environ["KB_ROOT"]` and connects to it;
- with `KB_ROOT=/tmp`, and with `KB_ROOT` naming another store while working in the shop's, the read answers `the store holds nothing by the name 'decision/...'`. That is the "empty shop" answer scenario 9 pins against, and it silently picks `KB_ROOT` where scenario 10 says neither is guessed at.

**What kb gives, probed in-process on 2026-09-27** over the Background's shape, with the older decision tagged `seasonal`:
- a whole read at depth 0: the content with links as names (`tags: [tag/pricing]`, `supersedes: decision/prices-are-reviewed-monthly`, then `sections`), and no identity in the content;
- depth 1: each link replaced by its target, which carries its identity (`id`, `type`, `schema_version`, `revision`, `title`) then its content, with the target's own links as names;
- depth 2: those filled in as well (the older decision's `tags` becomes the `seasonal` tag in full).

A section read takes the section's title exactly: `section="Rationale"` gives `title: Rationale` and `body`. `"rationale"` is refused with `'decision/…' holds no section titled 'rationale'`.

`kb.client.connect()` with no root refuses, with no artifact and no path, rule `store`:
- `no store was found, neither above <cwd> nor named outright`;
- `KB_ROOT names a directory that holds no store: <value>`;
- `KB_ROOT names a store other than the one <cwd> is working in: KB_ROOT is <named>, the working directory is inside <above>; neither is guessed at`.

`<cwd>` is the resolved working directory.

**Where it lands:**
- `cli.py`:
  - the `read` subparser gains `--section TITLE`, `--whole`, `--resolve [DEPTH]` and `--json`;
  - `_read` picks the level and depth and shows the answer;
  - `_client` connects with no root (cross-cutting decision 4);
  - `_show` writes JSON when asked.
- `answers.py`: the whole read's and the section read's shapes, next to `glance`.
- `tests/driver.py`: `knol` takes `cwd` (cross-cutting decision 6).
- `CLAUDE.md`, rule 3: YAML goes through `kb.content`, and JSON, the one other output, is the same document written by the standard library's `json`. The cli row: the store is found by kb from the working directory and `KB_ROOT`.
- Rules implemented once:
  - the spec's finding the store: one change, to `_client`, and every command gains it;
  - one output switch in `_show`.

**Decisions:**
1. **Levels.**
   - `--section <title>` is a section read with the title as given.
   - `--whole` is a whole read at depth 0.
   - `--resolve` alone is depth 1 ("`--resolve` alone is depth 1"), and `--resolve N` is depth N.
   - `--resolve` implies a whole read, since kb fills links in only on a whole read.
   - Neither flag gives the summary, as today.
   - `--section` given with `--whole` or `--resolve` is not refused. The section read is made. The checkpoint logs that as a question.
2. **What a whole read shows:** the identity (`id`, `type`, `schema_version`, `revision`, `title`), as `glance` leads with it, then kb's content as it comes. So a filled-in target appears in kb's own shape, identity first. No references, parts or inbound are added. A whole read is "the full contents of the one artifact".
3. **What a section read shows:** the section as kb gives it (`title`, `body`) and nothing else ("the user sees that section and nothing else").
4. **JSON** is the same document that would be printed as YAML, written with `json.dumps` (indented, non-ASCII kept) and a trailing newline. It is on `read` alone, the only command a scenario asks it of (Review Focus 2). Probed: `kb.content.loads` gives only strings, numbers, booleans, None, lists and dicts, never a date, so every answer serializes.
5. **Refusals from finding the store** pass kb's words through: "Errors are printed as returned by kb". The Thens assert kb's line exactly, with the working directory resolved as kb resolves it. The scenarios' "no knowledge base" is kb's "no store". The checkpoint notes the word difference as a question for the spec's bet passed-through-errors-are-actionable.
6. **The Thens of scenarios 3 and 5:**
   - "shown in place of the pointer" means `supersedes` is a mapping whose `id` is the older decision and whose `title`, `revision` and sections are as recorded ("as the shop holds it now").
   - In scenario 5, "the tag "seasonal" is shown in place of the pointer inside it" means that mapping's `tags` holds the tag's mapping, with `title: seasonal`.
   - In scenario 3, "what that older decision points at is shown by name only" is vacuous over the Background, whose older decision points at nothing. The step asserts every link inside the filled-in decision is a string, and the checkpoint logs that the Background cannot tell depth 1 from depth 2 there.
7. **Given "the older decision is tagged "seasonal"":** it drives shop-knol the way a user does. It uses `apply` (slice 15), with a batch that creates the tag `seasonal` and writes the older decision whole with `tags: [tag/seasonal]` and its two sections. `write` does not exist until slice 24, and CLAUDE.md allows the in-process client only for what no command does.
8. **The Givens that move the user** (cross-cutting decision 6):
   - "in a folder deep inside the directory that holds the shop's knowledge": a nested directory made under `shop` (not under `shop/kb`), with `KB_ROOT` removed from `env`;
   - "outside any knowledge base, with KB_ROOT naming the shop's": a fresh directory under `tmp_path`, with `KB_ROOT` kept;
   - "outside any knowledge base and nothing names one": the same directory, with `KB_ROOT` removed;
   - "KB_ROOT naming a directory that holds no knowledge base": an empty directory made under `tmp_path`, which `KB_ROOT` names;
   - "inside the shop's knowledge base, with KB_ROOT naming a different one": a second knowledge base started with `driver.start` at `tmp_path/"other"`. `workdir` is `shop`, and `KB_ROOT` names the other.

**Reuse:** in `tests/test_read_back_what_the_shop_knows.py`:
- the Background Given (`decision_id`), and the constants `DECISION` and `OLDER`;
- When "the user reads the decision" (`_read_the_decision`), given `workdir` and passing it as `cwd`;
- the fixture `shown`;
- the Then of slice 1 for "the user sees the decision" can read `shown["id"]`.

From `tests/conftest.py`: `env`, `shop`, and Then "the command reports failure to whatever ran it". From `tests/driver.py`: `knol`, `start`. The JSON Then compares `json.loads` of the JSON answer with `kb.content.loads` of a default read run in the step.

- [ ] **Step 1: Red.** `.venv/bin/python -m pytest -q -m slice-22 2>&1 | tail -1`: `10 failed, 52 deselected`.
- [ ] **Step 2: One scenario at a time**, as bdd-red-green says. Write its steps, see it red for the reason above, make it green, and keep GREEN green. A good order is 1, 2, 3, 5, 4, then 6 to 10. The last five need only the `_client` change once the Givens exist.
- [ ] **Step 3: Green.** `-m slice-22`: `10 passed, 52 deselected`. `make test`: `38 failed, 24 passed`. GREEN plus `slice-20 or slice-22`: `24 passed`. The shape check passes.
- [ ] **Step 4: Checkpoint and commit.** Use the capability form, with no assumption line, since there is no unknown:
  - `A user can now: ...`;
  - `Evidence:` with the stderr of scenarios 8, 9 and 10, verbatim;
  - `Surprised by:`;
  - `Open questions:` holding Review Focus 2 with its reproduction, Review Focus 1's `--resolve two`, decision 1's `--section` with `--whole`, decision 5's wording, and decision 6's vacuous Then;
  - `Next: slice 24.`

---

### Task 6: Slice 24, revise a recorded decision, whole or in part

**Slice plan entry:** capability, no unknown. Observable: a user replaces a decision from a file and it reads back with the new wording at a later version, or replaces only its rationale and the rest reads as before. Scenarios, in revise-what-the-shop-knows (`@slice-24`, 2):
1. The user revises a recorded decision
2. The user revises one part of a recorded decision

**Why each is red today:** both stop at `StepDefinitionNotFoundError` for the Background Given "a shop knowledge base holding a decision with a purpose and a rationale, at its first version". `tests/test_revise_what_the_shop_knows.py` holds only `scenarios(...)`. Underneath that, `shop-knol write` is refused by argparse (`invalid choice: 'write'`, exit 2).

**What kb gives, probed on 2026-09-27:**
- `Write` with `Locator(id=<decision>)` and content holding both sections gives `revision: 2`, and the title is kept.
- Content carrying a `title` is refused: `… at title: a title is given alongside the content, never inside it; the content carried the title 'Other'`.
- `Write` with `Locator(id=<decision>, path="sections/rationale")` and content `{title: Rationale, body: …}` gives the next revision, with the other section and every field unchanged.
- The same with no `title` is refused (`at sections/1: 'title' is a required property`).
- A section is named in a path by its title's name (lower-cased, hyphens), as kb names every place.

**Where it lands:**
- `cli.py`: a `write` subparser (`locator`, `--from FILE`, `-m`), a `_write_artifact` handler (the name `_write` is taken by the file writer), and one function reading a locator the user gives. `<name>` or `<name>#<place>` becomes `kb_pb2.Locator(id, path)`.
- The file goes through `_document` with the `content` shape.
- `answers.py`: the write answer (`id`, `revision`), shaped as the create answer is.
- The answer is refused through `_answered`.
- Rule implemented once: a locator is read from the user's words in one place, so later commands that take `<locator>` (`append`, `delete`, `refs`) reuse it.

**Decisions:**
1. **A part is named with kb's link notation**, `<name>#<place>`, e.g. `decision/price-reviews-happen-weekly#sections/rationale`. The spec's table gives `write <locator>`, not `<id>` (render takes `<id>`), and kb's contract locator is a name and a place. kb itself writes a link to a place as "a name and, after `#`, a place inside that artifact". shop-knol does not compute the place from a section's title: that would repeat kb's naming rule, which is not on the contract. The checkpoint logs, as a question, that `read` names a section by `--section <title>` while `write` uses the place.
2. **A whole write's file carries no title.** shop-knol passes the content as given, and kb refuses a title in it in its own words ("its title is kept"). Dropping the title silently would hide a user's attempt to retitle. The step's file holds the two sections alone. The checkpoint logs, as a question, that a user who copies their create file into `write` is refused over its title.
3. **A part's file** holds the part as kb holds it: for a section, `title` and `body`.
4. **The answer** is `id` and `revision`, as `create` prints.
5. **Actor and message:** `-m` is required by argparse and the actor comes from `_actor()`, the same as `create` today. Slice 26 changes all three commands together.

**Reuse:**
- `tests/driver.py`: `start`, `record`, `knol`. The Background Given records the decision with `record` and gives its name.
- `tests/conftest.py`: `env`, `shop`.
- The Thens read back with `read --whole` (Task 5). "At a later version than before" compares the whole read's `revision` with 1. "Only the rationale changes" and "the rest reads as before" compare the whole read taken in the Background, or in a `before`-style fixture requested by the When, with the read after: everything equal but `revision` and the rationale's `body`. The publish feature's `before` fixture is the pattern.
- The Whens give `result`.

- [ ] **Step 1: Red.** `-m slice-24`: `2 failed, 60 deselected`.
- [ ] **Step 2: Scenario 1, then scenario 2**, each red for the reason above, then green.
- [ ] **Step 3: Green.** `-m slice-24`: `2 passed, 60 deselected`. `make test`: `36 failed, 26 passed`. GREEN plus `slice-20 or slice-22 or slice-24`: `26 passed`. The shape check passes.
- [ ] **Step 4: Checkpoint and commit.** Capability form:
  - `A user can now: ...`;
  - `Evidence:` with the whole read before and after scenario 2, `revision` and the rationale's `body` shown;
  - `Open questions:` holding decisions 1 and 2;
  - `Next: slice 26.`

---

### Task 7: Slice 26, a decision the shop cannot accept is refused

**Slice plan entry:** capability, no unknown. Observable: a user who records a file that does not fit the decision type is told the artifact and place at fault; one who records without a role or without a message is refused for that reason, and nothing is written. Scenarios, in record-a-decision (`@slice-26`, 3):
1. A decision that does not fit the shop's decision type is refused
2. A decision recorded by nobody is refused
3. A decision recorded without a reason is refused

**Why each is red today:**
- 1 stops at a missing Given, "a file missing something the shop's decision type requires". Underneath that, `create` already refuses such a file through `_answered` (probed: a decision with only a Purpose section gives `decision/<name> at sections: the sections the type requires must all be present, in order; 'Rationale' is missing`, exit 1). So scenario 1 is expected to pass once its steps exist, with no change under `src/`. bdd-red-green's rule for a scenario that passes before code applies: confirm it goes red with the Then asserting the wrong line, then log that existing behaviour satisfies it.
- 2 and 3 stop at the missing Given "a decision in a file". Underneath that, run by hand on 2026-09-27:
  - `KB_ACTOR` unset: `KeyError: 'KB_ACTOR'`, a traceback;
  - `KB_ACTOR=` empty, and `-m ""`: kb creates the artifact, then git's commit fails with a `CalledProcessError` traceback, leaving the new file and a journal entry staged in `kb/`. kb v0.2.0 accepts an empty role and message (the 2026-09-26 re-check);
  - `-m` missing: argparse's usage, exit 2.

**Where it lands:** `cli.py`:
- `-m` stops being required at the argument level on `create`, `apply` and `write`;
- one function gives each mutating command its actor and message, or raises `Refused` with a fault for each that is missing, before the file is read and before any kb call;
- `init` keeps taking only the actor.

Rule implemented once: "Every mutating command requires an actor and `-m`." It is enforced in one function, so no handler checks its own, and kb's missing refusal can never leave a half-made change behind from shop-knol.

**Decisions:**
1. **The words.** Each is a fault with no artifact, rule `actor` or `message`, so the printer shows the message alone (Task 3):
   - `every change must say which role made it, through KB_ACTOR as role or role:execution`;
   - `every change must carry a message, given with -m`.

   The Thens assert these lines exactly.
2. **Unset and empty are the same:** no role, and no message. Missing both gives both lines.
3. **`init` without an actor** is refused by the same role check, in the same words. Slice 47's scenario wants its own words ("starting one must say which role did it") and stays red for its missing steps. The checkpoint notes that slice 47 will reword the refusal for `init`.
4. **The ill-fitting file** is a decision with a title and a Purpose section but no Rationale, so kb's answer is exactly one fault naming the artifact and the place (`sections`). A file without a title would give `decision/ at title: …`, whose artifact names no decision.

**Reuse:** in `tests/test_record_a_decision.py`:
- When "the user records that file as a decision, saying who they are and why" (`_record_it`) serves scenario 1;
- the `OLDER` constant can be the content of "a decision in a file", written unrecorded to a file under `tmp_path`, given as `decision_file`.

Given "the user has not said which role they are" is shared with start-a-shop-knowledge-base (slice 47), so it goes in `tests/conftest.py` (CLAUDE.md). It removes `KB_ACTOR` from `env` in place. From conftest, "the command reports failure to whatever ran it". New Whens: "the user records that file as a decision", with `-m` but run where the Given removed the actor, and "... without a message", with no `-m`. Both give `result`.

- [ ] **Step 1: Red.** `-m slice-26`: `3 failed, 59 deselected`.
- [ ] **Step 2: Scenario 1** (steps only; see above), **then 2, then 3.**
- [ ] **Step 3: Green.** `-m slice-26`: `3 passed, 59 deselected`. `make test`: `33 failed, 29 passed`. GREEN plus `slice-20 or slice-22 or slice-24 or slice-26`: `29 passed`. The shape check passes.
- [ ] **Step 4: Checkpoint and commit.** Capability form:
  - `Evidence:` with the three stderr lines;
  - a note that scenario 1 was met by existing behaviour once its steps existed;
  - `Open questions:` holding decision 3;
  - `Next: slice 28.`

---

### Task 8: Slice 28, record a decision from a pipe, under a piece of work, or with a title already used

**Slice plan entry:** capability, no unknown. Observable: a user pipes a decision into `create` and it is held as if from a file; a change made on a piece of work is attributed to the role and the work; a repeated title gets a name of its own while the earlier decision still reads back. Scenarios, in record-a-decision (`@slice-28`, 3):
1. The user pipes a decision in instead of naming a file
2. The user records a decision as part of a piece of work
3. A decision whose title is already used is given a name of its own

**Why each is red today:**
- 1 stops at Given "a decision produced by another command". Underneath that, `create decision --from -` gives `FileNotFoundError: [Errno 2] No such file or directory: '-'`, a traceback before Task 3 and one plain line after it.
- 2 stops at Given "a decision in a file" until Task 7 defines it, then at Given "the user works as the shopkeeper on a named piece of work". Underneath that, `_actor` already splits `role:execution`, and the journal already shows both. So scenario 2 is expected to pass on its steps alone.
- 3 stops at Given "a decision in a file whose title is already used by a decision the shop holds". Underneath that, kb mints `<name>-2` for a taken title (probed). So scenario 3 is expected to pass on its steps alone.

bdd-red-green's rule for a scenario that passes before code applies to 2 and 3.

**Where it lands:**
- `cli._document`, the one reader of a user's file, reads standard input when the source is `-`. So `create`, `write` and `apply` all take a pipe.
- `tests/driver.py`: `knol` takes `input` (cross-cutting decision 6).
- Rule implemented once: `--from <file or ->` is read in one place.

**Decisions:**
1. **A fault about piped text** names its source `standard input`. That is plainer than `-` in a line such as `standard input at sections/0/body: …`.
2. **"Just as if it had come from a file":** the whole read (Task 5) shows the title and sections as piped, at revision 1.
3. **The piece of work** is `KB_ACTOR=shopkeeper:<work>`, set in `env` in place. The Then reads `shop-knol journal --artifact <name>` and finds the create entry's actor `{role: shopkeeper, execution: <work>}`.
4. **The title already used:** the Given records a decision, then writes a second file with the same title and a different rationale. The Thens assert:
   - the shown name is `<taken name>-2`;
   - the earlier name still reads back its own title, its own rationale and revision 1.

**Reuse:** in `tests/test_record_a_decision.py`:
- `_record_it`, for scenarios 2 and 3;
- Given "a decision in a file" (Task 7);
- `WEEKLY` / `OLDER`, for content.

From `tests/driver.py`: `record` and `knol`. The pipe's When calls `knol(..., input=<text>)` with `--from -`.

- [ ] **Step 1: Red.** `-m slice-28`: `3 failed, 59 deselected`.
- [ ] **Step 2: Scenario 1, then 2 and 3** (steps only; confirm each goes red on a wrong Then, then log).
- [ ] **Step 3: Green.** `-m slice-28`: `3 passed, 59 deselected`. `make test`: `30 failed, 32 passed`. GREEN plus `slice-20 or slice-22 or slice-24 or slice-26 or slice-28`: `32 passed`. The shape check passes, and `grep -n stdin src/shop_knowledge/cli.py` shows lines inside `_document` only.
- [ ] **Step 4: Checkpoint and commit.** Capability form, with evidence: the piped decision's whole read, the journal entry's actor, and the `-2` name. Note that scenarios 2 and 3 were met by existing behaviour once their steps existed. `Next: slice 30.`

---

### Task 9: Slice 30, list what the shop has recorded

**Slice plan entry:** capability, no unknown. Observable: a user lists the decisions with name and title, narrows them by a field, or takes the names alone. Scenarios, in list-what-the-shop-has-recorded (`@slice-30`, 3):
1. The user lists every decision
2. The user lists the decisions that match a field
3. The user lists only the names, to feed another command

**Why each is red today:** all three stop at the Background Given "a shop knowledge base holding three decisions, one of them superseded". `tests/test_list_what_the_shop_has_recorded.py` holds only `scenarios(...)`. Underneath that, `shop-knol list` is refused by argparse (`invalid choice: 'list'`, exit 2).

**What kb gives, probed on 2026-09-27:**
- `List(type="decision")` gives stubs in the order the store holds them, each with `id`, `type`, `title` and the fields the type shows at a glance (`fields`, canonical YAML).
- `fields={"status": "superseded"}` narrows to the one whose `status` is `superseded`.
- `form=IDS` gives names alone.
- A kind the store lacks is refused: `a kind must name a type the store holds; …`, with no artifact.
- `kb.content.dumps` of a list writes a top-level sequence, indented two spaces.

**Where it lands:**
- `cli.py`: a `list` subparser (`--type` required, `--where FIELD=VALUE` repeatable, `--ids`) and a handler making one `List` call, refused through `_answered`.
- `answers.py`: the listed stubs, and the names.
- Rule implemented once: none new. The handler uses `_answered`, `_show` and `answers` as every command does.

**Decisions:**
1. **What `list` shows:**
   - By default, a sequence with one entry per artifact: `id`, `type`, `title`, then the stub's fields, as `glance` shows a reference (without `field`).
   - With `--ids`, the sequence of names and nothing else.
   - No wrapper key: the answer to "list" is the list. The Thens read `kb.content.loads(stdout)`.
   - Review Focus 3 logs that this is not bare lines.
2. **`--where FIELD=VALUE`** is split at the first `=` into kb's `fields` map, and repeating it narrows by each. A `--where` with no `=` is not pinned, and is not refused beyond what kb says.
3. **The superseded decision** carries `status: superseded` (shop-artifact's `status`, "the fields every shop artifact carries, such as owner, status, and tags"). The newest decision's `supersedes` points at it. The When is `list --type decision --where status=superseded` (Review Focus 4).
4. **The Background** records three decisions, each with both sections: one with `status: superseded`, one superseding it, and one unrelated.

**Reuse:** `tests/driver.py` `start`, `record` and `knol`; `tests/conftest.py` `env` and `shop`. Each When gives `result`. A `shown`-style fixture that asserts exit 0 and loads stdout serves all three Thens, as in the read-back module.

- [ ] **Step 1: Red.** `-m slice-30`: `3 failed, 59 deselected`.
- [ ] **Step 2: Scenarios 1, 2, 3** in turn.
- [ ] **Step 3: Green.**
  - `-m slice-30`: `3 passed, 59 deselected`;
  - `make test`: `27 failed, 35 passed`;
  - GREEN plus `slice-20 or slice-22 or slice-24 or slice-26 or slice-28 or slice-30`: `35 passed`;
  - `.venv/bin/python -m pytest -q -rf | grep ^FAILED | wc -l`: 27, and each failing test belongs to a slice tagged 32 or later (the Counts constraint's expression collects exactly 27);
  - the shape check passes;
  - `wc -l < src/shop_knowledge/cli.py` is at most 250.
- [ ] **Step 4: Checkpoint and commit.** Capability form:
  - `Evidence:` with the three answers;
  - `Open questions:` holding Review Focus 3 and 4, with reproductions;
  - `Next: slice 30.1, the third architecture review, which runs before the next plan (adrs/0011).`

---

## After the batch

Slice 30.1, the third architecture review, is not a task here. Architecture reviews run before planning, never inside a plan (adrs/0011). It follows the nine slices of this batch, as its check says.
