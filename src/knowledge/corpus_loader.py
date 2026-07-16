"""Load an :class:`~knowledge.coherence.ArtifactCorpus` from a directory tree.

Where :class:`~knowledge.coherence.ArtifactCorpus` is built in-process from
already-parsed :class:`~knowledge.artifact_types.Artifact` objects, this module
is the **filesystem boundary**: it walks a corpus *root directory* — the
per-type subdirectories and the living ``current-state.md`` — parses each
document's YAML frontmatter into a typed artifact, and hands the result to
:meth:`ArtifactCorpus.from_artifacts` so the same coherence checks run over a
real tree.

The loader is deliberately forgiving about *shape*, never about *content*:

* An **absent** typed-artifact subdirectory is treated as zero instances of
  that type — not a loader error — so a corpus that has never authored a
  prioritization-record still loads and reports a verdict.
* A file that parses to **non-empty** frontmatter is a typed artifact.
"""

from __future__ import annotations

from pathlib import Path

from knowledge.artifact_types import parse_artifact
from knowledge.coherence import ArtifactCorpus

# The per-type subdirectories the loader walks, each mapped to the artifact
# ``type`` it holds. A subdirectory absent from the root is treated as zero
# instances of its type rather than an error.
SUBDIR_TYPES: dict[str, str] = {
    "intent": "intent-record",
    "candidates": "candidate",
    "sessions": "session-record",
    "prioritizations": "prioritization-record",
    "briefs": "brief",
    "pdrs": "pdr",
    "adrs": "adr",
}


def load_corpus(root: str | Path) -> ArtifactCorpus:
    """Walk ``root`` and load its documents into an :class:`ArtifactCorpus`.

    Every per-type subdirectory named in :data:`SUBDIR_TYPES` is walked (an
    absent one contributes nothing rather than erroring), and every file
    directly under ``root`` — such as the living ``current-state.md`` — is read
    too. A file that parses to non-empty YAML frontmatter becomes a typed
    :class:`~knowledge.artifact_types.Artifact`.
    """
    root_path = Path(root)
    artifacts = []

    for subdir_name in SUBDIR_TYPES:
        subdir = root_path / subdir_name
        for file_path in sorted(subdir.iterdir()):
            if file_path.is_file():
                _ingest(file_path, artifacts)

    if root_path.is_dir():
        for file_path in sorted(root_path.iterdir()):
            if file_path.is_file():
                _ingest(file_path, artifacts)

    return ArtifactCorpus.from_artifacts(artifacts)


def _ingest(path: Path, artifacts: list) -> None:
    """Parse ``path`` and append it to ``artifacts`` when it is a typed artifact."""
    artifact = parse_artifact(path.read_text(encoding="utf-8"))
    if artifact.frontmatter:
        artifacts.append(artifact)
