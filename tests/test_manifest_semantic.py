"""Manifest contract tests (FR-003): the `semantic` block, its reference-form
`data_schema`, locator preservation, the lint rule, the repaired lexicon, and
what Quire's loader refuses.
"""

from __future__ import annotations

import shutil

import pytest
import yaml

from tests.conftest import (
    OBJECT_TYPES,
    PACKAGE_ROOT,
    REPO_ROOT,
    frontmatter,
    load_manifest,
)

ADMITTED_KEYS = {
    "contract_version",
    "semantic_core",
    "package",
    "exports",
    "imports",
    "targets",
    "mappings",
    "compatibility_posture",
    "legacy_forms",
}

#: The three definitions `agent-ix/spec-objects-operational#5` records as
#: truncated by an unquoted comma, with the wording that issue names as lost.
RESTORED_DEFINITIONS = {
    "container": "a packaged, isolated runtime unit",
    "deployment": "a released, running instance of a service",
    "build": "a produced, versioned artifact from source",
}


def module_copy(tmp_path, mutate=None):
    """A throwaway copy of the module directory, optionally with a mutated
    manifest. Returns the *search path* the loader walks, not the module dir."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    root = tmp_path / "module"
    shutil.copytree(PACKAGE_ROOT, root)
    if mutate is not None:
        data = yaml.safe_load((root / "manifest.yaml").read_text())
        mutate(data)
        (root / "manifest.yaml").write_text(yaml.safe_dump(data, sort_keys=False))
    return tmp_path


@pytest.mark.trace("TC-030", "FR-003-AC-1", "FR-003-CON-1")
def test_the_semantic_block_carries_the_nine_admitted_keys_and_eight_exports(
    semantic_block,
):
    assert set(semantic_block) == ADMITTED_KEYS
    assert semantic_block["contract_version"] == "1.0.0"
    assert semantic_block["package"] == "agent-ix/spec-objects-operational"
    assert semantic_block["exports"] == list(OBJECT_TYPES)
    assert semantic_block["imports"] == {}
    assert semantic_block["targets"] == ["json-schema", "markdown"]
    assert semantic_block["mappings"] == ["typed-table", "sysml-fence", "ocl-clause"]
    assert semantic_block["compatibility_posture"] == "additive"
    assert semantic_block["legacy_forms"] == "warning"


@pytest.mark.trace("TC-034", "FR-003-AC-4")
def test_the_registry_loads_all_eight_archetypes(quire_engine):
    registry = quire_engine.Registry.load_from([str(REPO_ROOT)])
    names = set(registry.archetype_names())
    for name in OBJECT_TYPES:
        assert name in names, f"{name} did not load from the module"


@pytest.mark.trace("TC-034", "FR-003-AC-4")
def test_validate_document_reports_no_semantic_load_failure_for_any_skeleton(
    quire_engine, skeletons
):
    for path in skeletons:
        text = path.read_text()
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        assert result["is_valid"], (path.name, result["errors"])
        assert not [
            e for e in result["errors"] if "semantic." in e["message"]
        ], path.name


@pytest.mark.xfail(
    strict=True,
    reason=(
        "FR-003-AC-6 requires the refusal to NAME the offending key and schema "
        "path. quire empties the registry silently instead: no "
        "ArchetypeLoadFailure, no semantic.* code, nothing naming `foo` or the "
        "path. Blocked on agent-ix/quire-rs#221 (unknown key). "
        "The criterion stands; the schema is "
        "not relaxed and the test is not skipped."
    ),
)
@pytest.mark.trace("TC-035", "FR-003-AC-6")
def test_the_refusal_names_the_offending_key_and_path(quire_engine, tmp_path):
    def add_unknown_key(data):
        data["semantic"]["foo"] = "bar"

    unknown = module_copy(tmp_path / "named-key", add_unknown_key)
    with pytest.raises(Exception) as error:
        quire_engine.Registry.load_from([str(unknown)])
    assert "foo" in str(error.value)


@pytest.mark.trace("TC-037", "FR-003-AC-7", "FR-003-CON-3")
def test_every_lexicon_definition_is_one_whole_scalar_with_the_restorations():
    """agent-ix/spec-objects-operational#5: an unquoted flow-mapping value
    truncates at the first comma and mints a garbage second key. Loading the
    manifest is the oracle — a truncated entry shows up as an extra key."""
    lexicon = load_manifest()["lexicon"]
    for term, entry in lexicon.items():
        assert set(entry) == {"definition"}, f"{term} minted a truncation key: {entry}"
        assert entry["definition"].strip(), term
    for term, definition in RESTORED_DEFINITIONS.items():
        assert lexicon[term]["definition"] == definition, term
        assert "," in definition, term


@pytest.mark.trace("TC-038", "FR-003-AC-8")
def test_the_configuration_scope_lint_rule_is_present():
    rules = load_manifest()["lint_rules"]
    rule = next(r for r in rules if r["id"] == "configuration-scope")
    assert rule["allowed"] == ["creation", "runtime", "session"]
    assert rule["severity"] == "warning"
