---
id: SR-104
title: "Spec review — spec-objects-operational PR #29 (PLAT-277 F1 optional record keys)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-operational; spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/functional/FR-006-optional-sections-optional-keys.md, spec/tests.md, spec/spec.md"
review_set: subset
---
# Spec review — spec-objects-operational PR #29 (PLAT-277 F1)

## Summary

Ticket: PLAT-277 (finding F1). Examined new FR-006 (statement, Behavior,
FR-006-CON-1, FR-006-AC-1, FR-006-AC-2), TC-092, the FR-004 table rows,
FR-004-AC-2..5, AC-9, AC-10, the removal of FR-004-CON-2, the FR-005
negative-fixture list, FR-005-AC-5 and the tests.md rows TC-041..049, TC-064.

FR-006's statement is a sound, testable rule and matches the manifest: every
`properties` / `invariants` / `operations` locator for all eight types is
`required: false`. Its Behavior keeps item rules on present keys and leaves
locators unchanged, and the diff honours both. Removing FR-004-CON-2 is
correct; it is not left dangling in tests or matrix. `quire validate` on the
three FRs is clean; `spec/tests.md` fails only on the pre-existing
`Coverage Status` column name, unchanged by this PR.

## Verdict

**CONDITIONAL** — no high finding. Two mediums: FR-005 and the FR-004 table
still describe a required set that FR-006 abolished. One low wording drift.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-005 still keys obligations on "types that require `fields`" / "require `operations`". Line 49 (which skeletons author `## Properties`), line 61 (which author `## Operations`) and FR-005-AC-4 ("`fields` `available` for the six types that require `fields`") now denote the empty set, so read literally they impose nothing. The PR updated the Invariants bullet (line 58) but not these. The same wording is in plan Task-005 line 46. Restate them as "the six types that admit `fields`" / "the types whose skeleton authors `operations`". | spec/functional/FR-005-executable-skeletons.md:49, spec/functional/FR-005-executable-skeletons.md:61, spec/functional/FR-005-executable-skeletons.md:91 | wrong-requirement |
| FND-002 | medium | In the FR-004 table, every row now reads Required keys "none (FR-006)", but `fields` / `clauses` / `operations` were not added to the Optional keys column. The table no longer lists the full key set each type admits; for example Deployment's row omits `fields` and `operations`. The prose still says "`Deployment` requires an identity field" (line 61) and "`Incident` is the only model that requires occurrence identity" (lines 65, 100). Under FR-006 those hold only when `fields` is present, and the spec does not say so. Two readers could disagree on whether an `Incident` with no `## Properties` must be refused. | spec/functional/FR-004-role-schemas.md:61, spec/functional/FR-004-role-schemas.md:65, spec/functional/FR-004-role-schemas.md:70-77, spec/functional/FR-004-role-schemas.md:100 | wrong-requirement |
| FND-003 | low | AC/TC wording drift. TC-041, TC-045, TC-046 and TC-047 (and their tests) now assert that an absent key validates, but FR-004-AC-2, AC-6, AC-7 and AC-8 do not say so. FR-004-AC-4 gained "a record without `fields` validates", but the TC-043 row did not. Plan.md line 157 still says "the ten named cases". | spec/functional/FR-004-role-schemas.md:122-128, spec/tests.md:118-122 | wrong-requirement |
