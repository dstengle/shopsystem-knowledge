"""The L1 decision digest: a self-contained, single-source view of accepted decisions.

Where :mod:`knowledge.projections` turns *one* source document into a
:class:`~knowledge.projections.ProjectionBundle`, this module lifts that to a
**digest** over a whole decision corpus: it keeps exactly the *accepted*
decisions and renders each as a self-contained :class:`DigestEntry` carrying its
own id, status, supersede edges, and the verbatim L1 decision extract. A reader
of a single entry can determine the decision, its status, and what it supersedes
without consulting any other entry or the source document.

Every fact in an entry is drawn from that decision's single source:

* ``id`` and ``status`` come from the artifact's YAML frontmatter (parsed with
  the real loader in :mod:`knowledge.artifact_types`, so list-valued
  ``supersedes`` / ``superseded-by`` fields round-trip as lists);
* the supersede edges are the frontmatter ``supersedes`` / ``superseded-by``
  link fields (the same :data:`~knowledge.typed_edges.LINK_FIELDS` the coherence
  gate reads — body prose is never scraped); and
* the verbatim L1 decision extract is exactly
  :attr:`~knowledge.projections.ProjectionBundle.l1` — the recognized decision
  section, reused rather than re-extracted.

Generation is deterministic and ambient-free, and — mirroring
:func:`~knowledge.projections.write_corpus` — the digest serializes to a
``path -> bytes`` byte manifest so that :func:`write_digest` rewrites only the
files whose bytes changed. A regeneration over an unchanged source therefore
writes **zero changed bytes**.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
import os

from knowledge.artifact_types import Artifact, parse_artifact
from knowledge.projections import (
    WriteResult,
    _serialize_json,
    generate_projections,
)

# The accepted status: the digest keeps exactly the decisions that carry it.
ACCEPTED_STATUS = "accepted"

# The artifact types the digest treats as decisions. The digest ranges over
# exactly these, so a non-decision artifact never enters the digest even when it
# carries an accepted status.
DECISION_TYPES: tuple[str, ...] = ("pdr", "adr")

# The frontmatter link fields that carry a decision's supersede edges. These are
# the same fields the typed-edge checks resolve; the digest reads them verbatim
# rather than re-deriving the supersede relation.
_SUPERSEDES_FIELD = "supersedes"
_SUPERSEDED_BY_FIELD = "superseded-by"

# The manifest path the serialized digest is written under. Kept as a named
# constant so a caller (and the idempotent write path) reference exactly this
# relative path rather than re-spelling the layout.
DIGEST_MANIFEST_PATH = "digest/l1_decisions.json"


def _link_targets(artifact: Artifact, field: str) -> tuple[str, ...]:
    """The string id targets a link ``field`` resolves to, in document order.

    A scalar id yields a single-element tuple; a list field yields its string
    entries; an unset, empty, or non-id value yields ``()``. This mirrors the
    edge-resolution rule the typed-edge checks use, so a list-valued
    ``supersedes`` and a scalar one read uniformly.
    """
    value = artifact.frontmatter.get(field)
    if isinstance(value, str):
        return (value,) if value else ()
    if isinstance(value, (list, tuple)):
        return tuple(entry for entry in value if isinstance(entry, str) and entry)
    return ()


@dataclass(frozen=True)
class DigestEntry:
    """One self-contained L1 digest entry for an accepted decision.

    An entry carries everything a reader needs to determine the decision, its
    status, and what it supersedes without consulting any other entry or the
    source document:

    Attributes
    ----------
    id:
        The decision's own frontmatter id.
    status:
        The decision's status — always ``accepted`` for an entry in the digest.
    supersedes:
        The ids this decision supersedes, drawn from its ``supersedes`` link
        field, in document order.
    superseded_by:
        The ids that supersede this decision, drawn from its ``superseded-by``
        link field, in document order. (Empty for a current accepted decision.)
    l1_extract:
        The verbatim L1 decision extract — exactly
        :attr:`~knowledge.projections.ProjectionBundle.l1`'s text, reused rather
        than re-extracted.
    """

    id: str
    status: str
    supersedes: tuple[str, ...]
    superseded_by: tuple[str, ...]
    l1_extract: str

    @property
    def supersede_edges(self) -> tuple[str, ...]:
        """Every supersede edge on this entry: what it supersedes then what supersedes it.

        A single accessor over both directions, so a caller that wants "the
        supersede edges" need not thread both fields. The outbound
        (:attr:`supersedes`) edges come first, then the inbound
        (:attr:`superseded_by`) edges, each in document order.
        """
        return self.supersedes + self.superseded_by

    def as_dict(self) -> dict[str, object]:
        """The entry as a plain, serialization-ready mapping.

        Used to build the deterministic byte manifest; every value is a JSON
        primitive (string or list of strings) so the serialized form is stable.
        """
        return {
            "id": self.id,
            "status": self.status,
            "supersedes": list(self.supersedes),
            "superseded-by": list(self.superseded_by),
            "l1_extract": self.l1_extract,
        }


@dataclass(frozen=True)
class Digest:
    """The L1 decision digest: the accepted-decision entries over a corpus.

    ``entries`` holds one :class:`DigestEntry` per accepted decision, in sorted
    id order, so the digest — and its serialized byte manifest — is
    deterministic. :meth:`entry_for` resolves an id to its entry (``None`` when
    the id is absent or was excluded), and :attr:`ids` names the decisions the
    digest covers.
    """

    entries: tuple[DigestEntry, ...]

    @property
    def ids(self) -> tuple[str, ...]:
        """The ids of the decisions the digest carries, in entry order."""
        return tuple(entry.id for entry in self.entries)

    def entry_for(self, decision_id: str) -> DigestEntry | None:
        """Resolve ``decision_id`` to its entry, or ``None`` when not in the digest."""
        for entry in self.entries:
            if entry.id == decision_id:
                return entry
        return None


def _is_accepted_decision(artifact: Artifact) -> bool:
    """Whether ``artifact`` is an accepted decision the digest should carry."""
    return artifact.type in DECISION_TYPES and artifact.status == ACCEPTED_STATUS


def _entry_for_source(source: str) -> DigestEntry:
    """Build the self-contained digest entry for one accepted decision source."""
    artifact = parse_artifact(source)
    decision_id = artifact.id if isinstance(artifact.id, str) else ""
    status = artifact.status if isinstance(artifact.status, str) else ""
    # Reuse the single-source L1 projection verbatim rather than re-extracting.
    l1_extract = generate_projections(source).l1.text
    return DigestEntry(
        id=decision_id,
        status=status,
        supersedes=_link_targets(artifact, _SUPERSEDES_FIELD),
        superseded_by=_link_targets(artifact, _SUPERSEDED_BY_FIELD),
        l1_extract=l1_extract,
    )


def generate_l1_digest(sources: Mapping[str, str]) -> Digest:
    """Generate the L1 decision digest over a decision corpus.

    Parameters
    ----------
    sources:
        A mapping of document key to that document's full source text. The corpus
        is the single source of truth; nothing else is read.

    Returns
    -------
    Digest
        A digest carrying exactly one :class:`DigestEntry` per **accepted**
        decision (a ``pdr`` or ``adr`` whose status is ``accepted``), in sorted
        id order. A decision whose status is ``proposed``, ``rejected``, or
        ``superseded`` — and any non-decision artifact — draws no entry. Every
        entry is self-contained and every fact in it is drawn from that
        decision's single source.
    """
    entries: list[DigestEntry] = []
    for source in sources.values():
        artifact = parse_artifact(source)
        if not _is_accepted_decision(artifact):
            continue
        entries.append(_entry_for_source(source))
    entries.sort(key=lambda entry: entry.id)
    return Digest(entries=tuple(entries))


def digest_manifest(sources: Mapping[str, str]) -> dict[str, bytes]:
    """Serialize the L1 decision digest to a deterministic ``path -> bytes`` manifest.

    The digest is rendered as a single JSON array of entries (in sorted id order)
    under :data:`DIGEST_MANIFEST_PATH`. Serialization reuses the canonical,
    ambient-free JSON encoder :func:`~knowledge.projections._serialize_json`
    (sorted keys, fixed indent, single trailing newline), so two generations over
    the same corpus produce byte-for-byte identical manifests — the property
    :func:`write_digest` turns into zero-changed-bytes idempotence.
    """
    digest = generate_l1_digest(sources)
    payload = [entry.as_dict() for entry in digest.entries]
    return {DIGEST_MANIFEST_PATH: _serialize_json(payload)}


def write_digest(sources: Mapping[str, str], out_dir: str | os.PathLike[str]) -> WriteResult:
    """Materialize the digest manifest under ``out_dir``, rewriting only drift.

    Mirrors :func:`~knowledge.projections.write_corpus`: the manifest from
    :func:`digest_manifest` is written path-by-path under ``out_dir``, and a file
    is (re)written only when its on-disk bytes differ from the manifest's bytes
    (or the file is absent). Because generation is deterministic, a regeneration
    over an unchanged source yields a manifest byte-identical to what is already
    on disk, so no file is rewritten and the returned :class:`WriteResult`
    reports an empty ``changed_paths`` — the "writes zero changed bytes"
    idempotence property.

    Parameters
    ----------
    sources:
        The decision corpus, passed straight through to :func:`digest_manifest`.
    out_dir:
        The output directory under which the manifest's relative path is
        materialized; it (and any needed parents) are created as required.

    Returns
    -------
    WriteResult
        Carrying the relative paths that were (re)written, in manifest order.
    """
    base = Path(out_dir)
    manifest = digest_manifest(sources)

    changed: list[str] = []
    for rel_path, data in manifest.items():
        target = base / rel_path
        if target.exists() and target.read_bytes() == data:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        changed.append(rel_path)

    return WriteResult(changed_paths=tuple(changed))
