---
id: SLI-001
title: "ArtifactStoreAvailability"
type: sli
object: sli
---
<!-- sli authoring skeleton, alternate Properties form. Declares exactly the
     same fields as sli.md, authored as one `sysml` fence instead of the
     typed table (FR-005-AC-2). One artifact carries one form; the alternate
     is a separate file, never a second block in the same artifact. -->
# [SLI-001] ArtifactStoreAvailability

Availability is the ratio of successful requests (any HTTP status outside the
5xx range) to total requests served by the artifact-store API, measured over a
5-minute rate window.

## Properties

```sysml
attribute success_ratio : Decimal(5,4) [1][1..1] { min: 0, max: 1 }
attribute evaluation_window : Duration [ms][1..1] { min: 1 }
attribute good_event_status_ceiling : Integer[1..1] { min: 100, max: 599 }
```

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
