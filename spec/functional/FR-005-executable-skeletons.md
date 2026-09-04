---
id: FR-005
title: "Make every skeleton an executable typed fixture"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-operational/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-operational/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-operational/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-071"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-072"
    type: "depends_on"
---
# FR-005: Make every skeleton an executable typed fixture

## Description

Every skeleton under `spec_objects_operational/skeletons/` SHALL author its
declarations in the quoin FR-071/FR-072 Markdown forms (typed `## Properties`
table by default, `## Invariants` clause fences, `## Operations`
subsections) and validate through Quire against this module, accompanied by
negative fixtures that fail for a named reason, so that the skeletons are the
module's executable positive fixtures and the negatives pin what the schemas
refuse.

## Inputs

- The rewritten skeletons `skeletons/<type>.md` (one per object type) and the
  alternate-form skeletons `skeletons/configuration.sysml.md`,
  `skeletons/sli.sysml.md`, `skeletons/deployment.sysml.md`.
- Negative fixtures `tests/fixtures/negative/<type>-<case>.md`, each with
  frontmatter `expect:` naming the diagnostic code or reason the fixture must
  produce.
- The Quire wheel 0.46.0 or later, exposing `extract_semantic`,
  `validate_document`, and `Registry`, installed into the module's Python
  environment by `make dev-quire` (see Behavior).

## Outputs

- A validation result per skeleton with no error and no `semantic.record-invalid`.
- A semantic record per skeleton whose `fields`, `clauses`, and `operations`
  availability match the type's declared set.

## Behavior

