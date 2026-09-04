---
id: Task-004
title: "FR-003 — manifest 0.3.0, semantic block, reference data_schema and the lexicon repair"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-operational/Task-003
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/Task-007
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-030
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-031
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-032
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-034
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-035
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-037
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-038
    type: verifies
---
# Task-004: FR-003 — manifest 0.3.0, semantic block, reference data_schema and the lexicon repair

## Scope

Turn `manifest.yaml` into a semantic module: version 0.3.0, the quoin FR-070
`semantic` block, and a reference-form `data_schema` per exported object type — without
changing a single 0.2.0 locator, lint rule or lexicon term. Also repairs the three
lexicon definitions issue #5 records as truncated.

## Subtasks

- [x] **`semantic` block.** Exactly the nine admitted keys: `contract_version: 1.0.0`, `semantic_core: 0.1.0`, `package: agent-ix/spec-objects-operational`, `exports` (the eight object-type names), `imports: {}`, `targets: [json-schema, markdown]`, `mappings: [typed-table, sysml-fence, ocl-clause]`, `compatibility_posture: additive`, `legacy_forms: warning`.
- [x] **Reference-form `data_schema`.** `{ schema: schemas/<Model>.json, digest: sha256:<hex> }` on every exported type, the digest written by the generator over the shipped bytes. No inline `data_schema` survives.
- [x] **Version.** `version: 0.3.0`, bumped together with the `@jsonSchema` base in one commit.
- [x] **Locator and lint-rule preservation.** Every 0.2.0 locator keeps its `from`, heading, `language`, `required`, `multiple` and `assert` facets, compared structurally against the checked-in baseline from Task-007; the `configuration-scope` rule keeps its three allowed values and `warning` severity.
- [x] **Lexicon repair (issue #5).** Every definition becomes a quoted scalar, so a comma can no longer truncate one and mint a garbage second key; `container`, `deployment` and `build` are restored to the wording issue #5 names as lost. No term is added, removed or renamed.
- [x] **Loader verification.** `quire.Registry.load_from([module dir])` lists all eight archetypes; a copy whose `semantic` block gains `foo` is refused; a copy with an altered digest drops that object type alone.

## Deliverables

- `spec_objects_operational/manifest.yaml` at 0.3.0
- Tests for TC-030, TC-031, TC-032, TC-034, TC-035, TC-037, TC-038

## Notes

- The manifest-schema copy all three consumers judge against is
  `agent-ix/spec-artifacts-iso` at `6686f11` — the only copy admitting both the
  `semantic` block and the FR-043 `lexicon` block. The narrower copy
  `agent-ix/filament-core-service` still ships is a real divergence, filed as
  `agent-ix/filament-core-service#26`, and this module does not drop its lexicon to
  satisfy it.
- The refusals are silent in quire 0.46.0 (`agent-ix/quire-rs#221`, `#394`), so the
  naming half of FR-003-AC-6 is an explicit expected failure, not a dropped criterion.
- This task is the only writer of the `semantic` block, the version, the
  `data_schema` values and the lexicon. Task-006 is the only writer of the added
  locators.
- Unblocks: Task-005, Task-006, Task-009, Task-010's re-verification half.
