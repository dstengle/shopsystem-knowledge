# 0052 kb is the source of a shop's spec; its files are rendered

2026-10-07. A shop's `spec/`, `features/` and `adrs/` are rendered from kb by shop-knol and committed as generated files; shopsystem-bdd's agents read them, and read kb through a read-only `shop-knol` allowlist. Agents writing kb directly, with the files only a view, comes later. The user's decision.
