"""Typed-edge coherence checks: the corpus graph's cross-artifact edge invariants.

Where :mod:`knowledge.coherence` folds the *artifact-lifecycle* checks over an
:class:`~knowledge.coherence.ArtifactCorpus`, this module adds the **typed-edge**
checks — the invariants of the *graph* the corpus forms once its frontmatter
link fields are read as edges. It defines the one canonical set of resolvable
link fields (:data:`LINK_FIELDS`), resolves the corpus into a deterministic edge
set (:func:`resolve_edges`), and supplies a registry of checks
(:data:`TYPED_EDGE_CHECKS`) that runs through the *same*
:func:`~knowledge.coherence.run_coherence_gate` fold and verdict machinery — a
new check tuple, not a re-spelled aggregate.

The edge model is deliberately narrow and deterministic:

* **Edges are frontmatter-only.** An id resolves into a graph edge exactly when
  it appears as the value (or a list entry) of one of the :data:`LINK_FIELDS`
  frontmatter fields. An id mentioned only in body prose forms **no** edge — the
  gate never scrapes prose — so promoting a load-bearing prose reference into a
  link field is the deliberate act that turns it into a resolved edge.
* **Every edge target must resolve.** A link field naming a target absent from
  the corpus is a ``dangling-edge`` finding.
* **A supersede must be symmetric and acyclic, and retire its target.** A
  ``supersedes`` edge to a present target that carries no ``superseded-by``
  back-edge is an ``asymmetric-supersede`` finding; an artifact carrying a
  ``superseded-by`` edge whose status is not ``superseded`` is an
  ``active-yet-superseded`` finding; a cycle in the supersede graph is a
  ``supersede-cycle`` finding.

The ``governed-delta`` invariant tripwire is **opt-in**: it is evaluated only
against artifacts that register a governed-delta invariant (a truthy
``governed-delta`` frontmatter field naming a governed surface) and skips every
artifact that registers none. :func:`evaluated_governed_delta_subjects` exposes
exactly which artifacts the tripwire ranges over.

Every check is a pure ``(corpus, config) -> list[Finding]`` function of the same
shape the lifecycle registry uses, so the two registries compose through one
fold.
"""

from __future__ import annotations

from dataclasses import dataclass

from knowledge.artifact_types import Artifact
from knowledge.coherence import (
    ArtifactCorpus,
    Check,
    CoherenceConfig,
    Finding,
    Severity,
)

# The canonical set of resolvable link fields: the frontmatter fields whose
# values are artifact ids (or lists of ids) and therefore form graph edges. This
# is the single source both the dangling-edge check and the edge-resolution pass
# share — a field outside this tuple is never read as an edge, and body prose is
# never read as an edge at all.
LINK_FIELDS: tuple[str, ...] = (
    "supersedes",
    "superseded-by",
    "derives-from",
    "session",
    "brief",
    "candidate",
    "produced",
    "incorporates",
)

# The frontmatter field an artifact opts into the governed-delta tripwire with.
# A truthy value registers the artifact; a mapping may name the governed surface
# under ``surface``.
GOVERNED_DELTA_FIELD = "governed-delta"


def _id_str(artifact: Artifact) -> str:
    """The artifact's id as a string (``""`` when absent or non-string)."""
    return artifact.id if isinstance(artifact.id, str) else ""


def _link_targets(artifact: Artifact, field: str) -> list[str]:
    """The string id targets a ``field`` link resolves to.

    A scalar id yields a single-element list; a list field yields its string
    entries in order; an unset, empty, or non-id value yields ``[]``. This is
    how a list-valued ``supersedes`` and a scalar ``brief`` are read uniformly.
    """
    value = artifact.frontmatter.get(field)
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, (list, tuple)):
        return [entry for entry in value if isinstance(entry, str) and entry]
    return []


@dataclass(frozen=True)
class Edge:
    """One resolved graph edge derived from a frontmatter link field.

    Attributes
    ----------
    source:
        The id of the artifact carrying the link field.
    link_field:
        The link field the edge was read from (one of :data:`LINK_FIELDS`).
    target:
        The id the link field names.
    resolved:
        Whether :attr:`target` is present in the corpus. A ``False`` value is a
        dangling edge.
    """

    source: str
    link_field: str
    target: str
    resolved: bool


def resolve_edges(corpus: ArtifactCorpus) -> tuple[Edge, ...]:
    """Resolve ``corpus`` into its deterministic set of frontmatter link edges.

    Every :data:`LINK_FIELDS` value on every artifact becomes an :class:`Edge`,
    in ``(artifact order, LINK_FIELDS order, value order)``. An edge whose target
    is present in the corpus is :attr:`~Edge.resolved`; one whose target is
    absent is a dangling edge. Body prose is never consulted — an id mentioned
    only in prose forms no edge.
    """
    by_id = corpus.by_id
    edges: list[Edge] = []
    for artifact in corpus.artifacts:
        source = _id_str(artifact)
        if not source:
            continue
        for field in LINK_FIELDS:
            for target in _link_targets(artifact, field):
                edges.append(Edge(source, field, target, target in by_id))
    return tuple(edges)


