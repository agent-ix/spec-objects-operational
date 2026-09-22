import "@typespec/json-schema";
import "@agent-ix/semantic-core";

using TypeSpec.JsonSchema;
using AgentIx.Semantic.Core;

/**
 * Tier-2 operational object declaration schemas (agent-ix/spec-objects-operational#6).
 *
 * One model per operational object type this module contributes, each validating
 * that type's Quire declaration record (fields, relations, clauses,
 * operations; quire-rs FR-070..FR-072) with type-specific required keys,
 * forbidden keys, and item rules (FR-004). Every grammar item is a `$ref` to
 * `@agent-ix/semantic-core` 0.3.0 and is never redeclared here (FR-004-CON-1);
 * this namespace contributes archetype shapes only.
 *
 * The module's central distinction (FR-004): `Configuration`, `Migration`,
 * `Sli`, `Slo`, `Alert`, `Runbook`, and `Deployment` are *standing definitions*
 * — what a system is configured to do, promises, and how it is remediated.
 * `Incident` is the one *observed execution*, and the only model that requires
 * an occurrence identity or declares `evidence`. Every model is sealed
 * (`...Record<never>`), so no type can carry an accumulated observation, a
 * measured sample, a consumed error budget, or an applied-migration timestamp;
 * those live in the `agent-ix/quoin#267` evidence record family, which
 * `EvidenceRef` references and never copies.
 *
 * The `$id` base embeds the manifest `version` by intent (FR-002-CON-5): one
 * schema URL names exactly one immutable byte sequence, so a downstream fixture
 * reader that pinned a version can never silently read later bytes. A bump edits
 * this base and `manifest.yaml`'s `version` in one commit and re-runs
 * `make schemas`.
 */
@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-operational/0.3.0/")
namespace AgentIx.SpecObjects.Operational;

// ---------------------------------------------------------------------------
// Open marker models — `@contains` predicates only
// ---------------------------------------------------------------------------

/**
 * Open marker: a `FieldDecl` flagged as identity. Used only as the `@contains`
 * predicate for the "≥ 1 identity field" and "0 identity fields" item rules;
 * it is deliberately open so it matches any identity-flagged field.
 */
model IdentityField {
  identity: true;
}

/** Open marker: a `TypeRef` whose target is the kernel `Timestamp` scalar. */
model OccurrenceTypeRef {
  target: KernelScalar.Timestamp;
}

/**
 * Open marker: a `FieldDecl` whose type targets `Timestamp` — the occurrence
 * time an observed-execution declaration must carry. Used as a `@contains`
 * predicate on `Incident.fields`.
 */
model OccurrenceField {
  type: OccurrenceTypeRef;
}

/** Open marker: a `TypeRef` carrying a unit symbol (quoin FR-071 `Type [unit]`). */
model UnitTypeRef {
  unit: UnitSymbol;
}

/**
 * Open marker: a `FieldDecl` whose type carries a unit — the typed measurement
 * an SLI or SLO declares. Used as a `@contains` predicate.
 */
model MeasuredField {
  type: UnitTypeRef;
}

// ---------------------------------------------------------------------------
// Closed vocabularies
// ---------------------------------------------------------------------------

/**
 * When a configuration parameter takes effect. The same closed set the 0.2.0
 * `configuration-scope` lint rule allows on the untyped `## Configuration`
 * table, so the typed and untyped forms cannot disagree.
 */
enum ConfigurationScope {
  creation,
  runtime,
  session,
}

/** How a migration can be undone. */
enum RollbackStrategy {
  reversible,
  forward_only,
  compensating,
}

/** How a new version replaces the running one. */
enum RolloutStrategy {
  recreate,
  rolling,
  blue_green,
  canary,
}

/** Threshold comparison of an alert condition. */
enum Comparator {
  lt,
  lte,
  gt,
  gte,
}

/** What a fired alert condition does. */
enum AlertSeverity {
  page,
  ticket,
  info,
}

/**
 * The shape of the operational evidence record an incident references.
 *
 * This is quoin FR-059's `record_shape` enum, copied as a *correspondence*
 * rather than invented here: a reference whose vocabulary does not match the
 * referenced family cannot name a real record. FR-059 owns the values; a
 * change there is a breaking change to this module.
 */
enum EvidenceRecordShape {
  standing_capability,
  exercise,
}

/**
 * A quoin FR-059 `record_id`.
 *
 * The pattern is FR-059's own `$defs/identity`, not a `SemanticId`: FR-059
 * identifies its records with a bare token (`artifact-store-capability`), and
 * a reference that only admits `ix://…` could not name most of the family it
 * claims to map to. An `ix://…` identity still matches, so a record that does
 * carry one is unaffected.
 */
