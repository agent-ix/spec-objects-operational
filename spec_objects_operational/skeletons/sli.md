---
id: SLI-001
title: "ArtifactStoreAvailability"
type: sli
object: sli
---
<!-- sli authoring skeleton (spec-objects-operational). Fill the query with
     the real measurement. Contract (manifest body_extraction):
     - Frontmatter MUST carry id, title, type: sli, object: sli.
     - "## Properties" (H2): the typed measurement. Header exactly
       `Field | Type | Multiplicity | Constraints`. Sli.json requires at
       least one MEASURED field — a `Type` cell with a trailing bracketed
       unit, e.g. `Duration [ms]` or `Decimal(5,4) [1]` (quoin FR-071) — so
       the indicator references a typed measurement rather than describing
       one in prose. It declares NO accumulated observation: no sample, no
       series, no measured value. Those are reached through an incident's
       evidence, never through a key here.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning one
       `ocl` fence.
     - "## Query" (H2, REQUIRED) MUST contain a fenced code block; its
       content is extracted as `query`.
     - State what counts as a good event so the ratio is unambiguous. -->
# [SLI-001] ArtifactStoreAvailability

Availability is the ratio of successful requests (any HTTP status outside the
5xx range) to total requests served by the artifact-store API, measured over a
5-minute rate window.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| success_ratio | Decimal(5,4) [1] | 1..1 | min: 0, max: 1 |
| evaluation_window | Duration [ms] | 1..1 | min: 1 |
| good_event_status_ceiling | Integer | 1..1 | min: 100, max: 599 |

## Invariants

The clauses the ArtifactStoreAvailability declaration enforces. Each clause
owns one `ocl` fence under its own `### <clauseId>` heading; the fence text is
carried verbatim and never evaluated here.

### RatioIsBounded

```ocl
context ArtifactStoreAvailability
inv RatioIsBounded:
  self.success_ratio >= 0 and self.success_ratio <= 1
```

### WindowIsPositive

```ocl
context ArtifactStoreAvailability
inv WindowIsPositive:
  self.evaluation_window > 0
```

## Query

```
sum(rate(http_requests_total{job="artifact-store", code!~"5.."}[5m]))
/
sum(rate(http_requests_total{job="artifact-store"}[5m]))
```
