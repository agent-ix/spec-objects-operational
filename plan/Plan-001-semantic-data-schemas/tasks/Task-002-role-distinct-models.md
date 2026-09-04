---
id: Task-002
title: "FR-004 — the eight role-distinct models and their support models"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-operational/Task-001
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-operational/US-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-040
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-041
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-042
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-043
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-044
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-045
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-046
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-047
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-048
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-049
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-050
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-051
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-052
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-053
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-054
    type: verifies
---
# Task-002: FR-004 — the eight role-distinct models and their support models

## Scope

Declare one model per operational object type in `typespec/main.tsp`, each with its
own required keys, forbidden keys and item rules, and the support models the item
rules and the reference keys need. This is where the module's central distinction is
encoded: seven standing definitions against one observed execution.

## Subtasks

- [x] **Standing definitions.** `Configuration` (fields, zero identity), `Migration` (fields + clauses, zero identity), `Sli` (fields with a measured field, operations forbidden), `Slo` (fields with a measured field + clauses, operations forbidden), `Alert` (clauses, fields forbidden), `Runbook` (operations, fields forbidden), `Deployment` (fields with an identity row + operations).
- [x] **The one observed execution.** `Incident` requires an identity row AND a `Timestamp` row — the second predicate through `@extension("allOf", …)`, because JSON Schema admits one `contains` per array.
- [x] **The occurrence-row ban.** Every standing definition that admits `fields` carries an `allOf` clause with `contains: OccurrenceField.json`, `minContains: 0`, `maxContains: 0`, so purity holds over declaration rows and not only over record keys.
- [x] **The single evidence mapping.** `Incident` alone declares `evidence: EvidenceRef[]`; `EvidenceRef` carries quoin FR-059's own `record_id` pattern and `record_shape` vocabulary and redeclares no field of that record.
- [x] **Support models.** The five open markers, `ScopeAssignment`, `RollbackDecl`, `RolloutDecl`, `ObjectiveDecl`, `AlertCondition`, `RunbookStep`, `EvidenceRef`, and the closed enums.
- [x] **Kernel discipline.** No semantic-core model or scalar is redeclared; every grammar item is a `$ref`.

## Deliverables

- `typespec/main.tsp`
- `spec_objects_operational/schemas/*.json` (27 files, emitted)
- Tests for TC-040..TC-054

## Notes

- Required keys are drawn only from `{fields, clauses, operations}` — the keys the
  extractor populates today. Every other key is optional, so a record produced by
  today's extractor validates and a future extractor can fill it without a schema
  change.
- Rows over the unpopulated keys are verified against hand-built JSON records and say
  so; they are schema evidence, not extraction evidence.
- Purity over field *names* is not claimed: a row named `consumed_budget` typed
  `Decimal(5,4) [1]` is a well-formed measured field and no JSON Schema over
  `FieldDecl` can refuse it. The enforceable rules are the key seal and the
  occurrence-row ban.
- Unblocks: Task-011 (gate), then Task-003.
