"""The shopsystem-knowledge bounded context.

Discovery-first knowledge context: generate every projection tier (L0/L1/L2)
and both index entries deterministically from a single source decision
document whose YAML frontmatter is the only machine truth.
"""

from knowledge.adversarial import (
    AdversarialResult,
    Verdict,
    VerdictKind,
    run_adversarial_pass,
)
from knowledge.discovery import (
    DiscoveryResult,
    DraftDecision,
    L0L1Index,
    L0L1IndexEntry,
    Neighbour,
    build_l0l1_index,
    run_authoring_discovery,
)
from knowledge.projections import (
    ARCHITECTURE_DECISION_KIND,
    RECOGNIZED_DECISION_HEADINGS,
    CheckResult,
    KindProjections,
    KnowledgeContext,
    L0Card,
    L1Extract,
    ProjectionBundle,
    WriteResult,
    check_corpus,
    extract_decision_section,
    generate_corpus,
    generate_projections,
    parse_frontmatter,
    write_corpus,
)

__all__ = [
    "ARCHITECTURE_DECISION_KIND",
    "RECOGNIZED_DECISION_HEADINGS",
    "AdversarialResult",
    "CheckResult",
    "DiscoveryResult",
    "DraftDecision",
    "KindProjections",
    "KnowledgeContext",
    "L0Card",
    "L0L1Index",
    "L0L1IndexEntry",
    "L1Extract",
    "Neighbour",
    "ProjectionBundle",
    "Verdict",
    "VerdictKind",
    "WriteResult",
    "build_l0l1_index",
    "check_corpus",
    "extract_decision_section",
    "generate_corpus",
    "generate_projections",
    "parse_frontmatter",
    "run_adversarial_pass",
    "run_authoring_discovery",
    "write_corpus",
]
