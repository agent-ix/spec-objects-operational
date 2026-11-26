"""Role-schema tests (FR-004): each object type's declaration schema accepts
the records its role admits and refuses the records its role forbids.

Every record here is hand-built JSON validated against the shipped schema
files. The keys the extractor does not populate today (`scopes`, `configures`,
`rollback`, `migrates`, `dependsOn`, `measures`, `objective`, `constrains`,
`conditions`, `escalatesTo`, `references`, `steps`, `remediates`, `evidence`,
`correlates`, `breaches`, `triggers`, `rollout`, `deploys`, `relations`) can
be exercised no other way, so these are **schema evidence, not extraction
evidence** — the extraction path for them is `agent-ix/quoin#335` and its
quire-rs successor. Tests that depend on it say so in their docstring.
"""

from __future__ import annotations

import json

import pytest

from tests.conftest import (
    MODEL_OF,
    OBJECT_TYPES,
    REPO_ROOT,
    SCHEMAS_DIR,
    STANDING_WITH_FIELDS,
)


def field(
    name: str,
    target: str = "String",
    *,
    identity: bool = False,
    unit: str | None = None,
) -> dict:
    # Multiplicity.json (semantic-core) requires `ordered`/`unique`; a
    # producer clamps both `false` on a singular multiplicity (`upper` at
    # most one). Every field this helper builds is singular.
    target_ref = (
        {"kind": "SemanticId", "value": target}
        if target.startswith("ix://")
        else {"kind": "KernelScalar", "value": target}
    )
    type_ref: dict = {
        "target": target_ref,
        "multiplicity": {"lower": 1, "upper": 1, "ordered": False, "unique": False},
    }
    if unit is not None:
        type_ref["unit"] = unit
    decl: dict = {"name": name, "type": type_ref}
    if identity:
        decl["identity"] = True
    return decl


CLAUSE = {"language": "ocl", "clauseId": "SomeInvariant"}
OPERATION = {"name": "deploy", "params": [field("image_digest", "String")]}
RELATION = {
    "verb": "deploys",
    "category": "dependency",
    "target": "ix://agent-ix/spec-objects-operational/type/ArtifactStore",
}
MEASURED = field("latency", "Duration", unit="ms")
OCCURRENCE = field("detected_at", "Timestamp")


def ok(validator, record) -> bool:
    return not list(validator.iter_errors(record))


def schema_of(name: str) -> dict:
    return json.loads((SCHEMAS_DIR / f"{MODEL_OF[name]}.json").read_text())


def valid_record(name: str) -> dict:
    """A minimal record each type's schema accepts."""
    return {
        "configuration": {"fields": [field("storage_root")]},
        "migration": {"fields": [field("target_table")], "clauses": [CLAUSE]},
        "sli": {"fields": [MEASURED]},
        "slo": {"fields": [MEASURED], "clauses": [CLAUSE]},
        "alert": {"clauses": [CLAUSE]},
        "runbook": {"operations": [OPERATION]},
        "maintenance_plan": {"operations": [OPERATION]},
        "incident": {
            "fields": [field("incident_id", "UUID", identity=True), OCCURRENCE]
        },
        "deployment": {
            "fields": [field("release_id", identity=True)],
            "operations": [OPERATION],
        },
    }[name]


@pytest.mark.trace("TC-040", "FR-004-AC-1")
def test_every_object_type_schema_differs_from_every_other_and_none_is_bare(
    schema_registry,
):
    schemas = {name: schema_of(name) for name in OBJECT_TYPES}
    fingerprints = {}
    for name, schema in schemas.items():
        assert set(schema) > {
            "$schema",
            "$id",
            "type",
        }, f"{name} is a bare `type: object`"
        assert schema["unevaluatedProperties"] == {"not": {}}, f"{name} is not sealed"
        fingerprints[name] = (
            tuple(sorted(schema.get("required", []))),
            tuple(sorted(schema["properties"])),
            json.dumps(
                {k: v for k, v in schema["properties"].items() if "contains" in v},
                sort_keys=True,
            ),
            json.dumps(schema.get("allOf", []), sort_keys=True),
        )
    for left in OBJECT_TYPES:
        for right in OBJECT_TYPES:
            if left < right:
                assert (
                    fingerprints[left] != fingerprints[right]
                ), f"{left} and {right} are identical"


