# shop-knowledge batch 3: slice 19

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. The one task is slice 19 of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, a capability slice: follow `shopsystem-bdd:bdd-red-green` over its one scenario. Its stop conditions, hand-back and checkpoint apply, and they override any step here that conflicts with them.

**Goal:** A user publishes a process into a directory and finds a diagram of its steps and their branches, a Mermaid flowchart that places no node itself.

**Architecture:** shop-knowledge (`/home/vscode/shopsystem-knowledge`) is the Python package `shop_knowledge`. Its `shop-knol` command (`cli.py`) calls kb through kb's in-process client (`kb.client.connect`) with the contract's messages (`kb.contract.kb_pb2`), and reads and prints YAML 1.2 through `kb.content`. Slice 17 settled how a renderer works, and this task reuses all of it with no change to `cli.py`:
- a renderer is a module under `renderers/`, named in `RENDERERS`, so `shop-knol render` offers it;
- it reads through the contract and gives back a `Rendered` (`files`, `faults`) from `renderers/rendered.py`;
- `cli._render` refuses that `Rendered` through `cli._answered`, as it does any kb answer, and `cli._write` writes the files only when nothing was refused.

This task adds `renderers/diagram.py` and names it `diagram` in `RENDERERS`. It reads the process whole, once, and gives back `<name>.mmd`. kb is **not** a checkout here. It is `shopsystem-kb` v0.2.0, installed from its git tag into this checkout's `.venv` by `make dev`, and it is never edited from this repository.

**Provenance:** Every code block in this plan was assembled in a scratch clone of this repository (`/tmp/skb3/shop`) on 2026-09-27, run with this checkout's `.venv/bin/python` and `PYTHONPATH=/tmp/skb3/shop/src`. The red and green results, the suite counts and the Review Focus reproductions below are what those runs gave. The plan was then replayed from its own text in a fresh clone (`/tmp/skb3-replay`, with `.venv` linked to this checkout's), in the foreground. Every check, red and suite count came out as stated, and every file under `src/` and `tests/`, and `CLAUDE.md`, came out byte-identical to the scratch run's. This checkout was not touched.

**Tech Stack:** Python 3.11, setuptools (src layout), kb v0.2.0 (protobuf contract, in-process client), pytest 8 + pytest-bdd 8, Mermaid flowchart text.

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md` (Renderers; the bet a-diagram-is-derivable-from-steps). `CLAUDE.md` in this repository, the rules the code is held to. Slice plan: `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, slice 19. Feature file: `features/publish-what-the-shop-knows.feature`, scenario "The user publishes a process as a diagram", tagged `@slice-19`, so it is selected with `.venv/bin/python -m pytest -q -m slice-19`. Slice 17's task in `2026-09-26-shop-knowledge-batch2-implementation.md` (Task 7) is where the renderer shape was settled.

## Global Constraints

