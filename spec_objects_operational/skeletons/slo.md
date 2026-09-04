---
id: SLO-001
title: "ArtifactStoreAvailabilityObjective"
type: slo
object: slo
target: "99.9%"
window: "30d"
---
<!-- slo authoring skeleton (spec-objects-operational). Contract (manifest
     body_extraction):
     - Frontmatter MUST carry id, title, type: slo, object: slo, AND the two
       extracted objective fields: `target` (e.g. "99.9%") and `window`
       (e.g. "30d", a rolling window).
     - "## Properties" (H2): the typed objective. Header exactly
       `Field | Type | Multiplicity | Constraints`. Slo.json requires at
       least one MEASURED field — a `Type` cell with a trailing bracketed
       unit (quoin FR-071). It declares the budget's SIZE, never the budget
       CONSUMED: a consumed budget is an observation, reached through an
       incident's evidence and never through a key here.
     - "## Invariants" (H2, REQUIRED by Slo.json): at least one clause. The
       objective IS an invariant over the indicator. One `### <clauseId>` per
       clause, each owning one `ocl` fence.
     - The body explains the objective and its error budget in prose. -->
# [SLO-001] ArtifactStoreAvailabilityObjective

The artifact-store API serves 99.9% of requests successfully, measured by
ArtifactStoreAvailability over a rolling 30-day window. The corresponding
error budget is roughly 43 minutes of full unavailability per window.

When the remaining error budget drops below 25%, feature deploys to the
artifact-store pause and only reliability fixes ship until the budget
recovers. Burn-rate alerting against this objective is defined in ALR-001.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| objective_target | Decimal(5,4) [1] | 1..1 | min: 0, max: 1 |
| rolling_window | Duration [d] | 1..1 | min: 1 |
| error_budget_size | Decimal(5,4) [1] | 1..1 | min: 0, max: 1 |
| deploy_freeze_threshold | Decimal(5,4) [1] | 1..1 | min: 0, max: 1 |

## Invariants

The clauses the ArtifactStoreAvailabilityObjective declaration enforces. Each
clause owns one `ocl` fence under its own `### <clauseId>` heading; the fence
text is carried verbatim and never evaluated here.

### BudgetIsComplementOfTarget

```ocl
context ArtifactStoreAvailabilityObjective
inv BudgetIsComplementOfTarget:
  self.error_budget_size = 1 - self.objective_target
```

### FreezeThresholdIsWithinBudget

```ocl
context ArtifactStoreAvailabilityObjective
inv FreezeThresholdIsWithinBudget:
  self.deploy_freeze_threshold > 0 and self.deploy_freeze_threshold < 1
```
