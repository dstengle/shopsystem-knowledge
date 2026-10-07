# 0051 The shop's types model the shopsystem-bdd spec

2026-10-07. The shop's types are reshaped to hold what shopsystem-bdd produces: `product`, `shop`, `capability` and `feature` (with scenarios as parts) are added or replaced, and `decision` is reshaped; `role`, `process`, `step`, `tag` and `work-item` stay. "Seven types close the loop" no longer holds. Terms: a shop manages one bounded context; a product is a group of shops, one product's knowledge base holds every shop's context, and a lead shop holds the product's own concerns. The user's decision.
