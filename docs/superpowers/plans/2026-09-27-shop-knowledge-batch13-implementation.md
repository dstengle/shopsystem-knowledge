# shop-knowledge batch 13: slices 50.16.8 to 50.18.3

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Each task is one or two slices of `docs/superpowers/plans/2026-09-23-shop-knowledge-slices.md`, in slice order, with one commit per slice. Task 1 is an enabling slice checked by its check. Tasks 2 to 4 are capability slices, built one scenario at a time under shopsystem-bdd:bdd-red-green.

**This plan carries no code** (adrs/0011).

**Goal:** every approved scenario is green, and shop-knowledge knows kb only through what kb v0.3.0 (released 2026-09-27) publishes. The work, in order:
- 50.16.8 makes room;
- 50.17 refuses a name given empty, everywhere a place is named;
- 50.18 and 50.18.1 cover a removed directory at `init`, and prose kb cannot keep;
- 50.18.2 and 50.18.3 cover markdown's remaining well-formed cases, and a check with no store to check.
- 50.22 pins kb v0.3.0 and reads from a removed directory;
- 50.23 takes nothing of kb but what it publishes.

The ninth architecture review runs after the batch, by a ruling: the batch is eight slices, and the review meets its cadence at the batch's end.

**Spec:** `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`, especially these passages:
- the CLI section: "Every refusal of shop-knol's own says in plain words what was refused and names the place it concerns ... A name given empty names no place and is refused"; "shop-knol never shows a traceback"; the store-finding sentence with the removed working directory; the validate row;
- the markdown bullet.

Read CLAUDE.md, adrs/0035, 0044 and 0047, and kb's adrs/0018. The eighth architecture review is `.superpowers/batch13/arch-review-50.16.7.md`; its section 4 gives Task 1 in full.

## Global Constraints

**Change control**
- Feature files are read-only, tag lines included.
- kb is v0.2.1 until Task 5 pins v0.3.0, and is never edited here.
- Every rule in CLAUDE.md holds.
- shop-knowledge knows kb only through what kb publishes. The known exceptions until 50.23 are listed in CLAUDE.md rule 1.

**Where to work**
- Work on `main`, and run every command from the checkout's root.
- Scratch goes under `.superpowers/batch13/`. Never create a file outside this repository's `.superpowers/`, and never export `GIT_*` variables. `/home/vscode` is shared with the kb checkout.

**Commits**
- Commit with `git -c user.name="David Stenglein" -c user.email=dave@missingmass.io commit`, the message ending with the model's Co-Authored-By line.
- One commit per slice, each holding its checkpoint in the slice plan's Log and its Status set to green.
- The implementer never pushes.

**Counts**
- The suite collects 101 scenarios (100 after the user removed the step scenario on 2026-09-28) and gives `80 passed, 21 failed` today.
- The tags select 50.17: 4; 50.18: 1; 50.18.1: 5; 50.18.2: 10, of which 4 already pass; 50.18.3: 3; 50.22: 2.

| after | failed | passed |
|---|---|---|
| 50.16.8 | 21 | 80 |
| 50.17 | 17 | 84 |
| 50.18 | 16 | 85 |
| 50.18.1 | 11 | 90 |
| 50.18.2 | 5 | 96 |
| 50.18.3 | 2 | 99 |
| 50.22 | 0 | 100 |
| 50.23 | 0 | 100 |

**Checks**
- Record the failing list at each slice's start with `.venv/bin/python -m pytest -q -rf | grep ^FAILED | sort`.
- The size check lists nothing at each slice's end.

---

### Task 1: Slice 50.16.8, the code makes room for batch 13, and batch 12's minors are tidied

**Check:** the eighth review's R-A to R-E, each check exactly as section 4 of the review states it. The suite is unchanged.

**Where it lands:** as section 4 says.
- For R-D, the concern that leaves `cli.py` is the file a user gives: `_document`, with what it needs. It is the concern 50.18.1 grows. If `Refused` must move to avoid an import cycle, it moves too, and CLAUDE.md's rule 4 and Size and shape sentences are reworded to name where each now lives.
- R-B's shared Thens compare with `driver.kb_answer` for the call the When made.

**Steps:**
- [ ] R-A.
- [ ] R-B.
- [ ] R-C.
- [ ] R-D.
- [ ] R-E.
- [ ] Run every check.
- [ ] Checkpoint and commit.

### Task 2: Slice 50.17, a name given empty is refused

**Scenarios** (`@slice-50.17`, 4):
- the start feature's empty directory name;
- record's empty file name;
- read-back's empty artifact name;
- publish's empty target directory.

**Unknown:** whether an empty name can be refused for every argument that names a place, the one way every argument refusal is refused (adrs/0023), with each argument's meaning still declared once (adrs/0032).

**Why red:**
- The four scenarios fail today on `StepDefinitionNotFoundError`.
- Once their steps exist, `init ""` fails because argparse types `""` as the path `.` and starts a store where the user works. The other three reach kb or the operating system.

**Where it lands:**
- `arguments.py`: every argument that names a place (`init`'s root, every `--from`, a locator, `render`'s `--to`) refuses an empty value, through one type or check that `ArgumentRefused` carries, so `cli.main` prints it the one way.
- The refusal says in plain words that the name is empty and names no place (the spec).
- The steps go beside each feature's other steps, or in the sibling modules Task 1 made. A step two features share goes in `conftest.py`.

**Steps:**
- [ ] Take the `init` scenario first, red then green.
- [ ] Take the other three, each seen red first or credited to the change that made it green.
- [ ] Checkpoint and commit.

### Task 3: Slices 50.18 and 50.18.1

