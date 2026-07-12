"""The artifact-lifecycle coherence gate: named checks over an artifact corpus.

Where :mod:`knowledge.schema` validates one artifact against its *own* type
schema, this module validates the **coherence of a whole corpus** — the
cross-artifact lifecycle invariants that only make sense once every artifact is
in view together. It runs a registry of named checks over an
:class:`ArtifactCorpus` and folds their :class:`Finding` outputs into a single
aggregate :class:`CoherenceReport`.

Every finding is reported in **doctor form** (mirroring ``bd doctor``): it names
its check (:attr:`Finding.check_name` / :attr:`Finding.check_id`), carries a
:class:`Severity` status, names the offending artifact(s) by id
(:attr:`Finding.subjects`, echoed into :attr:`Finding.message`), and states a
:attr:`Finding.remediation`. A finding's :class:`Severity` — ``BLOCKING`` or
``ADVISORY`` — is what decides whether it drives the aggregate verdict: a
blocking finding drives :attr:`CoherenceReport.exit_code` non-zero, while an
advisory (warning) finding reports a concern without by itself blocking.

The check registry :data:`LIFECYCLE_CHECKS` is deliberately a tuple of plain
functions ``(corpus, config) -> list[Finding]`` so later waves (typed-edge
checks, digest/distribution) reuse the same :class:`ArtifactCorpus` and
aggregate machinery by extending the registry rather than re-spelling the fold.

Every check is deterministic and ambient-free: staleness compares an artifact's
``updated`` date against the caller-supplied :attr:`CoherenceConfig.reference_date`
— never the wall clock — so a gate run over a fixed corpus is reproducible.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Callable, Mapping

from knowledge.artifact_types import Artifact


class Severity(Enum):
    """A finding's severity, and thus its pull on the aggregate verdict.

    ``BLOCKING`` findings drive :attr:`CoherenceReport.exit_code` non-zero (a
    distribution-mode veto); ``ADVISORY`` findings are warnings that report a
    concern without by themselves blocking.
    """

    BLOCKING = "blocking"
    ADVISORY = "advisory"


@dataclass(frozen=True)
class Finding:
    """One coherence finding, reported in doctor form.

    Attributes
    ----------
    check_id:
        The stable machine tag naming the check (e.g. ``"briefed-without-brief"``).
    check_name:
        The human-facing name of the check.
    severity:
        Whether the finding blocks (:attr:`Severity.BLOCKING`) or merely warns
        (:attr:`Severity.ADVISORY`).
    subjects:
        The artifact id(s) the finding is about, in report order — the ids a
        caller acts on. Always echoed into :attr:`message`.
    message:
        The human-readable diagnosis, naming every subject id.
    remediation:
        The concrete action that clears the finding.
    """

    check_id: str
    check_name: str
    severity: Severity
    subjects: tuple[str, ...]
    message: str
    remediation: str


@dataclass(frozen=True)
class CoherenceConfig:
    """The knobs the lifecycle checks read, kept ambient-free.

    Attributes
    ----------
    reference_date:
        The as-of date staleness is measured against. An in-flight artifact is
        stale when its ``updated`` date is older than
        ``reference_date - stale_age``. Supplied by the caller — never the wall
        clock — so a gate run is reproducible.
    stale_age:
        The age threshold beyond which an in-flight artifact is stale.
    legacy_brief_ceiling:
        The highest brief number exempt from the brief-without-candidate rule.
        Briefs numbered at or below it (the legacy corpus, ``brief-001`` through
        ``brief-015`` by default) predate the candidate-linkage convention and
        are exempt.
    in_flight_statuses:
        The statuses treated as "in flight" (still in progress) for the
        stale-in-flight check. Terminal/settled statuses are excluded, so a
        closed or accepted artifact is never reported stale.
    """

    reference_date: date
    stale_age: timedelta = timedelta(days=30)
    legacy_brief_ceiling: int = 15
    in_flight_statuses: frozenset[str] = frozenset(
        {"draft", "exploring", "proposed", "shaped", "open", "active"}
    )


@dataclass(frozen=True)
class ArtifactCorpus:
    """A collection of parsed artifacts the coherence checks range over.

    The corpus is the shared abstraction every check — and every later wave —
    reads: :meth:`get` resolves an id to its artifact (the cross-artifact
    linkage checks depend on it), :meth:`of_type` filters to one type, and
    :attr:`by_id` exposes the whole id index. Building from parsed
    :class:`~knowledge.artifact_types.Artifact` objects (rather than a directory)
    keeps the corpus deterministic and ambient-free.
    """

    artifacts: tuple[Artifact, ...] = ()

    @property
    def by_id(self) -> Mapping[str, Artifact]:
        """Map each artifact's id to its artifact (last wins on a duplicate id)."""
        index: dict[str, Artifact] = {}
        for art in self.artifacts:
            if isinstance(art.id, str):
                index[art.id] = art
        return index

    def get(self, artifact_id: object) -> Artifact | None:
        """Resolve ``artifact_id`` to its artifact, or ``None`` when absent."""
        if not isinstance(artifact_id, str):
            return None
        return self.by_id.get(artifact_id)

    def of_type(self, type_name: str) -> tuple[Artifact, ...]:
        """Every artifact whose frontmatter ``type`` equals ``type_name``."""
        return tuple(art for art in self.artifacts if art.type == type_name)

    @classmethod
    def from_artifacts(cls, artifacts) -> "ArtifactCorpus":
        """Build a corpus from any iterable of :class:`Artifact`."""
        return cls(artifacts=tuple(artifacts))


