# shop-knowledge Design

Date: 2026-09-23
Status: Draft for review

## Purpose

shop-knowledge is the only interface a shopsystem user or agent uses to the
shop's knowledge base. It is a client of kb (repository `shopsystem-kb`),
and it owns everything the shop knows that kb does not: the artifact types,
the seed content, the renderers, and the command line.

## Depends on

kb's contract, pinned by version. shop-knowledge never touches kb's files
or git. It calls the contract through the in-process client today and a
network channel when a server exists, with no other change.

## What use will tell us

Each is a belief that only use can prove wrong. None is tested by a
scenario or ordered by a slice; they are what the shop's measurement loop
should watch once the system runs.

- **one-command-line-is-enough.** Users and agents need nothing but
  `shop-knol` to work with the shop's knowledge. Fails if a role needs
  another path to the corpus.
- **seven-types-close-the-loop.** Decision, feature, work item, role,
  process, step, and tag are enough until the crossover. Fails if the first
  operating-system feature needs an eighth.
- **shared-steps-get-used.** Processes reuse steps rather than restating
  them. Fails if every step ends up written inline.
- **tags-replace-flags-in-prose.** A tag artifact with integrity replaces
  flags written into prose. Fails if a flag reappears in a body.
- **renderers-match-the-harness.** A rendered skill or agent loads in the
  harness unchanged. Fails if the harness rejects one or someone edits the
  output.
- **a-diagram-is-derivable-from-steps.** A process's steps and branches
  carry enough structure to draw it without hand layout. Fails if a
  rendered diagram needs manual arrangement to be readable.
- **markdown-projection-reads-well-enough.** The generic markdown rendering
  is enough for a person reading a type with no renderer of its own. Fails
  if a new type gets a renderer just to be readable.
- **corpus-only-roles-work-without-a-shell.** A role allowed only
  `shop-knol` can do its whole job. Observed in use through the harness's
  permission allowlist, which shop-knowledge does not implement, so no
  scenario tests it here.
- **actor-and-message-are-tolerable.** Requiring who and why on every
  change does not slow agents down. Fails if agents pad or omit them.
- **passed-through-errors-are-actionable.** kb's artifact, path, and
  message are enough for a user to fix a rejected change. Fails if users
  need to read the schema to understand a rejection.
- **yaml-and-json-are-the-only-outputs.** Fails if a consumer needs another
  shape.
- **a-scenario-status-ledger-can-wait.** No scenario status is needed before
  the crossover. Fails if assignment cannot be tracked without one.

## The CLI

`shop-knol` is the working name. The store is found the way git finds a
repository, upward from the working directory to a directory holding
`kb/store.yaml`, or through `KB_ROOT` when set; none found, `KB_ROOT` naming no store, or
the working directory inside one store while `KB_ROOT` names another: the
command refuses and says which. The actor comes from `KB_ACTOR` as `role` or
`role:execution-id`.
Every mutating command requires an actor and `-m`.

| command | maps to |
|---|---|
| `shop-knol create <type> --from <file or ->` | Create |
| `shop-knol read <locator> [--section <title>] [--whole] [--resolve [<depth>]]` | Read at the chosen level; `--resolve` alone is depth 1 |
| `shop-knol write <locator> --from <file or ->` | Write |
| `shop-knol append <locator> --from <file or ->` | Append |
| `shop-knol delete <locator>` | Delete |
| `shop-knol apply --from <batch>` | Apply |
| `shop-knol list --type <type> [--where k=v ...] [--ids]` | List |
| `shop-knol refs <locator> --inbound|--outbound [--via f] [--type t] [--depth n]` | Refs |
| `shop-knol search <text> [--type t] [--in sections|fields|all]` | Search |
| `shop-knol journal [--artifact] [--actor] [--execution] [--since]` | Journal |
| `shop-knol snapshot --execution <id> <ids...>` | Snapshot |
| `shop-knol validate` | Validate |
| `shop-knol init <root>` | Init, which creates `<root>/kb/`, then loads the bootstrap set through Create; needs an actor but no `-m`, its messages are fixed; refused where `<root>/kb/` exists or `<root>` is inside a store |
| `shop-knol render <renderer> <id> --to <dir>` | client-side rendering |

Ids are minted by kb from titles and never supplied by the user; `create`
and `append` print the id kb chose. A file given to `--from` is read the way
kb reads content, as YAML 1.2, so a title that looks like a date or a yes
is still text when it reaches kb. Output is YAML by default and `--json`
for the same structure. Errors are
printed as returned by kb, with artifact, path, and message, and exit
non-zero. The boundary for a corpus-only role is a harness permission
allowlist of exactly `shop-knol *`.

## Bootstrap types

Schema artifacts for: `decision`, `feature`, `work-item`, `role`,
`process`, `step`, `tag`. Plus whatever data-type schemas the process and
feature schemas share through `$ref`.

All seven build on a `shop-artifact` base schema through kb's composition
mechanism, so the fields every shop artifact carries, such as owner,
status, and tags, are declared once.

- `process` declares a `steps` part collection whose items either define a
  step inline or carry `uses: <ref to step>` and `with: <bindings>`.
- `role` separates the harness contract fields from the corpus identity
  fields into two named field groups, so the `agent` renderer can copy one
  into frontmatter.
- `tag` is a title and description; a `tags` reference field on other types
  targets it.
- Scenario status over time is a ledger modelled later, not a field on the
  scenario and not a field on a work item.

## Renderers

Client code, invoked only by `shop-knol render`. Each reads the resolved
whole artifact, the stubs of its references, and its schema through the
contract, and writes files to the target directory.

- `skill` for `process`: `SKILL.md` in Anthropic's frontmatter-plus-body
  shape with resolved steps as the body.
- `agent` for `role`: `.claude/agents/<name>.md` with the harness field
  group as frontmatter and the prose sections as the body.
- `diagram` for `process`: `<id>.mmd` generated from steps and branches.
- `markdown` for any type: identity as heading, fields as a definition
  list, sections at their levels, parts as tables.

`skill` and `agent` validate their output against the limits the harness
publishes and fail rather than emit something it would reject.

## Not in this version

- Product-local or user-local extensions. When wanted, they are additional
  schema and renderer sets shop-knowledge loads; kb never learns of them.
- Any validation that kb's schema language cannot express. If one is
  needed, it runs client-side before the call and is not binding.

## Order of building

shop-knowledge and kb are one effort until the walking skeleton is green,
then two. The living plan lives here because this is where value is
observable.

1. Feature files for both are formulated in one session from both specs.
   This repo's scenarios are the outer loop; every kb scenario cites the
   scenario here that needs it.
2. Slice 1 is create a decision and read it back through `shop-knol`, and
   it may touch both repos. kb is an editable path dependency until then.
3. When slice 1 is green, kb is tagged 0.1 and this repo pins it. From
   then, a kb change needed here is a request to bump the pin, and each
   repo plans alone.

## Testing

Built with the shopsystem-bdd workflow. Feature files are formulated from
this spec, from the perspective of a shopsystem user at the command line.
kb is exercised through its in-process transport, never mocked.
