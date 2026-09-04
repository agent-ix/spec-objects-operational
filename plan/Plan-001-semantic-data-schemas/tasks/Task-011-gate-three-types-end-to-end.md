---
id: Task-011
title: "Gate — Migration, Sli and Incident end to end"
type: Task
status: done
track: Gate
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-operational/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-042
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-043
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-047
    type: verifies
---
# Task-011: Gate — Migration, Sli and Incident end to end

## Scope

Before the remaining five types are authored against it, measure whether the
item-rule encoding survives the real 2020-12 validator rather than only `tsp compile`.
Three types cover the three encodings that could each fail independently.

## Subtasks

- [x] **`Migration`** — the zero-identity encoding (`@contains` + `@minContains(0)` + `@maxContains(0)`) and the occurrence-row ban riding an `allOf`.
- [x] **`Sli`** — the positive `@contains(MeasuredField)` encoding over a marker whose discriminator sits two levels down (`type.unit`).
- [x] **`Incident`** — two `contains` predicates on one array, the second through `@extension("allOf", …)` with a relative `$ref` the generator normalizes.
- [x] **The seal** — `unevaluatedProperties: {not: {}}` still refuses an unknown key when an `allOf` branch evaluates the same property.

## Deliverables

- The three schemas validating their positive records and refusing their negatives
  through `jsonschema` with a `referencing` registry over the committed bytes.

## Notes

- **Result: passed on the first attempt.** The emitter's decorator recipe and the
  `allOf` second predicate both survive the real validator with the schemas sealed.
- If it had failed, the item-rule encoding would have been wrong and the remaining
  five types must not have been authored against it.
- Unblocks: Task-003.