- Each skeleton whose type requires `fields` (`configuration`, `migration`, `sli`, `slo`, `incident`, `deployment`) SHALL author `## Properties` as one table with the header exactly `Field | Type | Multiplicity | Constraints`.
- The `alert` and `runbook` skeletons SHALL carry no `## Properties` section, because `Alert` and `Runbook` forbid `fields`.
- The `sli` and `slo` skeletons SHALL each carry at least one `## Properties` row whose `Type` cell has a trailing bracketed unit (for example `Decimal(5,4) [1]` or `Duration [ms]`), so the extracted record carries the measured field `Sli`/`Slo` require.
- The `incident` skeleton SHALL carry one `identity` row and one `Timestamp` row, so the extracted record carries the identity and occurrence fields `Incident` requires.
- The `configuration` and `migration` skeletons SHALL carry no `identity` row, because `Configuration` and `Migration` admit zero identity fields.
- The `configuration`, `sli`, and `deployment` alternate skeletons SHALL author the same declarations as one ```` ```sysml ```` fence of `attribute <name> : <Type>[<mult>] { <constraints> }` and `ref item <name> : <Type>[<mult>]` lines.
- Each alternate skeleton SHALL declare the same fields as its table skeleton, under that skeleton's frontmatter `id` and `title`; the module therefore ships two files under one id by intent, and the identity of their extracted `FieldDecl[]` is the obligation FR-005-AC-2 tests.
- Every skeleton SHALL author `## Invariants` with one `### <clauseId>` per clause, each owning exactly one ```` ```ocl ```` fence, because every object-type model of [FR-004](./FR-004-role-schemas.md) admits `clauses` and `migration`, `slo`, and `alert` require at least one.
- Each skeleton's frontmatter SHALL carry `object: <type name>` beside `type: <type name>`, because Quire runs the semantic layer (extraction and record validation) on the `object:` archetype of a document; a skeleton without it validates its headings only.
- The manifest SHALL gain a `required: false` `section_body` locator for every `## Properties`, `## Invariants`, and `## Operations` section a skeleton introduces, so the section is asserted by the manifest and remains optional for existing artifacts.
- Each skeleton whose type requires `operations` (`runbook`, `deployment`) SHALL author `## Operations` with one `### <name>` per operation, an optional `| Param | Type | Multiplicity | Constraints |` table, a `Returns:` line where the operation returns a value, and optional `Pre:`/`Post:` lines that, when present, name clause ids declared in the same artifact.
- Every skeleton `title` SHALL be an `Identifier` (`^[A-Za-z_][A-Za-z0-9_]*$`), distinct across all skeletons and outside the `KernelScalar` names, so a `Type` cell can name it.
- Every `Type` cell that names another skeleton SHALL use that skeleton's `title`, so that under a bundle index built from the skeletons every non-kernel token resolves to `ix://agent-ix/spec-objects-operational/type/<Title>` with no `semantic.unresolved-type` finding.
- Every skeleton SHALL keep every H2 heading whose manifest locator is `required: true` for its type.
- No skeleton SHALL carry an H2 heading the manifest does not assert.
- Each skeleton SHALL keep its kernel section with the heading, table columns, and fence language the manifest asserts: `## Configuration` (`Name | Scope | Type | Default | Description`) and `## Behavior` for `configuration`, the `## Migration` `sql` fence, the `## Query` fence for `sli`, the frontmatter `target`/`window` pair for `slo`, the `## Flow` mermaid fence for `alert`, `## Steps` for `runbook`, `## Timeline` for `incident`, and the `## Topology` mermaid fence for `deployment`.
- Where a typed section and a kernel section describe the same declarations (the configuration `## Properties` table and its `## Configuration` table; the runbook `## Operations` and its `## Steps` prose; the deployment `## Operations` and its `## Topology` diagram), the typed section SHALL be the authority and the kernel section a derived, human-facing view; the `## Configuration` table stays the asserted form while `agent-ix/quoin#335` decides the `scopes` mapping.
- Each negative fixture SHALL fail `validate_document` with an error whose message carries the fixture's `expect:` code, covering at least: a configuration with an identity row (`semantic.record-invalid`), a migration with no `## Invariants` (`semantic.record-invalid`), an SLI whose only field carries no unit (`semantic.record-invalid`), an alert carrying a `## Properties` table (`semantic.record-invalid`), a runbook whose `## Operations` declares no operation (`semantic.record-invalid`), an incident with no `Timestamp` row (`semantic.record-invalid`), a `## Properties` section carrying both a table and a fence (`semantic.properties-both-forms`), an operation whose `Post:` names an undeclared clause (`semantic.dangling-clause-ref`), and a `Type` token that is not an `Identifier` (`semantic.invalid-type-token`); the last three re-check the engine's published diagnostics under this module's schemas rather than re-specify them.
- The repository SHALL provide a `make dev-quire` target that installs the Quire wheel this requirement names into the module's Python environment, so the semantic test dependency is provisioned by a documented command rather than by an undeclared side install.
- If the installed Quire wheel is absent or lacks `extract_semantic`, then every semantic test SHALL fail — not skip — with a message naming the missing function, the `make dev-quire` target, and `agent-ix/quire-rs#392`, so that no matrix row can pass or be reported green without the engine under test.
- While no committable index carries Quire 0.46.0, the module SHALL NOT declare `quire` in `pyproject.toml`. `internal-pypi` (the index this repo's CI uses) serves 0.33.0 at most and no `quire-rs` tag carries the semantic layer, so the wheel exists only on the dev-only `pypi.ix`; `agent-ix/quire-rs#392` is the blocking issue, and its resolution replaces the `make dev-quire` target with a committed dev dependency.
- Only a criterion this specification names as blocked SHALL be exempt from the previous rule, as an explicit expected failure naming the blocking issue. Today that is the record validation of a legacy-form artifact declaring `object:` (`agent-ix/quire-rs#391`, beside [NFR-001](../non-functional/NFR-001-additive-compatibility.md)-AC-2) and the naming half of FR-003-AC-6 (`agent-ix/quire-rs#221`, `agent-ix/quire-rs#394`).

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-005-CON-1 | The module SHALL keep the skeletons and negatives in this repository only, editing no corpus repository and no vendored quoin/quire fixture. | Boundary | Inspection |
| FR-005-CON-2 | A skeleton SHALL carry one Properties form; the alternate form is a separate file, never a second block in the same artifact. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | Every skeleton file (eight types plus three alternates) passes `validate_document` against this module with `is_valid` true and no `semantic.record-invalid` error. | Test |
| FR-005-AC-2 | For `configuration`, `sli`, and `deployment`, the table and `sysml` skeletons extract to identical normalized `fields` with `fieldsForm` `table` and `fence` respectively. | Test |
| FR-005-AC-3 | Under a bundle index built from the skeleton frontmatter, every skeleton extracts with zero `error` diagnostics and zero `semantic.unresolved-type` findings, and every non-kernel `type.target` starts with `ix://agent-ix/spec-objects-operational/type/`. | Test |
| FR-005-AC-4 | Each skeleton's `availability` states match its type: `fields` `available` for the six types that require `fields` and `not_applicable` for `alert` and `runbook`; `operations` `available` for `runbook` and `deployment`; `clauses` `available` for every skeleton. | Test |
| FR-005-AC-5 | Every negative fixture fails validation with an error message containing its `expect:` code, and at least the nine cases listed in Behavior are present. | Test |
| FR-005-AC-6 | Every skeleton's H2 set equals a subset of the headings the manifest asserts for its type and includes every `required: true` heading. | Test |
| FR-005-AC-7 | The skeleton for each of the eight types has no placeholder token and every asserted section body is non-empty. | Test |
| FR-005-AC-8 | Every skeleton `title` matches the `Identifier` pattern, is unique across the skeletons, and is not a `KernelScalar` name; every skeleton frontmatter carries `object` equal to `type`. | Test |
| FR-005-AC-9 | The `sli` and `slo` skeletons each extract at least one field carrying `type.unit`, and the `incident` skeleton extracts at least one `identity` field and one field whose `type.target` is `Timestamp`. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md); quoin FR-071/FR-072 (`ix://agent-ix/quoin/FR-071`, `ix://agent-ix/quoin/FR-072`); quire-rs FR-070/FR-071/FR-072
- **Upstream (unpinned neighbour contract)**: the `semantic.record-invalid` diagnostic this requirement's Outputs and FR-005-AC-1 depend on exists in quire-rs source but in no quire-rs acceptance criterion; `agent-ix/quire-rs#391` is where that record-validation contract, and the code naming it, are being settled.
- **Upstream (provisioning)**: `agent-ix/quire-rs#392` — publish the 0.46.0 wheel to `internal-pypi` so `quire` can become a committed dev dependency.
- **Downstream**: `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` consume the skeletons read-only
