"""Activation and stakeholder tests, covering FR-001, IT-001 and the
StR-001 validation criteria.

FR-001-AC-1 and StR-001-VC-3 are discharged here against the committed tree.
FR-001-AC-2..AC-4, StR-001-VC-1 and StR-001-VC-2 need a running
`filament-core-service` at revision `a77f31e` or later; they are environment-
gated and their matrix rows stay `🚧` with that note. That is pre-existing
debt from issue #1, not this issue's, and it is not the semantic suite: the
Quire rows fail rather than skip (see `conftest.py`).
"""

from __future__ import annotations

import hashlib
import json
import os

import pytest

from tests.conftest import (
    MANIFEST_PATH,
    MODEL_OF,
    OBJECT_TYPES,
    REPO_ROOT,
    load_manifest,
)

# The FR-035 module-manifest schema as `agent-ix/spec-artifacts-iso` ships it
# at `6686f11` — the copy Quoin and Quire actually load, and the only copy that
# admits BOTH the `semantic` block (quoin FR-070) and the `lexicon` block
# (FR-043) this manifest carries. FR-001, FR-003 and IT-001 all judge this
# manifest against this one revision.
#
# `agent-ix/filament-core-service` still carries a narrower copy of its own
# (neither `semantic` nor `lexicon`), against which this manifest cannot
# validate; that divergence is filed as agent-ix/filament-core-service#26 and
# is not worked around here — the pin names the copy the engines load.
VENDORED_SCHEMA = REPO_ROOT / "tests" / "fixtures" / "module-manifest.schema.json"
VENDORED_SCHEMA_DIGEST = (
    "52bddd1c14e0df06e95322db45734925990a4472e6b4c980a5c14f00480bb874"
)

FILAMENT_CORE_URL = os.environ.get("FILAMENT_CORE_URL")
needs_filament_core = pytest.mark.skipif(
    not FILAMENT_CORE_URL,
    reason=(
        "FR-001-AC-2..AC-4 / IT-001 need a running filament-core-service at "
        "revision a77f31e or later (no release tag contains it). Set "
        "FILAMENT_CORE_URL to run them; the matrix row stays 🚧 until then."
    ),
)


@pytest.mark.trace("TC-001", "FR-001-AC-1")
def test_the_manifest_validates_against_the_pinned_fr035_schema(quire_engine):
    digest = hashlib.sha256(VENDORED_SCHEMA.read_bytes()).hexdigest()
    assert digest == VENDORED_SCHEMA_DIGEST, (
        "the vendored module-manifest schema is not the spec-artifacts-iso "
        "6686f11 revision the spec pins; FR-001 and FR-003 would judge the "
        "manifest against different schemas"
    )
    violations = quire_engine.validate_manifest(load_manifest(), str(VENDORED_SCHEMA))
    assert violations == [], violations


@pytest.mark.integration
@needs_filament_core
@pytest.mark.trace("TC-002", "FR-001-AC-2", "IT-001-SC-01")
def test_activation_against_a_clean_filament_core_returns_200():
    import urllib.request

    request = urllib.request.Request(
        f"{FILAMENT_CORE_URL.rstrip('/')}/api/v1/modules/activate",
        data=MANIFEST_PATH.read_bytes(),
        headers={"Content-Type": "application/yaml"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        assert response.status == 200


@pytest.mark.integration
@needs_filament_core
@pytest.mark.trace("TC-003", "FR-001-AC-3", "IT-001-SC-03")
def test_reactivation_is_a_content_hash_no_op():
    import urllib.request

    hashes = []
    for _ in range(2):
        request = urllib.request.Request(
            f"{FILAMENT_CORE_URL.rstrip('/')}/api/v1/modules/activate",
            data=MANIFEST_PATH.read_bytes(),
            headers={"Content-Type": "application/yaml"},
            method="POST",
        )
        with urllib.request.urlopen(request) as response:
            hashes.append(json.loads(response.read())["content_hash"])
    assert hashes[0] == hashes[1]


@pytest.mark.integration
@needs_filament_core
@pytest.mark.trace("TC-004", "FR-001-AC-4", "IT-001-SC-02", "TC-005", "StR-001-VC-1")
def test_every_declared_contribution_is_readable_from_the_registry_endpoints():
    """FR-001-AC-4 and StR-001-VC-1 observe the same run: activation registers
    the contents this module declares, and each exported object type's
    registered `data_schema` is the reference object as posted while
    agent-ix/filament-core-service#23 is open."""
    import urllib.request

    with urllib.request.urlopen(
        f"{FILAMENT_CORE_URL.rstrip('/')}/api/v1/object-types"
    ) as response:
        registered = {row["name"]: row for row in json.loads(response.read())}
    manifest = load_manifest()
    for declared in manifest["object_types"]:
        row = registered[declared["name"]]
        assert row["data_schema"] == declared["data_schema"]


@pytest.mark.integration
@needs_filament_core
@pytest.mark.trace("TC-006", "StR-001-VC-2")
def test_a_generator_produces_an_artifact_that_validates_against_the_shipped_module(
    quire_engine,
):
    """StR-001-VC-2, demonstration: an artifact authored from a shipped
    skeleton validates against the module the service serves."""
    from tests.conftest import PACKAGE_ROOT, SKELETONS_DIR, frontmatter

    text = (SKELETONS_DIR / "incident.md").read_text()
    result = quire_engine.validate_document(
        frontmatter(text)["type"], str(PACKAGE_ROOT), text
    )
    assert result["is_valid"]


@pytest.mark.trace("TC-007", "StR-001-VC-3")
def test_every_object_type_ships_a_typed_contract_a_fixture_reader_can_consume(
    schema_registry,
):
    """StR-001-VC-3: a standing definition and an observed execution are
    distinguishable to a consumer by schema alone, without reading the prose."""
    for name in OBJECT_TYPES:
        model = MODEL_OF[name]
        schema = json.loads(
            (
                REPO_ROOT / "spec_objects_operational" / "schemas" / f"{model}.json"
            ).read_text()
        )
        assert schema.get("properties"), f"{name} carries no declared shape"
        assert set(schema) > {"$schema", "$id", "type"}, name

    # Multiplicity.json (semantic-core 0.3.0) requires `ordered`/`unique`; a
    # producer clamps both `false` on a singular multiplicity (`upper` at
    # most one). Every field below is singular, so both are `false`.
    standing_record = {
        "fields": [
            {
                "name": "storage_root",
                "type": {
                    "target": "String",
                    "multiplicity": {
                        "lower": 1,
                        "upper": 1,
                        "ordered": False,
                        "unique": False,
                    },
                },
            }
        ]
    }
    observed_record = {
        "fields": [
            {
                "name": "incident_id",
                "type": {
                    "target": "UUID",
                    "multiplicity": {
                        "lower": 1,
                        "upper": 1,
                        "ordered": False,
                        "unique": False,
                    },
                },
                "identity": True,
            },
            {
                "name": "detected_at",
                "type": {
                    "target": "Timestamp",
                    "multiplicity": {
                        "lower": 1,
                        "upper": 1,
                        "ordered": False,
                        "unique": False,
                    },
                },
            },
        ]
    }
    configuration = schema_registry("Configuration")
    incident = schema_registry("Incident")
    assert not list(configuration.iter_errors(standing_record))
    assert list(configuration.iter_errors(observed_record))
    assert not list(incident.iter_errors(observed_record))
    assert list(incident.iter_errors(standing_record))