def check_asymmetric_supersede(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """A ``supersedes`` edge to a present target must carry a back-edge.

    For each present target of a ``supersedes`` link, the target must name the
    source back in its ``superseded-by`` field. A missing per-pair back-edge is a
    finding naming the source and that one target. Absent targets are left to the
    dangling-edge check.
    """
    findings: list[Finding] = []
    for artifact in corpus.artifacts:
        source = _id_str(artifact)
        if not source:
            continue
        for target in _link_targets(artifact, "supersedes"):
            target_art = corpus.get(target)
            if target_art is None:
                continue  # a dangling supersede is the dangling-edge check's job
            if source not in _link_targets(target_art, "superseded-by"):
                findings.append(
                    Finding(
                        check_id="asymmetric-supersede",
                        check_name="supersede carries no back-edge",
                        severity=Severity.BLOCKING,
                        subjects=(source, target),
                        message=(
                            f"artifact '{source}' supersedes '{target}', but "
                            f"'{target}' carries no superseded-by back-edge to "
                            f"'{source}'"
                        ),
                        remediation=(
                            f"write the superseded-by back-edge on '{target}' "
                            f"naming '{source}'"
                        ),
                    )
                )
    return findings


def check_active_yet_superseded(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """An artifact carrying a ``superseded-by`` edge must be status ``superseded``.

    An artifact whose ``superseded-by`` field names some newer artifact is
    superseded and must set its status to ``superseded``; any other status is a
    finding naming that artifact.
    """
    findings: list[Finding] = []
    for artifact in corpus.artifacts:
        superseders = _link_targets(artifact, "superseded-by")
        if not superseders:
            continue
        if artifact.status == "superseded":
            continue
        aid = _id_str(artifact)
        findings.append(
            Finding(
                check_id="active-yet-superseded",
                check_name="superseded artifact is not status superseded",
                severity=Severity.BLOCKING,
                subjects=(aid,),
                message=(
                    f"artifact '{aid}' is superseded by "
                    f"{', '.join(superseders)} but its status is "
                    f"'{artifact.status}', not superseded"
                ),
                remediation=f"set the status of artifact '{aid}' to superseded",
            )
        )
    return findings


def check_dangling_edge(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """Every frontmatter link-field target must resolve to a present artifact.

    A target present in the corpus as a **legacy file** (an id in
    :attr:`~knowledge.coherence.ArtifactCorpus.legacy_ids`) is *not* dangling —
    it resolves to a real file, so it is the unverifiable-legacy check's job
    (:func:`check_unverifiable_legacy`), not this one's. Only a target with no
    file at all — absent from both the typed index and the legacy set — is
    dangling.
    """
    findings: list[Finding] = []
    for edge in resolve_edges(corpus):
        if edge.resolved:
            continue
        if edge.target in corpus.legacy_ids:
            continue  # present-but-untyped legacy: unverifiable, not dangling
        findings.append(
            Finding(
                check_id="dangling-edge",
                check_name="link field names an absent target",
                severity=Severity.BLOCKING,
                subjects=(edge.source, edge.target),
                message=(
                    f"artifact '{edge.source}' declares a {edge.link_field} edge "
                    f"to '{edge.target}', which is not present in the corpus"
                ),
                remediation=(
                    f"add the missing artifact '{edge.target}' to the corpus, or "
                    f"remove the {edge.link_field} edge from '{edge.source}'"
                ),
            )
        )
    return findings


def check_unverifiable_legacy(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """A link-field target resolving to a present-but-untyped legacy file is advisory.

    An edge whose target carries no YAML frontmatter (an id in
    :attr:`~knowledge.coherence.ArtifactCorpus.legacy_ids`) resolves to a real
    file, but the gate can read neither its type nor its back-edges — so the
    edge cannot be verified for symmetry, incorporation, or any typed invariant.
    This is reported as an **advisory** ``unverifiable-legacy`` finding naming
    the source and the legacy target; it does not by itself drive the aggregate
    verdict non-zero. Because the target is present, it is *not* a dangling edge
    (:func:`check_dangling_edge` skips it); because the legacy file has no
    frontmatter to carry a ``superseded-by`` back-edge, a legacy ``supersedes``
    target is *not* an asymmetric-supersede finding either
    (:func:`check_asymmetric_supersede` already skips a target absent from the
    typed index).
    """
    findings: list[Finding] = []
    for edge in resolve_edges(corpus):
        if edge.resolved:
            continue
        if edge.target not in corpus.legacy_ids:
            continue
        findings.append(
            Finding(
                check_id="unverifiable-legacy",
                check_name="link field targets a present-but-untyped legacy file",
                severity=Severity.ADVISORY,
                subjects=(edge.source, edge.target),
                message=(
                    f"artifact '{edge.source}' declares a {edge.link_field} edge "
                    f"to '{edge.target}', which is present as a legacy file "
                    f"carrying no frontmatter, so the edge cannot be verified"
                ),
                remediation=(
                    f"add YAML frontmatter to legacy file '{edge.target}' so its "
                    f"type and back-edges can be verified, or remove the "
                    f"{edge.link_field} edge from '{edge.source}'"
                ),
            )
        )
    return findings


def _supersede_sccs(corpus: ArtifactCorpus) -> list[tuple[str, ...]]:
    """The strongly connected components of the supersede graph, size > 1 or self-loop.

    Edges run source -> target for each present ``supersedes`` target; Tarjan's
    algorithm yields the SCCs, and a component is a cycle when it has more than
    one node or a node supersedes itself. Each returned component is ordered by
    id so the finding it drives is deterministic.
    """
    adjacency: dict[str, list[str]] = {}
    for artifact in corpus.artifacts:
        source = _id_str(artifact)
        if not source:
            continue
        adjacency.setdefault(source, [])
        for target in _link_targets(artifact, "supersedes"):
            if corpus.get(target) is not None:
                adjacency[source].append(target)

    index_counter = [0]
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[tuple[str, ...]] = []

    def strongconnect(node: str) -> None:
        indices[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack.add(node)
        for neighbour in adjacency.get(node, ()):
            if neighbour not in indices:
                strongconnect(neighbour)
                lowlink[node] = min(lowlink[node], lowlink[neighbour])
            elif neighbour in on_stack:
                lowlink[node] = min(lowlink[node], indices[neighbour])
        if lowlink[node] == indices[node]:
            component: list[str] = []
            while True:
                member = stack.pop()
                on_stack.discard(member)
                component.append(member)
                if member == node:
                    break
            is_cycle = len(component) > 1 or node in adjacency.get(node, ())
            if is_cycle:
                components.append(tuple(sorted(component)))

    for node in adjacency:
        if node not in indices:
            strongconnect(node)
    return components


def check_supersede_cycle(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """The supersede graph must be acyclic."""
    findings: list[Finding] = []
    for component in _supersede_sccs(corpus):
        named = ", ".join(component)
        findings.append(
            Finding(
                check_id="supersede-cycle",
                check_name="supersede graph contains a cycle",
                severity=Severity.BLOCKING,
                subjects=component,
                message=(
                    f"the artifacts {named} form a supersede cycle, so no one of "
                    f"them cleanly supersedes the others"
                ),
                remediation=(
                    f"break the supersede cycle among {named} by removing one of "
                    f"the supersedes edges"
                ),
            )
        )
    return findings


def _governed_surface(value: object) -> object | None:
    """The governed surface a ``governed-delta`` registration names, if any."""
    if isinstance(value, dict):
        return value.get("surface")
    if isinstance(value, str) and value:
        return value
    return None


def _registers_governed_delta(artifact: Artifact) -> bool:
    """Whether ``artifact`` opts into the governed-delta tripwire."""
    value = artifact.frontmatter.get(GOVERNED_DELTA_FIELD)
    return value is not None and value != "" and value != {} and value != []


def governed_delta_registrants(corpus: ArtifactCorpus) -> tuple[str, ...]:
    """The ids of the artifacts that register a governed-delta invariant."""
    return tuple(
        _id_str(artifact)
        for artifact in corpus.artifacts
        if _registers_governed_delta(artifact)
    )


def evaluated_governed_delta_subjects(corpus: ArtifactCorpus) -> tuple[str, ...]:
    """The ids the governed-delta tripwire is evaluated against.

    The tripwire is opt-in, so it ranges over exactly the registrants — an
    artifact that registers no governed-delta invariant is never evaluated.
    """
    return governed_delta_registrants(corpus)


def check_governed_delta_tripwire(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """Evaluate the governed-delta invariant tripwire against registrants only.

    A non-registrant is skipped entirely. A registrant must name a governed
    surface for the invariant to bind to; a registration naming none is a
    finding. A well-formed registrant draws no finding.
    """
    findings: list[Finding] = []
    for artifact in corpus.artifacts:
        if not _registers_governed_delta(artifact):
            continue
        if _governed_surface(artifact.frontmatter.get(GOVERNED_DELTA_FIELD)):
            continue
        aid = _id_str(artifact)
        findings.append(
            Finding(
                check_id="governed-delta-without-surface",
                check_name="governed-delta invariant names no surface",
                severity=Severity.BLOCKING,
                subjects=(aid,),
                message=(
                    f"artifact '{aid}' registers a governed-delta invariant but "
                    f"names no governed surface for it to bind to"
                ),
                remediation=(
                    f"name the governed surface the governed-delta invariant on "
                    f"'{aid}' ranges over"
                ),
            )
        )
    return findings


# The typed-edge check registry, in report order. It runs through the same
# :func:`~knowledge.coherence.run_coherence_gate` fold the lifecycle registry
# uses — a new tuple, not a re-spelled aggregate.
TYPED_EDGE_CHECKS: tuple[Check, ...] = (
    check_asymmetric_supersede,
    check_active_yet_superseded,
    check_dangling_edge,
    check_unverifiable_legacy,
    check_supersede_cycle,
    check_governed_delta_tripwire,
)