@pattern("^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
scalar EvidenceRecordId extends string;

// ---------------------------------------------------------------------------
// Support declaration models
// ---------------------------------------------------------------------------

/**
 * One parameter's scope.
 *
 * Reader rule JSON Schema cannot express (FR-004): `parameter` names a
 * `fields[].name` of the same record. It is stated for the extractor that
 * first populates `scopes` (agent-ix/quoin#335) and is not claimed as a
 * schema refusal.
 */
model ScopeAssignment {
  parameter: Identifier;
  scope: ConfigurationScope;
  ...Record<never>;
}

/** A migration's declared undo intent. Never its execution state. */
model RollbackDecl {
  strategy: RollbackStrategy;
  clause?: ClauseRef;
  doc?: string;
  ...Record<never>;
}

/** A deployment's declared release strategy and its undo intent. */
model RolloutDecl {
  strategy: RolloutStrategy;
  rollback?: RollbackDecl;
  doc?: string;
  ...Record<never>;
}

/**
 * A service-level objective: the SLI it reads, the target it promises, and the
 * window it promises it over. It carries no consumed error budget and no
 * measured sample; those are observations, and an observation is reached
 * through an `Incident` and its `evidence`, never through a key here.
 */
model ObjectiveDecl {
  sli: SemanticId;
  target: float64;
  unit?: UnitSymbol;

  @pattern("^P(?!$)(\\d+Y)?(\\d+M)?(\\d+W)?(\\d+D)?(T(?=\\d)(\\d+H)?(\\d+M)?(\\d+(\\.\\d+)?S)?)?$")
  window: string;

  ...Record<never>;
}

/**
 * One firing condition of an alert.
 *
 * Reader rule JSON Schema cannot express (FR-004): `sli` names an `sli`
 * artifact of the same bundle.
 */
model AlertCondition {
  name: Identifier;
  sli: SemanticId;
  comparator: Comparator;
  threshold: float64;

  @pattern("^P(?!$)(\\d+Y)?(\\d+M)?(\\d+W)?(\\d+D)?(T(?=\\d)(\\d+H)?(\\d+M)?(\\d+(\\.\\d+)?S)?)?$")
  window: string;

  severity: AlertSeverity;
  ...Record<never>;
}

/**
 * One ordered step of a runbook.
 *
 * Reader rule JSON Schema cannot express (FR-004): `operation` names an
 * `operations[].name` of the same record.
 */
model RunbookStep {
  name: Identifier;

  @minValue(1)
  order: int32;

  doc: string;
  operation?: Identifier;
  ...Record<never>;
}

/**
 * A reference into the operational evidence record family that quoin FR-059 defines
 * (`agent-ix/quoin#267` is its closed epic).
 *
 * This is the module's single canonical mapping to that family: `Incident`
 * declares `evidence` and no other model does, and no model redeclares any
 * field of the referenced record. An incompatibility with that programme is
 * resolved by changing this reference, never by minting a second record family
 * here.
 */
model EvidenceRef {
  shape: EvidenceRecordShape;
  record: EvidenceRecordId;
  doc?: string;
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Object-type declaration records — standing definitions
// ---------------------------------------------------------------------------

/**
 * Seals the standing definitions against an occurrence row.
 *
 * The seal (`...Record<never>`) refuses an *observation key*; it says nothing
 * about a `fields` row. Without this rule a `Migration` could declare
 * `applied_at : Timestamp` and a `Deployment` a `deployed_at : Timestamp`, and
 * the type would be an observed execution wearing a standing definition's
 * schema. `Incident` is the only model that admits an occurrence field, and it
 * requires one. JSON Schema admits one `contains` per array, so this second
 * predicate rides an `allOf` clause; `minContains: 0` is required because the
 * keyword defaults to 1 and would otherwise contradict `maxContains: 0`.
 */

/**
 * A configuration: the tunable parameters of a configurable object. A
 * parameter set is keyed by the object it configures, not by itself, so it
 * carries no identity field. `relations` is forbidden by the seal.
 */
@extension(
  "allOf",
  #[#{
    properties: #{
      fields: #{ contains: #{ `$ref`: "OccurrenceField.json" }, minContains: 0, maxContains: 0 }
    }
  }]
)
model Configuration {
  @minItems(1)
  @contains(IdentityField)
  @minContains(0)
  @maxContains(0)
  fields: FieldDecl[];

  scopes?: ScopeAssignment[];
  configures?: SemanticId[];
  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  ...Record<never>;
}

/**
 * A migration: a versioned change and the safety condition it preserves.
 *
 * `clauses` is required because a migration that states no safety condition
 * states nothing a reviewer can check. The declaration carries rollback
 * *intent* (`rollback`) and never execution state: no applied-at timestamp, no
 * row count, no database status. A consumer needing execution state reads it
 * through `migrates` or through an `Incident` that references the migration.
 * `relations` is forbidden by the seal.
 */