@pytest.mark.trace("TC-041", "FR-004-AC-2")
def test_configuration_requires_fields_and_refuses_an_identity_row(schema_registry):
    """`scopes` is exercised against a hand-built record: the extractor does
    not populate it (agent-ix/quoin#335)."""
    configuration = schema_registry("Configuration")
    record = {"fields": [field("storage_root")]}
    assert ok(configuration, record)
    assert ok(configuration, {"fields": [field("f32_value", "Float32")]})
    assert ok(configuration, {"fields": [field("f64_value", "Float64")]})
    assert ok(
        configuration,
        {**record, "scopes": [{"parameter": "storage_root", "scope": "creation"}]},
    )
    assert not ok(
        configuration,
        {**record, "scopes": [{"parameter": "storage_root", "scope": "boot"}]},
    )
    assert not ok(
        configuration, {"fields": [field("config_id", "UUID", identity=True)]}
    )
    # FR-006: the key is optional, so its absence validates.
    assert ok(configuration, {})
    assert not ok(configuration, {"fields": []})


@pytest.mark.trace("TC-042", "FR-004-AC-3")
def test_migration_requires_a_safety_clause_and_refuses_an_identity_row(
    schema_registry,
):
    """`rollback` is exercised against a hand-built record: the extractor does
    not populate it (agent-ix/quoin#335)."""
    migration = schema_registry("Migration")
    record = {"fields": [field("target_table")], "clauses": [CLAUSE]}
    assert ok(migration, record)
    assert ok(migration, {**record, "rollback": {"strategy": "reversible"}})
    assert not ok(migration, {**record, "rollback": {"strategy": "pray"}})
    # FR-006: the key is optional, so its absence validates.
    assert ok(migration, {"fields": record["fields"]})
    assert not ok(migration, {**record, "clauses": []})
    assert not ok(
        migration,
        {"fields": [field("migration_id", "UUID", identity=True)], "clauses": [CLAUSE]},
    )


@pytest.mark.trace("TC-043", "FR-004-AC-4")
def test_sli_requires_a_measured_field_and_refuses_operations(schema_registry):
    sli = schema_registry("Sli")
    assert ok(sli, {"fields": [MEASURED]})
    assert not ok(sli, {"fields": [field("latency", "Duration")]})
    assert not ok(sli, {"fields": [MEASURED], "operations": [OPERATION]})
    # FR-006: the key is optional, so its absence validates.
    assert ok(sli, {})


@pytest.mark.trace("TC-044", "FR-004-AC-5", "FR-004-AC-19")
def test_slo_requires_a_measured_field_and_a_clause_and_refuses_operations(
    schema_registry,
):
    """`objective` is exercised against a hand-built record: the extractor does
    not populate it (agent-ix/quoin#335)."""
    slo = schema_registry("Slo")
    record = {"fields": [MEASURED], "clauses": [CLAUSE]}
    objective = {
        "sli": "ix://agent-ix/spec-objects-operational/type/ArtifactStoreAvailability",
        "target": 0.999,
        "window": "P30D",
    }
    # The manifest extracts the required kernel frontmatter pair verbatim;
    # preserve it in the sealed record until the engine maps it to objective.
    assert ok(slo, {**record, "target": "99.9%", "window": "30d"})
    assert not ok(slo, {**record, "target": 0.999, "window": "30d"})
    assert not ok(slo, {**record, "target": "99.9%", "window": 30})
    assert ok(slo, record)
    assert ok(slo, {**record, "objective": objective})
    assert not ok(slo, {**record, "objective": {**objective, "window": "30 days"}})
    # FR-006: the key is optional, so its absence validates.
    assert ok(slo, {"fields": [MEASURED]})
    assert not ok(slo, {"fields": [field("ratio", "Decimal")], "clauses": [CLAUSE]})
    assert not ok(slo, {**record, "operations": [OPERATION]})


