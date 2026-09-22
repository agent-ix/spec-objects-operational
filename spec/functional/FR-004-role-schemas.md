---
id: FR-004
title: "Give every operational object type a role-distinct declaration schema"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-operational/US-001"
    type: "implements"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
---
# FR-004: Give every operational object type a role-distinct declaration schema

## Description

The TypeSpec source SHALL declare one model per operational object type whose
emitted schema validates that type's declaration record
`{ fields?, clauses?, operations?, … }` with type-specific required keys,
forbidden keys, and item rules, so that no type is a placeholder, each
operational role refuses the records that violate its own rules, a standing
definition is refused where an observed execution is required and the reverse,
and operational evidence is referenced through exactly one key on exactly one
type.

## Inputs

- semantic-core 0.3.0 grammar models: `FieldDecl`, `RelationDecl`,
  `OperationDecl`, `ClauseRef`, `EnumValue`, `Identifier`, `SemanticId`,
  `UnitSymbol`, `KernelScalar`.
- The declaration record Quire assembles per artifact: `fields` from
  `## Properties`, `clauses` from `## Invariants`, `operations` from
  `## Operations` (quire-rs FR-070/FR-071), with any key absent when its
  section is absent.
- The `agent-ix/quoin#267` operational evidence record family, referenced by
  `SemanticId` and never copied.

## Outputs

- Eight object-type models, each emitted as `schemas/<Model>.json`, sealed
  (`unevaluatedProperties: {not: {}}`).
- Support models emitted as sibling files: the open marker schemas
  `IdentityField`, `OccurrenceField`, `OccurrenceTypeRef`, `MeasuredField`,
  and `UnitTypeRef`; the declaration models `ScopeAssignment`, `RollbackDecl`,
  `RolloutDecl`, `ObjectiveDecl`, `AlertCondition`, `RunbookStep`, and
  `EvidenceRef`; the scalar `EvidenceRecordId`; and the closed enums
  `ConfigurationScope`, `RollbackStrategy`, `RolloutStrategy`, `Comparator`,
  `AlertSeverity`, and `EvidenceRecordShape` — nineteen support models in all.

## Behavior

Each model SHALL enforce its row of the following table. "Identity field"
means a `FieldDecl` with `identity: true`; "occurrence field" a `FieldDecl`
whose `type.target` is `Timestamp`; "measured field" a `FieldDecl` whose
`type.unit` is present (a `Type` cell of the form `Duration [ms]`, quoin
FR-071). All three readings are semantic-core 0.3.0 and quoin FR-071 reader
conventions, so a release that renders `identity: false`, namespaces kernel
scalars, or moves `unit` off `TypeRef` is a breaking change to these schemas
and SHALL be handled by a manifest version bump, not by widening a rule.

"Occurrence identity" means an identity field *and* an occurrence field
together: which one it was, and when it was. It is not the same as an identity
field alone. `Deployment` requires an identity field — a release is a named,
addressable thing — and is still a standing definition, because it admits no
occurrence field: a deployment declaration says what the release *is*, and
`deployed_at` belongs to the execution that applied it. `Incident` is the only
model that requires occurrence identity, and the only model that admits an
occurrence field at all.

