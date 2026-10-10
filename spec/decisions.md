# Decisions

## decision/bdd-replaces-tdd
Work follows the shopsystem-bdd pipeline instead of TDD; approved Gherkin feature files are the functional contract, and approving them is the one human gate.
date: 2026-09-22
source: adrs/0001-bdd-replaces-tdd.md

## decision/bdd-plugin-in-its-own-repo
The BDD plugin is github.com/dstengle/shopsystem-bdd, its own single-plugin marketplace installed user-wide, never extracted from a component repository.
date: 2026-09-22
source: adrs/0002-plugin-in-its-own-repo.md

## decision/slices-by-observability
A slice is end to end, as thin as possible, and settles one unknown. It is verified by scenarios (capability) or by a check command (enabling), ordered by risk with the walking skeleton first, and only @slice tags are written into feature files.
date: 2026-09-23
source: adrs/0003-slices-by-observability.md

## decision/kb-and-shop-knowledge-split
The knowledge base is two repositories: kb, a domain-agnostic, schema-typed artifact store with a protobuf contract; and shop-knowledge, the shop's client owning types, seed content and renderers. kb never learns a domain type.
date: 2026-09-23
source: adrs/0004-kb-and-shop-knowledge-split.md

## decision/model-split
Execution runs on Sonnet with Opus reviewers; formulation, slicing and plans run on Opus; the interactive design session runs on Fable; every headless session names its model.
date: 2026-09-24
source: adrs/0005-model-split.md

## decision/each-repo-plans-alone
After kb 0.1 each repository keeps its own slice plan; shop-knowledge pins kb by git tag, a kb change it needs is a request to bump the pin, and tags are the user's decision.
date: 2026-09-24
source: adrs/0006-each-repo-plans-alone.md

## decision/findings-placed-by-risk
A scenario or refactor found after slicing is placed among the remaining slices by risk, never ahead of the plan, and takes a dotted number.
date: 2026-09-24
source: adrs/0007-findings-placed-by-risk.md

## decision/gh-through-agent-vault
Every gh invocation runs through `agent-vault run -- gh ...`; bare gh is not used.
date: 2026-09-22
source: adrs/0008-gh-through-agent-vault.md

## decision/implement-on-main
Execution sessions work on main in the real checkout, because each checkout's virtualenv installs it editable.
date: 2026-09-24
source: adrs/0009-implement-on-main.md

## decision/architecture-review-every-six-slices
Each repository's CLAUDE.md states its module map, rules and size limits. After every six slices, an enabling slice reviews the code against it; behaviour changes found are logged as questions for the spec, not coded.
date: 2026-09-26
source: adrs/0010-architecture-review-every-six-slices.md

## decision/planner-writes-no-code
Implementation plans carry no code; implementers write it under bdd-red-green, reviewers verify for themselves, and architecture reviews run before planning.
date: 2026-09-27
source: adrs/0011-planner-writes-no-code.md

## decision/decisions-in-adrs-not-memory
Every decision is a short dated file in adrs/ of the repository it applies to; assistant memory holds no project knowledge.
date: 2026-09-27
source: adrs/0012-decisions-in-adrs-not-memory.md

## decision/kb-pinned-by-tag
kb v0.3.0 is pinned (after v0.2.0 and v0.2.1); shop-knowledge knows kb only through what it publishes: `kb.contract`, `kb.client.connect` with its clock, `kb.content` with `NotCanonical`, and the rule names.
date: 2026-09-28
revisit_when: kb tags a release that shop-knowledge needs
source: adrs/0013-kb-0-2-0-pinned.md

## decision/renderers-read-through-source
A renderer reads what it publishes through one source module that returns kb's answer as it is; the renderer hands faults back as its own, and the whole read defaults to depth 0.
date: 2026-09-27
source: adrs/0014-renderers-read-through-source.md

## decision/markdown-page-laid-out-from-content-model
The markdown page is `<name>.md`, laid out from kb's content model (title heading, field list in kb's order, sections a level below their holder), reading no schema and naming no type.
date: 2026-09-27
source: adrs/0015-markdown-page-laid-out-from-content-model.md

## decision/user-files-checked-against-shapes
A user's file is checked against a JSON Schema shape, one fault per violation. A non-UTF-8 file and an operating-system error on a path are faults naming the file, and the printer keeps each fault to one line.
date: 2026-09-27
source: adrs/0016-user-files-checked-against-shapes.md