@pytest.mark.trace("TC-045", "FR-004-AC-6")
def test_alert_requires_a_clause_and_refuses_fields(schema_registry):
    """`conditions` is exercised against a hand-built record: the extractor
    does not populate it (agent-ix/quoin#335)."""
    alert = schema_registry("Alert")
    condition = {
        "name": "fast_burn",
        "sli": "ix://agent-ix/spec-objects-operational/type/ArtifactStoreAvailability",
        "comparator": "gt",
        "threshold": 14.0,
        "window": "PT5M",
        "severity": "page",
    }
    assert ok(alert, {"clauses": [CLAUSE]})
    assert ok(alert, {"clauses": [CLAUSE], "conditions": [condition]})
    assert not ok(
        alert, {"clauses": [CLAUSE], "conditions": [{**condition, "severity": "shout"}]}
    )
    assert not ok(alert, {"clauses": [CLAUSE], "fields": [field("burn_rate")]})
    assert not ok(alert, {"clauses": []})
    # FR-006: the key is optional, so its absence validates.
    assert ok(alert, {})


@pytest.mark.trace("TC-093", "FR-004-AC-16")
def test_incident_references_hazards_and_anomalies_and_no_other_type_does(
    schema_registry,
):
    """`hazards` and `anomalies` are exercised against a hand-built record: the
    extractor does not populate them (agent-ix/quoin#335)."""
    incident = schema_registry("Incident")
    ref = "ix://agent-ix/spec-objects-safety/HAZ-001"
    base = valid_record("incident")
    assert ok(incident, {**base, "hazards": [ref], "anomalies": [ref]})
    assert ok(incident, {**base, "hazards": [], "anomalies": []})
    assert ok(incident, base)
    assert not ok(incident, {**base, "hazards": ["HAZ-001"]})
    assert not ok(incident, {**base, "anomalies": ["ANOM-1"]})
    for key in ("hazards", "anomalies"):
        declaring = [
            name for name in OBJECT_TYPES if key in schema_of(name)["properties"]
        ]
        assert declaring == ["incident"], key


@pytest.mark.trace("TC-094", "FR-004-AC-17")
def test_maintenance_plan_requires_operations_owned_channels_and_assigns_nothing(
    schema_registry,
):
    """The channel, `maintains` and `responsible` keys are exercised against a
    hand-built record: the extractor does not populate them."""
    plan = schema_registry("MaintenancePlan")
    owner = "ix://agent-ix/example/ROLE-001"
    channel = {"name": "support_desk", "owner": owner}
    base = {"operations": [OPERATION]}
    assert ok(plan, base)
    assert ok(
        plan,
        {
            **base,
            "maintains": [owner],
            "responsible": [owner],
            "feedback_channels": [channel, {**channel, "doc": "Support tickets."}],
        },
    )
    assert not ok(plan, {**base, "feedback_channels": [{"name": "support_desk"}]})
    assert not ok(plan, {**base, "fields": [field("report_id", "UUID")]})
    assert not ok(plan, {**base, "severity": "high"})
    assert not ok(plan, {**base, "acceptability": "acceptable"})
    assert not ok(plan, {"operations": []})
    # FR-006: the key is optional, so its absence validates.
    assert ok(plan, {})


@pytest.mark.trace("TC-095", "FR-004-AC-18")
def test_no_judgment_key_is_declared_on_channel_plan_or_incident():
    """The module records who is accountable, never a grade."""
    judgments = {"severity", "class", "acceptability", "score"}
    for name in ("FeedbackChannel", "MaintenancePlan", "Incident"):
        schema = json.loads((SCHEMAS_DIR / f"{name}.json").read_text())
        assert not judgments & set(schema["properties"]), name


@pytest.mark.trace("TC-046", "FR-004-AC-7")
def test_runbook_requires_operations_and_refuses_fields(schema_registry):
    """`steps` is exercised against a hand-built record: the extractor does not
    populate it (agent-ix/quoin#335)."""
    runbook = schema_registry("Runbook")
    step = {"name": "acknowledge", "order": 1, "doc": "Acknowledge the page."}
    assert ok(runbook, {"operations": [OPERATION]})
    assert ok(runbook, {"operations": [OPERATION], "steps": [step]})
    assert not ok(runbook, {"operations": [OPERATION], "steps": [{**step, "order": 0}]})
    assert not ok(
        runbook, {"operations": [OPERATION], "fields": [field("page_id", "UUID")]}
    )
    assert not ok(runbook, {"operations": []})
    # FR-006: the key is optional, so its absence validates.
    assert ok(runbook, {})


