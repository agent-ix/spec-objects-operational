---
id: SR-1626
title: "Spec review (integrity) — spec-objects-operational PR #31 (PLAT-1835 incident hazard/anomaly links and maintenance plan)"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-objects-operational; spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/functional/FR-006-optional-sections-optional-keys.md, spec/integration/IT-002-quoin-module-install.md, spec/spec.md, spec/stakeholder/StR-001-module-activation.md, spec/tests.md"
review_set: subset
---
# Spec review (integrity) — spec-objects-operational PR #31 (PLAT-1835 part 2)

## Summary

Ticket: PLAT-1835. Examined the changed spec units: FR-003 Behavior and
FR-003-AC-1/AC-4; the FR-004 table rows for `incident` and `maintenance_plan`,
the five new Behavior bullets, the cross-reference and optional-key lists, and
FR-004-AC-1, AC-10, AC-13, AC-16 and AC-17; FR-005 Behavior and
FR-005-AC-1/AC-7; FR-006 Inputs; IT-002 Expected Results; `spec.md`; StR-001;
and `spec/tests.md` TC-030..TC-094. `quire validate --scope .` on all eight
changed spec files passes. Each new AC has a test row, and AC and TC agree for
AC-16 and AC-17. No score, class or acceptability value is introduced, and no
paywalled standard text is quoted.

The "eight" → "nine" edits were applied where the word appeared. Several lists
that enumerate the types by name, without a count word, were not updated.

## Verdict

**CONDITIONAL** — one medium (an AC now disagrees with its test), one low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-005 was not updated for `maintenance_plan` where it lists types by name. FR-005-AC-4 still says `fields` is `not_applicable` for "`alert` and `runbook`" and `operations` is `available` for "`runbook` and `deployment`". TC-063 now asserts both states for `maintenance_plan` (`FIELD_BEARING`/`OPERATION_BEARING` were edited), so the test exceeds its AC. Two Behavior bullets have the same gap: line 61's operations-bearing list (`runbook`, `deployment`) and line 66's kernel-section list, which has no `## Procedure` for `maintenance_plan`. Name `maintenance_plan` in all three. | spec/functional/FR-005-executable-skeletons.md:61, spec/functional/FR-005-executable-skeletons.md:66, spec/functional/FR-005-executable-skeletons.md:91 | wrong-requirement |
| FND-002 | low | Other enumerations of the types or support models miss the new ones: FR-004:103 "the other seven refuse the key" (now eight); FR-004:106's standing-definition list omits `MaintenancePlan`; FR-006 Outputs line 31 (models listing no required key) omits `MaintenancePlan`; FR-004 Outputs' support-model list omits `FeedbackChannel` and still says "nineteen support models in all" (now twenty). Add the names, and drop the count words ("seven", "nineteen", "nine") rather than bump them. The lists already carry the information, and a count is one more thing to resync on the next type. | spec/functional/FR-004-role-schemas.md:40-46, spec/functional/FR-004-role-schemas.md:103, spec/functional/FR-004-role-schemas.md:106, spec/functional/FR-006-optional-sections-optional-keys.md:31 | wrong-requirement |

## Dispositions
