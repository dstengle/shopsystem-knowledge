# shop-knowledge: how this code is shaped

Read before changing anything under `src/shop_knowledge/` or `tests/`. These are rules, not preferences; a change
that breaks one is refactored into place first, then made.

shop-knowledge is a client of kb. It owns the shop's types, the seed content, the renderers and the `shop-knol`
command line; kb owns storage, checking and history. kb is pinned in `pyproject.toml` and installed from its tag.

## Module map

| module | owns | never holds |
|---|---|---|
| `cli.py` | `shop-knol`: one handler per command making the kb calls that command maps to (init's through `init.py`, whose bootstrap answers it refuses through `_answered`), the actor from the environment and the client, whose store kb finds upward from the working directory or through `KB_ROOT`, and printing: answers as YAML on stdout, refusals as plain words on stderr | the shop's types, rendering, reading a batch, reading the file a user gives, finding or starting the knowledge base init furnishes |
| `init.py` | `shop-knol init`, furnishing the shop's knowledge base: finding one from where the user works (kb's refusal to find one passed on where `KB_ROOT` is set, even empty), telling whether it is empty, holds types but not all of the shop's (refused as not empty, naming them), or holds the shop's types where named through a `KB_ROOT` other than the working directory or as a directory, or reached through a server, told by the client's `where()` and named by its address (refused as already holding the shop's knowledge); a directory named is told apart only where the client's `where()` puts the knowledge base kb reaches at that directory itself, and one kb reaches only by searching above it gets `kb.init`'s own refusal, as kb gave it; furnishing it with the shop's types through bootstrap, or starting one with `kb.init`; its refusals raised as `refusal.Refused` | printing, arguments, the types themselves |
| `kb_requests.py` | each command's arguments as the request it sends kb, one public function per command, `<command>_request`, and `is_whole` for `cli._read` | kb calls, printing, reading files |
| `arguments.py` | every `shop-knol` command's arguments and help, declared with argparse, and the renderer names from `RENDERERS`; an argument it cannot take is refused by raising, never printed | handlers, kb calls, printing |
| `answers.py` | each kb answer as the document the user is shown: plain dicts and lists from kb's response messages or plain values, one public function per answer (`glance`, `whole`, `section`, `change`, `history`, `created`, `written_over`, `appended`, `applied`, `recorded`, `listed`, `names`, `written`, `reached`, `matched`, `deleted`, `checked`, `types`, `type_`) | printing, kb calls, arguments |
| `batch.py` | a batch file read into the items of one BatchCreate or one BatchReplace, in the order written | reading files, kb calls |
| `shape.py` | checking a user's file against its shape, and wording the violations as kb words a type's | reading files, kb calls |
| `coverage.py` | `shop-knol coverage`: which of a shop's Behaviour lines (those of the capabilities linking to it) no scenario formulates and which more than one does, read through the client it is given, each line as its link with its capability's title and its own; kb's refusal of a shop it does not hold, or a name that is no shop, raised as `refusal.Refused` | printing, arguments, writing |
| `dependencies.py` | `shop-knol dependencies`: which of a shop's active or deprecated capabilities depend on a deprecated or retired capability, in any shop, read through the client it is given, one entry for each such pair, with the dependency's shop and status and the scenarios of the depending capability's features whose `uses` name it; kb's refusal of a shop it does not hold, or a name that is no shop, raised as `refusal.Refused` | printing, arguments, writing |
| `document.py` | the file a user gives: read the way kb reads content (`document.read`), checked against its shape and against whether kb can keep it (`kb.content`'s own refusal), or refused as a `Fault` on it | kb calls, printing, arguments |
| `published.py` | what a publish leaves in the directory asked for: the files a renderer gave back, written, and, for the spec renderer, the files it published earlier directly in `spec/capabilities/`, `features/` and `adrs/` that carry the published-from line where the publisher puts it (told by `renderers/published_from.py`) and that it no longer writes, deleted after writing (a cleared directory that is a link, or sits under one, has nothing deleted) | rendering, kb calls, printing, deleting anything outside those three directories |
| `refusal.py` | the one exception every refusal travels in, `Refused`, before `cli`'s one printer shows it | kb calls, printing |
| `renderers/` | one module per renderer, each reading an artifact, and, for `spec`, the shop's other artifacts, through the contract and giving back a `Rendered` (`rendered.py`): `{path: text}`, or faults; `RENDERERS` names them for `shop-knol render` | writing files, kb writes |
| `renderers/source.py` | reading the artifact a renderer publishes, what stops it being published (the read's faults, then a type other than the one the renderer is made from), and its name without its kind; used by the renderers, `coverage.py` and `dependencies.py` | rendering, writing |
| `renderers/shop_capabilities.py` | finding a shop's capabilities, those linking to it whose status is active or deprecated, each read whole and in their order, and comparing dotted orders part by part as numbers, for the spec renderer, `coverage.py` and `dependencies.py`; it knows a capability's `status` and `order` as part of the spec renderer | rendering, files |
| `renderers/sections.py` | the layout of a content model's `sections` as headings and bodies, shared by the markdown, agent and spec page renderers | rendering a whole artifact, files |
| `renderers/gherkin.py` | the layout of a feature's fields and `scenarios` parts as the text of a `.feature` file, two-space indented, its tables padded to their widest cell | reading an artifact, files |
| `renderers/limits.py` | the limits the harness publishes, each checked against a renderer's output before anything is written, with where it was published | rendering, files |
| `renderers/spec.py` | the `spec` renderer: reading a shop whole, the shop's active and deprecated capabilities and the features formulating its capabilities, refusing what is no shop, and giving back the spec's files by path | writing files, the layout of any one file |
| `renderers/spec_capabilities.py` | the layout of a capability's page, `spec/capabilities/<name>.md`, from the capability's content and the name of the feature file formulating it | reading, files |
| `renderers/spec_decisions.py` | the shop's decisions as files: reading the decisions linking to the shop, laying out the ledger, `spec/decisions.md`, and a record, `adrs/<number>-<name>.md`, for each of the shop's own | writing files |
| `renderers/spec_index.py` | the layout of the spec's `spec/index.md` from the shop's content and its capabilities' names, gists and deprecated mark | reading, files |
| `renderers/names.py` | the name a published file is given from a title | reading, files |
| `renderers/published_from.py` | the line every published spec file carries to say it was published from the knowledge base, naming the artifact and its revision, as an HTML comment or a `#` comment | laying out a page, reading, files |
| `renderers/spec_faults.py` | what stops a shop's spec being published whole, in plain words, every fault at once: files two capabilities, decisions or features would share, a number two decisions carry, an order two capabilities carry, a capability resting on another shop's decision, a scenario using what its capability does not depend on, a table whose rows differ in width, a published capability depending on a retired one, a constraint tested in a retired one; run before any page is laid out | laying out a page, files |
| `bootstrap.py` | loading the shop's types through Create when a knowledge base starts, and naming which of them is the base the ten build on | the types themselves |
| `types/*.yaml` | the shop's types, one file each, as schema artifacts in kb's schema language | code |
| `shapes/*.yaml` | the shape of each file a user gives, as JSON Schema | code |
| `__main__.py` | `python -m shop_knowledge` | anything else |

A new concern gets a new module and a row here. Nothing is added "beside" existing code in a module that does not
own it.

## Rules that make whole classes of defect unreachable

1. **kb only through its contract.** Code under `src/` and `tests/` knows kb only through what kb publishes
   (kb adrs/0018, adrs/0047): it calls kb through `kb.client.connect` with `kb.contract.kb_pb2` messages, asks a
   client where its store is only through the client's `where()`, whose answer is a `kb.client.Where`, starts a
   store only through `kb.init`, whose refusal is `kb.NotStarted`, gives kb a clock only as the `clock` that
   `connect`, `kb.init` and `kb.testing.served` take, and from the rest of kb imports only `kb.content`: content as YAML 1.2 text, and `NotCanonical`, its refusal
   of text kb cannot keep; and, under `tests/` alone and in one module, `kb.testing.served`. It never reads or writes a file inside a
   knowledge base, names kb's storage or runs git. A scenario that needs a server of kb's gets it from the served-store double
   kb publishes, `kb.testing.served` (adrs/0050); no test starts such a server or writes a connection to one. `jsonschema` is imported by `shape.py` alone.
2. **kb is pinned, never edited here.** A change shop-knowledge needs from kb is logged in the slice plan as a
   request to bump the pin, and the slice that needs it waits for the release.
3. **YAML 1.2, the way kb reads it.** Every file a user gives and everything printed goes through `kb.content`.
   No other YAML library is imported. JSON, the one other output, is the same document written by the standard
   library's `json`.
4. **One way to refuse.** Every refusal, kb's or shop-knol's own, is a `Fault` printed by the one printer in
   `cli.py`, one line each, with exit 1. shop-knol never shows a traceback. Code that refuses raises
   `refusal.Refused` with its faults and `main` alone prints them, so no handler prints a refusal of its own.
5. **Types are data.** The shop's types reach kb only as schema artifacts created at `init`. No code outside a
   renderer for that type, `coverage.py` and `dependencies.py` (adrs/0057), and the step definitions, knows a type's fields.
6. **Renderers only read.** A renderer reads through the contract and gives back the files to write, or faults.
   It writes nothing; the command writes the files, and only when the renderer refused nothing.

## Size and shape

- No module over 250 lines, under `src/` or `tests/`. When a change would cross the limit, split first.
- A function does one thing at one level of abstraction; if it needs a comment to separate its phases, it is two
  functions.
- A file a user gives is read, checked against its shape, and checked against whether kb can keep it (`kb.content`'s
  own refusal), in one place, `document.read`, and a kb answer's refusal is refused in one way, `cli._answered`. One
  place differs: a renderer turns a kb answer's refusal into the `Rendered` faults it gives back, which `_render`
  refuses through `_refused`, the one refusal `_answered` itself makes. `init.py`, `coverage.py` and `dependencies.py` raise kb's
  refusals as `refusal.Refused` beside it (adrs/0057).

## Step definitions

- Step definitions drive shop-knol the way a user does, a subprocess per command, through `tests/driver.py`.
- They use kb only through what kb publishes (adrs/0047), and never read or write a knowledge base's files. A state
  no contract call can produce (a stored file damaged, an artifact unfit for its type, a link pointing at nothing)
  comes from the stand-in, `tests/stand_in/`: put on shop-knol's `PYTHONPATH` only through `driver.answering`, it
  answers the calls a step describes with the `kb_pb2` messages the step wrote, its faults in the step's own words,
  and hands every other call to the real kb. Nothing under `src/` knows it is there. The one place kb's contract names,
  a root's `kb/`, is named in `tests/driver.py` alone. A scenario that needs a server of kb's gets it from the served-store double kb
  publishes, `kb.testing.served`, used through one fixture (adrs/0050); no test starts such a server or writes a connection to one.
- Fixtures and steps shared by more than one feature live in `tests/conftest.py`; the rest sit beside the scenarios
  they serve. When one feature's steps outgrow a module, the steps of one of its concerns go to a module beside it,
  not named `test_*`, which the feature's test module alone star-imports (a plain import does not register them).
  When `conftest.py` itself would outgrow the limit, the shared steps of one concern move the same way, to a module
  beside it that `conftest.py` alone star-imports; the session guard's hooks may move there too, since pytest sees
  them through `conftest.py` (adrs/0048).
- What more than one of a feature's step modules need, that is not itself a step, goes to a helper module of its own,
  imported plainly, as `tests/driver.py` is: a sibling step module is star-imported by its feature's test module
  alone (adrs/0035), so no step module imports another.
- A When that runs shop-knol gives what it ran as the fixture `result`, so the shared Thens that say how a command
  ended, such as "the command reports failure to whatever ran it", read it under one name in every feature.
- `tests/clock/` is put on shop-knol's `PYTHONPATH`, with `TEST_NOW` set, only through `driver.at`, when a scenario
  says what day it is. Nothing under `src/` knows the day is set.
- Every shop-knol run the driver makes stays inside the scenario's own temporary directory: `tests/driver.py`'s
  `knol` takes its working directory from `cwd`, or, with none given, from `_default_cwd`, which conftest's autouse
  `_working_directory` fixture sets to the test's own `tmp_path`; a run with neither is refused. The suite itself
  refuses to start if a knowledge base is reachable upward from the checkout or the system's own temporary
  directory (conftest's `pytest_sessionstart` guard, `_refuse_near_a_real_store`).
- A scenario's environment, and the guard's own call to kb, is built from an allowlist (conftest's `_allowlisted`),
  never copied from the developer's whole shell: PATH, LANG and LC_*, whatever the interpreter needs, and HOME
  pointed at a directory of the test's own, with KB_ROOT and KB_ACTOR set by the `env` fixture as today. Nothing
  else of the developer's shell - a shell GIT_DIR, a shell sitecustomize on PYTHONPATH, global git config reached
  through the developer's own HOME - reaches a scenario's shop-knol or the guard's own call.
- No Then relies on the order kb gives its faults in; each compares a set of lines (or of `(at, field)` pairs),
  never a position.
- A Then that reads kb's own words gets them from `kb_oracle.kb_answer`
  (`tests/kb_oracle.py`): kb's own answer to the same call for the same state, asked in-process, under the same allowlisted environment, after shop-knol's own call was refused, so
  no step spells kb's wording, which is kb's to change. A Then over a fault the stand-in gave compares with what
  the stand-in gave (`kb_oracle.printed`, over the step's own words), never with kb's.

## Working here

- `make dev` once; `make test` runs the suite in this checkout's `.venv`, in parallel (pytest-xdist, `-n auto`, one
  worker per core, each scenario still in its own temporary directory). While scenarios are red its last line is
  make's own error; pytest's summary line above it is the answer. When a run's output must be read in order, run it
  serially: `.venv/bin/python -m pytest -q`, which also takes `-m slice-<n>` or a single test id as it is.
- The spec is `spec/`: `index.md`, `decisions.md`, and one capability per `features/<name>.feature`. Behaviour comes from `features/`; code is written red-green against a scenario, one at a time, and never adds
  behaviour no scenario asks for.
- A refactor is an enabling slice: its check is the suite giving the same answer and the structural target met.