@pytest.mark.trace("TC-047", "FR-004-AC-8")
def test_incident_requires_an_occurrence_identity_and_admits_evidence(schema_registry):
    """`evidence` is exercised against a hand-built record: the extractor does
    not populate it (agent-ix/quoin#335)."""
    incident = schema_registry("Incident")
    identity = field("incident_id", "UUID", identity=True)
    evidence = {
        "shape": "standing_capability",
        "record": "artifact-store-capability",
    }
    assert ok(incident, {"fields": [identity, OCCURRENCE]})
    assert ok(incident, {"fields": [identity, OCCURRENCE], "evidence": [evidence]})
    assert not ok(incident, {"fields": [identity]})
    assert not ok(incident, {"fields": [OCCURRENCE]})
    # FR-006: the key is optional, so its absence validates.
    assert ok(incident, {})


@pytest.mark.trace("TC-048", "FR-004-AC-9")
def test_deployment_requires_a_release_identity_and_lifecycle_operations(
    schema_registry,
):
    """`rollout` is exercised against a hand-built record: the extractor does
    not populate it (agent-ix/quoin#335)."""
    deployment = schema_registry("Deployment")
    record = {
        "fields": [field("release_id", identity=True)],
        "operations": [OPERATION],
    }
    assert ok(deployment, record)
    assert ok(deployment, {**record, "rollout": {"strategy": "canary"}})
    assert not ok(deployment, {**record, "rollout": {"strategy": "yolo"}})
    # FR-006: the key is optional, so its absence validates.
    assert ok(deployment, {"fields": record["fields"]})
    assert not ok(deployment, {**record, "operations": []})
    assert not ok(
        deployment, {"fields": [field("release_id")], "operations": [OPERATION]}
    )


@pytest.mark.trace("TC-049", "FR-004-AC-10", "FR-004-CON-4")
def test_an_observation_key_fails_every_type_and_the_empty_record_validates(
    schema_registry,
):
    """The `observations` half is seal evidence only: any unknown key fails a
    sealed schema. The type-specific purity evidence is the occurrence-row test below.
    """
    for name in OBJECT_TYPES:
        validator = schema_registry(MODEL_OF[name])
        # FR-006: every record key is optional, so the empty record validates.
        assert ok(validator, {}), f"{name} refused the empty record"
        polluted = dict(valid_record(name))
        polluted["observations"] = [{"at": "2026-06-02T09:12:00Z", "value": 0.974}]
        assert not ok(validator, polluted), f"{name} accepted an observations key"


@pytest.mark.trace("TC-050", "FR-004-AC-11", "FR-004-CON-3")
def test_evidence_is_declared_by_incident_alone_and_is_typed(schema_registry):
    declaring = [
        name for name in OBJECT_TYPES if "evidence" in schema_of(name)["properties"]
    ]
    assert declaring == ["incident"], declaring

    incident = schema_registry("Incident")
    base = {"fields": [field("incident_id", "UUID", identity=True), OCCURRENCE]}
    good = {"shape": "exercise", "record": "artifact-store-rollback-exercise"}
    assert ok(incident, {**base, "evidence": [good]})
    # An `ix://` identity is also a valid FR-059 `record_id`, so a record that
    # carries one is unaffected by the pattern.
    assert ok(
        incident,
        {**base, "evidence": [{**good, "record": "ix://agent-ix/quoin/EXE-0001"}]},
    )
    # A record id outside quoin FR-059's `$defs/identity` pattern is refused,
    # and so is a shape outside its `record_shape` enum.
    assert not ok(incident, {**base, "evidence": [{**good, "record": "has spaces"}]})
    assert not ok(incident, {**base, "evidence": [{**good, "shape": "vibes"}]})