| Object type | Model | Required keys | Optional keys | Item rules |
|---|---|---|---|---|
| configuration | `Configuration` | `fields` | `scopes: ScopeAssignment[]`, `configures: SemanticId[]`, `clauses`, `operations` | `fields` has ≥ 1 item, 0 identity fields (a parameter set is keyed by the configured object, not by itself) and 0 occurrence fields; `relations` forbidden |
| migration | `Migration` | `fields`, `clauses` | `rollback: RollbackDecl`, `migrates: SemanticId[]`, `dependsOn: SemanticId[]`, `operations` | `fields` has ≥ 1 item, 0 identity fields and 0 occurrence fields (an `applied_at` row is execution state); `clauses` has ≥ 1 item — a migration declares the safety condition it preserves; `relations` forbidden |
| sli | `Sli` | `fields` | `measures: SemanticId[]`, `clauses` | `fields` has ≥ 1 item, ≥ 1 measured field and 0 occurrence fields; `operations` forbidden — an SLI declares a measurement, not behaviour |
| slo | `Slo` | `fields`, `clauses` | `objective: ObjectiveDecl`, `constrains: SemanticId[]`, `dependsOn: SemanticId[]` | `fields` has ≥ 1 item, ≥ 1 measured field and 0 occurrence fields; `clauses` has ≥ 1 item — the objective is an invariant over the SLI; `operations` forbidden |
| alert | `Alert` | `clauses` | `conditions: AlertCondition[]`, `escalatesTo: SemanticId[]`, `references: SemanticId[]`, `operations` | `clauses` has ≥ 1 item — an alert is a firing condition; `fields` forbidden |
| runbook | `Runbook` | `operations` | `steps: RunbookStep[]`, `remediates: SemanticId[]`, `clauses` | `operations` has ≥ 1 item — a runbook declares the actions an operator performs; `fields` forbidden |
| incident | `Incident` | `fields` | `evidence: EvidenceRef[]`, `correlates: SemanticId[]`, `breaches: SemanticId[]`, `triggers: SemanticId[]`, `clauses`, `operations` | `fields` has ≥ 1 item, ≥ 1 identity field, and ≥ 1 occurrence field — an incident is an observed occurrence and is the only type that is |
| deployment | `Deployment` | `fields`, `operations` | `rollout: RolloutDecl`, `deploys: SemanticId[]`, `dependsOn: SemanticId[]`, `relations`, `clauses` | `fields` has ≥ 1 item, ≥ 1 identity field (the release identity) and 0 occurrence fields; `operations` has ≥ 1 item (the lifecycle actions) |

