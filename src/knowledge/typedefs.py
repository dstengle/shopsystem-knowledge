"""Typedef generation and the drift check over a type's generated set.

An artifact type's rules (:class:`~knowledge.artifact_types.ArtifactType`) are
its **typedef**: from a typedef the context deterministically emits a document
**template** and a **schema fragment**, and commits that generated set alongside
the typedef. Because the registry in :mod:`knowledge.artifact_types` is the
single source of truth, the generated set is a pure derivation of it — and the
**drift check** exists to prove the committed set never diverges from what the
typedef would emit today.

The three public behaviours mirror the corpus generate/write/check trio in
:mod:`knowledge.projections`, so the two waves share one mental model:

* :func:`generate_typedef_set` — the pure ``path -> bytes`` manifest for a
  typedef (its template and schema fragment). It reads only the typedef; no
  wall clock, hostname, or absolute path enters the bytes, so regeneration is
  byte-for-byte reproducible.
* :func:`write_typedef_set` — materializes the manifest under an output
  directory, rewriting only files whose bytes differ. Over an unchanged typedef
  this rewrites nothing (zero changed bytes) — regeneration is idempotent.
* :func:`check_typedef_drift` — compares the on-disk generated set against a
  freshly generated manifest without writing, reporting the drifted files (and a
  non-zero exit) when a generated file has been hand-edited, or no drift (exit
  zero) when the set still matches its typedef.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from knowledge.artifact_types import (
    ARTIFACT_TYPES,
    SHARED_REQUIRED_FIELDS,
    ArtifactType,
)

# The manifest path segments the template and schema fragment are emitted under.
# Named constants so a caller selects by exactly these segments rather than
# re-spelling the layout.
TEMPLATE_SEGMENT = "templates"
SCHEMA_SEGMENT = "schema"

# The generated/read-only mark carried in the bytes of every generated file so a
# reader sees the file is generated and must not be hand-edited. In a template it
# rides as a YAML frontmatter comment (ignored by the YAML loader, so the
# template stays a usable document); in a schema fragment it is the
# ``generated``/``read_only`` payload keys. This is what "marked generated and
# read-only" means concretely — and, because the mark is a constant, it carries
# no timestamp, hostname, or path and keeps generation byte-stable.
GENERATED_TEMPLATE_MARKER = (
    "# GENERATED — single-sourced from the typedef; read-only. "
    "Regenerate from the typedef, do not hand-edit."
)

# The body marker a living-document (``document_shape == "living"``) template
# carries, distinguishing a single stewarded record revised in place from an
# append-only numbered-series instance. Emitted only for living typedefs, so its
# presence is the observable "this is a living stewarded document" signal.
LIVING_DOCUMENT_MARKER = (
    "<!-- LIVING DOCUMENT — a single record stewarded in place; revise it as "
    "decisions land rather than appending a numbered-series instance. -->"
)

# The document shape a living-in-place typedef declares.
LIVING_SHAPE = "living"


def _serialize_json(payload: object) -> bytes:
    """Serialize ``payload`` to canonical, ambient-free JSON bytes.

    ``sort_keys`` makes byte order independent of field insertion order,
    ``ensure_ascii`` makes it independent of locale, and the fixed indent plus a
    single trailing newline make the layout a pure function of ``payload`` — no
    timestamp, hostname, or path enters the bytes.
    """
    text = json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True)
    return (text + "\n").encode("utf-8")


def render_template(atype: ArtifactType) -> bytes:
    """Emit the document template for ``atype`` as deterministic bytes.

    The template is a Markdown skeleton: a YAML frontmatter stub listing the
    type's required fields (shared then type-additional) with the ``type`` fixed
    to the type name, followed by one empty ``## `` heading per required section
    in the type's declared order. It is a pure function of the typedef.

    A ``document_shape == "living"`` typedef (e.g. ``current-state``) renders a
    single stewarded living document instead of an append-only numbered-series
    instance: its type-additional fields (such as ``incorporates``) are rendered
    as YAML lists it accumulates in place, and the body opens with the
    :data:`LIVING_DOCUMENT_MARKER`.
    """
    living = atype.document_shape == LIVING_SHAPE
    lines: list[str] = ["---", GENERATED_TEMPLATE_MARKER]
    for name in SHARED_REQUIRED_FIELDS:
        if name == "type":
            lines.append(f"type: {atype.name}")
        else:
            lines.append(f"{name}:")
    for name in atype.extra_required_fields:
        # A living document carries its type-additional fields as lists it
        # accumulates in place; an instance leaves them as bare scalar stubs.
        lines.append(f"{name}: []" if living else f"{name}:")
    lines.append("---")
    lines.append("")
    if living:
        lines.append(LIVING_DOCUMENT_MARKER)
        lines.append("")
    for section in atype.required_sections:
        lines.append(f"## {section}")
        lines.append("")
    text = "\n".join(lines).rstrip("\n") + "\n"
    return text.encode("utf-8")


def render_schema_fragment(atype: ArtifactType) -> bytes:
    """Emit the schema fragment for ``atype`` as deterministic JSON bytes.

    The fragment serializes every rule the typedef defines — id pattern and
    example, status enum, shared and type-additional required fields, non-empty
    anchor fields, and required sections — as canonical JSON. It is a pure
    function of the typedef.
    """
    payload = {
        "generated": True,
        "read_only": True,
        "type": atype.name,
        "document_shape": atype.document_shape,
        "id_pattern": atype.id_pattern,
        "id_example": atype.id_example,
        "statuses": list(atype.statuses),
        "shared_required_fields": list(SHARED_REQUIRED_FIELDS),
        "type_required_fields": list(atype.extra_required_fields),
        "non_empty_fields": list(atype.non_empty_fields),
        "required_sections": list(atype.required_sections),
    }
    return _serialize_json(payload)


def generate_typedef_set(atype: ArtifactType) -> dict[str, bytes]:
    """Generate the ``path -> bytes`` manifest for ``atype``'s typedef.

    Returns an ordered manifest carrying ``templates/<name>.md`` (the document
    template) and ``schema/<name>.json`` (the schema fragment). The manifest is a
    pure function of the typedef: two generations of the same typedef produce
    byte-for-byte identical manifests regardless of host, time, or working
    directory, and every manifest key is a relative path.
    """
    return {
        f"{TEMPLATE_SEGMENT}/{atype.name}.md": render_template(atype),
        f"{SCHEMA_SEGMENT}/{atype.name}.json": render_schema_fragment(atype),
    }


@dataclass(frozen=True)
class TypedefWriteResult:
    """The outcome of materializing a typedef's generated set under a directory.

    ``changed_paths`` holds the relative paths whose on-disk bytes were
    (re)written because they differed from the freshly generated manifest — an
    empty tuple means the set already matched the typedef and nothing was
    rewritten. Regenerating over an unchanged typedef therefore reports
    ``changed_paths == ()`` and :attr:`changed_count` ``0`` — the "writes zero
    changed bytes" idempotence property.
    """

    changed_paths: tuple[str, ...]

    @property
    def changed_count(self) -> int:
        """The number of files (re)written — zero on an idempotent regeneration."""
        return len(self.changed_paths)


@dataclass(frozen=True)
class TypedefDriftResult:
    """The outcome of checking a typedef's on-disk set against a fresh manifest.

    ``drift`` holds the relative paths whose on-disk bytes are missing or differ
    from what the typedef would emit — the generated files that no longer match
    the typedef. :attr:`has_drift` and :attr:`exit_code` surface that verdict for
    callers and a process exit respectively: a clean set yields ``drift == ()``,
    ``has_drift is False`` and ``exit_code == 0``; a hand-edited file yields a
    non-empty ``drift`` naming it and ``exit_code == 1``.
    """

    drift: tuple[str, ...]

    @property
    def has_drift(self) -> bool:
        """Whether any generated file has drifted from the typedef."""
        return bool(self.drift)

    @property
    def exit_code(self) -> int:
        """A conventional exit status: ``0`` when clean, ``1`` on drift."""
        return 1 if self.drift else 0


def write_typedef_set(
    atype: ArtifactType, out_dir: str | os.PathLike[str]
) -> TypedefWriteResult:
    """Materialize ``atype``'s generated set under ``out_dir``, rewriting only drift.

    Each manifest path from :func:`generate_typedef_set` is written under
    ``out_dir``, but a file is (re)written only when its on-disk bytes differ
    from the manifest (or the file is absent); a file already matching is left
    untouched. Because generation is deterministic, a regeneration over an
    unchanged typedef yields a manifest byte-identical to what is on disk, so no
    file is rewritten and the returned :class:`TypedefWriteResult` reports an
    empty ``changed_paths``.
    """
    base = Path(out_dir)
    manifest = generate_typedef_set(atype)

    changed: list[str] = []
    for rel_path, data in manifest.items():
        target = base / rel_path
        if target.exists() and target.read_bytes() == data:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        changed.append(rel_path)

    return TypedefWriteResult(changed_paths=tuple(changed))


def check_typedef_drift(
    atype: ArtifactType, out_dir: str | os.PathLike[str]
) -> TypedefDriftResult:
    """Check ``atype``'s on-disk generated set under ``out_dir`` against a fresh manifest.

    A freshly generated manifest (see :func:`generate_typedef_set`) is compared
    path-by-path against the bytes on disk **without writing anything**. A path
    drifts when its file is absent or its bytes differ from what the typedef
    would emit — so a hand-edited template or schema fragment is caught and named
    in :attr:`TypedefDriftResult.drift`, and the result's ``exit_code`` is
    non-zero. An unchanged set drifts nowhere and exits zero.
    """
    base = Path(out_dir)
    manifest = generate_typedef_set(atype)

    drift: list[str] = []
    for rel_path, data in manifest.items():
        target = base / rel_path
        if not target.exists() or target.read_bytes() != data:
            drift.append(rel_path)

    return TypedefDriftResult(drift=tuple(drift))


def typedef_type_names(
    atypes: Mapping[str, ArtifactType] = ARTIFACT_TYPES,
) -> tuple[str, ...]:
    """Enumerate the artifact type names that have a typedef, in registry order.

    The set of per-type typedefs is exactly the registry in
    :mod:`knowledge.artifact_types`: every entry is one type's typedef, and the
    type it declares is its :attr:`~knowledge.artifact_types.ArtifactType.name`.
    Enumerating those names is how a caller proves the typedef set covers exactly
    the recognized types — no recognized type lacks a typedef, and no typedef
    declares a type outside the recognized set.
    """
    return tuple(atype.name for atype in atypes.values())


def _template_is_marked(data: bytes) -> bool:
    """Whether ``data`` carries the generated/read-only template mark."""
    return GENERATED_TEMPLATE_MARKER.encode("utf-8") in data


def _fragment_is_marked(data: bytes) -> bool:
    """Whether ``data`` is a schema fragment marked generated and read-only."""
    payload = json.loads(data.decode("utf-8"))
    return payload.get("generated") is True and payload.get("read_only") is True


@dataclass(frozen=True)
class GeneratedArtifact:
    """One generated file for a typedef: its bytes and its generated/read-only marks.

    ``generated`` and ``read_only`` are read back from the bytes themselves (a
    template's YAML comment mark, a fragment's payload keys) rather than asserted
    blindly — so a file that lost its mark reports ``generated is False`` and the
    drift/single-source checks catch it.
    """

    rel_path: str
    data: bytes
    generated: bool
    read_only: bool


@dataclass(frozen=True)
class TypedefFormat:
    """The generated format for one typedef: its template and schema fragment.

    ``required_fields`` is the full frontmatter requirement the schema fragment
    encodes — the shared field set plus this type's own additions — surfaced so a
    caller can prove every fragment requires the shared set (including
    ``description``) without re-parsing the JSON.
    """

    type_name: str
    template: GeneratedArtifact
    schema_fragment: GeneratedArtifact
    required_fields: tuple[str, ...]


def generate_typedef_format(atype: ArtifactType) -> TypedefFormat:
    """Generate the :class:`TypedefFormat` for one typedef.

    The template and schema-fragment bytes are exactly those
    :func:`generate_typedef_set` emits (and the drift check compares against), so
    the format is single-sourced from the typedef: nothing about the generated
    template or fragment is spelled anywhere but the typedef.
    """
    manifest = generate_typedef_set(atype)
    tpl_path = f"{TEMPLATE_SEGMENT}/{atype.name}.md"
    frag_path = f"{SCHEMA_SEGMENT}/{atype.name}.json"
    tpl_bytes = manifest[tpl_path]
    frag_bytes = manifest[frag_path]
    template = GeneratedArtifact(
        rel_path=tpl_path,
        data=tpl_bytes,
        generated=_template_is_marked(tpl_bytes),
        read_only=_template_is_marked(tpl_bytes),
    )
    fragment = GeneratedArtifact(
        rel_path=frag_path,
        data=frag_bytes,
        generated=_fragment_is_marked(frag_bytes),
        read_only=_fragment_is_marked(frag_bytes),
    )
    required_fields = tuple(SHARED_REQUIRED_FIELDS) + tuple(atype.extra_required_fields)
    return TypedefFormat(
        type_name=atype.name,
        template=template,
        schema_fragment=fragment,
        required_fields=required_fields,
    )


def generate_format_set(
    atypes: Mapping[str, ArtifactType] = ARTIFACT_TYPES,
) -> dict[str, TypedefFormat]:
    """Run the format generator over the whole typedef set.

    Returns a ``type name -> TypedefFormat`` mapping carrying every typedef's
    generated template and schema fragment (each marked generated and read-only)
    in registry order. This is the set-level counterpart to
    :func:`generate_typedef_format`: it is how the context proves every
    recognized type is single-sourced by its own typedef.
    """
    return {atype.name: generate_typedef_format(atype) for atype in atypes.values()}


def generate_all_typedefs(atypes: Mapping[str, ArtifactType]) -> dict[str, bytes]:
    """Generate the combined manifest for every typedef in ``atypes``.

    A convenience over :func:`generate_typedef_set` for the whole registry: the
    merged ``path -> bytes`` manifest carries every type's template and schema
    fragment, visited in sorted type-name order so the manifest order is stable.
    Later waves that drift-check the entire committed typedef tree at once build
    on this.
    """
    manifest: dict[str, bytes] = {}
    for name in sorted(atypes):
        manifest.update(generate_typedef_set(atypes[name]))
    return manifest
