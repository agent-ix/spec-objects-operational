---
id: RUN-001
title: "RestoreArtifactStoreAvailability"
type: runbook
object: runbook
---
<!-- runbook authoring skeleton (spec-objects-operational). Contract (manifest
     body_extraction):
     - Frontmatter MUST carry id, title, type: runbook, object: runbook.
     - A runbook declares ACTIONS, not data: Runbook.json forbids `fields`,
       so this skeleton carries NO "## Properties" section.
     - "## Operations" (H2, REQUIRED by Runbook.json): at least one
       operation. One `### <name>` per operation, an optional
       `| Param | Type | Multiplicity | Constraints |` table, a `Returns:`
       line where the operation returns a value, and optional `Pre:`/`Post:`
       lines naming clause ids declared in this same artifact.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning one
       `ocl` fence.
     - "## Steps" (H2) is REQUIRED; its body is extracted as `steps`. It is
       the human-facing ordered view of the operations above, which are the
       authority. -->
# [RUN-001] RestoreArtifactStoreAvailability

Use this runbook when ALR-001 pages for an availability burn against SLO-001.

## Operations

The operations an operator performs. Each operation owns one `### <name>`
heading with an optional parameter table, a `Returns:` line where it returns a
value, and `Pre:`/`Post:` lines where it names clauses declared in this
artifact.

### acknowledge_page

Acknowledge the page and confirm the burn rate on the availability dashboard,
so a flapping probe is ruled out before anything is changed.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| page_id | UUID | 1..1 | |

Returns: Boolean[1..1]

Post: NoActionBeforeAcknowledgement

### restart_unhealthy_replicas

Delete any pod stuck in `CrashLoopBackOff` so the scheduler replaces it;
`kubectl get pods -n apps -l app=artifact-store` lists the candidates.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| namespace | String | 1..1 | minLength: 1 |
| max_restarts | Integer | 1..1 | min: 1, max: 5 |

Returns: Integer[1..1]

### roll_back_release

Roll the deployment back to the previous known-good revision with
`helm rollback artifact-store -n apps` when a release shipped within the hour
that error onset began.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| release_name | String | 1..1 | minLength: 1 |

Returns: Boolean[1..1]

### resolve_page

Resolve the page once the success ratio has held above target for fifteen
minutes, and open an incident record for the follow-up.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| page_id | UUID | 1..1 | |

Post: PageResolvedOnlyAfterRecovery

## Invariants

The clauses the RestoreArtifactStoreAvailability declaration enforces. Each
clause owns one `ocl` fence under its own `### <clauseId>` heading; the fence
text is carried verbatim and never evaluated here.

### NoActionBeforeAcknowledgement

```ocl
context RestoreArtifactStoreAvailability
inv NoActionBeforeAcknowledgement:
  self.acknowledged = true
```

### PageResolvedOnlyAfterRecovery

```ocl
context RestoreArtifactStoreAvailability
inv PageResolvedOnlyAfterRecovery:
  self.recoveredMinutes >= 15
```

## Steps

1. Acknowledge the page and confirm the burn rate on the availability
   dashboard so a flapping probe is ruled out (`acknowledge_page`).
2. Check pod health: `kubectl get pods -n apps -l app=artifact-store`. Restart
   any pod stuck in `CrashLoopBackOff` with `kubectl delete pod <name> -n apps`
   (`restart_unhealthy_replicas`).
3. Compare error onset with the deploy history. If a release shipped within
   the last hour, roll it back: `helm rollback artifact-store -n apps`
   (`roll_back_release`).
4. If errors persist, inspect dependency health — PostgreSQL connections and
   object-storage latency — via `kubectl logs deploy/artifact-store -n apps`.
5. Once the success ratio recovers above target for 15 minutes, resolve the
   page and open an incident record (`resolve_page`; see INC-001 for the
   expected shape).
