---
id: FR-003
title: "Declare the semantic-module contract in the manifest"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-operational/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-operational/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-070"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-073"
    type: "depends_on"
---
# FR-003: Declare the semantic-module contract in the manifest

## Description

`spec_objects_operational/manifest.yaml` SHALL carry the quoin FR-070
`semantic` block and reference every exported object type's emitted schema by
path (quoin FR-073), so that Quoin
verifies the shipped schemas at install and Quire validates every declaration
record against them, while every existing extraction locator, lint rule, and
lexicon entry keeps its meaning.

## Inputs

- The emitted schemas of [FR-002](./FR-002-emitted-json-schemas.md).
- The `lexicon` block as repaired by `agent-ix/spec-objects-operational#5`.

## Outputs

- `manifest.yaml` with a `version`, a `semantic` block, and reference-form
  `data_schema` on every exported object type.

## Behavior

- The manifest `semantic` block SHALL carry exactly these keys and values: `contract_version: 1.0.0`, `semantic_core` (the one semantic-core version the module declares it extends), `package: agent-ix/spec-objects-operational`, `exports` listing every object type that ships a schema, `imports: {}`, `targets: [json-schema, markdown]`, `mappings: [typed-table, sysml-fence, ocl-clause]`, `compatibility_posture: additive`, `legacy_forms: warning`.
- `semantic.exports` SHALL name all eight object types: `configuration`, `migration`, `sli`, `slo`, `alert`, `runbook`, `incident`, `deployment`.
- No exported object type SHALL carry an inline `data_schema`.
- The `configuration_table` locator (`table_row` under `Configuration`, asserting the columns `Name | Scope | Type | Default | Description`) SHALL stay in place, so the untyped configuration table continues to be yielded beside the semantic record.
- The `configuration-scope` advisory lint rule SHALL stay in place with the same allowed values and `warning` severity, because it is the only check on the Scope column of the untyped table and remains advisory under quire-rs FR-036.
- The `lexicon` block SHALL author every definition as a quoted scalar, so that a definition containing a comma is stored whole.
- The manifest SHALL restore the three definitions `agent-ix/spec-objects-operational#5` records as truncated (`container`, `deployment`, `build`) to the wording that issue names.
- A refused schema drops that object type alone, while a manifest key the loader cannot parse (an unknown `semantic` key) drops every object type of the module, so a consumer sees the module as absent. Both refusals are silent — no diagnostic names the offending key, or path — which `agent-ix/quire-rs#221` record as engine defects; the naming half of FR-003-AC-6 is blocked on them and is verified as an explicit expected failure rather than dropped.
- The manifest SHALL install through `quoin module install path:<module dir>` with no `semantic.*` error diagnostic.
- When the install has completed, `quoin module` SHALL list `spec-objects-operational`.
- If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or schemas rather than relax the contract keys or the `$id` rules to make a consumer accept them.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-003-CON-1 | The `semantic` block SHALL contain no key outside the admitted list. Quire's loader refusal of an unknown key is verified here (FR-003-AC-6); Quoin's refusal is the neighbour's own obligation (quoin FR-070) and is assumed, evidenced only by the clean install of [IT-002](../integration/IT-002-quoin-module-install.md). | Compatibility | Test |
| FR-003-CON-3 | The manifest SHALL carry every lexicon definition as one whole scalar, including the three definitions `agent-ix/spec-objects-operational#5` names as truncated. | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | The loaded `semantic` block equals the nine admitted keys with the values above, and `exports` equals the eight object-type names. | Test |
| FR-003-AC-3 | The `id`, `title` and `type` frontmatter locators and each object type's defining locators are `required: true`. | Test |
| FR-003-AC-4 | `quire.Registry.load_from([module dir])` lists all eight archetypes and `validate_document` on each skeleton reports no `semantic.*` load failure. | Test |
| FR-003-AC-5 | `quoin module install path:<module dir>` exits zero and `quoin module` lists `spec-objects-operational`; the previously installed entry is restored afterwards. | Demonstration |
| FR-003-AC-6 | A manifest copy whose `semantic` block gains a key `foo` is refused by Quire's loader naming `foo`. | Test |
| FR-003-AC-7 | Every lexicon definition is a single whole scalar with no truncation-minted key, and the three definitions `agent-ix/spec-objects-operational#5` names carry their restored wording. | Test |
| FR-003-AC-8 | The `configuration-scope` lint rule is present with `allowed: [creation, runtime, session]` and `severity: warning`. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), [FR-002](./FR-002-emitted-json-schemas.md); quoin FR-070/FR-073 (`ix://agent-ix/quoin/FR-070`, `ix://agent-ix/quoin/FR-073`); quire-rs FR-069 (`ix://agent-ix/quire-rs/FR-069`)
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [IT-002](../integration/IT-002-quoin-module-install.md)