@extension(
  "allOf",
  #[#{
    properties: #{
      fields: #{ contains: #{ `$ref`: "OccurrenceField.json" }, minContains: 0, maxContains: 0 }
    }
  }]
)
model Migration {
  @minItems(1)
  @contains(IdentityField)
  @minContains(0)
  @maxContains(0)
  fields: FieldDecl[];

  @minItems(1)
  clauses: ClauseRef[];

  rollback?: RollbackDecl;
  migrates?: SemanticId[];
  dependsOn?: SemanticId[];
  operations?: OperationDecl[];
  ...Record<never>;
}

/**
 * A service level indicator: what is measured, in what unit.
 *
 * At least one field carries a `type.unit`, so the declaration references a
 * typed measurement rather than describing one in prose. `operations` is
 * forbidden by the seal: an SLI declares a measurement, not behaviour. Every
 * accumulated observation key is forbidden by the seal.
 */
@extension(
  "allOf",
  #[#{
    properties: #{
      fields: #{ contains: #{ `$ref`: "OccurrenceField.json" }, minContains: 0, maxContains: 0 }
    }
  }]
)
model Sli {
  @minItems(1)
  @contains(MeasuredField)
  fields: FieldDecl[];

  measures?: SemanticId[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/**
 * A service level objective: the promise made over an SLI.
 *
 * `clauses` is required because the objective is an invariant over the
 * indicator, expressed as a clause; `objective` carries the same promise in
 * typed form once the extractor populates it. `operations` is forbidden by the
 * seal, and so is every consumed-budget or sample key.
 */
@extension(
  "allOf",
  #[#{
    properties: #{
      fields: #{ contains: #{ `$ref`: "OccurrenceField.json" }, minContains: 0, maxContains: 0 }
    }
  }]
)
model Slo {
  @minItems(1)
  @contains(MeasuredField)
  fields: FieldDecl[];

  @minItems(1)
  clauses: ClauseRef[];

  objective?: ObjectiveDecl;
  constrains?: SemanticId[];
  dependsOn?: SemanticId[];
  ...Record<never>;
}

/**
 * An alert: a firing condition over an indicator.
 *
 * `fields` is forbidden by the seal — an alert declares a condition, not data.
 * `clauses` is required and carries the condition; `conditions` carries the
 * same condition in typed form once the extractor populates it.
 */
model Alert {
  @minItems(1)
  clauses: ClauseRef[];

  conditions?: AlertCondition[];
  escalatesTo?: SemanticId[];
  references?: SemanticId[];
  operations?: OperationDecl[];
  ...Record<never>;
}

/**
 * A runbook: the operations an operator performs to remediate something.
 *
 * `fields` is forbidden by the seal — a runbook declares actions, not data.
 * `operations` is required; `steps` orders them once the extractor populates
 * it.
 */
model Runbook {
  @minItems(1)
  operations: OperationDecl[];

  steps?: RunbookStep[];
  remediates?: SemanticId[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

/**
 * A deployment: a released, running instance of a deployable and its lifecycle
 * operations.
 *
 * `fields` carries the release identity, so at least one row is an identity
 * field; `operations` carries the lifecycle actions (deploy, roll back, scale)
 * and has at least one item. `rollout` is the declared release strategy, never
 * an executed rollout.
 */
@extension(
  "allOf",
  #[#{
    properties: #{
      fields: #{ contains: #{ `$ref`: "OccurrenceField.json" }, minContains: 0, maxContains: 0 }
    }
  }]
)
model Deployment {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  @minItems(1)
  operations: OperationDecl[];

  rollout?: RolloutDecl;
  deploys?: SemanticId[];
  dependsOn?: SemanticId[];
  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Object-type declaration record — the one observed execution
// ---------------------------------------------------------------------------

/**
 * An incident: something that happened.
 *
 * This is the module's one observed-execution type and the only model that
 * requires an occurrence identity — at least one identity field (which
 * incident it was) and at least one `Timestamp` field (when it was). The
 * second `contains` predicate is expressed through `allOf`, because JSON
 * Schema admits one `contains` per array.
 *
 * `Incident` is also the only model that declares `evidence`, which is what
 * makes the `agent-ix/quoin#267` mapping canonical: exactly one key on exactly
 * one type, referencing that family's records by `SemanticId` and copying none
 * of their fields.
 */
@extension(
  "allOf",
  #[#{ properties: #{ fields: #{ contains: #{ `$ref`: "OccurrenceField.json" } } } }]
)
model Incident {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  evidence?: EvidenceRef[];
  correlates?: SemanticId[];
  breaches?: SemanticId[];
  triggers?: SemanticId[];
  clauses?: ClauseRef[];
  operations?: OperationDecl[];
  ...Record<never>;
}