- Feature files are read-only. Only `slicing-into-increments` edits a tag line, and only `formulating-features` edits a Given, When or Then. Any other diff under `features/` is a stop condition.
- Code only what a scenario asserts (bdd-red-green). Where the scenario is silent the code is silent, and the silence goes into the checkpoint entry as an open question.
- kb is v0.2.0 from its tag, in `.venv`, and is never edited here. "shop-knowledge never touches kb's files or git. It calls the contract through the in-process client." A kb change the slice needs is not coded: it is logged in the slice plan as a request to bump the pin, and the slice stops. This slice needs none.
- `CLAUDE.md`'s rules are implemented once, and the new renderer uses that one implementation rather than a check of its own: a kb answer and a renderer's `Rendered` are refused only by `cli._answered`; a refusal is printed only by `main`, through `_refuse`, from a `Refused`; files are written only by `cli._write`, after `_answered` (rule 6, renderers only read). `renderers/diagram.py` holds no `print`, no `raise`, no `open` and no `write_text`.
- Renderers: "Client code, invoked only by `shop-knol render`. Each reads the resolved whole artifact, the stubs of its references, and its schema through the contract, and writes files to the target directory." "`diagram` for `process`: `<id>.mmd` generated from steps and branches."
- The bet: "**a-diagram-is-derivable-from-steps.** A process's steps and branches carry enough structure to draw it without hand layout. Fails if a rendered diagram needs manual arrangement to be readable."
- "shop-knol never shows a traceback." "Errors are printed as returned by kb, with artifact, path, and message, and exit non-zero."
- Work on `main` in this checkout. `make test` runs the suite in `.venv`; while scenarios are red its last line is make's own `Error 1`, so read pytest's summary line above it.
- Commits: `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with the Co-Authored-By line of the model that made the commit, e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
- pytest-bdd prints `PytestRemovedIn10Warning`s, two for each `target_fixture` step. That is the baseline, not a fault.
- Baseline before Task 1: `50 failed, 12 passed`, every failure tagged slice 19 or later. After Task 1: `49 failed, 13 passed`, every failure tagged slice 20 or later. The slices already green stay green: `-m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28 or slice-4 or slice-15 or slice-16 or slice-17 or slice-18"` gives `12 passed` before and after.
- **The shape check**, run at the end of the task:

  ```bash
  cd /home/vscode/shopsystem-knowledge && grep -c "_refuse(" src/shop_knowledge/cli.py; grep -c "if response.faults:" src/shop_knowledge/cli.py; grep -c read_text src/shop_knowledge/cli.py; find src -name "*.py" -exec wc -l {} + | awk '$2 != "total" && $1 > 250'; grep -cE "print|raise|open\(|write_text" src/shop_knowledge/renderers/diagram.py
  ```

  Expected: `2` (the printer's definition and `main`'s one call), `1` (`_answered`), `1` (`_document`), no module over 250 lines, and `0`: the renderer prints, raises, opens and writes nothing.

## Decisions this plan makes (the spec left them open or silent)

1. **What slice 17 settled, and where it holds for a diagram.** A renderer gives back a `Rendered`, and `_render` refuses it through `_answered` and writes it through `_write`: held, reused unchanged, so `cli.py` is not touched. The skill renderer reads each reused step whole because it writes that step's `does` out in full. A diagram draws the process's own steps, and a reused step's node is labelled with the title the process gives that use ("Check it"), which is in the process's own item. So the diagram renderer reads the process whole, once, and reads no reused step: that part of slice 17 does not hold here, because the diagram needs nothing from the shared step.
2. **Mermaid, in a `.mmd` file.** The spec names `<id>.mmd`, Mermaid's extension. Mermaid lays out a flowchart itself from its nodes and edges, so the file says only what connects to what and places nothing, which is the bet the scenario pins.
3. **The file's name: `<name>.mmd`, the process's name without its kind** (`restock-a-shelf.mmd`), as the skill renderer names its directory. The spec's `<id>` read literally is `process/restock-a-shelf`, which would put the file in a `process/` directory under `--to`. The diagram renderer takes only processes, so the kind adds nothing. The checkpoint logs this as a question for the spec.
4. **The flowchart's shape.** `flowchart TD`, top to bottom. Every step is a node, in the process's order, labelled `<n>. <title>` as the skill numbers them. A reused step is drawn in Mermaid's subroutine shape (`[[...]]`), an inline step as a box (`[...]`). Node ids are `step1`, `step2` and so on, not the names kb gave the steps. A step's name can be anything a user writes (kb keeps a given `id`), and Mermaid reads some words, such as `end`, as its own. Probed: a step titled "End" is named `end` by kb and drawn as `step2`. Then the edges. A step with branches goes where each branch says, the edge labelled with the branch's `when` (`-->|"<when>"|`), and only there. A step without branches goes on to the next step. The last step, if it has no branches, goes nowhere. That is how the skill reads a process too: its steps are followed in order unless a branch says otherwise.
5. **A branch to no step.** kb stores a `go_to` naming no step of the process (batch 2, decision 4). The skill writes the name as written. The diagram does the same: the edge goes to a node of that name, which Mermaid draws as a box of its own. So no process kb holds makes the renderer fail with a traceback. Whether to refuse such a branch is batch 1's Review Focus 5, still open.