@pytest.mark.trace("TC-051", "FR-004-AC-12")
def test_an_unresolved_placeholder_target_is_accepted_and_a_bare_token_is_refused(
    schema_registry, quire_engine, semantic_module
):
    incident = schema_registry("Incident")
    placeholder = {
        "name": "mystery",
        "type": {
            "target": {
                "kind": "SemanticId",
                "value": "ix://agent-ix/spec-objects-operational/unresolved/Mystery",
            },
            "multiplicity": {"lower": 1, "upper": 1, "ordered": False, "unique": False},
        },
    }
    identity = field("incident_id", "UUID", identity=True)
    assert ok(incident, {"fields": [identity, OCCURRENCE, placeholder]})
    bare = json.loads(json.dumps(placeholder))
    bare["type"]["target"] = {"kind": "KernelScalar", "value": "Mystery"}
    assert not ok(incident, {"fields": [identity, OCCURRENCE, bare]})

    markdown = (
        '---\nid: probe-001\ntitle: "Probe"\ntype: incident\nobject: incident\n---\n'
        "# [probe-001] Probe\n\n## Properties\n\n"
        "| Field | Type | Multiplicity | Constraints |\n|---|---|---|---|\n"
        "| probe_id | UUID | 1..1 | identity |\n"
        "| detected_at | Timestamp | 1..1 | |\n"
        "| mystery | Mystery | 1..1 | |\n"
    )
    record = quire_engine.extract_semantic(
        {
            "markdown": markdown,
            "module": semantic_module,
            "bundle": {
                "package": semantic_module["package"],
                "objects": [],
                "enumerations": [],
                "imports": {},
            },
        }
    )
    codes = [d.get("code") for d in record.get("diagnostics", [])]
    assert "semantic.unresolved-type" in codes


@pytest.mark.trace("TC-052", "FR-004-AC-13", "FR-004-CON-1")
def test_no_module_schema_redeclares_a_semantic_core_model():
    """FR-004-CON-1: the module namespace contributes archetype shapes only."""
    grammar = {
        "FieldDecl",
        "TypeRef",
        "TypeRefTarget",
        "Multiplicity",
        "ConstraintDecl",
        "RelationDecl",
        "OperationDecl",
        "ClauseRef",
        "EnumValue",
        "EnumValueName",
        "DefaultDecl",
        "SourceLocus",
        "KernelScalar",
        "Identifier",
        "SemanticId",
        "UnitSymbol",
    }
    shipped = {path.stem for path in SCHEMAS_DIR.glob("*.json")}
    assert shipped & grammar == set(), f"the module redeclares {shipped & grammar}"
    #: Keys whose items are `SemanticId[]` reference arrays; the emitter inlines
    #: the `$ref` on the item, so they are checked the same way.
    for name in OBJECT_TYPES:
        schema = schema_of(name)
        for key, prop in schema["properties"].items():
            item = prop.get("items", prop)
            if name == "slo" and key in {"target", "window"}:
                assert prop["type"] == "string", f"slo.{key} is a string kernel field"
                assert set(prop) <= {
                    "type",
                    "description",
                }, f"unexpected slo.{key} shape"
                if key == "target":
                    assert prop.get("description") == (
                        "Kernel frontmatter form retained until Quire maps it into "
                        "`objective`."
                    )
                else:
                    assert "description" not in prop
                continue
            assert "$ref" in item, f"{name}.{key} is not validated by $ref"


@pytest.mark.trace("TC-053", "FR-004-AC-14", "FR-004-CON-5")
def test_only_the_observed_execution_type_admits_an_occurrence_field(schema_registry):
    """FR-004-CON-5: the purity rule holds over declaration rows, not only over
    record keys. Without it a migration could declare `applied_at: Timestamp`."""
    for name in STANDING_WITH_FIELDS:
        validator = schema_registry(MODEL_OF[name])
        record = valid_record(name)
        assert ok(validator, record), name
        polluted = {
            **record,
            "fields": [*record["fields"], field("applied_at", "Timestamp")],
        }
        assert not ok(validator, polluted), f"{name} accepted an occurrence row"

    incident = schema_registry("Incident")
    record = valid_record("incident")
    assert ok(incident, record)
    assert ok(
        incident, {"fields": [*record["fields"], field("closed_at", "Timestamp")]}
    )


