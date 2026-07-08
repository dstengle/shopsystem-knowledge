"""The shopsystem-knowledge bounded context.

Discovery-first knowledge context: generate every projection tier (L0/L1/L2)
and both index entries deterministically from a single source decision
document whose YAML frontmatter is the only machine truth.
"""

from knowledge.projections import (
    RECOGNIZED_DECISION_HEADINGS,
    L0Card,
    L1Extract,
    ProjectionBundle,
    extract_decision_section,
    generate_projections,
    parse_frontmatter,
)

__all__ = [
    "RECOGNIZED_DECISION_HEADINGS",
    "L0Card",
    "L1Extract",
    "ProjectionBundle",
    "extract_decision_section",
    "generate_projections",
    "parse_frontmatter",
]
