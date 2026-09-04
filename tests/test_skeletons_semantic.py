"""Skeleton fixture tests (FR-005): the skeletons as executable typed
fixtures, and the negative fixtures that pin what the schemas and the engine
refuse.

Two resolution paths are exercised and are kept distinct: `validate_document`
runs the module's own registry over one document, while `extract_semantic`
runs under a bundle index built from the skeleton frontmatter. Only the second
can resolve a `Type` cell that names another skeleton.
"""

from __future__ import annotations

import re
import subprocess

import pytest

from tests.conftest import (
    NEGATIVE_DIR,
    OBJECT_TYPES,
    PACKAGE_ROOT,
    REPO_ROOT,
    SKELETONS_DIR,
    frontmatter,
    locators,
    object_type,
    object_types,
)

KERNEL_SCALARS = {
    "UUID",
    "Boolean",
    "Integer",
    "Decimal",
    "String",
    "Timestamp",
    "Duration",
    "Bytes",
    "JsonObject",
}

IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

#: Every model admits `clauses`, and three require one, so every skeleton
#: authors `## Invariants` (FR-005).
INVARIANT_BEARING = set(OBJECT_TYPES)
#: `Alert` and `Runbook` forbid `fields`; the other six require them.
FIELD_BEARING = set(OBJECT_TYPES) - {"alert", "runbook"}
#: `Runbook` and `Deployment` require at least one operation.
OPERATION_BEARING = {"runbook", "deployment"}
#: The types that ship a `sysml` alternate beside the typed table.
ALTERNATES = {"configuration", "sli", "deployment"}

TYPE_TARGET_PREFIX = "ix://agent-ix/spec-objects-operational/type/"


def skeleton_paths() -> list:
    return sorted(SKELETONS_DIR.glob("*.md"))


def extract(quire_engine, module, bundle, path):
    text = path.read_text()
    return quire_engine.extract_semantic(
        {
            "markdown": text,
            "module": module,
            "path": str(path),
            "sourceIdentity": (
                f"ix://agent-ix/spec-objects-operational/{frontmatter(text)['id']}"
            ),
            "bundle": bundle,
        }
    )


@pytest.mark.trace("TC-060", "FR-005-AC-1")
def test_every_skeleton_validates_with_no_error(quire_engine, skeletons):
    assert len(skeletons) == 11
    for path in skeletons:
        text = path.read_text()
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        assert result["is_valid"], (path.name, result["errors"])
        assert not [
            e for e in result["errors"] if "semantic.record-invalid" in e["message"]
        ], path.name


@pytest.mark.trace("TC-061", "FR-005-AC-2", "FR-005-CON-2")
def test_table_and_sysml_skeletons_extract_to_identical_fields(
    quire_engine, semantic_module, bundle_index
):
    for name in sorted(ALTERNATES):
        table = extract(
            quire_engine, semantic_module, bundle_index, SKELETONS_DIR / f"{name}.md"
        )
        fence = extract(
            quire_engine,
            semantic_module,
            bundle_index,
            SKELETONS_DIR / f"{name}.sysml.md",
        )
        assert table["fieldsForm"] == "table", name
        assert fence["fieldsForm"] == "fence", name
        assert table["fields"] == fence["fields"], name


@pytest.mark.trace("TC-062", "FR-005-AC-3")
def test_under_the_bundle_index_every_skeleton_extracts_clean(
    quire_engine, semantic_module, bundle_index
):
    for path in skeleton_paths():
        record = extract(quire_engine, semantic_module, bundle_index, path)
        diagnostics = record.get("diagnostics", [])
        assert not [d for d in diagnostics if d.get("severity") == "error"], (
            path.name,
            diagnostics,
        )
        assert not [
            d for d in diagnostics if d.get("code") == "semantic.unresolved-type"
        ], (path.name, diagnostics)
        for decl in record.get("fields") or []:
            target = decl["type"]["target"]
            if target in KERNEL_SCALARS:
                continue
            assert target.startswith(TYPE_TARGET_PREFIX), (path.name, target)


@pytest.mark.trace("TC-063", "FR-005-AC-4")
def test_availability_states_match_each_type(
    quire_engine, semantic_module, bundle_index
):
    for path in skeleton_paths():
        name = frontmatter(path.read_text())["object"]
        record = extract(quire_engine, semantic_module, bundle_index, path)
        availability = record["availability"]
        expected = {
            "fields": "available" if name in FIELD_BEARING else "not_applicable",
            "clauses": "available" if name in INVARIANT_BEARING else "not_applicable",
            "operations": (
                "available" if name in OPERATION_BEARING else "not_applicable"
            ),
        }
        actual = {kind: availability[kind]["state"] for kind in expected}
        assert actual == expected, (path.name, actual)


