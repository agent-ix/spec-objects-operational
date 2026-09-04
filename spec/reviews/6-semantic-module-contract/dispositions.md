---
id: SR-009
title: "Disposition record for the issue #6 review round"
type: SpecReview
analysis: base
scope: "spec/reviews/6-semantic-module-contract/"
review_set: all
---
# Disposition record for the issue #6 review round

## Summary

The eight review artifacts beside this one are **snapshots**: each states the
tree as it stood when that analysis ran, and several of their findings were
applied while later analyses were still running. This document is the single
place that says what happened to each finding, so a reader does not have to
guess whether a verdict still stands. It raises no new finding of its own.

## Verdict

**CONDITIONAL** — every high is applied; the mediums and lows are dispositioned
below, and the ones carried are carried with a named blocker.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-900 | low | Disposition record only; no new finding is raised here. | spec/reviews/6-semantic-module-contract/ |

## Highs — all applied

| Finding | Analysis | Disposition |
|---|---|---|
| FND-200 | failure-domain | **Applied.** Purity was enforced over record *keys* only. Every standing definition that admits `fields` now bans occurrence rows through an `allOf` clause (FR-004-CON-5, TC-053), with `migration-execution-state-row.md` as a tenth negative fixture. The unenforceable half — purity over field *names* — is now stated as unenforceable rather than claimed, and FR-004-AC-10's tautological half says so. |
| FND-201 | failure-domain | **Applied.** FR-005 now names the three overlaps where the kernel form is required and the typed key optional (alert `## Flow`, the slo `target`/`window` pair, incident `## Timeline`), and states that the kernel form stays the authority until `agent-ix/quoin#335` publishes the mapping. |
| FND-400 | dependency | **Applied.** `EvidenceRef.record` was a `SemanticId`, which could not name a quoin FR-059 record identified by a bare token. `EvidenceRecordId` now carries FR-059's own `$defs/identity` pattern and `EvidenceRecordShape` its `record_shape` enum. |
| FND-401 | dependency | **Applied.** FR-005 now states that AC-3 is verified through `extract_semantic` with a hand-built index, not through `validate_document`, which supplies `imports` only. |
| FND-402 | dependency | **Applied.** FR-005 now states the bundle-index identity rule: one entry per frontmatter `id`, not one per file, because the resolver matches entries rather than distinct ids. |
| FND-403 | dependency | **Applied before the finding was written.** `package-lock.json` was regenerated against `registry.npmjs.org` with `@agent-ix` scoped to npm.ix; risk-complexity FND-708 confirms 74/75 from npmjs. |
| FND-700 | risk-complexity | **Applied.** FR-004's Outputs, `EvidenceRef` bullets and AC-11 said `{ kind: EvidenceKind, record: SemanticId }` while the shipped schema required `{ shape, record }`. The spec now matches the emitted bytes, names nineteen support models, and FR-002-AC-1 counts twenty-seven files. |
| FND-701 | risk-complexity | **Partly applied, partly carried.** The vocabulary is now sourced from quoin FR-059 (live) rather than from the closed `#267` epic, and FR-004 says so. The referential half — that a given `record` names a real record — is stated as unverified rather than asserted, because no schema can reach the neighbour's store. |

## Mediums applied

| Finding | Analysis | Disposition |
|---|---|---|
| FND-001, FND-003, FND-006 | base | FR-001's verification cells now read `Test`; matrix rule 5 names the two availability states the skeletons actually produce; TC-023 retraced to FR-002-AC-2. |
| FND-002 | base | StR-001's need now names the eight shipped types instead of the non-existent `hooks` and `jobs`. |
| FND-004, FND-005 | base | FR-005-AC-10/AC-11 and FR-002-AC-10..AC-13 added with TC-024..TC-027, TC-071 and TC-072. |
| FND-007 | base | FR-004-AC-15 added for the three cross-key reader rules, in the spec's own expected-failure form. |
| FND-008 | base | Recorded and filed upstream as `agent-ix/quoin#340`; the header here follows the archetype, which is the contract this document validates against. |
| FND-100, FND-101, FND-103, FND-104, FND-105, FND-108, FND-109 | integrity | "templates" corrected to "skeletons" throughout; FR-001 traces to StR-001; FR-002-AC-13 added for `make install` provisioning the toolchain; the FR-001-AC-4 / IT-001-SC-02 reading corrected; FR-004-AC-15 restated as an expected failure; `.gitattributes` Behavior widened to four patterns; US-001-EX-2 replaced with the migration case the schemas now refuse. |
| FND-500, FND-502 | evidence | FR-002-AC-12, FR-002-CON-2, FR-005-CON-1 and FR-005-AC-11 moved from `Inspection` to `Test`, and TC-021/TC-026/TC-069/TC-072 retyped, because an executable symbol decides each. Only FR-002-CON-1's hand-edit half stays `Inspection`. |
| FND-503 | evidence | A `@pytest.mark.xfail` between a trace marker and its `def` made the binder skip the marker. Every trace marker in the suite is now the last decorator before its `def`; `authoring.tag_rate` went 85/88 → 88/88. |

## Carried, with a named blocker

| Finding | Analysis | Why it is carried |
|---|---|---|
| FND-800, FND-704 | scope-boundary, risk-complexity | `agent-ix/quoin#335` is scoped to the sibling module and will not publish a mapping for eighteen of this module's declared-but-unextracted keys. The keys stay optional and the tests over them say they are schema evidence, not extraction evidence. A successor ticket for the operational mapping is the neighbour's to file. |
| FND-801, FND-802 | scope-boundary | `agent-ix/quoin#267` is closed and FR-059 has no live reconciliation owner. This module references FR-059's contract and copies none of its fields; the "redeclares no field" obligation is stated but not falsifiable from here, and is recorded as such. |
| FND-803 | scope-boundary | `agent-ix/filament-core-service#26`: the live activation boundary is red because the service's own manifest schema copy admits neither `semantic` nor `lexicon`. Filed, not worked around. |
| FND-804, FND-702 | scope-boundary, risk-complexity | The harness's out-of-repo effects (a service DB, the machine-global Quoin store, a `pypi.ix` install) are each gated behind an explicit opt-in and are not constrained by a requirement. Recorded; a CI that provisions both indexes is `agent-ix/quire-rs#392`'s successor work. |
| FND-805, FND-706 | scope-boundary, risk-complexity | Build-time and validation-time semantic-core are two artifacts and `toolchain.json` records name and version only. A bundle-digest pin belongs upstream in `agent-ix/filament-core-data`. |
| FND-703, FND-705 | risk-complexity | The hard-pinned `0.3.0` in FR-003 and the absence of a content-fix (as opposed to version-bump) procedure. Both are the sibling module's shape too; changing them is a contract change, not a fix. |
| FND-504, FND-505, FND-506, FND-509 | evidence | NFR-001's five measurement rows mint no trace target, no evidence store exists, `criticality` is null on all sixty obligations, and `coverage.implements` is 0/79. All four are engine and programme concerns, not module ones. |
| FND-300..FND-314 | ears-conformance | Grammar is clean in both modes (21/21 documents, zero `[ears:*]` findings). The semantic observations are style, and several describe the ISO skeleton's own shape. |
| FND-009..FND-015, FND-106, FND-107, FND-110..FND-114, FND-207..FND-214, FND-404..FND-413, FND-501, FND-507, FND-508, FND-707, FND-708, FND-806, FND-807 | all | Recorded, no change. |