# --- Small field helpers -----------------------------------------------------


def _present(artifact: Artifact, field_name: str) -> bool:
    """Whether ``field_name`` is present with a truthy (non-empty) value."""
    value = artifact.frontmatter.get(field_name)
    return value is not None and value != "" and value != [] and value != ()


def _id_str(artifact: Artifact) -> str:
    """The artifact's id as a string (``""`` when absent)."""
    return artifact.id if isinstance(artifact.id, str) else ""


def _id_number(artifact_id: str) -> int | None:
    """The trailing numeric component of ``prefix-NNN``, or ``None``."""
    _, _, tail = artifact_id.rpartition("-")
    return int(tail) if tail.isdigit() else None


def _as_date(value: object) -> date | None:
    """Coerce a frontmatter ``updated`` value to a :class:`date`.

    YAML round-trips an ISO date as a :class:`date`/:class:`datetime`; a
    hand-built frontmatter may carry the ISO string instead. Both coerce; an
    unparseable value yields ``None`` (drawing no staleness finding).
    """
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _as_list(value: object) -> list:
    """A frontmatter list field as a list (``[]`` for unset/non-list)."""
    return list(value) if isinstance(value, (list, tuple)) else []


# --- The lifecycle checks ----------------------------------------------------
#
# Each check is a pure function (corpus, config) -> list[Finding]. The registry
# below folds them; later waves extend the registry rather than re-spelling the
# fold.


