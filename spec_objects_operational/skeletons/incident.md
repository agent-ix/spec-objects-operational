---
id: INC-001
title: "ArtifactStoreOutage"
type: incident
object: incident
---
<!-- incident authoring skeleton (spec-objects-operational). Contract
     (manifest body_extraction):
     - Frontmatter MUST carry id, title, type: incident, object: incident.
     - An incident is the module's one OBSERVED EXECUTION type, and the only
       one that carries an occurrence identity. Incident.json requires
       "## Properties" (H2, header exactly
       `Field | Type | Multiplicity | Constraints`) to hold at least one
       `identity` row (WHICH incident) and at least one `Timestamp` row
       (WHEN it was).
     - Incident is also the only type that declares `evidence`, the single
       canonical reference into the agent-ix/quoin#267 operational evidence
       record family. It references those records; it never copies a field
       of one.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning one
       `ocl` fence.
     - "## Timeline" (H2) is REQUIRED; its body is extracted as `timeline`.
     - Timeline entries are timestamped (UTC), factual, and ordered. -->
# [INC-001] ArtifactStoreOutage

A bad configuration reload dropped artifact-store availability to 97.4% for
38 minutes, consuming most of the monthly error budget for SLO-001. Root
cause: `max_upload_size_mb` was set below the size of in-flight uploads,
turning resumed uploads into 500s.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| incident_id | UUID | 1..1 | identity |
| detected_at | Timestamp | 1..1 | |
| resolved_at | Timestamp | 0..1 | |
| severity | String | 1..1 | enumValues: sev1\|sev2\|sev3 |
| breached_objective | ArtifactStoreAvailabilityObjective | 1..1 | |

## Invariants

The clauses the ArtifactStoreOutage declaration enforces. Each clause owns one
`ocl` fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### ResolutionFollowsDetection

```ocl
context ArtifactStoreOutage
inv ResolutionFollowsDetection:
  self.resolved_at->notEmpty() implies self.resolved_at > self.detected_at
```

### SeverityOneBreachesAnObjective

```ocl
context ArtifactStoreOutage
inv SeverityOneBreachesAnObjective:
  self.severity = 'sev1' implies self.breached_objective->notEmpty()
```

## Timeline

- 09:12 UTC — ALR-001 fast-burn alert pages the on-call engineer.
- 09:15 UTC — On-call confirms elevated 5xx on the availability dashboard.
- 09:21 UTC — Pod restarts ruled out; deploy history shows a config-only
  change at 09:05 lowering `max_upload_size_mb` from 512 to 64.
- 09:33 UTC — Configuration change reverted and reloaded via `SIGHUP`.
- 09:50 UTC — Success ratio back above target; alert resolves.
- 10:30 UTC — Follow-up filed to validate upload-size changes against
  in-flight upload sizes before reload.
