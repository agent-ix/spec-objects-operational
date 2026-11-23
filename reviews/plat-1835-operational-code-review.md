---
id: SR-1624
title: "Code review — spec-objects-operational PR #31 (PLAT-1835 incident hazard/anomaly links and maintenance plan)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-operational; spec_objects_operational/manifest.yaml, spec_objects_operational/schemas/Incident.json, spec_objects_operational/schemas/MaintenancePlan.json, spec_objects_operational/schemas/FeedbackChannel.json, spec_objects_operational/skeletons/maintenance_plan.md, typespec/main.tsp, tests/conftest.py, tests/test_role_schemas.py, tests/test_skeletons_and_validate.py, tests/test_skeletons_semantic.py"
review_set: subset
---
# Code review — spec-objects-operational PR #31 (PLAT-1835 part 2)

## Summary

Ticket: PLAT-1835. Reviewed `git diff origin/main...HEAD` at `41622f7`
(one commit). The change adds optional `hazards` and `anomalies`
(`SemanticId[]`) to `Incident` and a ninth object type, `maintenance_plan`
(`MaintenancePlan`, `FeedbackChannel`), with a skeleton, manifest entry and
two new tests (TC-093, TC-094).

What is right: the TypeSpec models are sealed (`...Record<never>`), every new
cross-reference is a `$ref` to semantic-core `SemanticId`, `operations` is
optional with `minItems: 1`, `fields` is refused by the seal, and no new schema
declares a score, class or acceptability key. `node scripts/generate-schemas.mjs
--check` reports all 29 schemas match the committed output. The
`maintenance_plan` skeleton validates under quire 0.62.2 with no error and
extracts two operations and one clause, with `fields` `not_applicable`. There
is no compatibility layer and no quoted standard text. The cross-module targets
`hazard` and `soup_record` follow the established pattern: spec-objects-safety
names `soup_record`, `threat` and `control` the same way. With the safety and
security modules loaded, quire resolves them and the `UnknownRole` advisories
go away.

Baseline measurement: the focused tests below were run on HEAD and on
origin/main in temporary worktrees. The runs used semantic-core 0.3.2 from the
npm cache and two engines: quire 0.53.0 (local) and quire 0.62.2 (scratch
venv). `poetry.lock` pins quire **0.50.0**, not 0.62. Under 0.62.2, origin/main
has 8 failures in the `slo`/`incident` skeleton and negative-fixture tests, not
6. HEAD has the same 8. So the red baseline is not an artifact of an old local
engine, and none of those failures come from this PR. The PR's claim that "none
involve `maintenance_plan`" is still wrong: see FND-001.

## Verdict

