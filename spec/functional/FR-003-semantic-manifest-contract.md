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
path and digest (quoin FR-073), at manifest `version` 0.3.0, so that Quoin
verifies the shipped schemas at install and Quire validates every declaration
record against them, while every existing extraction locator, lint rule, and
lexicon entry keeps its meaning.

## Inputs

- The emitted schemas and digests of [FR-002](./FR-002-emitted-json-schemas.md).
- The module-manifest schema with the `semantic` block, at
  `agent-ix/filament-core-service` revision `a77f31e` (CR-003) — the same
  revision [FR-001](./FR-001-module-manifest-activates.md) names, and the
  revision Quoin and Quire each vendor byte-identically. All three consumers
  therefore judge this manifest against one schema; a consumer vendoring an
  older copy is a skew defect on that consumer, not a change here.
- The `lexicon` block as repaired by `agent-ix/spec-objects-operational#5`.

## Outputs

- `manifest.yaml` with `version: 0.3.0`, a `semantic` block, and reference-form
  `data_schema` on every exported object type.

## Behavior

- The manifest `semantic` block SHALL carry exactly these keys and values: `contract_version: 1.0.0`, `semantic_core: 0.1.0`, `package: agent-ix/spec-objects-operational`, `exports` listing every object type that ships a schema, `imports: {}`, `targets: [json-schema, markdown]`, `mappings: [typed-table, sysml-fence, ocl-clause]`, `compatibility_posture: additive`, `legacy_forms: warning`.
- `semantic.exports` SHALL name all eight object types: `configuration`, `migration`, `sli`, `slo`, `alert`, `runbook`, `incident`, `deployment`.
- Every exported object type's `data_schema` SHALL be `{ schema: schemas/<Model>.json, digest: sha256:<hex> }` where `<hex>` is the SHA-256 of the shipped file bytes.
- No exported object type SHALL carry an inline `data_schema`.
- The manifest `version` SHALL be `0.3.0`, because the emitted `$id` embeds it and the previous version was `0.2.0`.
- Every `body_extraction` locator present at version 0.2.0 SHALL remain present with the same `from`, heading, `language`, `required`, `multiple`, and `assert` facets.
- The `configuration_table` locator (`table_row` under `Configuration`, asserting the columns `Name | Scope | Type | Default | Description`) SHALL stay in place, so the untyped configuration table continues to be yielded beside the semantic record.
- The `configuration-scope` advisory lint rule SHALL stay in place with the same allowed values and `warning` severity, because it is the only check on the Scope column of the untyped table and remains advisory under quire-rs FR-036.
- Where an object type gains a locator after 0.2.0, that locator SHALL be `required: false`, so existing artifacts stay valid (the additions themselves are specified by [FR-005](./FR-005-executable-skeletons.md)).
- The `lexicon` block SHALL author every definition as a quoted scalar, so that a definition containing a comma is stored whole.
- The manifest SHALL restore the three definitions `agent-ix/spec-objects-operational#5` records as truncated (`container`, `deployment`, `build`) to the wording that issue names.
- The manifest SHALL leave every other lexicon definition byte-identical to its 0.2.0 text.
- The manifest SHALL load through Quire's registry loader with no `ArchetypeLoadFailure` for any object type and with the recorded schema digest equal to the manifest digest.
- Measured against quire 0.46.0: a refused schema drops that object type alone, while a manifest key the loader cannot parse (an unknown `semantic` key) drops every object type of the module, so a consumer sees the module as absent. Both refusals are silent — no diagnostic names the offending key, path, or digest — which `agent-ix/quire-rs#221` and `agent-ix/quire-rs#394` record as engine defects; the naming half of FR-003-AC-6 is blocked on them and is verified as an explicit expected failure rather than dropped.
- The manifest SHALL install through `quoin module install path:<module dir>` with no `semantic.*` error diagnostic.
- When the install has completed, `quoin module` SHALL list `spec-objects-operational`.
- If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or schemas rather than relax the contract keys, the digests, or the `$id` rules to make a consumer accept them.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-003-CON-1 | The `semantic` block SHALL contain no key outside the admitted list. Quire's loader refusal of an unknown key is verified here (FR-003-AC-6); Quoin's refusal is the neighbour's own obligation (quoin FR-070) and is assumed, evidenced only by the clean install of [IT-002](../integration/IT-002-quoin-module-install.md). | Compatibility | Test |
| FR-003-CON-2 | The manifest SHALL mark every locator added after 0.2.0 `required: false`. | Compatibility | Test |
| FR-003-CON-3 | The manifest SHALL keep every 0.2.0 lexicon term, changing only the three definitions `agent-ix/spec-objects-operational#5` names as truncated. | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | The loaded `semantic` block equals the nine admitted keys with the values above, and `exports` equals the eight object-type names. | Test |
| FR-003-AC-2 | For every exported type, `data_schema` is the reference form, the referenced file exists, and its SHA-256 equals the recorded digest. | Test |
| FR-003-AC-3 | Every 0.2.0 locator, compared against the checked-in 0.2.0 baseline, is present unchanged; every added locator is `required: false`. | Test |
| FR-003-AC-4 | `quire.Registry.load_from([module dir])` lists all eight archetypes and `validate_document` on each skeleton reports no `semantic.*` load failure. | Test |
| FR-003-AC-5 | `quoin module install path:<module dir>` exits zero and `quoin module` lists `spec-objects-operational`; the previously installed entry is restored afterwards. | Demonstration |
| FR-003-AC-6 | A manifest copy whose `semantic` block gains a key `foo` is refused by Quire's loader naming `foo`; a copy whose digest is altered is refused naming the path. | Test |
| FR-003-AC-7 | Every lexicon definition is a single whole scalar with no truncation-minted key, the term set is unchanged against the 0.2.0 baseline, and the three definitions `agent-ix/spec-objects-operational#5` names carry their restored wording. | Test |
| FR-003-AC-8 | The `configuration-scope` lint rule is present with `allowed: [creation, runtime, session]` and `severity: warning`, unchanged from 0.2.0. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), [FR-002](./FR-002-emitted-json-schemas.md); quoin FR-070/FR-073 (`ix://agent-ix/quoin/FR-070`, `ix://agent-ix/quoin/FR-073`); quire-rs FR-069 (`ix://agent-ix/quire-rs/FR-069`)
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [IT-002](../integration/IT-002-quoin-module-install.md)
