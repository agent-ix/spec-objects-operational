---
id: SR-103
title: "Gap analysis — spec-objects-operational PR #29 (PLAT-277 F1 optional record keys)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-operational; spec/functional/FR-006-optional-sections-optional-keys.md, spec/functional/FR-004-role-schemas.md, spec/tests.md, tests/test_role_schemas.py"
review_set: subset
---
# Gap analysis — spec-objects-operational PR #29 (PLAT-277 F1)

## Summary

Ticket: PLAT-277 (finding F1). Planless; plan completion: not assessed.
`quoin matrix --repo . --json` (quoin 0.29.1) on the PR head: FR-006-AC-1 and
FR-006-AC-2 are tagged (both by
`test_a_record_lacking_an_optional_section_key_validates_and_the_key_stays_checked`);
FR-004-AC-10 is tagged by the renamed empty-record test; FR-004-CON-2 is gone
from spec and matrix. FR-006-CON-1 is untagged. No production code in the
diff lacks an owning requirement: the TypeSpec change is owned by FR-006 and
the regenerated schemas by FR-002.

## Verdict

**CONDITIONAL** — one medium (an untagged constraint that `spec/tests.md`
reports as covered), one low (no document-level evidence for the F1 outcome).

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-006-CON-1 is `untagged` in the computed matrix, yet `spec/tests.md` maps it to TC-092 and marks FR-006 ✅. The constraint also restates FR-006-AC-1's first half ("no shipped object-type schema lists a required key"), so either tag it or delete the redundant constraint. | spec/functional/FR-006-optional-sections-optional-keys.md:51, spec/tests.md:75, spec/tests.md:146 | correct-requirement-no-evidence |
| FND-002 | low | F1 is a document-level defect (a document without the optional section was refused as `semantic.record-invalid`), but every FR-006 test runs on hand-built records. Nothing asserts that `validate_document` accepts a document lacking `## Invariants` / `## Operations` / `## Properties`. Reviewer checked by hand with quire 0.54.0: a runbook without `## Operations` and the deleted migration fixture produce no `semantic.record-invalid`. The deleted fixture could have become that positive check. | tests/fixtures/negative/migration-no-invariants.md, tests/test_role_schemas.py:488 | correct-requirement-no-evidence |
