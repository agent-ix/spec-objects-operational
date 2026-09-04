---
id: SR-001
title: "Base review of the issue #6 semantic module contract specification"
type: SpecReview
analysis: base
scope: "spec/spec.md, spec/stakeholder/StR-001, spec/usecase/US-001, spec/functional/FR-001..FR-005, spec/non-functional/NFR-001, spec/integration/IT-001..IT-002, spec/tests.md"
review_set: all
---
# Base review of the issue #6 semantic module contract specification

## Summary

Checklist review (id formats, story and requirement quality, the six coverage
rules, cross-references, matrix bookkeeping) of the specification authored for
`agent-ix/spec-objects-operational#6`, read against the sibling
`agent-ix/spec-objects-business#4` base review whose dispositions this spec has
already absorbed (NFR acceptance criteria present rather than metrics-only;
`Inspection` constraint rows carried in the matrix; the `$id`-version and
fail-not-skip rules stated). Ids are well-formed and sequential per class
(StR-001, US-001, FR-001..FR-005, NFR-001, IT-001..IT-002, TM-001, and
TC-001..TC-091 in per-requirement blocks); every FR but FR-001 links US-001;
every acceptance criterion, named constraint and NFR metric has at least one
matrix row. `quire validate --scope . "spec/**/*.md"` exits 0 with no error and
no grammar warning; `quire coverage` reports 0/109 rows backed, which is the
expected pre-implementation state.

Eight medium findings: one verification-vocabulary defect the engine names, one
stakeholder-need/scope contradiction, one matrix rule that claims more than its
criteria assert, one mis-traced test row, three clusters of normative `SHALL`
behaviour with no owning criterion and no matrix row, and one matrix
status-column mismatch that silently disables status classification. Seven low
findings are recorded without change.

## Verdict

