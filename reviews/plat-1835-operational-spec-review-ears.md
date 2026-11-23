---
id: SR-1627
title: "Spec review (EARS) — spec-objects-operational PR #31 (PLAT-1835 incident hazard/anomaly links and maintenance plan)"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-objects-operational; spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/stakeholder/StR-001-module-activation.md"
review_set: subset
---
# Spec review (EARS) — spec-objects-operational PR #31 (PLAT-1835 part 2)

## Summary

Ticket: PLAT-1835. Examined every requirement statement the PR adds or edits.
In FR-004: the new `maintenance_plan` table row, which the opening "Each model
SHALL enforce its row" governs; the `FeedbackChannel` shape bullet; the
no-severity/class/acceptability bullet; the `Incident.hazards`,
`Incident.anomalies` and optionality bullets; and the edited cross-reference
and optional-key bullets. Also the edited FR-005 `## Properties` bullet and
the StR-001 need statement.

All are ubiquitous `SHALL` statements with a named subject (a model or a key)
and a single obligation each. The optionality bullet defines absent vs empty
explicitly. No statement uses a weak modal.

## Verdict

**PASS with one low** — wording only.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | low | "`Incident.hazards` SHALL name the hazards an incident bears on, so post-production information reaches the risk record…" — "bears on" is not defined, and two authors could disagree on whether a hazard the incident did not realise but made more likely belongs in the list. The schema checks only the `SemanticId` form, so the meaning rests on this sentence. State the relation plainly, for example "the hazards the incident realised or that its investigation found relevant", and move the purpose clause to the Description. | spec/functional/FR-004-role-schemas.md:88 | wrong-requirement |

## Dispositions
