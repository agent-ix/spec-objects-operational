---
id: NFR-001
title: "Additive compatibility of the semantic contract"
type: NFR
quality_attribute: compatibility
relationships:
  - target: "ix://agent-ix/spec-objects-operational/FR-003"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-operational/FR-004"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-operational/FR-005"
    type: "constrains"
---
# NFR-001: Additive compatibility of the semantic contract

## Statement

The module SHALL keep every artifact of the checked-in 0.2.0 skeleton set —
the eight skeletons as they stood at manifest version 0.2.0, which is the
population this NFR measures — validating against version 0.3.0 with at most
warning-level semantic findings.

The module SHALL keep every 0.2.0 `body_extraction` locator definition and the
0.2.0 `configuration-scope` lint rule unchanged at 0.3.0, and SHALL keep the
untyped section bodies those locators yield byte-identical between the two
versions. Yields not named here are unmeasured and are not claimed.

## Scope

- Applies to: `manifest.yaml`, the shipped schemas, and the skeletons.
- Operational context: existing corpus artifacts authored in legacy
  Properties forms (bullet lists, free-column tables) under `legacy_forms:
  warning`; no corpus repository is edited.

## Rationale

The ticket's merge gate is advisory-only until corpus promotion. A module that
turned legacy artifacts into errors would force corpus edits this campaign
forbids; a module that changed a locator would change every existing
extraction record; a module that changed the `configuration-scope` lint rule
would change the only check that exists today on the untyped Scope column.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| 0.2.0 locators changed | 0 | 0 | Test |
| 0.2.0 lint rules changed | 0 | 0 | Test |
| 0.2.0 lexicon terms removed or renamed | 0 | 0 | Test |
| Checked-in 0.2.0 skeleton set under 0.3.0: error findings, per skeleton | 0 | 0 | Test |
| Yield of each 0.2.0 required locator, 0.2.0 vs 0.3.0 | identical | identical | Test |

## Verification

NFR-001-AC-2 holds on the population this NFR measures, and the measurement
says why: no 0.2.0 skeleton carries a frontmatter `object:` key, so Quire runs
headings-only validation on it and never assembles or checks a typed record.
That is what makes 0.3.0 additive for the artifacts that exist today, and it is
asserted rather than assumed.

The engine defect behind it is real but differently scoped: once a legacy-form
artifact *does* declare `object:`, quire 0.47.1 assembles its declaration
record as `{}` and validates it against the type schema unconditionally, so it
fails `semantic.record-invalid` at error severity even under
`legacy_forms: warning`. `agent-ix/quire-rs#391` owns that rule. The module
carries that case as an explicit expected failure beside NFR-001-AC-2 rather
than relaxing a schema, so the day the engine changes, the row turns red and is
noticed.

A checked-in copy of the 0.2.0 `body_extraction`, `lint_rules`, `lexicon` term
set, and all eight 0.2.0 skeletons is compared against the 0.3.0 manifest and
validated under it: the locator and lint-rule definitions are equal, the term
set is equal, each legacy skeleton validates with no error, and the body each
0.2.0 required locator yields is unchanged.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Every 0.2.0 `body_extraction` locator is present in 0.3.0 with identical facets (0 changed), and the `configuration-scope` lint rule is present unchanged. | Test |
| NFR-001-AC-2 | Every skeleton of the checked-in 0.2.0 set validates under 0.3.0 with 0 error findings. | Test |
| NFR-001-AC-3 | The 0.2.0 lexicon term set is present in 0.3.0 with no term removed or renamed; only the three definitions `agent-ix/spec-objects-operational#5` names as truncated differ, and each differs by restoring the text that issue records as lost. | Test |
| NFR-001-AC-4 | For each 0.2.0 skeleton, the body extracted by each 0.2.0 `required: true` locator is byte-identical under 0.2.0 and 0.3.0. | Test |

## Dependencies

- **Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md), [FR-005](../functional/FR-005-executable-skeletons.md); quoin FR-074 (`ix://agent-ix/quoin/FR-074`)
- **Downstream**: corpus promotion (`agent-ix/quoin#291` sweep), outside this module