@pytest.mark.trace("TC-064", "FR-005-AC-5")
def test_every_negative_fixture_fails_for_its_own_reason(quire_engine):
    """Seven of the ten fixtures surface as `semantic.record-invalid`, so the
    code alone does not tell them apart: each fixture also names a `detail:`
    substring no other fixture's message carries, and both are asserted."""
    fixtures = sorted(NEGATIVE_DIR.glob("*.md"))
    assert len(fixtures) >= 10, "the ten named negative cases are not all present"
    expected_codes = {
        "semantic.record-invalid",
        "semantic.properties-both-forms",
        "semantic.dangling-clause-ref",
        "semantic.invalid-type-token",
    }
    seen: set[str] = set()
    details: dict[str, str] = {}
    for path in fixtures:
        text = path.read_text()
        front = frontmatter(text)
        assert front["expect"] in expected_codes, path.name
        assert front["because"], f"{path.name} does not say why it must fail"
        assert front["detail"], f"{path.name} names no distinguishing detail"
        seen.add(front["expect"])
        details[path.name] = front["detail"]
        result = quire_engine.validate_document(front["type"], str(PACKAGE_ROOT), text)
        assert not result["is_valid"], path.name
        messages = [e["message"] for e in result["errors"]]
        hits = [m for m in messages if front["expect"] in m]
        assert hits, (path.name, messages)
        assert any(front["detail"] in m for m in hits), (
            path.name,
            front["detail"],
            hits,
        )
    assert seen == expected_codes
    assert len(set(details.values())) == len(details), "two fixtures share a detail"


@pytest.mark.trace("TC-065", "FR-005-AC-6")
def test_every_skeleton_heading_is_asserted_and_every_required_heading_is_present():
    for path in skeleton_paths():
        text = path.read_text()
        name = frontmatter(text)["object"]

        # A locator names its heading with `after_heading` (section_body,
        # code_block) or `under_section` (table_row).
        def heading_of(loc):
            return loc.get("after_heading") or loc.get("under_section")

        asserted = {
            heading_of(loc)
            for loc in locators(object_type(name)).values()
            if heading_of(loc)
        }
        required = {
            heading_of(loc)
            for loc in locators(object_type(name)).values()
            if loc.get("required") and heading_of(loc)
        }
        body = re.sub(r"^```.*?^```\s*$", "", text, flags=re.DOTALL | re.MULTILINE)
        headings = {
            m.group(1).strip() for m in re.finditer(r"^## (.+)$", body, re.MULTILINE)
        }
        assert headings <= asserted, (path.name, headings - asserted)
        assert required <= headings, (path.name, required - headings)


@pytest.mark.trace("TC-066", "FR-005-AC-7")
def test_every_skeleton_is_placeholder_free():
    tokens = ("TODO", "TBD", "{{", "}}", "XXX", "FIXME", "lorem ipsum")
    for path in skeleton_paths():
        body = re.sub(
            r"^---\n.*?\n---\n", "", path.read_text(), count=1, flags=re.DOTALL
        )
        body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
        for token in tokens:
            assert token.lower() not in body.lower(), (path.name, token)
        assert len(body.strip()) > 200, path.name


@pytest.mark.trace("TC-067", "FR-005-AC-8")
def test_skeleton_titles_are_distinct_identifiers_and_object_equals_type():
    titles: dict[str, str] = {}
    for path in skeleton_paths():
        front = frontmatter(path.read_text())
        title = front["title"]
        assert IDENTIFIER.match(title), (path.name, title)
        assert title not in KERNEL_SCALARS, (path.name, title)
        assert front["object"] == front["type"], path.name
        stem = path.stem.removesuffix(".sysml")
        owner = titles.setdefault(title, stem)
        assert owner == stem, f"{title} is used by both {owner} and {stem}"
    declared = {ot["name"] for ot in object_types()}
    assert set(titles.values()) == declared


@pytest.mark.trace("TC-068", "FR-005-AC-9")
def test_the_measurement_and_occurrence_rows_are_actually_extracted(
    quire_engine, semantic_module, bundle_index
):
    """The three item rules that only an extracted record can evidence: a unit
    on an SLI/SLO field, and an identity plus a `Timestamp` row on an
    incident."""
    for name in ("sli", "slo"):
        record = extract(
            quire_engine, semantic_module, bundle_index, SKELETONS_DIR / f"{name}.md"
        )
        measured = [f for f in record["fields"] if f["type"].get("unit")]
        assert measured, (name, record["fields"])

    record = extract(
        quire_engine, semantic_module, bundle_index, SKELETONS_DIR / "incident.md"
    )
    assert [f for f in record["fields"] if f.get("identity")]
    assert [f for f in record["fields"] if f["type"]["target"] == "Timestamp"]


@pytest.mark.trace("TC-069", "FR-005-CON-1")
def test_the_branch_edits_no_corpus_repository_or_vendored_fixture():
    """FR-005-CON-1, inspection over the branch diff against `main`."""
    diff = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if diff.returncode != 0:  # pragma: no cover - a detached clone has no origin/main
        pytest.fail(f"cannot read the branch diff: {diff.stderr.strip()}")
    changed = [line for line in diff.stdout.splitlines() if line]
    assert changed, "the branch changes nothing"
    for path in changed:
        assert not path.startswith("corpus/"), path
        assert "fixtures/semantic-module" not in path, path
        assert "/vendor/" not in path, path


@pytest.mark.trace("TC-070", "FR-005-CON-2")
def test_a_properties_section_with_both_forms_is_refused(quire_engine):
    path = NEGATIVE_DIR / "properties-both-forms.md"
    text = path.read_text()
    result = quire_engine.validate_document(
        frontmatter(text)["type"], str(PACKAGE_ROOT), text
    )
    assert not result["is_valid"]
    assert any(
        "semantic.properties-both-forms" in e["message"] for e in result["errors"]
    )