## decision/answers-shaped-in-answers-py
Every kb answer shown to the user is turned into a plain document in one module, one function per answer; that module never prints, calls kb or reads arguments.
date: 2026-09-27
source: adrs/0017-answers-are-shaped-in-answers-py.md

## decision/read-levels-and-json
`read` takes `--section`, `--whole` and `--resolve [DEPTH]`: `--resolve` implies whole, `--section` wins, and `--json` (on read alone) writes the same document. kb finds the store and its refusals pass through.
date: 2026-09-27
source: adrs/0018-read-levels-and-json.md

## decision/a-part-is-named-with-a-hash
A locator is a name, or a name, `#` and a place (kb's link notation). A whole write's file is passed as given, and a part's file holds the part as kb holds it.
date: 2026-09-27
source: adrs/0019-a-part-is-named-with-a-hash.md

## decision/actor-and-message-asked-once
Actor and message are asked for once, before any file is read or kb is called. Unset and empty count the same, and each lack is its own fault.
date: 2026-09-27
source: adrs/0020-actor-and-message-asked-once.md

## decision/arguments-apart-from-handlers
Every command's arguments are declared with argparse in a module that knows no handler.
date: 2026-09-27
source: adrs/0021-arguments-apart-from-handlers.md

## decision/requests-built-apart-from-handlers
Each command's request to kb is built in a module of its own, which never prints, connects or calls kb.
date: 2026-09-27
source: adrs/0022-requests-built-apart-from-handlers.md

## decision/argument-errors-are-refusals
An argument shop-knol cannot take is refused as one fault: the command, then argparse's message, with exit 1 and no usage block. `-h` stays help on stdout with exit 0.
date: 2026-09-27
source: adrs/0023-argument-errors-are-refusals.md

## decision/follow-and-search
`refs` makes one Refs call: a direction is required, depth defaults to one step, and it answers nearest first with the route. `search` makes one Search call, defaults to sections, and answers with the match and a snippet. Neither answer has a wrapper key.
date: 2026-09-27
source: adrs/0024-follow-and-search.md

## decision/history-filters-and-snapshot
`journal` passes `--actor`, `--execution` and `--since` to kb as given. `snapshot` is a mutating command whose `--execution` replaces `KB_ACTOR`'s and whose answer is `entry`. An entry that read something shows `read`.
date: 2026-09-27
source: adrs/0025-history-filters-and-snapshot.md

## decision/append-and-delete
`append <name>#<collection>` adds one item and answers `<name>#<collection>/<item>` with the revision. `delete <name>` retires an artifact, and a delete refused because the artifact is still pointed at prints one line per thing pointing at it.
date: 2026-09-27
source: adrs/0026-append-and-delete.md

## decision/history-scenario-starts-the-store-as-founder
The history scenarios start the store as `founder`, because kb records the start and the types under the role that ran init.
date: 2026-09-27
source: adrs/0027-history-scenario-starts-the-store-as-founder.md

## decision/argument-errors-name-their-command
An argument refusal carries the refusing parser's prog and argparse's message, as one fault.
date: 2026-09-27
source: adrs/0028-argument-errors-name-their-command.md

## decision/the-checks-answer
A check that finds no fault shows `sound: true` with `behind:` (kb's stale artifacts) and exits 0. Being behind is never a fault.
date: 2026-09-27
source: adrs/0029-the-checks-answer.md

## decision/init-refuses-kbs-answers
Init's answer, and each Create of the bootstrap set, passes through the one refusal path, stopping at the first refusal; a directory that does not exist is refused in kb's words.
date: 2026-09-27
source: adrs/0030-init-refuses-kbs-answers.md

## decision/the-agent-renderer
`agent` publishes a role as `.claude/agents/<name>.md`, with the `harness` group as its heading block and the sections, from level 1, as its body, sharing the markdown page's section layout.
date: 2026-09-27
source: adrs/0031-the-agent-renderer.md

## decision/an-arguments-meaning-is-declared-once
An argument's type and default are declared only where the argument is declared. `refs --depth` defaults to 1, and `--resolve` keeps "not given" as a meaning of its own.
date: 2026-09-27
source: adrs/0032-an-arguments-meaning-is-declared-once.md

## decision/the-section-layout-is-shared
The layout of a content model's sections lives in one place: the markdown renderer uses it from level 2, the agent renderer from level 1.
date: 2026-09-27
source: adrs/0033-the-section-layout-is-shared.md

## decision/size-limit-covers-step-definitions
The 250-line module limit holds under `tests/` as it does under `src/`.
date: 2026-09-27
source: adrs/0034-the-size-limit-covers-the-step-definitions.md

## decision/a-features-steps-split-into-a-sibling-module
When a feature's steps pass the limit, one concern's steps move to a sibling module that only that feature's test module star-imports.
date: 2026-09-27
source: adrs/0035-a-features-steps-split-into-a-sibling-module.md

## decision/every-batch-is-pushed
An execution session pushes main when its batch is green and reviewed, and a planning session pushes its plan.
date: 2026-09-27
source: adrs/0036-every-batch-is-pushed.md

## decision/init-defaults-to-the-working-directory
`init` starts the knowledge base in the working directory by default; naming a directory starts one elsewhere on purpose.
date: 2026-09-27
source: adrs/0037-init-defaults-to-the-working-directory.md

## decision/markdown-never-shows-a-repr
Every value on a markdown page is laid out as markdown, and a language's representation on a page is a defect.
date: 2026-09-27
source: adrs/0038-markdown-never-shows-a-repr.md

## decision/spec-settles-what-needs-no-approval
A scenario that follows from an unambiguous passage of the spec needs no approval; only a scenario that decides something open, or changes an approved scenario's meaning, waits.
date: 2026-09-27
source: adrs/0039-the-spec-settles-what-needs-no-approval.md

## decision/an-agents-limits-are-its-names
An agent is held to the two limits the harness's subagent documentation publishes for `harness.name`: no `:`, and no leading `-`. No length limit is checked.
date: 2026-09-27
revisit_when: the harness's subagent documentation publishes another limit
source: adrs/0040-an-agents-limits-are-its-names.md

## decision/markdown-lays-out-lists-and-tables
On a markdown page, a list of plain values is a bullet list and a list of mappings is a table after the field list. Where a block cannot sit, a value is laid out inline.
date: 2026-09-27
source: adrs/0041-markdown-lays-out-lists-and-tables.md

## decision/init-starts-where-the-user-works
With no directory named, `init` starts in the working directory as an absolute path and never reads `KB_ROOT`, which finds a store that exists, while init makes one.
date: 2026-09-27
source: adrs/0042-init-starts-where-the-user-works.md

## decision/markdown-spells-yes-no-and-nothing-in-words
On a markdown page a yes is `yes`, a no is `no`, and an empty value is nothing; the user chose this over YAML's own spelling.
date: 2026-09-27
source: adrs/0043-markdown-spells-yes-no-and-nothing-in-words.md

## decision/a-case-a-spec-principle-answers-is-settled
A case one of the spec's principles answers is settled and sliced; only a case no principle answers, or two answer differently, goes to the user as a question.
date: 2026-09-27
revisit_when: shopsystem-bdd carries this rule itself
source: adrs/0044-a-case-a-spec-principle-answers-is-settled.md

## decision/an-empty-list-is-an-empty-value
On a markdown page an empty list is laid out as an empty value is; the user chose one spelling of nothing.
date: 2026-09-27
source: adrs/0045-an-empty-list-is-an-empty-value.md

## decision/a-failing-check-still-shows-what-is-behind
A check that finds faults refuses with them and also shows `sound: false` with the `behind:` list on stdout, because the user chose the whole finding in one run. Supersedes the last three sentences of the-checks-answer; the rest of it stands.
date: 2026-09-27
supersedes: decision/the-checks-answer
source: adrs/0046-a-failing-check-still-shows-what-is-behind.md

## decision/kb-only-through-its-published-contract
No code or test knows kb beyond what it publishes. A state no contract call can produce comes from a stand-in at the contract boundary, and no test reaches a knowledge base outside its own temporary directory.
date: 2026-09-27
source: adrs/0047-kb-only-through-its-published-contract.md

## decision/shared-steps-split-beside-conftest
When conftest.py would pass the limit, one concern's shared steps move beside it, star-imported by conftest.py alone.
date: 2026-09-27
source: adrs/0048-shared-steps-split-beside-conftest.md

## decision/shop-knol-reaches-kb-wherever-kb-finds-it
shop-knol does nothing different whether kb finds the store or a connection to a server hosting it, so roles in containers work through a shared server. Tests reach only a server they started.
date: 2026-09-28
source: adrs/0049-shop-knol-reaches-kb-wherever-kb-finds-it.md

## decision/store-found-like-git
A command finds its store the way git finds a repository, upward from the working directory, or through `KB_ROOT`. When nothing is found, or the two disagree, it refuses and says which.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/actor-from-kb-actor
The actor comes from `KB_ACTOR` as `role` or `role:execution-id`, and every mutating command requires an actor and `-m`.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/ids-minted-by-kb
Ids are minted by kb from titles and never supplied by the user.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/yaml-1-2-the-way-kb-reads
Every file shop-knol reads or writes, its own output included, is YAML 1.2 read the way kb reads content, so a title that looks like a date or a yes is still text when it reaches kb.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/init-beside-the-shops-work
`init` creates `<root>/kb/` with `<root>` defaulting to the working directory, since the shop's knowledge sits beside the shop's work. Naming a root exists only to start a knowledge base somewhere else on purpose.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/seven-types-on-a-shop-artifact-base
The bootstrap set is decision, feature, work-item, role, process, step and tag, all built on a `shop-artifact` base through kb's composition so the fields every shop artifact carries are declared once.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/role-splits-harness-from-identity
`role` keeps the harness contract fields and the corpus identity fields in two named field groups, so the agent renderer can copy one into frontmatter.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/a-tag-is-an-artifact
`tag` is a title and a description, targeted by a `tags` reference field on other types.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/renderers-are-client-code
Renderers are client code invoked only by `shop-knol render`; `skill` and `agent` check their output against the limits the harness publishes and fail rather than emit what it would reject.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/corpus-only-boundary-is-the-harness-allowlist
The boundary for a corpus-only role is a harness permission allowlist of exactly `shop-knol *`, which the harness enforces and shop-knowledge does not implement.
date: 2026-09-23
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/one-command-line-is-enough
Users and agents need nothing but `shop-knol` to work with the shop's knowledge.
date: 2026-09-23
revisit_when: a role needs another path to the corpus
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/seven-types-close-the-loop
Decision, feature, work item, role, process, step and tag are enough until the crossover.
date: 2026-09-23
revisit_when: the first operating-system feature needs an eighth type
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/shared-steps-get-used
Processes reuse steps rather than restating them.
date: 2026-09-23
revisit_when: every step ends up written inline
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/tags-replace-flags-in-prose
A tag artifact with integrity replaces flags written into prose.
date: 2026-09-23
revisit_when: a flag reappears in a body
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/renderers-match-the-harness
A rendered skill or agent loads in the harness unchanged.
date: 2026-09-23
revisit_when: the harness rejects a rendered skill or agent, or someone edits the output
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/a-diagram-is-derivable-from-steps
A process's steps and branches carry enough structure to draw it without hand layout.
date: 2026-09-23
revisit_when: a rendered diagram needs manual arrangement to be readable
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/markdown-projection-reads-well-enough
The generic markdown rendering is enough for a person reading a type that has no renderer of its own.
date: 2026-09-23
revisit_when: a new type gets a renderer just to be readable
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/corpus-only-roles-work-without-a-shell
A role allowed only `shop-knol` can do its whole job; this is observed in use through the harness's permission allowlist, not tested by a scenario here.
date: 2026-09-23
revisit_when: a role allowed only `shop-knol` cannot do its whole job
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/actor-and-message-are-tolerable
Requiring who and why on every change does not slow agents down.
date: 2026-09-23
revisit_when: agents pad or omit the actor or the message
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/passed-through-errors-are-actionable
kb's artifact, path and message are enough for a user to fix a rejected change.
date: 2026-09-23
revisit_when: users need to read the schema to understand a rejection
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/yaml-and-json-are-the-only-outputs
YAML and JSON are the only output shapes.
date: 2026-09-23
revisit_when: a consumer needs another shape
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/a-scenario-status-ledger-can-wait
No scenario status is needed before the crossover.
date: 2026-09-23
revisit_when: assignment cannot be tracked without one
source: docs/superpowers/specs/2026-09-23-shop-knowledge-design.md

## decision/types-are-readable
The user can at least see which types the shop holds and read one; defining or changing a type is not offered until product-local or user-local extensions are wanted.
date: 2026-10-05
source: the person, 2026-10-05 ("types should be readable at the very least")

## decision/init-furnishes-an-empty-knowledge-base
`shop-knol init` sets up an empty knowledge base with the shop's types, including one that kb's operator started empty, in place or reached through a server; the outcome is a knowledge base holding the shop's types and nothing else of the shop's yet.
date: 2026-10-05
source: the person, 2026-10-05

## decision/json-where-a-command-offers-it
Answers are YAML, with JSON (the same structure) only where a command offers it, which today is `read` alone (read-levels-and-json); this narrows the design note's general `--json`.
date: 2026-10-05
source: the person, 2026-10-05

## decision/agent-renderer-refuses-a-non-role-and-checks-limits
Two sentences of the-agent-renderer are superseded: an artifact that is not a role is refused, not published with an empty heading block (scenario slice-50.15); and an agent is held to the harness's published limits (an-agents-limits-are-its-names). The rest of the-agent-renderer stands.
date: 2026-10-05
supersedes: decision/the-agent-renderer
source: the person, 2026-10-05

## decision/init-refuses-a-knowledge-base-holding-the-shops-types
If the knowledge base init meets already holds the shop's types, starting is refused because it already holds the shop's knowledge, and nothing changes.
date: 2026-10-05
source: the person, 2026-10-05

## decision/init-furnishes-only-an-empty-knowledge-base
init furnishes only an empty knowledge base; one holding anything else (other types, or content) is refused because it is not empty, naming what it holds.
date: 2026-10-05
source: the person, 2026-10-05

## decision/init-furnishes-the-knowledge-base-kb-finds
With no directory named, init furnishes the knowledge base kb finds from the working directory (upward, through `KB_ROOT`, or a connection to a server) when it was started empty, and starts one in the working directory only where nothing is found; naming a directory still starts one there on purpose. This supersedes only the sentence of init-starts-where-the-user-works that says init never reads `KB_ROOT`; the rest of that entry stands.
date: 2026-10-05
supersedes: decision/init-starts-where-the-user-works
source: the person, 2026-10-05

## decision/types-have-a-command-of-their-own
Reading the shop's types, and any later defining or changing of them, is a command of its own, not `list`, `read`, `create` or `write`, because a type has a greater impact on the knowledge store than an artifact.
date: 2026-10-05
source: the person, 2026-10-05 ("Reading and especially writing types should be a separate command due to the greater impact to the knowledge store.")

## decision/furnishing-waits-for-the-kb-v0-5-0-migration
Furnishing a knowledge base that kb's operator started is not built on the kb v0.3.0 pin; it is built after the kb v0.5.0 migration that follows this one.
date: 2026-10-05
revisit_when: the kb v0.5.0 migration lands
source: the person, 2026-10-05

## decision/init-edge-cases-settled-by-principle
Three cases are settled by principles already decided (a-case-a-spec-principle-answers-is-settled): a named directory holding a knowledge base kb's operator started empty is furnished (init-furnishes-an-empty-knowledge-base); with no directory named, a finding that refuses refuses init for the same reason (store-found-like-git); a knowledge base holding the shop's types and other content too is refused as already holding the shop's knowledge.
date: 2026-10-05
source: the person, 2026-10-05 (approved at the spec gate)

## decision/kb-v0-5-0-pinned
kb v0.5.0 is pinned, which publishes contract v1 as one breaking release. shop-knowledge knows kb only through what kb publishes: `kb.contract`, `kb.client.connect` with its clock, `kb.content` with `NotCanonical`, the rule names, and now `kb.init` and `kb.NotStarted` (kb's index, Constraints carried).
date: 2026-10-05
revisit_when: kb tags a release that shop-knowledge needs
supersedes: decision/kb-pinned-by-tag
source: docs/superpowers/specs/2026-10-05-kb-v0-5-0-migration.md

## decision/a-batch-holds-one-kind-of-change
`shop-knol apply` takes a batch of one kind of change, all creates or all writes. kb v0.5.0 lands a set of one kind of change only, and a set that mixes kinds of change is gone from what a client can do.
date: 2026-10-05
source: docs/superpowers/specs/2026-10-05-kb-v0-5-0-migration.md

## decision/the-batch-scenarios-record-two-linked-creates
The approved scenario "The user makes several changes at once" changes its meaning. Its batch, once a create and a write (a decision recorded and an existing work item pointed at it), now records a decision and a work item pointing at it: two creates linked by a key. Its Thens stand: both are in the shop, and the history shows one change. "A batch whose prose the shop cannot keep leaves the shop untouched" uses the same batch and changes the same way.
date: 2026-10-05
source: docs/superpowers/specs/2026-10-05-kb-v0-5-0-migration.md

## decision/furnishing-is-built-on-kb-v0-5-0
Furnishing is buildable on kb v0.5.0 because a client starts a store with `kb.init`. Where kb finds an empty knowledge base that kb's operator started, in place or through a server, init loads the shop's types into it without starting anything. It starts a store with `kb.init` only where it starts one.
date: 2026-10-05
supersedes: decision/furnishing-waits-for-the-kb-v0-5-0-migration
source: docs/superpowers/specs/2026-10-05-kb-v0-5-0-migration.md

## decision/the-command-line-survives-contract-v1
Under contract v1 the commands, their flags and their answers stay as they are. `write`, `append`, `delete`, `refs`, `journal` and `validate` keep their names, and their answers keep their keys: an answer still says `type`, not kb's `kind`.
date: 2026-10-05
source: docs/superpowers/specs/2026-10-05-kb-v0-5-0-migration.md

## decision/moving-an-earlier-store-is-the-operators-kb-import
Moving a knowledge base made by an earlier kb into a v0.5.0 store is the operator's `kb import`, not a shop-knol command.
date: 2026-10-05
source: docs/superpowers/specs/2026-10-05-kb-v0-5-0-migration.md

## decision/a-working-directory-holding-the-shops-knowledge-keeps-its-reasons
init keeps both jobs: it starts a store where none is found, and furnishes an empty one it finds. With no directory named, a working directory that holds the shop's knowledge is refused because it already holds a knowledge base, and one inside it because it is inside a knowledge base, as today. The refusal "already holds the shop's knowledge" covers only a knowledge base found through `KB_ROOT` or a server, or sitting in a named directory. The rest of init-refuses-a-knowledge-base-holding-the-shops-types stands.
date: 2026-10-05
supersedes: decision/init-refuses-a-knowledge-base-holding-the-shops-types
source: the person, 2026-10-05

## decision/only-a-create-carries-a-key
A write in a batch that carries a key is refused because only a create carries a key, naming the key, and none of the batch's changes land; the batch shape allows `key` only beside `create`.
date: 2026-10-05
source: the person, 2026-10-05

## decision/tests-reach-a-server-only-through-kbs-double
A scenario that needs a kb server gets it from a served-store double kb publishes for its clients' tests; shop-knowledge's tests never start `kb serve` or write `kb/server.yaml` themselves, and its scenarios that need a server wait until kb publishes the double. Supersedes the testing sentence of shop-knol-reaches-kb-wherever-kb-finds-it (a server the test starts in its own temporary directory on a port of its own); the rest of that entry stands.
date: 2026-10-06
supersedes: decision/shop-knol-reaches-kb-wherever-kb-finds-it
source: the person, 2026-10-06 ("I'd prefer that this start using a mock provided by kb")

## decision/naming-a-directory-inside-a-knowledge-base-is-refused
Naming a directory that sits inside a knowledge base but holds none of its own is refused because that directory is inside a knowledge base, and nothing changes: init neither furnishes nor names the knowledge base above it. Settled by principle (a-case-a-spec-principle-answers-is-settled): start-a-knowledge-base's Purpose (init refuses rather than nest the shop's knowledge) and its Implementation (kb.init's refusal for a directory inside a store reaches the user in kb's words). Found by batch 15's branch review, after kb v0.6.0 began searching upward from a root given to `connect`.
date: 2026-10-07
source: the person's delegation, 2026-10-07 ("Please proceed and work independently")

## decision/the-shops-types-model-the-bdd-spec
The shop's types model what shopsystem-bdd produces for each shop (its index, capabilities, decision records and feature files), and one product's knowledge base holds every one of its shops, each managing one bounded context.
date: 2026-10-07
supersedes: decision/seven-types-close-the-loop
source: adrs/0051-the-shops-types-model-the-bdd-spec.md

## decision/ten-types-on-a-shop-artifact-base
The shop's types are ten, all on the `shop-artifact` base (owner, status, tags): `role`, `process`, `step`, `tag` and `work-item` as they were, `feature` replaced, `decision` reshaped, and `product`, `shop` and `capability` new.
date: 2026-10-07
supersedes: decision/seven-types-on-a-shop-artifact-base
source: adrs/0051-the-shops-types-model-the-bdd-spec.md

## decision/old-feature-and-decision-artifacts-are-not-converted
Artifacts of the old `feature` and `decision` types are not converted when the types change, because no knowledge base in use holds any.
date: 2026-10-07
source: docs/superpowers/specs/2026-10-07-spec-system-types-design.md

## decision/kb-is-the-source-of-the-spec
A shop's spec, ledger, decision records and feature files are published from the knowledge base by the `spec` publisher, and each published file says it is not to be edited by hand.
date: 2026-10-07
source: adrs/0052-kb-is-the-source-of-the-spec.md

## decision/spec-writes-are-batches-applied-after-the-gate
shopsystem-bdd's writer agents draft `shop-knol apply` batch files and read kb only through `shop-knol read`, `list`, `refs`, `search` and `types`; the controller validates the drafts before the gate, applies the creates and then the writes after it, publishes the shop's spec and commits it.
date: 2026-10-07
source: adrs/0053-spec-writes-are-batches-applied-after-the-gate.md

## decision/every-decision-is-an-adr
Every decision in a shop's ledger is a decision artifact the knowledge base holds, numbered as the shop's next and published as its ADR; no ledger entry stands alone.
date: 2026-10-07
source: adrs/0054-every-decision-is-an-adr.md

## decision/short-fields-for-progressive-disclosure
Progressive disclosure is a rule of every type: what a glance shows is one short line or a link, every part carries a short title, and long prose lives in sections and part body fields; kb checks the short lines through limits written into the types.
date: 2026-10-07
source: adrs/0055-short-fields-for-progressive-disclosure.md

## decision/a-shop-names-its-decisions
A decision carries no link to a shop; a shop names its decisions through an optional `decisions` field, and the shop's decisions (the ledger's own entries, its ADR records, the numbers judged for collisions) are those it names, so the approved scenarios that see what a decision points at, and a glance's stubs, are unchanged.
date: 2026-10-07
source: the person's delegation, 2026-10-07, slicing batch 16

## decision/a-ragged-table-is-refused
A feature table whose rows have different widths is refused when the shop's spec is published, rather than laid out or crashed on, by the principle that shop-knol never shows a traceback and refuses in plain words.
date: 2026-10-07
source: the person's delegation, 2026-10-07, batch 16's branch review (small-change path)

## decision/a-decision-links-to-its-shop
A decision links to its one shop through a required `shop` shown at a glance, and a shop's decisions are those linking to it, because kb answers a link from either end and each fact is held in one direction only; following the links out of a decision, and its glance, now show its shop.
date: 2026-10-08
supersedes: decision/a-shop-names-its-decisions
source: adrs/0058-a-decision-links-to-its-shop.md

## decision/a-ledger-holds-only-the-shops-own-decisions
A shop's ledger lists only the shop's own decisions, in number order; a capability resting on a decision of another shop is refused when the shop's spec is published.
date: 2026-10-08
source: adrs/0059-a-ledger-holds-only-the-shops-own-decisions.md

## decision/capabilities-depend-on-capabilities
A capability names the capabilities it builds on, in any shop, through `depends_on`, kept apart from `rests_on`; a scenario is part of its capability and its `uses` names only dependencies of that capability, in its own shop or another; who depends on a capability is a query, not a stored list.
date: 2026-10-08
source: adrs/0060-capabilities-depend-on-capabilities.md

## decision/a-capability-carries-its-reading-order
A capability carries its place in its shop's reading order as a dotted number, sorted numerically part by part, so a capability can be inserted without renumbering; a shop no longer lists its capabilities.
date: 2026-10-08
source: adrs/0061-a-capability-carries-its-reading-order.md

## decision/capabilities-are-deprecated-then-retired
A capability's status is active, deprecated or retired. Removing one is three checked steps: deprecate it, remove its spec and code through the shop's normal work, retire it. Retiring is the shop's own act on its public contract, accepted whatever depends on it elsewhere; other shops find out when they publish or ask, and act on their own schedule.
date: 2026-10-08
source: adrs/0062-capabilities-are-deprecated-then-retired.md

## decision/uses-is-kept-and-checked-for-consistency
A scenario's `uses` is kept, and `shop-knol validate` reports as a fault every scenario whose `uses` names a capability not among its capability's `depends_on`, across the whole knowledge base, whichever shop it is in.
date: 2026-10-08
source: adrs/0064-uses-is-kept-and-checked-for-consistency.md

## decision/a-constraint-is-tested-in-capabilities
A shop's constraint names the capabilities whose scenarios show its promise holds through `tested_in`, replacing `pinned_in`, and the published index writes `Tested in <names>.`; a constraint tested in a retired capability stops the publish.
date: 2026-10-08
source: adrs/0065-a-constraint-is-tested-in-capabilities.md

## decision/an-unreadable-file-stops-the-publish
When publishing a shop's spec finds, among the files it may delete, one it cannot read, the publish is refused naming the file, and nothing is written or deleted.
date: 2026-10-08
source: adrs/0066-an-unreadable-file-stops-the-publish.md

## decision/this-repositorys-capabilities-declare-depends-on
Every capability of this repository's `spec/` lists the capabilities it builds on under a `depends_on` frontmatter key after `rests_on`, and `rests_on` keeps decisions only.
date: 2026-10-08
source: adrs/0067-this-repositorys-capabilities-declare-depends-on.md

## decision/a-renamed-shop-field-is-not-converted
The shop type's constraint field renamed from `pinned_in` to `tested_in` keeps the type's version, and shops recorded under the old name are not converted, because no knowledge base in use holds shops; settled as old-feature-and-decision-artifacts-are-not-converted was.
date: 2026-10-08
source: the person's delegation (adrs/0068), batch 18's branch review

## decision/a-fault-is-printed-with-its-rule
Every fault shop-knol prints names its rule, `artifact at place: rule: message`, leaving out `rule: ` when a fault carries none, as kb's own command line words a refusal.
date: 2026-10-08
source: adrs/0069-a-fault-is-printed-with-its-rule.md

## decision/an-artifacts-iri-is-its-types-then-its-owners-path
An artifact's IRI is its type's IRI, then its owner's domain, product, bounded context and name; a shop's IRI ends at its context, a product's at its product, a part's is its artifact's with `#<collection>/<part name>`, and a type version's is its type's with `@<n>`.
date: 2026-10-10
source: adrs/0073

## decision/the-user-names-what-they-create
The user names what they create: `create` and `apply` carry the artifact's name and may name its parts, a part not named being named by kb from its title, and links in a batch name IRIs; kb no longer mints an artifact's id from its title.
date: 2026-10-10
supersedes: decision/ids-minted-by-kb
source: docs/superpowers/specs/2026-10-10-portable-knowledge-design.md, shopsystem-kb/adrs/0022, shopsystem-kb/adrs/0031

## decision/names-are-iris-printed-short
Every name shop-knol takes or prints is an IRI, printed short and taken short or full; shop-knol shortens each of the shop's types by a fixed prefix, and kb holds no prefixes.
date: 2026-10-10
source: docs/superpowers/specs/2026-10-10-portable-knowledge-design.md

## decision/shop-context-names-the-context
`SHOP_CONTEXT` names the context a command works in: a name, alone or after its type, is read in that context; a short or full IRI names an artifact anywhere; a bare name with no `SHOP_CONTEXT` is refused, naming the variable.
date: 2026-10-10
source: adrs/0082

## decision/the-capability-and-shop-types-gain-a-version
Two of the shop's types gain a version: the capability type an optional section "Implementation, may change", and the shop type an optional section "Mechanisms every command shares", both published by `render spec`, the shop's under "Constraints carried".
date: 2026-10-10
source: adrs/0076

## decision/a-placeholder-fails-validate-and-stops-the-publish
`validate` reports each placeholder kb lists as a fault of the artifact linking to it, under a rule of its own, and fails; `render spec` refuses a shop whose published pages would link to a placeholder.
date: 2026-10-10
source: adrs/0074

## decision/published-files-are-named-from-the-iri
A published file is named from the name in its artifact's IRI, never from its title: a capability's page and the feature file formulating it from the capability's, and a decision's record, `adrs/<number>-<name>.md`, from the decision's.
date: 2026-10-10
source: docs/superpowers/specs/2026-10-10-portable-knowledge-design.md

## decision/rendered-and-exported-after-every-change
After every round of changes applied, the shop's spec is published with `render spec` and its knowledge exported with `shop-knol export`, and both are committed.
date: 2026-10-10
source: adrs/0071, adrs/0075

## decision/a-markdown-spec-is-migrated-once-by-an-agent
shopsystem-knowledge and shopsystem-kb are each migrated into kb once, by an agent following a brief, not by code: it writes a batch, applies it to a scratch knowledge base until nothing is refused and nothing but the product is a placeholder, then publishes over a copy of the repository and compares until only layout differs.
date: 2026-10-10
source: adrs/0081

## decision/a-repository-switches-over-when-the-writers-draft-against-kb
A repository switches its spec over to kb when shopsystem-bdd's writers draft batches against kb: its markdown is left unchanged, the agent runs the migration loop, the person approves the difference once, the batch is applied to the real knowledge base, published and committed, and kb is the source from then on.
date: 2026-10-10
source: adrs/0079

## decision/a-decisions-name-holds-no-number
A decision's IRI name holds no number: the number is its `number` field alone, and its record is published as `adrs/<padded number>-<name>.md`, so the ledger and the records stay in number order as before.
date: 2026-10-10
source: docs/superpowers/specs/2026-10-10-portable-knowledge-design.md (the person's answer, 2026-10-10)

## decision/shop-knol-makes-no-name-from-a-title
shop-knol makes no name from a title: every artifact is named by the user and every published file from the name in its IRI, so nothing is left to make a name from a title for.
date: 2026-10-10
source: docs/superpowers/specs/2026-10-10-portable-knowledge-design.md (the person's answer, 2026-10-10)