**50.18: starting a knowledge base from a removed directory says the directory is gone** (1 scenario, the rewritten start scenario).
- **Unknown:** whether shop-knol can tell a working directory that is gone apart from the operating system's other refusals, before kb is called.
- **Why red:** its Then "rejected because the directory they are working in is gone". Today `kb_requests.init_request` resolves the root, the operating system refuses, and `cli._run`'s `OSError` guard prints `No such file or directory`, which names nothing.
- **Where it lands:** where shop-knol reads its working directory for `init`, which is shop-knol's own code; kb is not called. The words are shop-knol's own. The step compares with the rule-free, plain line shop-knol prints; kb's words are not involved.

**50.18.1: prose the shop cannot keep is refused in plain words** (5 scenarios: record; revise, 2 rows; add a step; apply a batch).
- **Unknown:** whether text kb cannot keep is found where a user's file is read and checked, once, for every command that sends content.
- **Why red:** `kb.content.dumps` raises `NotCanonical` in `kb_requests` and `batch`, outside the reading of the user's file, and ends in a traceback. The batch 11 review reproduced this with `body: "a \nb\n"`.
- **Where it lands:**
  - The one place a user's file is read and checked (Task 1's new module for `_document`) also checks that its content can be kept, by the published `kb.content`'s own refusal.
  - The refusal is printed as kb returned it, naming the place.
  - The batch file goes through the same check for each change's content.
  - The Thens compare with `driver.kb_answer` or with kb's own refusal for the same text. They never spell kb's words.

**Steps:**
- [ ] 50.18 red then green; checkpoint and commit.
- [ ] 50.18.1, one scenario at a time; checkpoint and commit.

### Task 4: Slices 50.18.2 and 50.18.3

**50.18.2: markdown's remaining well-formed cases** (the well-formed outline's six red rows):
- a title ending in a space;
- a section title ending in a space;
- a list of lists with an empty last item;
- a list holding a mapping with an empty last value;
- a field group's list of mappings with an empty last value;
- a column name holding the cell separator.

**Why red:** the six rows fail on `StepDefinitionNotFoundError`, then on the page. There are three causes:
- `_inline` ends in a space whenever its last part is empty;
- headings are written as given;
- header cells take no cell escaping.

**Where it lands:** `renderers/markdown.py` and `renderers/sections.py`, still by kind and shape and never by a field's name (rule 5).
- The escape moves where the header cells take it too. That means `_row` or its caller, said once.
- A heading's and an inline value's trailing space is not shown, as the user approved for text.

**50.18.3: a check with no knowledge base to check shows no answer** (3 rows).
- **Why red:** the rows fail on `StepDefinitionNotFoundError`. The behaviour itself has been in place since 0c7d199.
- **Where it lands:** the check feature's steps, reusing the shared Givens and Thens Task 1 moved to `conftest.py`. The Then "shown no answer from a check" checks that stdout is empty.

**Steps:**
- [ ] 50.18.2, one row at a time; checkpoint and commit.
- [ ] 50.18.3; checkpoint and commit.

### Task 5: Slice 50.22, reading from a removed directory, refused or served through KB_ROOT, on kb v0.3.0

- **Needs, first:** `pyproject.toml` pins `shopsystem-kb @ git+https://github.com/dstengle/shopsystem-kb.git@v0.3.0`; `pip uninstall -y shopsystem-kb && make dev` installs it; the suite then gives the same answer as before the bump (`99 passed, 2 failed`, the 2 this slice's) — kb 0.3.0 keeps `kb.canonical`, `kb.journal.now` and `connect(root)`, so nothing else changes. Log the before/after.
- **Scenarios (`@slice-50.22`, 2):** read-back / Reading from a directory that has been removed ends in a plain refusal (rewritten); read-back / The user reads from a directory that has been removed, having named the knowledge base.
- **Why red:** until the pin, kb's client read the working directory before `KB_ROOT` and raised; kb 0.3.0 finds the store through `KB_ROOT` and otherwise answers with a `store` fault saying the working directory is gone.
- **Where it lands:** the steps; shop-knol passes kb's answer through as it does every refusal. The Then compares with kb's own answer for the same state; `driver.kb_answer` cannot chdir into a removed directory (batch 12 review), so the oracle runs where it can (for example, a subprocess of the same allowlisted environment that removes its own working directory, as the driver's `Removed` does), or the Then asserts the published `store` rule of the answer shop-knol relayed and that the line is kb's — the implementer's choice, logged. No kb wording spelled.

### Task 6: Slice 50.23, shop-knowledge imports nothing of kb but what kb publishes

- **Check:** as the slice plan states it (`grep -rhoE '^\s*(from kb[a-z_.]* import|import kb[a-z_.]*)' src tests | sort -u` -> only `kb.client`, `kb.content`, `kb.contract`; `grep -rn "kb.journal\|kb.canonical" src tests` -> nothing; `record_refused_files`' named-once Then catches `kb.content.NotCanonical` and takes the place from its `path`; CLAUDE.md's rule 1 names only what kb publishes, its exceptions gone); every scenario passes.
- **Where it lands:** `NotCanonical` from `kb.content` wherever Task 1 left it; `tests/clock/sitecustomize.py` stops replacing `kb.journal.now` and wraps `kb.client.connect` to give the clock kb publishes (`connect(root=None, *, clock=None)`), keeping `TEST_NOW`'s meaning (a second later at each stamp); the stand-in's `connect` takes and forwards `clock`; `driver`'s refusal to combine the clock and the stand-in stays while both are `sitecustomize` (or they are merged into one, said once). Nothing under `src/` knows.

## After the batch

- [ ] A whole-branch review on the most capable model.
- [ ] Push.
- [ ] Then, once kb 0.3.0 is tagged and pinned, slices 50.22 and 50.23, and the ninth review.