## Review Focus

writing-plans asks that each line here get a test in the owning task. In this project tests are scenarios, and the feature files are the human gate, so no unit tests are added. Instead each line goes into the task's checkpoint entry as a `QUESTION FOR THE SPEC`, with the reproduction given here. Each was run in scratch after the task, with the output shown.

1. **A step title or branch condition holding a double quote** (a process with a step titled `Greet with "hi"` and a branch when `the customer says "no"`): the file holds `step1["1. Greet with "hi""]` and `step1 -->|"the customer says "no""| nowhere`, which Mermaid cannot parse. The command exits 0. A person would expect a diagram that draws, with the quote kept (Mermaid writes it `#quot;`) or refused in plain words.
2. **Publishing something that is not a process as a diagram** (`shop-knol render diagram tag/pricing --to out`): `pricing.mmd` holding only `flowchart TD` is written and the command exits 0. A process with no steps gives the same empty diagram. A person would expect a refusal saying a diagram is published from a process with steps.
3. **A branch to a name no step has** (`go_to: nowhere`): the edge goes to a bare node `nowhere`, and the diagram draws a step the process does not hold. A name Mermaid reads as its own, or one with a space in it, breaks the file. A person would expect the process refused when recorded, or the renderer to refuse (decision 5).
4. **`render diagram --to` a path that is a file** (`touch afile; shop-knol render diagram process/say-hello --to afile`): `FileExistsError: [Errno 17] File exists: 'afile'` traceback, against "shop-knol never shows a traceback". The skill's form of it is batch 1's Review Focus 4; `_write` is shared, so one answer covers both.
5. **Nothing here draws the diagram.** The scenario pins that the steps and branches are enough to generate the file with nothing placed by hand. Whether it "needs manual arrangement to be readable", as the spec's bet fails, is seen only when a person opens it in something that draws Mermaid. No Mermaid tool is installed here to check that the file parses. A person would expect the bet judged on the drawn diagram, as `corpus-only-roles-work-without-a-shell` is judged in use.

A publish of a process that does not exist is refused in plain words through `_answered` (`process/nope: the store holds nothing by the name 'process/nope'`, exit 1), so it is not a Review Focus line.

---

### Task 1: Slice 19, publish a process as a diagram

**Slice plan entry:** Slice 19, capability. Unknown: do steps and branches carry enough structure to draw the diagram without hand layout? Scenario:

1. publish-what-the-shop-knows / The user publishes a process as a diagram

**Files:**
- Create: `src/shop_knowledge/renderers/diagram.py`
- Modify: `src/shop_knowledge/renderers/__init__.py`
- Modify: `tests/test_publish_what_the_shop_knows.py`
- Modify: the slice plan (status, checkpoint)
- Not modified: `src/shop_knowledge/cli.py`, and `CLAUDE.md`, whose `renderers/` row ("one module per renderer") already covers the new module.

**Interfaces:**
- Consumes: the publish Background (gives `process_name`, the process `process/restock-a-shelf`: step 1 "Check it" reuses `step/check-the-stock`; step 2 "Decide" branches to `order-more` and `stop`; steps 3 "Order more" and 4 "Stop" are inline), and the fixture `target`, the empty directory published into, both in `tests/test_publish_what_the_shop_knows.py` since slice 17. From `renderers/rendered.py`: `Rendered(files: dict[str, str], faults: list[kb_pb2.Fault])` and `refused(faults) -> Rendered`. From `cli.py`, unchanged: `_render`, which calls `RENDERERS[args.renderer](client, args.locator)`, refuses through `_answered`, then `_write`s and prints `written:`.
- Produces: `shop_knowledge.renderers.diagram.render(client, name: str) -> Rendered` and `renderers.diagram.flowchart(steps: list[dict]) -> str`; `RENDERERS["diagram"]`, so `shop-knol render diagram <name> --to DIR` writes `<DIR>/<name without kind>.mmd`. `When the user publishes the process as a diagram into a directory` gives `result`.

