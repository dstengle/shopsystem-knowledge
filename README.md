# shopsystem-knowledge

The shop's interface to its knowledge base: the artifact types, the seed
content, the renderers, and the `shop-knol` command line. A client of
[kb](https://github.com/dstengle/shopsystem-kb).

Design: `docs/superpowers/specs/2026-09-23-shop-knowledge-design.md`.

## Developing

Python 3.11, with `shopsystem-kb` checked out beside this repository.
`make dev` installs kb editable from that checkout and this package editable
(`KB=<path> make dev` if it lives elsewhere). `python -m pytest -q` runs the
feature suite; `python -m pytest -q -m slice-1` runs one slice.
