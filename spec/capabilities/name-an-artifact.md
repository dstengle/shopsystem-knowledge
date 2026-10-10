---
id: capability/name-an-artifact
title: Name an artifact
narrator: the user, naming an artifact to any shop-knol command
rests_on:
  - decision/an-artifacts-iri-is-its-types-then-its-owners-path
  - decision/names-are-iris-printed-short
  - decision/shop-context-names-the-context
  - decision/shop-knol-makes-no-name-from-a-title
  - decision/a-type-is-shown-by-its-name-and-version
  - decision/a-type-beside-an-artifact-is-shown-at-the-version-it-conforms-to
depends_on: []
formulated_as: features/name-an-artifact.feature
---

# Name an artifact

## Purpose

Every name shop-knol takes or prints is an IRI: its type, then its owner's domain, product, bounded context and name. This capability covers how the user names an artifact to any command, short or full, anywhere, or by its name alone in the context `SHOP_CONTEXT` names, and how a name is shown back. Choosing an artifact's name when it is created is record-an-artifact; finding the knowledge base the name is read in is find-the-knowledge-base.

## Behaviour

- Whenever shop-knol shows the user the name of an artifact, the name is shown short, in a JSON answer as in a YAML one.
- Whenever shop-knol shows the user the name of a shop or a product, the name is shown short, in a JSON answer as in a YAML one.
- Whenever shop-knol shows the user a type beside an artifact, the type is shown by its name and the version that artifact names, the one it was last written against, in a JSON answer as in a YAML one.
- Whenever shop-knol shows the user a type on its own, the type is shown by its name and its current version, in a JSON answer as in a YAML one.
- When the user names an artifact by its short IRI, the command works on that artifact, whatever context it is in.
- When the user names an artifact by its full IRI, the command works on that artifact, whatever context it is in.
- Where `SHOP_CONTEXT` names a context, when the user names an artifact by its name alone, the command works on the artifact of that name in that context.
- Where `SHOP_CONTEXT` names a context, when the user names an artifact by its type and its name, the command works on the artifact of that type and name in that context.
- Where `SHOP_CONTEXT` names a context, if the user names an artifact by its name alone and artifacts of more than one type in that context carry that name, the command is refused because the name is ambiguous, naming each of those artifacts.
- If the user names an artifact by a name that is neither a short nor a full IRI while `SHOP_CONTEXT` is not set, the command is refused because no context is named, naming `SHOP_CONTEXT`.
- If the user names an artifact by a name that is neither a short nor a full IRI while `SHOP_CONTEXT` is set empty, the command is refused because `SHOP_CONTEXT` names no context.

## Implementation, may change

```
type IRI         https://missingmass.io/shopsystem/<type>
version IRI      https://missingmass.io/shopsystem/<type>@<n>
artifact IRI     <type IRI>/<owner>/<product>/<context>/<name>
shop IRI         <type IRI>/<owner>/<product>/<context>        a shop is its context
product IRI      <type IRI>/<owner>/<product>                  a product is its product
part IRI         <artifact IRI>#<collection>/<part name>
```

- A short IRI is a fixed prefix for each of the shop's types in place of the type's IRI: `capability:missingmass.io/shopsystem/shop-knowledge/find-the-knowledge-base`. kb holds no prefixes; shop-knol expands a short IRI before calling kb.
- A shop is shown short like any artifact: `shop:missingmass.io/shopsystem/shop-knowledge`.
- A type is shown as `<type>@<n>`, e.g. `capability@2`.
- `SHOP_CONTEXT` is written `<owner>/<product>/<context>`, e.g. `SHOP_CONTEXT=missingmass.io/shopsystem/shop-knowledge`. Under it, `find-the-knowledge-base` and `capability/find-the-knowledge-base` both name `capability:missingmass.io/shopsystem/shop-knowledge/find-the-knowledge-base`.
- One module owns IRIs: building one from type, owner, product, context and name, and the prefixes that shorten and expand them. Every command and renderer uses it.

## Not yet

Nothing deferred.