- [ ] **Step 1: Run it red**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-19 2>&1 | grep -E "StepDefinitionNotFound|passed|failed" | head -3
```

Expected: `StepDefinitionNotFoundError` for When "the user publishes the process as a diagram into a directory", then `1 failed, 61 deselected`.

- [ ] **Step 2: The steps, and run it red again**

Append to `tests/test_publish_what_the_shop_knows.py`:

```python


@when("the user publishes the process as a diagram into a directory", target_fixture="result")
def _publish_as_a_diagram(env, process_name, target):
    return knol(env, "render", "diagram", process_name, "--to", str(target))


@then("that directory holds a diagram of the process's steps and their branches")
def _a_diagram(result, target):
    """One node a step, in order and numbered, the reused step drawn as a subroutine; a step without branches goes on to
    the next, and a step with them goes where each says, labelled with its condition. Nothing places a node."""
    assert result.returncode == 0, result.stderr
    assert [path.name for path in target.iterdir()] == ["restock-a-shelf.mmd"]
    assert (target / "restock-a-shelf.mmd").read_text().splitlines() == [
        "flowchart TD",
        '    step1[["1. Check it"]]',
        '    step2["2. Decide"]',
        '    step3["3. Order more"]',
        '    step4["4. Stop"]',
        "    step1 --> step2",
        '    step2 -->|"the shelf is short"| step3',
        '    step2 -->|"it is not"| step4',
        "    step3 --> step4",
    ]
```

The Then asks for the file's exact lines, so a node's shape, its label and every edge are pinned. The directory listing pins that the diagram is the only file written.

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m slice-19 2>&1 | grep -E "^E  |passed|failed" | head -2
```

Expected: `E       AssertionError: usage: shop-knol render [-h] --to DIR {skill} locator`, then `E         shop-knol render: error: argument renderer: invalid choice: 'diagram' (choose from 'skill')`.

- [ ] **Step 3: The renderer, named for `shop-knol render`**

Create `src/shop_knowledge/renderers/diagram.py`:

```python
"""The diagram renderer: a process as a Mermaid flowchart, laid out by whatever draws it, so nothing here places a node.
Each step is a node numbered in the process's order, a reused step drawn as a subroutine. A step without branches goes
on to the next; a step with branches goes where each says, the edge labelled with its condition."""
from kb.content import loads
from kb.contract import kb_pb2

from shop_knowledge.renderers.rendered import Rendered, refused


def render(client, name: str) -> Rendered:
    """The diagram's file by path, the process's name without its kind, or the faults of the read that could not be
    made."""
    process = client.Read(kb_pb2.ReadRequest(locator=kb_pb2.Locator(id=name), level=kb_pb2.ReadRequest.WHOLE))
    if process.faults:
        return refused(process.faults)
    slug = process.id.split("/", 1)[1]
    return Rendered({f"{slug}.mmd": flowchart(loads(process.content).get("steps", []))}, [])


def flowchart(steps: list[dict]) -> str:
    """Every step's node, then every edge between them, top to bottom."""
    nodes = {step["id"]: f"step{number}" for number, step in enumerate(steps, 1)}
    lines = ["flowchart TD"]
    lines += [_node(nodes[step["id"]], number, step) for number, step in enumerate(steps, 1)]
    for step, following in zip(steps, [*steps[1:], None]):
        lines += _edges(step, following, nodes)
    return "\n".join(lines) + "\n"


def _node(node: str, number: int, step: dict) -> str:
    """A step by its number and title; a reused step in the subroutine shape."""
    label = f'"{number}. {step["title"]}"'
    return f"    {node}[[{label}]]" if "uses" in step else f"    {node}[{label}]"


def _edges(step: dict, following: dict | None, nodes: dict) -> list[str]:
    """Where a step goes: each branch's step, labelled with its condition, or else the step after it, if there is one.
    A branch to a name no step of the process has goes to that name as written."""
    node = nodes[step["id"]]
    if "branches" in step:
        return [
            f'    {node} -->|"{branch["when"]}"| {nodes.get(branch["go_to"], branch["go_to"])}'
            for branch in step["branches"]
        ]
    return [f"    {node} --> {nodes[following['id']]}"] if following else []
```

