"""L1 distribution: pour the decision digest to BCs, gated by the coherence check.

This is the boundary step that carries knowledge *out* of the context to the
bounded contexts that consume it. It reuses the pieces the earlier waves built
rather than re-deriving them:

* the **L1 decision digest** (:func:`~knowledge.digest.generate_l1_digest`) is
  what gets poured;
* the **L0 cards** (:attr:`~knowledge.projections.ProjectionBundle.l0`) ride
  along with each L1 entry; and
* the **distribution-mode coherence check**
  (:func:`~knowledge.coherence.run_coherence_gate` under
  :attr:`~knowledge.coherence.GateMode.DISTRIBUTION`, over
  :data:`~knowledge.coherence.LIFECYCLE_CHECKS` +
  :data:`~knowledge.typed_edges.TYPED_EDGE_CHECKS`) is the gate that decides
  whether the pour proceeds.

Two invariants define the boundary:

* **A blocking finding refuses the pour.** If the distribution-mode gate
  surfaces any blocking-severity finding, :func:`distribute_l1` delivers nothing
  to any channel and reports the blocking finding that refused the pour.
* **L2 never crosses.** Only L0 cards and L1 digest entries are ever delivered;
  an L2 full source document is never poured to a consuming BC. A
  :class:`BCChannel` refuses any attempt to deliver an ``"L2"`` tier, so the
  boundary holds structurally, not merely by convention.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

from knowledge.artifact_types import parse_artifact
from knowledge.coherence import (
    ArtifactCorpus,
    Check,
    CoherenceConfig,
    CoherenceReport,
    Finding,
    GateMode,
    LIFECYCLE_CHECKS,
    run_coherence_gate,
)
from knowledge.digest import DigestEntry, generate_l1_digest
from knowledge.projections import generate_projections
from knowledge.typed_edges import TYPED_EDGE_CHECKS

# The check registry the distribution gate runs: the lifecycle checks and the
# typed-edge checks together, so distribution is vetoed by any blocking finding
# either registry surfaces. Named so a caller reuses exactly this composed gate
# rather than re-spelling the concatenation.
DISTRIBUTION_CHECKS: tuple[Check, ...] = LIFECYCLE_CHECKS + TYPED_EDGE_CHECKS

# The projection tiers that are allowed to cross the distribution boundary. L2
# (the full source document) is deliberately absent.
CROSSABLE_TIERS: frozenset[str] = frozenset({"L0", "L1"})


class L2BoundaryError(ValueError):
    """An attempt to deliver an L2 full document across the distribution boundary.

    The distribution boundary crosses only L0 and L1 projections; a delivery
    tagged with any tier outside :data:`CROSSABLE_TIERS` (notably ``"L2"``) is
    refused here so the "L2 never crosses" invariant holds structurally rather
    than by convention.
    """


@dataclass(frozen=True)
class DeliveredProjection:
    """One projection that crossed the boundary to a BC channel.

    Attributes
    ----------
    tier:
        The projection tier that crossed — always one of :data:`CROSSABLE_TIERS`
        (``"L0"`` or ``"L1"``); an ``"L2"`` tier never reaches a channel.
    doc_id:
        The id of the decision the projection is for.
    payload:
        The delivered projection itself — an
        :class:`~knowledge.projections.L0Card` for the ``"L0"`` tier, a
        :class:`~knowledge.digest.DigestEntry` for the ``"L1"`` tier. Never the
        full L2 source document.
    """

    tier: str
    doc_id: str
    payload: object


@dataclass
class BCChannel:
    """An in-memory delivery target modelling one consuming BC's channel.

    A channel records every projection delivered to it and enforces the boundary
    on delivery: :meth:`deliver` refuses any projection whose tier is not in
    :data:`CROSSABLE_TIERS`, so an L2 full document can never be recorded as
    having crossed. The accessors expose what crossed for a caller to assert on.
    """

    name: str
    _deliveries: list[DeliveredProjection] = field(default_factory=list)

    def deliver(self, projection: DeliveredProjection) -> None:
        """Record ``projection`` as crossed, refusing any non-crossable tier."""
        if projection.tier not in CROSSABLE_TIERS:
            raise L2BoundaryError(
                f"tier {projection.tier!r} may not cross the distribution "
                f"boundary; only {sorted(CROSSABLE_TIERS)} cross"
            )
        self._deliveries.append(projection)

    @property
    def deliveries(self) -> tuple[DeliveredProjection, ...]:
        """Every projection delivered to this channel, in delivery order."""
        return tuple(self._deliveries)

    @property
    def l0_deliveries(self) -> tuple[DeliveredProjection, ...]:
        """The L0 cards delivered to this channel, in delivery order."""
        return tuple(p for p in self._deliveries if p.tier == "L0")

    @property
    def l1_deliveries(self) -> tuple[DeliveredProjection, ...]:
        """The L1 digest entries delivered to this channel, in delivery order."""
        return tuple(p for p in self._deliveries if p.tier == "L1")

    @property
    def tiers_crossed(self) -> frozenset[str]:
        """The distinct projection tiers that crossed to this channel."""
        return frozenset(p.tier for p in self._deliveries)


@dataclass(frozen=True)
class DistributionResult:
    """The outcome of running the L1 distribution over a corpus.

    Attributes
    ----------
    poured:
        Whether the digest was poured. ``True`` when the distribution-mode gate
        found no blocking finding; ``False`` when a blocking finding refused the
        pour.
    report:
        The distribution-mode :class:`~knowledge.coherence.CoherenceReport` the
        gate produced — the evidence behind the pour/refuse decision.
    channels:
        The channels the distribution ran against (each carries what it
        received; all empty on a refusal).
    """

    poured: bool
    report: CoherenceReport
    channels: tuple[BCChannel, ...]

    @property
    def refused(self) -> bool:
        """Whether the pour was refused (the complement of :attr:`poured`)."""
        return not self.poured

    @property
    def blocking_findings(self) -> tuple[Finding, ...]:
        """The blocking findings that refused the pour (empty when it poured)."""
        return self.report.blocking_findings

    @property
    def l2_crossed(self) -> bool:
        """Whether any L2 full document crossed to a channel — always ``False``.

        L2 is never poured and a channel refuses an L2 delivery, so no L2
        document can have crossed. Exposed so a caller can assert the invariant
        directly.
        """
        return any("L2" in channel.tiers_crossed for channel in self.channels)


def _sources_by_id(sources: Mapping[str, str]) -> dict[str, str]:
    """Re-key the corpus by each document's frontmatter id (not its map key)."""
    keyed: dict[str, str] = {}
    for text in sources.values():
        artifact = parse_artifact(text)
        if isinstance(artifact.id, str) and artifact.id:
            keyed[artifact.id] = text
    return keyed