**CHANGES REQUESTED** — one high (TC-060 is broken by a count pin this PR made
false) and one medium (three new edge verbs are not in the registered
vocabulary). One low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | high | `test_every_skeleton_validates_with_no_error` (TC-060, FR-005-AC-1) still runs `assert len(skeletons) == 11`. The PR adds a twelfth skeleton, so the test fails on HEAD at that line under any engine, before it validates a single skeleton. On origin/main the line passes and the test fails later for the pre-existing incident reason, which hid this. It is a count pin; delete the line rather than bump it to 12. The glob already covers every skeleton, and `test_skeletons_and_validate.py` parametrizes one case per object type. | tests/test_skeletons_semantic.py:78 | implementation-bug-despite-evidence |
| FND-002 | medium | The new `allowed_links` verbs `hazards`, `anomalies` (incident) and `maintains` (maintenance_plan) are not in spec-artifacts-iso `edge_types`. `quire validate --module <iso> --module <safety> --module <security> --module spec_objects_operational` reports `UnknownEdgeType` for all three, and origin/main reports none. The ecosystem rule, stated in spec-objects-safety's manifest, is to reuse an existing verb before adding one. Either reuse a registered verb (`references`, `relates_to`, `manages`), or register the new verbs in spec-artifacts-iso first. The schema keys can keep their names. | spec_objects_operational/manifest.yaml:265-266, spec_objects_operational/manifest.yaml:336 | missing-requirement |
| FND-003 | low | `anomalies: [soup_record]` limits the incident→anomaly link to SOUP records. An incident that surfaces an anomaly in the product's own software has no allowed target, and the link draws a `disallowed-edge-target` warning. FR-004 states the key more broadly: "the artifacts that record the anomalies an incident surfaced". Either widen the target list, or narrow the FR statement to SOUP anomalies and say where own-software anomalies are recorded. | spec_objects_operational/manifest.yaml:266, spec/functional/FR-004-role-schemas.md:89 | wrong-requirement |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-004 | medium | The fix maps the schema keys `hazards`/`anomalies` (Incident) and `maintains` (MaintenancePlan) onto the registered verbs `references` and `manages`, and FR-004 now states this mapping. No engine implements it. Under quire-rs FR-076 a typed relation key is a `SemanticId[]` schema property *named after* an allowed verb (`typed_keys`, src/semantic/relations.rs:234), which is how the module's other keys work: `correlates`, `breaches`, `triggers`, `configures`, `deploys`. Measured at `9b508b7` with quire 0.62.2, the `relationships` mapping enabled in a temp copy, and iso, safety, security and operational loaded. A `## Relationships` row `references HAZ-001` on an incident is refused with "verb `references` is no typed relation key of object type incident". A `hazards` row is refused as "not in the edge_types registry". No authored form can populate these three keys, and FR-004's mapping sentence asserts a correspondence the engine contradicts. Either register verbs whose names equal the keys in spec-artifacts-iso (a cross-repo change), or drop the mapping sentence and say the keys have no relation path until agent-ix/quoin#335 defines one. | spec/functional/FR-004-role-schemas.md:90, spec_objects_operational/manifest.yaml:267, spec_objects_operational/manifest.yaml:334 | wrong-requirement |

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-005 | medium | Round 2 removed working graph links along with the false mapping sentence. `incident.allowed_links.references` is back to `[deployment]`, and `maintenance_plan` has no `allowed_links` at all. The round-1 targets were registered verbs with foreign targets resolvable the same way spec-objects-safety does it, and they were not the defect in FND-004. Measured with `quire validate --okf`, iso/safety/security/operational loaded, and a bundle holding the safety `hazard` skeleton plus an incident whose frontmatter has `relationships: [{type: references, target: HAZ-001}]`. At `8465742` it warns `disallowed-edge-target` ("target type 'hazard' ... does not satisfy the forward target list [\"deployment\"]"). With the round-1 manifest it is clean. So an incident can no longer reference a hazard or SOUP record by any path: the schema keys are populated by no extractor and the graph edge is refused, though the ticket asks for exactly that link. `maintenance_plan` is also the only type of the nine with no `allowed_links`, so Tier-1 edge checking is skipped for it (open vocabulary, quire-rs `validate_document.rs`), unlike every other type. Restore `references: [deployment, hazard, soup_record]` on incident and `manages: [deployable]`, `references: [runbook]` on maintenance_plan. Keep FR-004 free of any key-to-verb mapping claim. | spec_objects_operational/manifest.yaml:267, spec_objects_operational/manifest.yaml:332 | wrong-requirement |

## Dispositions

| FND | Outcome | Reason |
|---|---|---|
| FND-001 | fixed | Round 1 (9b508b7): `assert len(skeletons) == 11` deleted; no new count pin in the fix diff. TC-060 now fails only on the pre-existing incident-skeleton error shared with origin/main. |
| FND-002 | fixed | Round 1: allowed_links now use `references: [deployment, hazard, soup_record]` and `manages: [deployable]`; `quire validate` with iso, safety, security and operational loaded reports no UnknownEdgeType for incident or maintenance_plan. The key-to-verb mapping this introduced is new finding FND-004. |
| FND-003 | fixed | Round 1: FR-004 now restricts `Incident.anomalies` to `soup_record` artifacts and states that an anomaly of the product's own software has no target here, matching the manifest. |
| FND-004 | still-open | Round 2 (8465742): the false key-to-verb mapping sentence is gone, but its replacement says the keys "SHALL be plain frontmatter `SemanticId` lists". Measured with quire 0.62.2: an incident or maintenance-plan document carrying `hazards:` / `maintains:` in frontmatter extracts a record with no `hazards` or `maintains` key, so the engine does not read them from frontmatter either. State instead that no extraction path populates them yet (agent-ix/quoin#335), as FR-004 already says for the other unpopulated keys. |
| FND-004 | fixed | Round 3 (a2c5fe8): FR-004 now says the current extractor does not populate `hazards`, `anomalies` or `maintains`, and points to the unfilled-keys bullet, which lists all three. Graph links are authored through the registered `references` / `manages` verbs. There is no frontmatter claim and no key-to-verb mapping. |
| FND-005 | fixed | Round 3 (a2c5fe8): the manifest is byte-identical to round 1 (blob 65613f2): incident `references: [deployment, hazard, soup_record]`, maintenance_plan `manages: [deployable]`, `references: [runbook]`. In the `quire validate --okf` bundle, an incident `references HAZ-001` edge and a maintenance-plan `manages DEP-001` edge raise no disallowed-edge-target warning. As a negative control, `manages HAZ-001` does warn. No UnknownEdgeType. |