- `ScopeAssignment` SHALL be `{ parameter: Identifier, scope: ConfigurationScope }` with `ConfigurationScope` the closed set `creation`, `runtime`, `session` — the same vocabulary the 0.2.0 `configuration-scope` lint rule allows on the untyped `## Configuration` table.
- `RollbackDecl` SHALL be `{ strategy: RollbackStrategy, clause?: ClauseRef, doc?: string }` with `RollbackStrategy` the closed set `reversible`, `forward_only`, `compensating`.
- `RolloutDecl` SHALL be `{ strategy: RolloutStrategy, rollback?: RollbackDecl, doc?: string }` with `RolloutStrategy` the closed set `recreate`, `rolling`, `blue_green`, `canary`.
- `ObjectiveDecl` SHALL be `{ sli: SemanticId, target: float64, unit?: UnitSymbol, window: string matching the ISO 8601 duration form }`.
- `AlertCondition` SHALL be `{ name: Identifier, sli: SemanticId, comparator: Comparator, threshold: float64, window: string matching the ISO 8601 duration form, severity: AlertSeverity }` with `Comparator` the closed set `lt`, `lte`, `gt`, `gte` and `AlertSeverity` the closed set `page`, `ticket`, `info`.
- `RunbookStep` SHALL be `{ name: Identifier, order: int32 ≥ 1, doc: string, operation?: Identifier }`.
- `EvidenceRef` SHALL be `{ shape: EvidenceRecordShape, record: EvidenceRecordId, doc?: string }`.
- `EvidenceRecordShape` SHALL be quoin FR-059's own `record_shape` enum — the closed set `standing_capability`, `exercise` — copied as a correspondence rather than invented here, because a reference whose vocabulary does not match the referenced family cannot name a real record. FR-059 owns the values; a change there is a breaking change to this module.
- `EvidenceRecordId` SHALL carry quoin FR-059's own `$defs/identity` pattern, `^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$`, rather than the `SemanticId` pattern: FR-059 identifies its records with a bare token (`artifact-store-capability`), so a reference admitting only `ix://…` could not name most of the family it claims to map to. An `ix://…` identity still matches the pattern, so a record that does carry one is unaffected.
- The `evidence` key SHALL be declared by `Incident` and by no other model, so operational evidence has exactly one canonical semantic mapping; every other model refuses an `evidence` key through its seal.
- An `EvidenceRef.record` SHALL name a record of the operational evidence family quoin FR-059 defines (`agent-ix/quoin#267` is that programme's closed epic). Which record it names is not checkable from here — no schema can reach the neighbour's store — so this requirement claims the *pattern* and the *shape vocabulary* only, and states the referential half as unverified rather than asserting it.
- No model SHALL redeclare any field of that evidence record, so this module maps to the evidence programme rather than minting a second record family.
- No model SHALL declare a key for an accumulated observation, a measured sample, a consumed error budget, an applied-migration timestamp, or a database execution state; each such key is refused by the model's seal, so a standing definition cannot carry the values that only an execution has.
- Every standing-definition model that admits `fields` (`Configuration`, `Migration`, `Sli`, `Slo`, `Deployment`) SHALL admit zero occurrence fields, so the purity rule holds over declaration *rows* and not only over record keys: without it a `Migration` could declare `applied_at : Timestamp` and be an observed execution wearing a standing definition's schema.
- The TypeSpec source SHALL express that ban as an `@extension("allOf", …)` clause carrying `contains: OccurrenceField.json` with `minContains: 0` and `maxContains: 0`; `minContains: 0` is required because the keyword defaults to 1 and would otherwise contradict `maxContains: 0`.
- This specification SHALL NOT claim that purity is enforced over field *names*. A row named `consumed_budget` typed `Decimal(5,4) [1]` is a well-formed measured field and no JSON Schema over `FieldDecl` can refuse it; the enforceable rules are the key seal and the occurrence-row ban above, and the remaining discipline is a review obligation, recorded here rather than asserted as a refusal.
- Where a consumer needs a migration's execution state, that consumer SHALL read it through the `migrates` reference to the migrated schema or through an `Incident` that references the migration, never through a key on `Migration`.
- Every `fields`, `params`, `clauses`, `operations`, and `relations` item SHALL be validated by `$ref` to the semantic-core 0.3.0 model, never by a copied definition.
- `Deployment` SHALL be the only model that declares `relations`; the other seven refuse the key through their seal. The table names the refusal only where the key would otherwise be expected.
- The TypeSpec source SHALL express the item rules through the official emitter's decorators over open marker models: `@contains(IdentityField)` for "≥ 1 identity field", `@contains(IdentityField) @minContains(0) @maxContains(0)` for "0 identity fields", `@contains(MeasuredField)` for "≥ 1 measured field", and, because JSON Schema admits one `contains` per array, the incident occurrence rule as an `@extension("allOf", …)` clause whose `contains` references `OccurrenceField.json`; the generator normalizes that relative `$ref` per [FR-002](./FR-002-emitted-json-schemas.md).
- Every cross-reference a declaration makes (`type.target`, `configures`, `measures`, `constrains`, `dependsOn`, `migrates`, `deploys`, `escalatesTo`, `references`, `correlates`, `breaches`, `triggers`, `ObjectiveDecl.sli`, `AlertCondition.sli`) SHALL be a `SemanticId` or `KernelScalar` per semantic-core — `EvidenceRef.record` is the one deliberate exception, and carries the neighbour's own pattern for the reason above — so a bare token is rejected by the schema; resolution against the bundle, and the placeholder `ix://<org>/<repo>/unresolved/<Token>` with its `semantic.unresolved-type` finding, exist today for `type.target` only (quire-rs FR-070) and for the other keys once `agent-ix/quoin#335` publishes their mapping.
- Each schema SHALL describe the declared shape only. `Configuration`, `Migration`, `Sli`, `Slo`, `Alert`, `Runbook`, and `Deployment` are standing definitions and carry no occurrence identity; `Incident` is the one observed execution and is the only model that requires one.
- Where a key is declared but the current extractor does not populate it (`scopes`, `configures`, `rollback`, `migrates`, `dependsOn`, `measures`, `objective`, `constrains`, `conditions`, `escalatesTo`, `references`, `steps`, `remediates`, `evidence`, `correlates`, `breaches`, `triggers`, `rollout`, `deploys`) — and likewise `relations` — the key SHALL be optional, so a record produced by today's extractor validates and a future extractor can fill it without a schema change.
- The test suite SHALL verify every criterion over a key the extractor does not populate against a hand-built JSON record rather than an extracted one, naming that limitation in the test itself, so that no row claims extraction evidence it does not have; the extraction path for those keys is `agent-ix/quoin#335` (mapping) and its quire-rs successor.
- An `AlertCondition.sli` SHALL name an `sli` artifact of the same bundle.
- A `RunbookStep.operation` SHALL name an `operations[].name` of the same record.
- A `ScopeAssignment.parameter` SHALL name a `fields[].name` of the same record.
- JSON Schema cannot express any of those three rules, so all three are reader rules stated here for the extractor that first populates those keys; none is claimed as a schema refusal.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-004-CON-1 | No model SHALL redeclare a semantic-core model or scalar; the module namespace contributes archetype shapes only (semantic-core NFR-014 kernel discipline). | Architecture | Test |
| FR-004-CON-2 | The empty record `{}` SHALL fail every one of the eight object-type schemas, because every type has a non-empty required set. | Integrity | Test |
| FR-004-CON-3 | Exactly one model SHALL declare `evidence`. | Boundary | Test |
| FR-004-CON-4 | No model SHALL declare a key holding an observation, sample, consumed budget, or execution timestamp. | Boundary | Test |
| FR-004-CON-5 | No standing-definition model SHALL admit an occurrence field. | Boundary | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | Each of the eight shipped object-type schemas differs from every other in at least one required, forbidden, or item rule listed in the table; a schema with only `type: object` is absent. | Test |
| FR-004-AC-2 | A configuration record with one non-identity field validates against `Configuration.json`, with `scopes` accepted when present; the same record with an identity field fails; a record with no `fields` fails. | Test |
| FR-004-AC-3 | A migration record with one non-identity field and one clause validates against `Migration.json`, with `rollback` accepted when present; the same record without `clauses` fails; a record with an identity field fails. | Test |
| FR-004-AC-4 | An SLI record whose field carries a `type.unit` validates against `Sli.json`; the same record with the unit removed fails; a record carrying `operations` fails. | Test |
| FR-004-AC-5 | An SLO record with a measured field and one clause validates against `Slo.json`, with `objective` accepted when present; the same record without `clauses` fails; a record carrying `operations` fails. | Test |
| FR-004-AC-6 | An alert record with one clause validates against `Alert.json`, with `conditions` accepted when present; a record carrying `fields` fails; a record with an empty `clauses` array fails. | Test |
| FR-004-AC-7 | A runbook record with one operation validates against `Runbook.json`, with `steps` accepted when present; a record carrying `fields` fails; a record with an empty `operations` array fails. | Test |
| FR-004-AC-8 | An incident record with an identity field and a `Timestamp` field validates against `Incident.json`, with `evidence` accepted when present; the same record without the `Timestamp` field fails; the same record without the identity field fails. | Test |
| FR-004-AC-9 | A deployment record with an identity field and one operation validates against `Deployment.json`, with `rollout` accepted when present; the same record without `operations` fails; the same record with the identity flag removed fails. | Test |
| FR-004-AC-10 | The empty record `{}` fails all eight object-type schemas, and a record carrying an `observations` key fails every one of them. The second half holds for any unknown key, so it is evidence of the seal only; the type-specific purity evidence is FR-004-AC-14. | Test |
| FR-004-AC-11 | `evidence` is declared by `Incident.json` and by no other shipped schema; an `evidence` entry whose `record` falls outside quoin FR-059's `$defs/identity` pattern fails, one carrying an `ix://` identity (also a valid FR-059 `record_id`) validates, and one whose `shape` is outside `EvidenceRecordShape` fails. | Test |
| FR-004-AC-12 | A `type.target` of `ix://agent-ix/spec-objects-operational/unresolved/Mystery` is accepted by the schema (it is a `SemanticId`) and reported by the extractor as `semantic.unresolved-type`; a bare `Mystery` string is rejected by the schema. | Test |
| FR-004-AC-13 | No module schema redeclares a semantic-core model; every grammar item across the eight object-type schemas is a `$ref` to semantic-core 0.3.0. | Test |
| FR-004-AC-14 | A record adding one `Timestamp` field to an otherwise valid configuration, migration, SLI, SLO or deployment record fails that type's schema, while the same field added to a valid incident record still validates; `Incident.json` is the only shipped schema whose `fields` admits an occurrence field. | Test |
| FR-004-AC-15 | A record violating each of the three cross-key reader rules (`AlertCondition.sli`, `RunbookStep.operation`, `ScopeAssignment.parameter`) is refused. Blocked: JSON Schema cannot express any of the three and `agent-ix/quoin#335` owns the mapping that will, so the criterion is carried as an explicit expected failure — the test asserts the refusal and is marked strict-xfail, and it turns red the day the engine can enforce it. | Test |

## Dependencies

- **Upstream**: semantic-core FR-031 (`ix://agent-ix/filament-core-data/FR-031`); quoin FR-071 (`ix://agent-ix/quoin/FR-071`) for the measured-field and identity readings; the `agent-ix/quoin#267` evidence record family
- **Build**: [FR-002](./FR-002-emitted-json-schemas.md) emits these models
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md); `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` read these schemas as fixtures
