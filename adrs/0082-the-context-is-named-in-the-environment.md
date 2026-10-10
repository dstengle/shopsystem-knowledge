# 0082 The context a command works in is named in the environment

2026-10-10. `SHOP_CONTEXT` names the owner, product and context a shop-knol command works in (`missingmass.io/shopsystem/shop-knowledge`), beside `KB_ROOT` and `KB_ACTOR`. A bare name, or one with its kind, is read in that context; a short or full IRI always names an artifact wherever it is. A bare name with no `SHOP_CONTEXT` is refused, naming the variable. The user's decision.
