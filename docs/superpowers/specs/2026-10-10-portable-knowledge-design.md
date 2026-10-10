# Portable knowledge: shop-knowledge on IRIs, exported after every change, and markdown specs migrated

Proposal, 2026-10-10. Decided by the person in a brainstorming session; the decisions are adrs/0071-0076,
0079, 0081 and 0082 here (0070, 0077, 0078 and 0080 superseded in the session) and shopsystem-kb/adrs/0022-0031.
Rests on the requests to kb in docs/superpowers/specs/2026-10-10-requests-to-kb-portable-knowledge.md.

## Why

The shop's specs are to move from markdown into kb, with the files published from kb (adrs/0052). Two things
stand in the way:

- An id kb mints from a title means something in one store only, so a link survives a move only into a fresh
  store. A product's contexts link to each other and to the product's lead shop, so neither a context nor a
  product can be moved, exported or restored on its own.
- Nothing keeps the shop's knowledge if the kb server is lost, which matters most early on.

kb's part is requested of it: ids are IRIs the client chooses, under their type's; each type version has an IRI
of its own; a link may land on a placeholder; export is a streamed call of the contract; import goes into any
store; a store is backed up and restored whole; a create may name its parts. This proposal is shop-knowledge's
part, and the way the two existing markdown specs are moved.

## Identity

An artifact's IRI is its type's IRI, then its owner's domain, product, bounded context and name (adrs/0073):

```
type IRI         https://missingmass.io/shopsystem/<type>
version IRI      https://missingmass.io/shopsystem/<type>@<n>
artifact IRI     <type IRI>/<owner>/<product>/<context>/<name>
shop IRI         <type IRI>/<owner>/<product>/<context>        a shop is its context
product IRI      <type IRI>/<owner>/<product>                  a product is its product
part IRI         <artifact IRI>#<collection>/<part name>
```

For example `https://missingmass.io/shopsystem/capability/missingmass.io/shopsystem/shop-knowledge/find-the-knowledge-base`,
its first Behaviour line `…/find-the-knowledge-base#behaviour/answers-from-the-knowledge-base-found-upward`, kb's
decision `https://missingmass.io/shopsystem/decision/missingmass.io/shopsystem/kb/ids-minted-from-titles` (a decision's
name holds no number; its number is a field, and it is published as `adrs/0002-ids-minted-from-titles.md`), and
a hosted product's capability `https://missingmass.io/shopsystem/capability/missingmass.io/ecommercesite/catalog/browse-the-catalog`.

shop-knol shortens each of the shop's types by a fixed prefix, `capability:missingmass.io/shopsystem/shop-knowledge/find-the-knowledge-base`,
and kb holds no prefixes. `SHOP_CONTEXT` names the context a command works in (adrs/0082):
`SHOP_CONTEXT=missingmass.io/shopsystem/shop-knowledge` reads `find-the-knowledge-base` or
`capability/find-the-knowledge-base` there; a short or full IRI names an artifact anywhere; a bare name with no
`SHOP_CONTEXT` is refused, naming the variable.

## S1: shop-knowledge onto kb v2

Waits for kb's identity and export release (requests 2-10, kb.v2).

- **Types.** `init` furnishes the shop's types at their IRIs, each at its version IRI. Two gain a version
  (adrs/0076): the capability type a section "Implementation, may change", and the shop type a section for the
  mechanisms every command shares, both published again by `render spec`.
- **Names.** Every name shop-knol takes or prints is an IRI, printed short and taken short or full. The user names
  what they create: `create` and `apply` carry the artifact's name and may name its parts, and the constraint
  "kb mints the ids" is reversed. `@key` in a batch goes if kb drops it; links in a batch name IRIs.
- **Placeholders.** `read` and `refs` mark a link whose target is not held. `validate` reports each placeholder kb
  lists as a fault of the artifact linking to it, under its own rule, and fails; `render spec` refuses a shop
  whose published pages would link to one (adrs/0074).
- **Renderers** name pages and links from IRIs; a shop's own pages link to its own artifacts by name, as today.
- **Code.** One module owns IRIs: building one from type, owner, product, context and name, and the prefixes that
  shorten and expand them; every command and renderer uses it. Published files are named from the name in the
  artifact's IRI, and shop-knol makes no name from a title.

## S2: rendered and exported after every change

Waits for S1 (adrs/0071, 0075).

- `shop-knol export <dir>` writes kb's streamed export, whole or selected by context, into an empty directory.
- A request to shopsystem-bdd: after every round of changes applied, the controller publishes with `render spec`
  and exports with `shop-knol export`, and commits both.
- Losing the server is recovered from the operator's backup, history included (kb's request 1); the committed
  export is the readable copy, imported into any store.

## S3: migrating the two markdown specs

shopsystem-knowledge and shopsystem-kb are migrated once each, by an agent, not by code (adrs/0081).

- **The brief**, `docs/migrating-a-spec-into-kb.md`, written when kb's IRI grammar is settled: the IRI
  construction; that text is copied verbatim; and how the markdown maps onto the types:

  | from | to |
  |---|---|
  | `spec/index.md` | the shop: title, Purpose, Order of building, Testing, the shared mechanisms; each `**Title.** says … Tested in …` constraint a part with `tested_in`; a gist the agent writes |
  | the index's Composition | each capability's `order` and `gist` |
  | `spec/capabilities/*.md` | a capability: narrator, Purpose, Implementation, `rests_on` split by kind into decisions (`rests_on`) and capabilities (`depends_on`), `status: active`, each Behaviour line a part (`says` verbatim, a title the agent writes, the part named from it), each Not-yet entry a part (defers, trigger) |
  | `spec/decisions.md`, `adrs/` | a decision, named from its ledger id without any leading number: statement, date, `supersedes`, `extends`, `revisit_when`; number, title and Purpose from its ADR, or, for one with none, the next free number and Purpose from the ledger; a statement over 200 characters shortened, kept whole as Purpose |
  | `features/*.feature` | a feature formulating its capability; each scenario a part linking to the Behaviour line it formulates; `uses` left empty |

- **The loop.** The agent writes the batch, applies it to a scratch knowledge base (`shop-knol init`, `apply`,
  `validate`) until nothing is refused and nothing but the product is a placeholder, then publishes from the
  scratch knowledge base over a copy of the repository and compares until only layout differs.
- **The day of switching over**, when shopsystem-bdd's writers draft batches against kb (adrs/0079): the markdown
  is left unchanged, the agent runs the loop, the person approves the difference once, the batch is applied to the
  real knowledge base, published and committed, and kb is the source from then on.

## Order

1. kb K1 (backup and restore), requested first; a make target running `kb export` on the server's machine until
   then. The order is the session's assumption, not yet the person's.
2. kb K2 and K3 as one release (kb.v2).
3. S1, then S2, then the brief.
4. Each repository switches over when shopsystem-bdd's writers are ready.

## Not in this proposal

- Export of what changed since a position (kb adds it later, without breaking).
- Which types a shop commits in its export and which it leaves to the backup; the spec types are all committed
  until types such as transcripts arrive.
- Moving content between type versions.
- A skill for migrating; the brief is promoted to one if a third repository needs it.
- The product artifact for shopsystem; it is a placeholder until written.
