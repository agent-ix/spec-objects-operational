---
id: FR-006
title: "Require a declaration key only when its source section is required"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-operational/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-operational/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-operational/FR-005"
    type: "depends_on"
---
# FR-006: Require a declaration key only when its source section is required

## Description

An object type's declaration schema SHALL NOT require a record key whose source
section the same module's manifest locator marks optional (`required: false`),
so that a document satisfying every mandatory locator is not refused as
`semantic.record-invalid` for a key it was allowed to omit.

## Inputs

- The manifest `properties`, `invariants` and `operations` locators of the eight
  object types, all `required: false`.
- The declaration record Quire assembles per artifact, which omits a key whose
  section is absent ([FR-004](./FR-004-role-schemas.md) Inputs).

## Outputs

- `Configuration`, `Migration`, `Sli`, `Slo`, `Alert`, `Runbook`, `Incident` and
  `Deployment` list no required key.

## Behavior

- A key made optional here keeps every item rule it had: `minItems`, `contains`
  and the occurrence-field rules apply to the key whenever it is present.
- The absence of `fields`, `clauses` or `operations` is a valid declaration, not
  a defect.
- Locators stay as they are: no section is made mandatory by this requirement.
- This manifest declares no `construct:` for any type. If one is added later and requires a member, that member's locator SHALL become `required: true` in the same change and its schema key required again.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | No shipped object-type schema lists a required key; a record lacking `fields`, `clauses` or `operations` validates against each type that declares the key, and a skeleton with its `## Properties`, `## Invariants` or `## Operations` section removed validates. | Test |
| FR-006-AC-2 | A present key is still checked: an empty `fields`, `clauses` or `operations` array, an `Slo` field without a unit, an `Incident` without an occurrence field, or a `Deployment` with an empty `operations` array fails. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-005](./FR-005-executable-skeletons.md)
