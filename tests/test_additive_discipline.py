"""Step definitions for the additive-discipline check over the typedef set.

Binds the two scenarios in ``additive_discipline.feature``. The check runs over
the per-type TYPEDEF SET (not an artifact corpus): the base schema governs the
shared fields and the base-governed optionals, and a per-type typedef must state
only its per-type deltas (its own required body sections, status enum, and edge
participation / extra required fields). A typedef that re-declares a
base-governed field — e.g. carries ``distribution`` in its
``extra_required_fields`` — is a ``base-field-redeclaration`` defect.

RED leg: no additive-discipline check exists yet, so the check function is
resolved via :func:`_load_additive_check` (an ``getattr`` over the candidate
modules) and defaults to ``None`` — the flag scenario then fails on its first
``Then`` (the expected ``base-field-redeclaration`` finding is absent), a genuine
assertion failure rather than a collection/import error. The GREEN sibling
(ckk.2) adds ``check_additive_discipline`` and makes the flag scenario report the
defect. The pass scenario passes trivially until then.
"""

from __future__ import annotations

import importlib

import pytest
from pytest_bdd import given, scenario, then, when

from knowledge.artifact_types import ArtifactType

FEATURE = "additive_discipline.feature"


def _load_additive_check():
    """Resolve the not-yet-existing additive-discipline check function.

    Tries each candidate module the GREEN leg might land the check in and returns
    the first ``check_additive_discipline`` it finds. Returns ``None`` when no
    such function exists yet — so the RED leg fails on a real assertion (the
    finding is absent), not on an ``ImportError`` at collection time.
    """
    for module_name in (
        "knowledge.additive_discipline",
        "knowledge.artifact_types",
        "knowledge.typedefs",
    ):
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue
        fn = getattr(module, "check_additive_discipline", None)
        if fn is not None:
            return fn
    return None


@pytest.fixture
def context() -> dict:
    return {}


# --- Scenario bindings -------------------------------------------------------


@scenario(FEATURE, "a per-type typedef re-declaring a base shared field is reported as a defect")
def test_base_field_redeclaration_flagged() -> None: ...


@scenario(
    FEATURE,
    "a per-type typedef stating only its per-type deltas and re-declaring no base field passes",
)
def test_clean_typedef_passes() -> None: ...


# --- Given steps -------------------------------------------------------------


@given(
    "a per-type typedef that, beyond its per-type deltas, re-declares the base "
    "shared field distribution the base schema already governs"
)
def _typedef_redeclaring_distribution(context: dict) -> None:
    context["subject"] = "adr"
    context["field"] = "distribution"
    context["typedefs"] = [
        ArtifactType(
            name="adr",
            id_prefix="adr",
            id_pattern=r"adr-\d{3,}",
            id_example="adr-NNN",
            statuses=("proposed", "accepted", "superseded", "rejected"),
            # Its per-type deltas (derives-from) PLUS a re-declaration of the
            # base-governed field distribution — the defect this check catches.
            extra_required_fields=("derives-from", "distribution"),
            non_empty_fields=("derives-from",),
            required_sections=("Context", "Decision", "Consequences"),
        ),
    ]


@given(
    "a per-type typedef that declares only its required body sections, its status "
    "enum and its edge participation, re-declaring no base shared field"
)
def _clean_typedef(context: dict) -> None:
    context["subject"] = "brief"
    context["typedefs"] = [
        ArtifactType(
            name="brief",
            id_prefix="brief",
            id_pattern=r"brief-\d{3,}",
            id_example="brief-NNN",
            statuses=("draft", "ready", "delivered", "withdrawn"),
            # Only its per-type delta (derives-from edge participation); no
            # base-governed field re-declared.
            extra_required_fields=("derives-from",),
            required_sections=("Summary", "Scope"),
        ),
    ]


# --- When step (shared) ------------------------------------------------------


@when("the knowledge context runs the additive-discipline check over the per-type typedefs")
def _run_additive_check(context: dict) -> None:
    from knowledge.coherence import CoherenceReport

    check = _load_additive_check()
    findings = list(check(context["typedefs"])) if check is not None else []
    context["findings"] = findings
    context["report"] = CoherenceReport(findings=tuple(findings))


# --- Then steps --------------------------------------------------------------


def _redeclaration_findings(context: dict):
    return context["report"].findings_for_check("base-field-redeclaration")


@then(
    "it reports a base-field-redeclaration defect naming the typedef and the "
    "re-declared field distribution"
)
def _reports_redeclaration(context: dict) -> None:
    found = _redeclaration_findings(context)
    assert found, "expected a base-field-redeclaration finding"
    finding = found[0]
    assert context["subject"] in finding.subjects, (
        f"finding should name the typedef {context['subject']!r}; subjects={finding.subjects}"
    )
    assert context["subject"] in finding.message
    assert context["field"] in finding.message, (
        f"finding should name the re-declared field {context['field']!r}; "
        f"message={finding.message!r}"
    )


@then(
    "the finding carries its check-id and a remediation to remove the re-declared "
    "base field and inherit it from the base schema"
)
def _redeclaration_remediation(context: dict) -> None:
    finding = _redeclaration_findings(context)[0]
    assert finding.check_id == "base-field-redeclaration"
    remediation = finding.remediation.lower()
    assert "remove" in remediation
    assert "inherit" in remediation


@then("it reports no base-field-redeclaration defect for that typedef")
def _no_redeclaration(context: dict) -> None:
    for f in _redeclaration_findings(context):
        assert context["subject"] not in f.subjects, (
            f"unexpected base-field-redeclaration finding naming {context['subject']!r}: "
            f"{f.subjects}"
        )


@then("the aggregate verdict exits non-zero")
def _exits_non_zero(context: dict) -> None:
    assert context["report"].exit_code != 0


@then("the aggregate verdict exits zero")
def _exits_zero(context: dict) -> None:
    assert context["report"].exit_code == 0, (
        f"expected zero; findings: {[f.check_id for f in context['report'].findings]}"
    )
