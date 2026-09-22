"""Additive-compatibility tests (NFR-001): the 0.3.0 module stays additive
over the checked-in 0.2.0 set.

The population is the frozen baseline under `tests/fixtures/baseline-0.2.0/`:
the 0.2.0 `body_extraction` locators, the 0.2.0 `lint_rules`, the 0.2.0
lexicon term set, and all eight 0.2.0 skeletons, captured before this change
touched anything.
"""

from __future__ import annotations

import json
import re

import pytest

from tests.conftest import (
    BASELINE_DIR,
    PACKAGE_ROOT,
    frontmatter,
    load_manifest,
    locators,
    object_type,
)

#: The `required: true` `section_body` locators of 0.2.0, per type. These are
#: the yields NFR-001-AC-4 measures; `code_block` and `frontmatter_field`
#: yields are not claimed.
REQUIRED_SECTION_YIELDS = {
    "runbook": ("steps", "Steps"),
    "incident": ("timeline", "Timeline"),
}


def baseline_locators() -> dict:
    return json.loads((BASELINE_DIR / "body_extraction.json").read_text())


def baseline_skeletons() -> list:
    return sorted((BASELINE_DIR / "skeletons").glob("*.md"))


@pytest.mark.trace("TC-080", "NFR-001-AC-1")
def test_no_baseline_locator_or_lint_rule_definition_changed():
    baseline = baseline_locators()
    assert baseline["version"] == "0.2.0"
    changed = []
    for name, extraction in baseline["object_types"].items():
        old = (extraction or {})["yield_pattern"]["match"]
        new = locators(object_type(name))
        for key, facets in old.items():
            if new.get(key) != facets:
                changed.append(f"{name}.{key}")
    assert changed == []
    assert load_manifest()["lint_rules"] == baseline["lint_rules"]


@pytest.mark.trace("TC-081", "NFR-001-AC-2")
def test_every_baseline_skeleton_validates_under_the_new_manifest(quire_engine):
    """Measured, not assumed: the eight 0.2.0 skeletons carry no frontmatter
    `object:` key, so Quire runs headings-only validation on them and the
    typed record is never assembled or checked. That is what makes 0.3.0
    additive for the artifacts that exist today."""
    baseline = baseline_skeletons()
    assert len(baseline) == 8
    failures = {}
    for path in baseline:
        text = path.read_text()
        assert "object" not in frontmatter(text), path.name
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        if result["errors"]:
            failures[path.name] = [e["message"] for e in result["errors"]]
    assert failures == {}


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The engine defect NFR-001's Verification names: once a legacy-form "
        "artifact carries `object:`, quire 0.47.1 assembles its declaration "
        "record as `{}` and checks it against the type schema "
        "unconditionally, so it fails `semantic.record-invalid` at error "
        "severity even under `legacy_forms: warning`. "
        "agent-ix/quire-rs#391 owns the rule. The schema is not relaxed and "
        "the row is an expected failure, never a skip."
    ),
)
@pytest.mark.trace("TC-081", "NFR-001-AC-2")
def test_a_legacy_form_artifact_that_declares_its_object_is_not_an_error(quire_engine):
    text = (BASELINE_DIR / "skeletons" / "incident.md").read_text()
    text = text.replace("type: incident\n", "type: incident\nobject: incident\n", 1)
    result = quire_engine.validate_document("incident", str(PACKAGE_ROOT), text)
    assert [e["message"] for e in result["errors"]] == []


@pytest.mark.trace("TC-082", "NFR-001-AC-3")
def test_the_lexicon_term_set_is_intact_and_only_the_three_issue_5_entries_differ():
    baseline = baseline_locators()
    current = load_manifest()["lexicon"]
    assert sorted(current) == baseline["lexicon_terms"]

    truncated = json.loads(
        json.dumps({term: entry for term, entry in _baseline_lexicon().items()})
    )
    differing = {
        term
        for term in current
        if current[term]["definition"] != truncated[term].get("definition")
    }
    assert differing == {"container", "deployment", "build"}, differing
    for term in differing:
        # Each differs by RESTORING text: the 0.2.0 value is a strict prefix.
        assert current[term]["definition"].startswith(
            truncated[term]["definition"]
        ), term
        assert len(current[term]["definition"]) > len(truncated[term]["definition"])


def _baseline_lexicon() -> dict:
    """The 0.2.0 lexicon as YAML actually parsed it — truncations included.

    Read from the frozen 0.2.0 manifest, so the truncation this test measures
    is the real one and not a re-description of it.
    """
    import yaml

    return yaml.safe_load((BASELINE_DIR / "manifest.yaml").read_text())["lexicon"]


@pytest.mark.trace("TC-083", "NFR-001-AC-4")
def test_each_required_020_section_yield_is_byte_identical_across_versions(
    quire_engine,
):
    """The untyped section bodies are what every existing consumer reads; the
    0.3.0 locators must leave them untouched."""
    for name, (key, heading) in REQUIRED_SECTION_YIELDS.items():
        path = BASELINE_DIR / "skeletons" / f"{name}.md"
        extracted = quire_engine.extract(name, str(PACKAGE_ROOT), path.read_text())
        records = extracted["extraction"]
        assert len(records) == 1, (name, records)
        assert records[0][key] == expected_section_body(path, heading), name


def expected_section_body(path, heading: str) -> str:
    """The named section body as it stood at 0.2.0, read straight from the
    frozen fixture — an independent oracle, not another engine run."""
    text = path.read_text()
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    match = re.search(
        rf"^## {re.escape(heading)}[ \t]*$(.*?)(?=^## |\Z)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    assert match, f"{path.name} has no `## {heading}` section"
    return match.group(1).strip()
