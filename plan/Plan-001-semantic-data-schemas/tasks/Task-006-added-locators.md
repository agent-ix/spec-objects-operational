---
id: Task-006
title: "FR-003 / FR-005 — required:false locators for the sections the skeletons introduced"
type: Task
status: done
track: A
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-operational/Task-005
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-operational/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-033
    type: verifies
---
# Task-006: FR-003 / FR-005 — required:false locators for the sections the skeletons introduced

## Scope

Assert the sections the rewritten skeletons introduce, without invalidating a single
existing artifact.

## Subtasks

- [x] **`properties`** on the six types whose models admit `fields`; **`invariants`** on all eight; **`operations`** on `runbook` and `deployment`.
- [x] **Every added locator is `required: false`**, so a 0.2.0 artifact that carries none of these sections stays valid.
- [x] **No locator asserted on a type whose model forbids the key** — `alert` and `runbook` gain no `properties` locator.

## Deliverables

- The added `body_extraction` entries in `spec_objects_operational/manifest.yaml`
- Test for TC-033

## Notes

- This is the only task that writes the added locators; Task-004 owns everything else
  in the manifest.
- Unblocks: Task-008.