**CONDITIONAL** — no high finding in the base checklist; the eight mediums are
bookkeeping and criterion-ownership fixes that should be applied before
`spec-to-plan`. Note that the sibling failure-domain analysis (SR-006) carries
two high findings of its own; this verdict speaks only for the base checklist.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | FR-001's Verification cells read `Schema Test` and `Integration Test`, which `quire coverage` reports as `uncatalogued-verification-method` (4 rows: neither a catalog id nor a declared class); the class value `Test` is the declared form. This is the same pre-existing wording the sibling module corrected as its FND-003, and it matters here because the matrix now depends on those rows. Escape cause: wrong-requirement. | FR-001-AC-1..4, `quire coverage` |
| FND-002 | medium | StR-001's Stakeholder Need and Rationale name "configuration, migrations, hooks, jobs, SLIs, and SLOs", but the module ships eight types — configuration, migration, sli, slo, alert, runbook, incident, deployment — and ships no hook or job type. The need therefore omits four of the eight types this spec traces to it and names two that do not exist, so StR-001-VC-1 ("registers all the contents this module declares") is judged against a need that does not describe them. Restate the need over the eight types. Escape cause: wrong-requirement. | StR-001 Stakeholder Need, StR-001 Rationale, spec.md Purpose, FR-004 table |
| FND-003 | medium | Matrix rule 5 claims availability states `available`, `not_applicable` and `missing` are tested per declaration kind, but FR-005-AC-4 asserts only `available` and `not_applicable`, and TC-063 restates AC-4; no criterion or row exercises `missing`. Either extend FR-005-AC-4 with the `missing` case (a type that admits a kind whose section is absent) or drop `missing` from rule 5 — the rule as written reports coverage the criteria do not carry. Escape cause: correct-requirement-no-evidence. | spec/tests.md rule 5, FR-005-AC-4, TC-063 |
| FND-004 | medium | FR-005 states four normative rules with no acceptance criterion and no matrix row: the `make dev-quire` provisioning target, the fail-not-skip rule ("if the wheel is absent or lacks `extract_semantic`, every semantic test SHALL fail — not skip — naming the target and `agent-ix/quire-rs#392`"), the prohibition on declaring `quire` in `pyproject.toml`, and the "only a criterion this specification names as blocked" exemption rule. The Test Environment section of the matrix leans on the fail-not-skip guarantee to claim no row can be reported green without the engine, so the one rule that makes the matrix honest is itself unverified. Add a criterion and a row for it. Escape cause: correct-requirement-no-evidence. | FR-005 Behavior (dev-quire, fail-not-skip, pyproject, exemption bullets), spec/tests.md Test Environment |
| FND-005 | medium | Four FR-002 `SHALL` behaviours have no criterion and no row: the generator writes under `spec_objects_operational/schemas/` only; it edits `manifest.yaml` only at `data_schema.digest`; `make lint` runs `make schemas-check`; and `.gitattributes` marks `*.json`/`*.tsp` `eol=lf`. TC-018 covers only that `--check` writes nothing. The write-scope pair and the `eol=lf` rule are the guarantees behind FR-002-CON-3 determinism and the digest stability the whole contract rests on. Add criteria (or fold them into FR-002-CON-3) and rows. Escape cause: correct-requirement-no-evidence. | FR-002 Behavior (write-scope, manifest-edit, `make lint`, `.gitattributes` bullets), FR-002-CON-3, TC-018, TC-019 |
| FND-006 | medium | TC-023 ("no acceptance test hard-codes the `$id` version segment; each reads it from the manifest `version`") traces to FR-002-CON-5, which is the atomic-bump rule already covered by TC-017; the rule TC-023 actually asserts is the second half of FR-002-AC-2 and the two `SHALL` bullets beside it. Retrace TC-023 to FR-002-AC-2 so CON-5 is not credited with evidence for a different rule. Escape cause: correct-requirement-no-evidence. | spec/tests.md TC-023, FR-002-AC-2, FR-002-CON-5, TC-017 |
| FND-007 | medium | FR-004's three cross-key reader rules are authored as `SHALL` (an `AlertCondition.sli` names an `sli` of the same bundle; a `RunbookStep.operation` names an `operations[].name` of the same record; a `ScopeAssignment.parameter` names a `fields[].name` of the same record) and the next sentence says JSON Schema cannot express any of them and none is claimed as a schema refusal — so all three are binding obligations with no criterion, no row, and no named owner. Either restate them as informative notes addressed to the extractor that first populates those keys, or give each a criterion naming the consumer that discharges it (`agent-ix/quoin#335`). Escape cause: missing-requirement. | FR-004 Behavior (last four bullets), spec/tests.md TC-040..TC-052 |
| FND-008 | medium | `quire coverage` reports `status-column-matches-nothing` for the `functional-coverage` declaration: it reads a status column named `Status`, while the "Functional Requirement Coverage" table heads its column `Coverage Status`. Status classification is skipped for that table, so a complete-but-unbacked FR row cannot be detected. The same header is used by the sibling business module, so the fix is either to rename the column to `Status` in both matrices or to change `traceability.status.column` in `spec-artifacts-process`; the engine will not guess between them. Escape cause: correct-requirement-no-evidence. | spec/tests.md "Functional Requirement Coverage", `quire coverage`, spec-artifacts-process `functional-coverage` |
| FND-009 | low | FR-004's Item-rules column names `relations` forbidden on `configuration` and `migration` only, and silent for `sli`, `slo`, `alert`, `runbook` and `incident`, although the seal (`unevaluatedProperties: {not: {}}`) refuses it on all five. The column reads as if `relations` were admitted there. Wording only; the schemas are unambiguous. No change proposed. | FR-004 table, FR-004 Outputs |
| FND-010 | low | IT-001 closes with `## Traceability` while IT-002 closes with `## Dependencies`; the two integration tests of one module carry two section shapes. Both validate. No change proposed. | IT-001, IT-002 |
| FND-011 | low | US-001 carries illustrative examples (US-001-EX-1..3) rather than Given/When/Then acceptance criteria; this follows the `spec-artifacts-iso` US skeleton, which keeps verification out of stories, so the checklist item "≥ 2 acceptance criteria" is satisfied by the examples plus the FR criteria they lead to. Same disposition as the sibling module's FND-004. No change. | US-001 |
| FND-012 | low | No FR carries an `## Options` section; the TypeSpec-over-hand-authored choice and the map-don't-duplicate choice for `agent-ix/quoin#267` are recorded in US-001 Options and the ticket's authoring contract, so an FR-level options table would repeat them. No change. | FR-002..FR-005, US-001 Options |
| FND-013 | low | The matrix rows TC-002..TC-007, TC-036 and TC-091 depend on a running `filament-core-service`, a Quoin built from `agent-ix/quoin` main, or a human, and stay `🚧` with a note after implementation. TC-002..TC-007 predate this issue. Recorded so the gap analysis does not read them as this issue's debt. | spec/tests.md, IT-001, IT-002 |
| FND-014 | low | The Coverage Gaps section already records that no `SuiteRegistry` and no `Inspections` document exists; `quire coverage` confirms both declarations with `archetype-matches-nothing` (each scans nothing and mints no rows), so the `Inspection`, `Manual` and `Demonstration` rows have no declared discharge mechanism. Carried by the plan, as the matrix says. No change here. | spec/tests.md Coverage Gaps, `quire coverage` |
| FND-015 | low | `quire coverage` reports `no-symbol-bound` and `hollow-denominator`: the 16 existing evidence symbols in `tests/test_basic.py` carry no tag any declared form matches, so `coverage.backed` publishes 0/109 over a corpus the binder could not read. This is the expected pre-implementation state for the issue #6 rows, but the pre-existing FR-001 tests are also untagged and should gain tracking tags when the suite is extended. | `tests/test_basic.py`, spec/tests.md, `quire coverage` |

