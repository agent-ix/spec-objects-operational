---
id: MNT-001
title: "ArtifactStoreMaintenancePlan"
type: maintenance_plan
object: maintenance_plan
---
<!-- maintenance_plan authoring skeleton (spec-objects-operational). Contract
     (manifest body_extraction):
     - Frontmatter MUST carry id, title, type: maintenance_plan,
       object: maintenance_plan.
     - A maintenance plan declares PROCEDURES, not data: MaintenancePlan.json
       forbids `fields`, so this skeleton carries NO "## Properties" section.
       It records who is accountable; it assigns no score, class or
       acceptability.
     - "## Operations" (H2, at least one operation when present): one
       `### <name>` per procedure, an optional
       `| Param | Type | Multiplicity | Constraints |` table, a `Returns:`
       line where the operation returns a value, and optional `Pre:`/`Post:`
       lines naming clause ids declared in this same artifact.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning one
       `ocl` fence.
     - "## Procedure" (H2) is REQUIRED; its body is extracted as `procedure`,
       the human-facing statement of how feedback from released software is
       received, documented and evaluated, and how a modification is made. -->
# [MNT-001] ArtifactStoreMaintenancePlan

How feedback on the released artifact store is handled once it is in use.

## Operations

The procedures the maintainer follows. Each operation owns one `### <name>`
heading with an optional parameter table, a `Returns:` line where it returns a
value, and `Pre:`/`Post:` lines where it names clauses declared in this
artifact.

### record_feedback

Record each report from a user, a support contact or a security advisory in
the problem register, with its origin and the release it concerns.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| report_id | UUID | 1..1 | |

Returns: Boolean[1..1]

Post: EveryReportIsRegistered

### evaluate_feedback

Evaluate a registered report for its bearing on safety and decide, by a named
person, whether a hazard or an anomaly record is opened or updated.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| report_id | UUID | 1..1 | |

## Invariants

The clauses the ArtifactStoreMaintenancePlan declaration enforces. Each clause
owns one `ocl` fence under its own `### <clauseId>` heading; the fence text is
carried verbatim and never evaluated here.

### EveryReportIsRegistered

```ocl
context ArtifactStoreMaintenancePlan
inv EveryReportIsRegistered:
  self.unregisteredReports = 0
```

## Procedure

1. Receive feedback through each channel the plan names and record it, with
   its origin, in the problem register (`record_feedback`).
2. A named reviewer evaluates each registered report for its bearing on safety
   and records the decision (`evaluate_feedback`).
3. Where a report calls for a modification, the change follows the
   modification process, and the affected hazard and anomaly records are
   updated by the person accountable for them.
