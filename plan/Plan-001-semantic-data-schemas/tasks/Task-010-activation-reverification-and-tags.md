---
id: Task-010
title: "FR-001 / StR-001 — activation re-verification and trace tags"
type: Task
status: done
track: B
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-operational/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/FR-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/StR-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-001
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-002
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-003
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-004
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-005
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-006
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-007
    type: verifies
---
# Task-010: FR-001 / StR-001 — activation re-verification and trace tags

## Scope

The manifest changed, so re-verify the activation contract against the pinned schema
revision, and give every pre-existing test a tracking tag so the coverage denominator
is real.

## Subtasks

- [x] **Manifest validation.** The 0.3.0 manifest validates through `quire.validate_manifest` against the pinned FR-035 copy with zero violations.
- [x] **Verification methods.** FR-001's cells read `Test`, the declared class, rather than the uncatalogued `Schema Test` / `Integration Test`.
- [x] **Trace tags.** Every symbol in `tests/test_basic.py`, `tests/test_manifest.py` and `tests/test_skeletons_and_validate.py` carries a `@pytest.mark.trace`, so `quire coverage` reports a real denominator instead of a hollow one.
- [x] **StR-001-VC-3.** A standing definition and an observed execution are distinguishable by schema alone.
- [ ] **Activation rows.** FR-001-AC-2..AC-4, StR-001-VC-1 and VC-2 need a running `filament-core-service`; environment-gated behind `FILAMENT_CORE_URL`.

## Deliverables

- `tests/test_activation_and_stakeholder.py`
- Trace tags across the three pre-existing test modules
- Tests for TC-001..TC-007

## Notes

- Repinning the manifest schema to the `spec-artifacts-iso` copy surfaced
  `agent-ix/filament-core-service#26`: the service's own copy admits neither the
  `semantic` block nor the `lexicon` block, so this manifest cannot validate against
  it. Recorded, not worked around.
- The four activation rows are pre-existing issue #1 debt, not this issue's, and they
  are not semantic rows — they skip rather than fail, and their matrix rows stay
  `🚧` with that note.
