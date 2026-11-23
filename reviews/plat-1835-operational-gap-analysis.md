---
id: SR-1625
title: "Gap analysis — spec-objects-operational PR #31 (PLAT-1835 incident hazard/anomaly links and maintenance plan)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-operational; spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/tests.md, tests/test_role_schemas.py, tests/test_skeletons_semantic.py, spec_objects_operational/schemas/*.json"
review_set: subset
---
# Gap analysis — spec-objects-operational PR #31 (PLAT-1835 part 2)

## Summary

Ticket: PLAT-1835. Planless audit scoped to the PR diff at `41622f7`. Plan
completion: not assessed.

`quoin matrix --repo . --json` tags FR-004-AC-16 to
`test_incident_references_hazards_and_anomalies_and_no_other_type_does`
(TC-093) and FR-004-AC-17 to
`test_maintenance_plan_requires_operations_owned_channels_and_assigns_nothing`
(TC-094). Both pass under quire 0.62.2. Neither has stubs or skips, and both
use hand-built records, naming the extractor limitation (agent-ix/quoin#335)
as FR-004 requires.

Mutation probes, run in a temporary worktree and reverted:

- Remove `hazards`/`anomalies` from `Incident`: TC-093 fails (seal).
- Bare token in either list: asserted and refused.
- Drop `owner` from `FeedbackChannel.required`: TC-094 fails.
- Drop `minItems` on `operations`: TC-094 fails.
- Add `severity?: AlertSeverity` to `FeedbackChannel` and to `Incident` in
  `typespec/main.tsp` and regenerate: **every** test in
  `tests/test_role_schemas.py` still passes (FND-001).

Every new schema element has an owning FR-004 statement. TC-060 (FR-005-AC-1)
is broken by this PR; that is recorded as code-review SR-1624 FND-001 and is
not repeated here.

## Verdict

**CONDITIONAL** — one medium. AC-16 and AC-17 can fail and are backed. The
program-level "no score, class or acceptability" statement is only partly
backed.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-004 Behavior says `FeedbackChannel`, `MaintenancePlan` and `Incident` SHALL declare no severity, class or acceptability key, but only `MaintenancePlan` is checked, and only through its seal (TC-094 asserts `severity` and `acceptability` fail; `class` is never asserted). Adding `severity` to `FeedbackChannel` and `Incident` in TypeSpec and regenerating leaves all role-schema tests green. Assert over the three schemas' declared `properties` (and `FeedbackChannel`'s) that none of `severity`, `class`, `acceptability`, `score` is declared, and add that clause to FR-004-AC-16/17 or a new AC. | spec/functional/FR-004-role-schemas.md:87, tests/test_role_schemas.py:219-266 | correct-requirement-no-evidence |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-002 | low | The new `test_no_judgment_key_is_declared_on_channel_plan_or_incident` is tagged TC-094 / FR-004-AC-17, but it asserts over `FeedbackChannel` and `Incident`, which neither FR-004-AC-17 (a maintenance-plan record carrying `severity` or `acceptability` fails) nor the TC-094 row states. The test exceeds its AC. Extend AC-17 and the TC-094 row to "`FeedbackChannel`, `MaintenancePlan` and `Incident` declare none of `severity`, `class`, `acceptability`, `score`", or add a new AC for the FR-004 Behavior bullet. | tests/test_role_schemas.py:269-275, spec/functional/FR-004-role-schemas.md:144, spec/tests.md:148 | wrong-requirement |

## Dispositions

| FND | Outcome | Reason |
|---|---|---|
| FND-001 | fixed | Round 1 (9b508b7): `test_no_judgment_key_is_declared_on_channel_plan_or_incident` asserts that no `severity`, `class`, `acceptability` or `score` property is declared on the three schemas. Mutation re-run: adding `severity?: AlertSeverity` to FeedbackChannel, or `class?: string` to Incident, in TypeSpec and regenerating now fails that test. The AC text gap is new finding FND-002. |
| FND-002 | fixed | Round 2 (8465742): new FR-004-AC-18 ("None of `severity`, `class`, `acceptability` or `score` is a declared property of `FeedbackChannel.json`, `MaintenancePlan.json` or `Incident.json`") and TC-095. The test is retagged TC-095 / FR-004-AC-18, and `quoin matrix` binds it there. AC-17/TC-094 are left scoped to plan structure. Mutation re-run: `severity` added to FeedbackChannel or to Incident in TypeSpec and regenerated fails the test. |
