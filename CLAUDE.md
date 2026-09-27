# shop-knowledge: how this code is shaped

Read before changing anything under `src/shop_knowledge/` or `tests/`. These are rules, not preferences; a change
that breaks one is refactored into place first, then made.

shop-knowledge is a client of kb. It owns the shop's types, the seed content, the renderers and the `shop-knol`
command line; kb owns storage, checking and history. kb is pinned in `pyproject.toml` and installed from its tag.

## Module map

| module | owns | never holds |
|---|---|---|
| `cli.py` | `shop-knol`: one handler per command making the kb calls that command maps to, the actor from the environment and the client, whose store kb finds upward from the working directory or through `KB_ROOT`, and printing: answers as YAML on stdout, refusals as plain words on stderr | the shop's types, rendering, reading a batch |
| `arguments.py` | every `shop-knol` command's arguments and help, declared with argparse, and the renderer names from `RENDERERS` | handlers, kb calls, printing |
| `answers.py` | each kb answer as the document the user is shown: plain dicts from kb's response messages or plain values, one public function per answer (`glance`, `change`, `history`, `created`, `written_over`, `applied`, `listed`, `names`, `written`, `reached`, `matched`) | printing, kb calls, arguments |
| `batch.py` | a batch file read into the operations of one Apply, in the order written | reading files, kb calls |
| `shape.py` | checking a user's file against its shape, and wording the violations as kb words a type's | reading files, kb calls |
| `renderers/` | one module per renderer, each reading an artifact through the contract and giving back a `Rendered` (`rendered.py`): `{path: text}`, or faults; `RENDERERS` names them for `shop-knol render` | writing files, kb writes |
| `renderers/source.py` | reading the artifact a renderer publishes, and its name without its kind | rendering, writing |
| `renderers/limits.py` | the limits the harness publishes, each checked against a renderer's output before anything is written, with where it was published | rendering, files |
| `bootstrap.py` | loading the shop's types through Create when a knowledge base starts | the types themselves |
| `types/*.yaml` | the shop's types, one file each, as schema artifacts in kb's schema language | code |
| `shapes/*.yaml` | the shape of each file a user gives, as JSON Schema | code |
| `__main__.py` | `python -m shop_knowledge` | anything else |

A new concern gets a new module and a row here. Nothing is added "beside" existing code in a module that does not
own it.

## Rules that make whole classes of defect unreachable

1. **kb only through its contract.** Code under `src/` calls kb through `kb.client.connect` with
   `kb.contract.kb_pb2` messages. From the rest of kb it imports only `kb.content`, content as YAML 1.2 text, and
   `kb.canonical`, for `NotCanonical` alone, the exception `kb.content` raises. It never reads or writes a file inside a
   knowledge base and never runs git. `jsonschema` is imported by `shape.py` alone.
2. **kb is pinned, never edited here.** A change shop-knowledge needs from kb is logged in the slice plan as a
   request to bump the pin, and the slice that needs it waits for the release.
3. **YAML 1.2, the way kb reads it.** Every file a user gives and everything printed goes through `kb.content`.
   No other YAML library is imported. JSON, the one other output, is the same document written by the standard
   library's `json`.
4. **One way to refuse.** Every refusal, kb's or shop-knol's own, is a `Fault` printed by the one printer in
   `cli.py`, one line each, with exit 1. shop-knol never shows a traceback. Code that refuses raises `cli.Refused`
   with its faults and `main` alone prints them, so no handler prints a refusal of its own.
5. **Types are data.** The shop's types reach kb only as schema artifacts created at `init`. No code outside a
   renderer for that type, and the step definitions, knows a type's fields.
6. **Renderers only read.** A renderer reads through the contract and gives back the files to write, or faults.
   It writes nothing; the command writes the files, and only when the renderer refused nothing.

## Size and shape

- No module over 250 lines. When a change would cross the limit, split first.
- A function does one thing at one level of abstraction; if it needs a comment to separate its phases, it is two
  functions.
- A file a user gives is read, and checked against its shape, in one place, `cli._document`, and a kb answer's faults are refused in one way,
  `cli._answered`. Two places differ: Validate's answer is raised as `Refused` over its faults and violations together,
  and a renderer turns a kb answer's faults into the `Rendered` faults it gives back, which `_render` refuses through
  `_answered`.

## Step definitions

- Step definitions drive shop-knol the way a user does, a subprocess per command, through `tests/driver.py`.
- They may use kb's in-process client, or read and hand-edit a knowledge base's files, only to set up or observe
  what no shop-knol command yet does; the step says so where it does.
- Fixtures and steps shared by more than one feature live in `tests/conftest.py`; the rest sit beside the scenarios
  they serve.
- A When that runs shop-knol gives what it ran as the fixture `result`, so the shared Thens that say how a command
  ended, such as "the command reports failure to whatever ran it", read it under one name in every feature.
- `tests/clock/` is put on shop-knol's `PYTHONPATH`, with `TEST_NOW` set, only through `driver.at`, when a scenario
  says what day it is. Nothing under `src/` knows the day is set.

## Working here

- `make dev` once; `make test` runs the suite in this checkout's `.venv`. While scenarios are red its last line is
  make's own error; pytest's summary line above it is the answer.
- Behaviour comes from `features/`; code is written red-green against a scenario, one at a time, and never adds
  behaviour no scenario asks for.
- A refactor is an enabling slice: its check is the suite giving the same answer and the structural target met.