## Coverage Rules

1. Coverage: every acceptance criterion, named constraint and NFR metric has ≥ 1 test case (StR-001: 3 VC; FR-001: 4 AC; FR-002: 9 AC + 5 CON; FR-003: 8 AC + 3 CON; FR-004: 13 AC + 4 CON; FR-005: 9 AC + 2 CON; NFR-001: 4 AC over 5 metrics; IT-001: 3 SC; IT-002: 6 SC). Verified row by row; no orphan criterion and no orphan TC. FND-004, FND-005 and FND-007 are unowned `SHALL` behaviour rather than uncovered criteria.
2. Option permutation: both Properties forms (typed table, `sysml` fence) over the three alternate-form types (TC-061), and all eight object types (TC-041..TC-048).
3. Constraint boundary: zero versus one identity field (TC-041, TC-042, TC-047, TC-048), unit present versus absent (TC-043, TC-044, TC-068), empty versus one-item arrays (TC-045, TC-046), `Timestamp` field present versus absent (TC-047).
4. Error path: digest mismatch and unknown `semantic` key (TC-035), both Properties forms (TC-070), dangling clause reference and non-`Identifier` token (TC-064), observation key (TC-049), stale committed schema (TC-018), mismatched `$id` base (TC-014).
5. State transition: availability states per declaration kind (TC-063) — `available` and `not_applicable` only; `missing` is unasserted, see FND-003.
6. Edge case: empty record (TC-049), legacy 0.2.0 artifacts under 0.3.0 (TC-081), unresolved type token (TC-051).

## Dispositions

| Finding | Disposition |
|---|---|
| FND-001 | Proposed: change FR-001's four Verification cells to `Test`. |
| FND-002 | Proposed: restate StR-001's Stakeholder Need and Rationale over the eight shipped types, dropping "hooks" and "jobs". |
| FND-003 | Proposed: extend FR-005-AC-4 (and TC-063) with the `missing` availability state, or narrow matrix rule 5 to the two states asserted. |
| FND-004 | Proposed: add FR-005-AC-10 covering `make dev-quire`, the fail-not-skip rule and the `pyproject.toml` prohibition, with a matrix row. |
| FND-005 | Proposed: add criteria (or extend FR-002-CON-3) for the generator write scope, the `manifest.yaml` edit scope, the `make lint` wiring and `.gitattributes eol=lf`, with matrix rows. |
| FND-006 | Proposed: retrace TC-023 from FR-002-CON-5 to FR-002-AC-2. |
| FND-007 | Proposed: restate FR-004's three cross-key reader rules as informative notes owned by `agent-ix/quoin#335`, or give each a criterion and a row. |
| FND-008 | Proposed: align the "Functional Requirement Coverage" status header with `traceability.status.column`, in this module and the sibling, or change the declaration upstream. |
| FND-009..FND-015 | Recorded, no change. |
