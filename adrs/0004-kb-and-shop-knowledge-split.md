# 0004 The knowledge base is two repositories

2026-09-23. kb (github.com/dstengle/shopsystem-kb) is a domain-agnostic, schema-typed, graph-oriented artifact store with a protobuf contract and in-process transport. shop-knowledge (this repository, CLI shop-knol) is the shop's client: bootstrap schemas, seed content, renderers. kb never learns a domain type. kb's features are written from a contract client's perspective, shop-knowledge's from a CLI user's.
