---
id: Task-005
title: "FR-005 — executable skeletons, sysml alternates and negative fixtures"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-operational/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-operational/US-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-060
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-061
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-062
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-063
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-064
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-065
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-066
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-067
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-068
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-070
    type: verifies
---
# Task-005: FR-005 — executable skeletons, sysml alternates and negative fixtures

## Scope

Rewrite every skeleton as an executable typed fixture in the quoin FR-071/FR-072
Markdown forms, add the three `sysml` alternates, and add the ten negative fixtures
that pin what the schemas and the engine refuse.

## Subtasks

- [x] **Typed `## Properties`.** The six types that require `fields` author one table with the header exactly `Field | Type | Multiplicity | Constraints`; `alert` and `runbook` carry no such section because their models forbid `fields`.
- [x] **The item rules, authored.** `sli` and `slo` each carry a `Type` cell with a trailing bracketed unit; `incident` carries one `identity` row and one `Timestamp` row; `configuration` and `migration` carry neither an identity nor a `Timestamp` row.
- [x] **`## Invariants`.** Every skeleton, one `### <clauseId>` per clause, each owning exactly one ```ocl``` fence.
- [x] **`## Operations`.** `runbook` and `deployment`, one `### <name>` per operation with an optional param table, a `Returns:` line and `Pre:`/`Post:` lines naming clauses declared in the same artifact.
- [x] **Alternates.** `configuration.sysml.md`, `sli.sysml.md`, `deployment.sysml.md` declaring the same fields as one ```sysml``` fence under the same `id` and `title`.
- [x] **Frontmatter.** Every skeleton gains `object: <type>` beside `type: <type>`, and every `title` is a distinct `Identifier` outside `KernelScalar`.
- [x] **Negative fixtures.** Ten under `tests/fixtures/negative/`, each with `expect:`, `detail:` and `because:`.

## Deliverables

- `spec_objects_operational/skeletons/*.md` (8 rewritten + 3 alternates)
- `tests/fixtures/negative/*.md` (10)
- Tests for TC-060..TC-070

## Notes

- A triple-backtick sequence inside an HTML authoring comment opens a fence and hides
  the section that follows from a `code_block` locator; the comments name fence
  languages as `` `ocl` ``, never as a literal fence.
- Seven of the ten negatives surface as `semantic.record-invalid`, so the code alone
  does not tell them apart — each carries a `detail:` substring no other fixture's
  message carries, and the test asserts both.
- The bundle index carries one entry per frontmatter `id`, not one per file: the
  resolver matches entries rather than distinct ids, so a per-file index would raise
  `semantic.ambiguous-type` on the alternates' shared title.
- Unblocks: Task-006, Task-008.
