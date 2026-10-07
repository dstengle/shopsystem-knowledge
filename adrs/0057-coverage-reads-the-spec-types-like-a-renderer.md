# 0057 coverage reads the spec types as a renderer does

2026-10-07. `coverage.py`, which answers `shop-knol coverage`, may know the fields of the types it reads (a shop's `reading_order`, a capability's `behaviour`, a scenario's `formulates`), as a renderer for a type may, and it refuses a kb answer by raising `refusal.Refused` with the answer's faults, as `init.py` and the renderers do, beside `cli._answered`. CLAUDE.md's rule 5 and its "Size and shape" section name it. Found by batch 16's branch review; a ruling under the person's delegation (adrs/0056).