def distribute_l1(
    sources: Mapping[str, str],
    config: CoherenceConfig,
    channels: Sequence[BCChannel],
    checks: tuple[Check, ...] = DISTRIBUTION_CHECKS,
) -> DistributionResult:
    """Pour the L1 decision digest to ``channels``, gated by the distribution check.

    The corpus ``sources`` is parsed into an
    :class:`~knowledge.coherence.ArtifactCorpus` and run through the
    distribution-mode coherence gate (``checks`` under
    :attr:`~knowledge.coherence.GateMode.DISTRIBUTION`). Then:

    * **A blocking finding refuses the pour.** If the report carries any
      blocking-severity finding, nothing is delivered to any channel and the
      returned :class:`DistributionResult` has ``poured is False`` and reports
      the blocking finding(s).
    * **Otherwise the digest pours.** For each accepted decision in the L1
      decision digest, its L0 card and its L1 digest entry are delivered to every
      channel — and only those tiers. The L2 full source document is never
      delivered (and a channel would refuse it), so the boundary holds.

    Parameters
    ----------
    sources:
        The corpus as an ``key -> source text`` mapping — the single source both
        the gate and the digest read.
    config:
        The coherence config the gate runs under (ambient-free reference date).
    channels:
        The consuming BC channels to pour to.
    checks:
        The check registry the distribution gate runs; defaults to the composed
        :data:`DISTRIBUTION_CHECKS`.

    Returns
    -------
    DistributionResult
        The pour/refuse outcome, the gate report behind it, and the channels.
    """
    corpus = ArtifactCorpus.from_artifacts(
        parse_artifact(text) for text in sources.values()
    )
    report = run_coherence_gate(
        corpus, config, mode=GateMode.DISTRIBUTION, checks=checks
    )

    channels = tuple(channels)
    if report.blocking_findings:
        # A blocking finding refuses the pour: nothing crosses to any BC.
        return DistributionResult(poured=False, report=report, channels=channels)

    digest = generate_l1_digest(sources)
    by_id = _sources_by_id(sources)
    for channel in channels:
        for entry in digest.entries:
            card = generate_projections(by_id[entry.id]).l0
            channel.deliver(DeliveredProjection(tier="L0", doc_id=entry.id, payload=card))
            channel.deliver(
                DeliveredProjection(tier="L1", doc_id=entry.id, payload=entry)
            )

    return DistributionResult(poured=True, report=report, channels=channels)
