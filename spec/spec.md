---
type: master-requirements
name: spec-objects-operational
org: agent-ix
component_type: filament-object-module
implementation_language: python
tags:
  - filament
  - operational
depends_on: []
standards_alignment:
  - iso-iec-ieee-29148
relationships:
  - target: "ix://agent-ix/filament-core-service/FR-035"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/quoin/FR-070"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/quire-rs/FR-069"
    type: "depends_on"
    cardinality: "1:1"
security_critical: false
---
# Master Requirements Specification

## Purpose

This document specifies the requirements for `spec-objects-operational`, a
Filament Module that contributes eight tier-2 ObjectTypes for runtime
operational concerns (configuration, migration, SLI, SLO, alert, runbook,
incident, deployment). Operational specs need extractable graph entities for
what a system is configured to do, what it promises, how it is remediated, and
what actually happened; this module ships those ObjectTypes (with their
templates and schemas) so that authors, reviewers, and agent generators share
one authoritative definition of what the module activates against
`filament-core`.

## Scope

### In Scope

- The Module manifest (`spec_objects_operational/manifest.yaml`) and the eight
  tier-2 operational ObjectTypes it contributes.
- The functional requirement that the manifest activates idempotently against
  `filament-core-service`, and the integration test that verifies it.
- The semantic-module contract (issue #6): a TypeSpec source importing
  `@agent-ix/semantic-core` 0.1.0, the emitted JSON Schema per object type
  shipped under `spec_objects_operational/schemas/`, the manifest `semantic`
  block with reference-form `data_schema`, and the skeletons rewritten as
  executable typed fixtures with negative counterparts.
- The separation of standing definitions (configuration, migration, SLI, SLO,
  alert, runbook, deployment) from the one observed-execution type (incident),
  and the single reference-form mapping from an incident to the
  `agent-ix/quoin#267` operational evidence record family.
- Repair of the truncated `lexicon` definitions this repository's issue #5
  records.

### Out of Scope

- The behaviour of `filament-core-service` itself, referenced here only by the
  relationship to its manifest schema (FR-035).
- Deployment topology and cluster infrastructure of consuming clusters, which
  live in the operating environment rather than this specification.
- The `agent-ix/quoin#267` operational evidence record family itself. This
  module references a record by `SemanticId` and declares no field of it; the
  record's own shape, storage, and lifecycle stay with that programme, and an
  incompatibility there is resolved by changing the reference, never by minting
  a second record family here.
- Runtime control behaviour: nothing in this module deploys, scales, migrates,
  pages, or rolls back anything. The schemas describe declarations; execution
  belongs to the operating environment.
- Accumulated observations of any kind — measured samples, consumed error
  budgets, applied-migration timestamps, database execution state. These are
  refused by every model's seal and are reached through a referenced evidence
  record, not through a key on a standing definition.
- Generated-language fixtures (Rust, TypeScript, Python) for the operational
  types: produced by the TypeSpec frontend and compiler core
  (`agent-ix/filament-core-data#21`, `#22`, `#23`) and published only behind the
  promotion gate (`agent-ix/quoin#290`); the semantic-core language packages are
  `agent-ix/filament-core-data#11`. None is produced or faked here.
- Extraction of the declared-but-not-yet-extracted keys (`scopes`, `configures`,
  `rollback`, `migrates`, `dependsOn`, `measures`, `objective`, `constrains`,
  `conditions`, `escalatesTo`, `references`, `steps`, `remediates`, `evidence`,
  `correlates`, `breaches`, `triggers`, `rollout`, `deploys`, `relations`) from
  Markdown: the mapping is owned by `agent-ix/quoin#335` (FR-071/FR-072 define
  `Properties`, `Invariants`, and `Operations` only) and the extractor by
  `agent-ix/quire-rs` once the mapping is published; the schemas declare the
  keys as optional so the engine can fill them without a schema change.
- Naming what a module load refused: `agent-ix/quire-rs#221` (an unknown
  manifest key empties the model silently) and `agent-ix/quire-rs#394` (a
  `data_schema` digest mismatch drops the object type with no diagnostic).
  FR-003-AC-6's "naming the key or the path" half is blocked on them and is
  carried as an explicit expected failure.
- Record validation of a legacy-form artifact that declares `object:`:
  `agent-ix/quire-rs#391` (the engine validates an `unavailable` record as
  `{}`, so a legacy form errors even under `legacy_forms: warning`).
  NFR-001-AC-2 itself holds — no 0.2.0 artifact carries `object:` — and the
  defect is carried as an explicit expected failure beside it rather than
  worked around by relaxing a schema.
- Publishing the Quire 0.46.0 wheel to an index a repository may commit
  against: `agent-ix/quire-rs#392`. `internal-pypi` serves 0.33.0 at most and
  no `quire-rs` tag carries the semantic layer, so this module provisions the
  wheel with a documented `make dev-quire` target and its semantic tests fail
  rather than skip when the engine is absent (FR-005). Declaring `quire` as a
  committed dev dependency waits on that issue.
- Reconciling the three divergent copies of the FR-035 module-manifest schema:
  `agent-ix/filament-core-service#26`. The service's own copy admits neither
  the `semantic` block nor the `lexicon` block this manifest carries, so this
  module pins the `agent-ix/spec-artifacts-iso` copy that Quoin and Quire load,
  and FR-001-AC-1 is measured against that. Dropping the `lexicon` to satisfy
  the stale copy is refused.
- Resolving a reference-form `data_schema` into a stored snapshot at
  activation: `agent-ix/filament-core-service#23`. Until it lands the service
  stores the reference verbatim, which is the reading FR-001-AC-4 and
  IT-001-SC-02 take of "appears in the corresponding table": the registered
  `data_schema` is the reference object as posted, not a resolved snapshot.
- Editing any corpus repository or vendored fixture; the legacy-form sweep and
  corpus promotion (`agent-ix/quoin#291`).
- Application database schema generation: none is produced by these schemas.
  A `migration` declaration describes intent and safety, not DDL execution.

## System Overview

### System Description

`spec-objects-operational` is a Python package that publishes a Filament Module
manifest declaring eight tier-2 ObjectTypes for operational modelling. The
manifest is activated against `filament-core-service` over its HTTP API, which
registers the declared archetypes, object types, grammars, and artifact types.

### Intended Users

The Filament platform (which activates and serves the contributed ObjectTypes),
spec authors (who model operational concerns using them), and agent CLI
generators such as `minijinja-cli` (which produce artifacts from the shipped
templates and schemas).

## Requirements Architecture

The requirement classes that make up this specification trace from the
stakeholder need for extractable operational graph entities (`stakeholder/`)
through the maintainer's story of declaring those types against semantic-core
(`usecase/`) to the functional requirements (`functional/`): FR-001 activates
the manifest against `filament-core`; FR-002 emits the schemas; FR-003 declares
the semantic contract in the manifest; FR-004 fixes each type's role-distinct
schema; FR-005 makes the skeletons executable fixtures. NFR-001 bounds the
change to additive compatibility. Integration tests in `integration/` verify
the activation and Quoin-install boundaries; the third external boundary, the
Quire engine (loader, extraction, record surface), has no IT artifact of its
own — the FR-003 and FR-005 test harness is this module's Quire contract test,
and the wheel version is pinned once in FR-005 Inputs. The Test Matrix in
`tests.md` records every criterion's test case.

## References

- ISO/IEC/IEEE 29148 — Requirements engineering.
- This module's source repository and `manifest.yaml`.
- `filament-core-service` FR-035 (Module Manifest Schema), the upstream
  specification this module's manifest conforms to.
- `agent-ix/filament-core-data` FR-031..FR-034 (semantic-core grammar,
  scalars, JSON Schema projection, lowering) and ADR-0005 (TypeSpec source).
- `agent-ix/quoin` FR-070..FR-075 (semantic-module contract, mappings,
  `data_schema` by digest, legacy forms, package manifests).
- `agent-ix/quire-rs` FR-069..FR-072 (contract at load, typed Properties,
  clauses and operations, extraction surface).