In `src/shop_knowledge/renderers/__init__.py`, replace:

```python
from shop_knowledge.renderers import skill

RENDERERS = {"skill": skill.render}
```

with:

```python
from shop_knowledge.renderers import diagram, skill

RENDERERS = {"diagram": diagram.render, "skill": skill.render}
```

`cli.py` is not touched: `render`'s `choices=sorted(RENDERERS)` now offers `diagram`, and `_render` refuses and writes what it gives back as it does the skill's.

- [ ] **Step 4: Run it green, the suite, and the shape check**

```bash
cd /home/vscode/shopsystem-knowledge && .venv/bin/python -m pytest -q -m "slice-19 or slice-18 or slice-17" 2>&1 | tail -1 && make test 2>&1 | grep -E "^[0-9]+ failed" && .venv/bin/python -m pytest -q -m "slice-1 or slice-1.17 or slice-1.24 or slice-1.27 or slice-1.28 or slice-4 or slice-15 or slice-16 or slice-17 or slice-18 or slice-19" 2>&1 | tail -1
```

Expected: `3 passed, 59 deselected`, then `49 failed, 13 passed`, then `13 passed, 49 deselected`: every slice through 19 is green, so the 49 failures are all tagged 20 or later. Then the shape check (Global Constraints): `2`, `1`, `1`, nothing, `0`.

- [ ] **Step 5: Checkpoint and commit**

Set slice 19's status to green and append to the very end of the log (verify with `tail -3`):

```markdown
- 2026-09-27 slice 19 green. A user can now: publish a process into a directory as a Mermaid diagram of its steps and their branches, `<name>.mmd`, which places no node itself.
  Assumption "steps and branches carry enough structure to draw the diagram without hand layout": held. The steps' order gives each step without branches its next step, each branch gives a labelled edge to the step it names, and a reused step is known from its own item, so the renderer reads the process whole once and nothing else; Mermaid lays the flowchart out. Evidence: <the .mmd the scenario publishes, complete>.
  Surprised by: <anything, or "nothing">.
  Open questions:
  - QUESTION FOR THE SPEC: the spec names the file `<id>.mmd`; it is `<name>.mmd`, the process's name without its kind, as the skill's directory is. Literally `<id>` would put it at `process/<name>.mmd`.
  - QUESTION FOR THE SPEC (Review Focus 1): a step title or branch condition holding `"` gives a label Mermaid cannot parse (`step1["1. Greet with "hi""]`), and the command exits 0.
  - QUESTION FOR THE SPEC (Review Focus 2): `shop-knol render diagram tag/pricing` writes `pricing.mmd` holding only `flowchart TD` and succeeds; so does a process with no steps.
  - QUESTION FOR THE SPEC (Review Focus 3): a branch whose go_to names no step is drawn to a bare node of that name.
  - QUESTION FOR THE SPEC (Review Focus 4): `render diagram --to` a path that is a file gives a `FileExistsError` traceback.
  - QUESTION FOR THE SPEC (Review Focus 5): no Mermaid tool is installed here, so the bet's "needs manual arrangement to be readable" is judged by a person opening the file, not by the suite.
  Next: slice 19.1.
```

```bash
cd /home/vscode/shopsystem-knowledge && git add src/shop_knowledge tests docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md && git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit -q -m "Slice 19: publish a process as a diagram

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>" && git status --short
```

Expected: `git status --short` prints nothing.

After Task 1: `make test` gives `49 failed, 13 passed`, every failure tagged 20 or later. Next in the slice plan is slice 19.1, the second architecture review, over slices 4 to 19.