def check_briefed_without_brief(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """A ``briefed`` candidate must name the brief it was briefed into."""
    findings: list[Finding] = []
    for cand in corpus.of_type("candidate"):
        if cand.status == "briefed" and not _present(cand, "brief"):
            cid = _id_str(cand)
            findings.append(
                Finding(
                    check_id="briefed-without-brief",
                    check_name="briefed candidate names no brief",
                    severity=Severity.BLOCKING,
                    subjects=(cid,),
                    message=(
                        f"candidate '{cid}' has status briefed but names no brief"
                    ),
                    remediation=(
                        f"set the brief field on candidate '{cid}' to the brief it "
                        f"was briefed into"
                    ),
                )
            )
    return findings


def check_briefed_brief_asymmetry(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """A briefed candidate and its brief must point back at one another."""
    findings: list[Finding] = []
    for cand in corpus.of_type("candidate"):
        if cand.status != "briefed":
            continue
        brief_id = cand.frontmatter.get("brief")
        if not isinstance(brief_id, str) or not brief_id:
            continue
        brief = corpus.get(brief_id)
        if brief is None:
            continue
        if brief.frontmatter.get("candidate") != cand.id:
            cid = _id_str(cand)
            findings.append(
                Finding(
                    check_id="briefed-brief-asymmetry",
                    check_name="brief does not point back to its candidate",
                    severity=Severity.BLOCKING,
                    subjects=(cid, brief_id),
                    message=(
                        f"candidate '{cid}' names brief '{brief_id}', but that "
                        f"brief's candidate field does not point back to '{cid}'"
                    ),
                    remediation=(
                        f"set brief '{brief_id}'s candidate field back to '{cid}'"
                    ),
                )
            )
    return findings


def check_brief_without_candidate(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """A brief numbered above the legacy ceiling must name its candidate."""
    findings: list[Finding] = []
    for brief in corpus.of_type("brief"):
        number = _id_number(_id_str(brief))
        if number is None or number <= config.legacy_brief_ceiling:
            continue
        if not _present(brief, "candidate"):
            bid = _id_str(brief)
            findings.append(
                Finding(
                    check_id="brief-without-candidate",
                    check_name="brief names no candidate",
                    severity=Severity.BLOCKING,
                    subjects=(bid,),
                    message=(
                        f"brief '{bid}' is numbered above the legacy ceiling but "
                        f"names no candidate"
                    ),
                    remediation=(
                        f"set the candidate field on brief '{bid}' to the candidate "
                        f"it was shaped from"
                    ),
                )
            )
    return findings


def check_empty_closed_session(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """A ``closed`` session-record must link the work it produced or revised."""
    findings: list[Finding] = []
    for session in corpus.of_type("session-record"):
        if session.status != "closed":
            continue
        produced = _as_list(session.frontmatter.get("produced"))
        revised = _as_list(session.frontmatter.get("revised"))
        if not produced and not revised:
            sid = _id_str(session)
            findings.append(
                Finding(
                    check_id="empty-closed-session",
                    check_name="closed session-record links no work",
                    severity=Severity.BLOCKING,
                    subjects=(sid,),
                    message=(
                        f"session-record '{sid}' is closed but its produced and "
                        f"revised fields are both empty"
                    ),
                    remediation=(
                        f"link at least one produced or revised artifact on "
                        f"session-record '{sid}'"
                    ),
                )
            )
    return findings


def check_unincorporated_decision(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """An accepted decision must be claimed by some current-state incorporates list."""
    incorporated: set[str] = set()
    for art in corpus.artifacts:
        for entry in _as_list(art.frontmatter.get("incorporates")):
            if isinstance(entry, str):
                incorporated.add(entry)

    findings: list[Finding] = []
    for art in corpus.artifacts:
        if art.type not in ("pdr", "adr") or art.status != "accepted":
            continue
        did = _id_str(art)
        if did not in incorporated:
            findings.append(
                Finding(
                    check_id="unincorporated-decision",
                    check_name="accepted decision is not incorporated",
                    severity=Severity.BLOCKING,
                    subjects=(did,),
                    message=(
                        f"{art.type} '{did}' is accepted but appears in no "
                        f"current-state incorporates list"
                    ),
                    remediation=(
                        f"claim {art.type} '{did}' in a current-state incorporates "
                        f"list"
                    ),
                )
            )
    return findings


def check_stale_in_flight(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """An in-flight artifact must not sit older than the age threshold."""
    cutoff = config.reference_date - config.stale_age
    findings: list[Finding] = []
    for art in corpus.artifacts:
        if art.status not in config.in_flight_statuses:
            continue
        updated = _as_date(art.frontmatter.get("updated"))
        if updated is None or updated >= cutoff:
            continue
        aid = _id_str(art)
        findings.append(
            Finding(
                check_id="stale-in-flight",
                check_name="in-flight artifact is stale",
                severity=Severity.ADVISORY,
                subjects=(aid,),
                message=(
                    f"artifact '{aid}' is in flight (status {art.status}) but was "
                    f"last updated {updated.isoformat()}, older than the age "
                    f"threshold"
                ),
                remediation=f"advance or close artifact '{aid}'",
            )
        )
    return findings


def check_root_decision_anchor(
    corpus: ArtifactCorpus, config: CoherenceConfig
) -> list[Finding]:
    """A pdr should anchor to an upstream unless it is a root decision."""
    findings: list[Finding] = []
    for pdr in corpus.of_type("pdr"):
        derives = pdr.frontmatter.get("derives-from")
        if isinstance(derives, (list, tuple)) and len(derives) == 0:
            pid = _id_str(pdr)
            findings.append(
                Finding(
                    check_id="root-decision-anchor",
                    check_name="pdr anchors to no upstream artifact",
                    severity=Severity.ADVISORY,
                    subjects=(pid,),
                    message=(
                        f"pdr '{pid}' has an empty derives-from list and anchors to "
                        f"no upstream artifact"
                    ),
                    remediation=(
                        f"anchor pdr '{pid}' to an upstream artifact unless it is a "
                        f"root decision"
                    ),
                )
            )
    return findings


# A check is any function folding a corpus (under a config) into findings.
Check = Callable[[ArtifactCorpus, CoherenceConfig], "list[Finding]"]

# The lifecycle check registry, in report order. Later waves extend this tuple
# (or pass their own) rather than re-spelling the aggregate fold below.
LIFECYCLE_CHECKS: tuple[Check, ...] = (
    check_briefed_without_brief,
    check_briefed_brief_asymmetry,
    check_brief_without_candidate,
    check_empty_closed_session,
    check_unincorporated_decision,
    check_stale_in_flight,
    check_root_decision_anchor,
)


@dataclass(frozen=True)
class CoherenceReport:
    """The aggregate outcome of one gate run: its findings and one verdict.

    ``findings`` holds every finding, in check-registry order. The aggregate
    verdict folds them by severity: a single :attr:`Severity.BLOCKING` finding
    drives :attr:`exit_code` non-zero, while :attr:`Severity.ADVISORY` findings
    are warnings that never by themselves block. :attr:`findings_for_check` and
    :attr:`has_finding` select findings by check-id for a caller that acts on a
    specific check.
    """

    findings: tuple[Finding, ...]

    @property
    def blocking_findings(self) -> tuple[Finding, ...]:
        """Every blocking-severity finding, in report order."""
        return tuple(f for f in self.findings if f.severity is Severity.BLOCKING)

    @property
    def advisory_findings(self) -> tuple[Finding, ...]:
        """Every advisory-severity (warning) finding, in report order."""
        return tuple(f for f in self.findings if f.severity is Severity.ADVISORY)

    @property
    def exit_code(self) -> int:
        """``0`` when nothing blocks, ``1`` when any blocking finding is present."""
        return 1 if self.blocking_findings else 0

    def findings_for_check(self, check_id: str) -> tuple[Finding, ...]:
        """Every finding carrying ``check_id``, in report order."""
        return tuple(f for f in self.findings if f.check_id == check_id)

    def has_finding(self, check_id: str) -> bool:
        """Whether any finding carries ``check_id``."""
        return any(f.check_id == check_id for f in self.findings)


def run_coherence_gate(
    corpus: ArtifactCorpus,
    config: CoherenceConfig,
    checks: tuple[Check, ...] = LIFECYCLE_CHECKS,
) -> CoherenceReport:
    """Run every check in ``checks`` over ``corpus`` and fold into one report.

    The checks run in registry order; each returns its findings and the gate
    concatenates them into a single :class:`CoherenceReport` whose aggregate
    verdict folds by severity (any blocking finding drives the exit code
    non-zero). Passing an explicit ``checks`` tuple is how a later wave runs its
    own registry over the same corpus and reuses this fold.
    """
    findings: list[Finding] = []
    for check in checks:
        findings.extend(check(corpus, config))
    return CoherenceReport(findings=tuple(findings))
