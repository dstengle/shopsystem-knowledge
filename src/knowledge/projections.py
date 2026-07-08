"""Single-source projection generation.

The public entry point is :func:`generate_projections`, which turns one source
decision document (YAML frontmatter + Markdown body) into the full set of
architecture-decision projections:

* an **L0 card** carrying the ``id``, ``title``, ``status`` and ``description``
  drawn from the frontmatter;
* an **L1 extract** carrying the verbatim text of the recognized decision
  section from the body;
* an **L2 projection** that is the source document itself;
* a **machine index entry** and a **human index entry**, both derived from the
  same frontmatter.

No projection may introduce a fact that is not present in the single source.

This module is the thin RED-leg surface. The behaviour is unimplemented on
purpose so the outer-loop scenario (@scenario_hash:d121b489919c177e) fails for
the right reason; the GREEN leg fills in the concrete projection types and the
generation logic behind this signature.
"""

from __future__ import annotations


def generate_projections(source: str):
    """Generate the architecture-decision projections from a single source.

    Parameters
    ----------
    source:
        The full text of one source decision document: YAML frontmatter
        (``id``, ``title``, ``status``, ``description``) followed by a Markdown
        body carrying a recognized decision section heading.

    Returns
    -------
    A projections bundle exposing ``l0`` (id/title/status/description card),
    ``l1`` (verbatim recognized-decision-section extract), ``l2`` (the source
    document itself), ``machine_index_entry`` and ``human_index_entry`` — all
    derived from the single source, introducing no fact absent from it.

    Raises
    ------
    NotImplementedError
        Always, until the GREEN leg implements the behaviour.
    """
    raise NotImplementedError(
        "generate_projections is not implemented yet (RED leg for "
        "@scenario_hash:d121b489919c177e)"
    )