@pytest.mark.trace("TC-054", "FR-004-AC-15")
def test_the_three_cross_key_reader_rules_are_stated_and_owned(schema_registry):
    """The measurable half of FR-004-AC-15: the three rules are stated in the
    requirement, no shipped schema expresses them, and the mapping that will
    make them checkable is `agent-ix/quoin#335`. The refusal itself is the
    strict-xfail below."""
    text = (REPO_ROOT / "spec" / "functional" / "FR-004-role-schemas.md").read_text()
    for rule in (
        "`AlertCondition.sli` SHALL name",
        "`RunbookStep.operation` SHALL name",
        "`ScopeAssignment.parameter` SHALL name",
    ):
        assert rule in text, rule
    assert "agent-ix/quoin#335" in text
    # No shipped schema relates one key of a record to another: the only
    # cross-key keywords JSON Schema has are absent everywhere.
    for name in OBJECT_TYPES:
        rendered = json.dumps(schema_of(name))
        for keyword in ('"dependentRequired"', '"dependentSchemas"', '"if"'):
            assert keyword not in rendered, (name, keyword)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "FR-004-AC-15 requires each of the three cross-key reader rules to be "
        "refused. JSON Schema can express none of them — they relate one key of "
        "a record to another — and agent-ix/quoin#335 owns the mapping that "
        "will make them checkable. The criterion stands; the schema is not "
        "relaxed to fake it and the row is not skipped. This turns red the day "
        "the engine can enforce the rules, which is when the claim is revisited."
    ),
)
@pytest.mark.trace("TC-054", "FR-004-AC-15")
def test_the_three_cross_key_reader_rules_are_refused(schema_registry):
    configuration = schema_registry("Configuration")
    assert not ok(
        configuration,
        {
            "fields": [field("storage_root")],
            # `parameter` names no `fields[].name` of this record.
            "scopes": [{"parameter": "no_such_parameter", "scope": "runtime"}],
        },
    )
    runbook = schema_registry("Runbook")
    assert not ok(
        runbook,
        {
            "operations": [OPERATION],
            # `operation` names no `operations[].name` of this record.
            "steps": [
                {
                    "name": "acknowledge",
                    "order": 1,
                    "doc": "…",
                    "operation": "no_such_operation",
                }
            ],
        },
    )
    alert = schema_registry("Alert")
    assert not ok(
        alert,
        {
            "clauses": [CLAUSE],
            # `sli` names no `sli` artifact of any bundle.
            "conditions": [
                {
                    "name": "fast_burn",
                    "sli": "ix://agent-ix/nowhere/type/NoSuchSli",
                    "comparator": "gt",
                    "threshold": 14.0,
                    "window": "PT5M",
                    "severity": "page",
                }
            ],
        },
    )


@pytest.mark.trace("TC-092", "FR-006-AC-1", "FR-006-AC-2")
def test_a_record_lacking_an_optional_section_key_validates_and_the_key_stays_checked(
    schema_registry,
):
    """Hand-built: the record a document without the optional section yields."""
    for name in OBJECT_TYPES:
        assert not schema_of(name).get("required"), name
        assert ok(schema_registry(MODEL_OF[name]), {}), name
    identity = field("incident_id", "UUID", identity=True)
    assert not ok(schema_registry("Configuration"), {"fields": []})
    assert not ok(schema_registry("Migration"), {"clauses": []})
    assert not ok(schema_registry("Slo"), {"fields": [field("ratio", "Decimal")]})
    assert not ok(schema_registry("Alert"), {"clauses": []})
    assert not ok(schema_registry("Runbook"), {"operations": []})
    # An identity field alone fails for the missing occurrence field.
    assert not ok(schema_registry("Incident"), {"fields": [identity]})
    assert ok(schema_registry("Incident"), {"fields": [identity, OCCURRENCE]})
    assert not ok(schema_registry("Deployment"), {"operations": []})
