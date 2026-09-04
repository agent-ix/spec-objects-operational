---
id: Task-008
title: "NFR-001 — additive-compatibility verification"
type: Task
status: done
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-operational/Task-006
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/Task-007
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-080
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-081
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-082
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-083
    type: verifies
---
# Task-008: NFR-001 — additive-compatibility verification

## Scope

Measure, rather than assume, that 0.3.0 is additive over the artifacts that exist
today.

## Subtasks

- [x] **Locators and lint rules.** Zero 0.2.0 definitions changed, compared structurally against the frozen baseline.
- [x] **Legacy skeletons.** All eight 0.2.0 skeletons validate under 0.3.0 with zero errors, and the test asserts *why*: none carries a frontmatter `object:` key, so Quire runs headings-only validation and never assembles a typed record.
- [x] **The engine defect beside it.** A legacy-form artifact that *does* declare `object:` fails `semantic.record-invalid` even under `legacy_forms: warning`; carried as a strict expected failure naming `agent-ix/quire-rs#391`, never as a relaxed schema.
- [x] **Lexicon.** The term set is intact and exactly the three issue #5 definitions differ, each by restoring text the 0.2.0 value truncated — asserted as a strict-prefix relation, not as an equality against a hand-copied string.
- [x] **Yields.** Each `required: true` 0.2.0 `section_body` locator yields a byte-identical body under 0.2.0 and 0.3.0, checked against an independent regex oracle rather than a second engine run.

## Deliverables

- `tests/test_additive_compatibility.py`
- Tests for TC-080..TC-083

## Notes

- The population this NFR measures is the frozen 0.2.0 skeleton set, and the
  statement says so; yields of the `code_block` and `frontmatter_field` locators are
  unmeasured and are not claimed.
