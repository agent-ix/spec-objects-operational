---
id: US-001
title: "Declare operational object types against semantic-core"
type: US
relationships:
  - target: "ix://agent-ix/spec-objects-operational/StR-001"
    type: "traces_to"
---
# US-001: Declare operational object types against semantic-core

## Story

**As a** maintainer of the operational object module
**I want** every operational object type (configuration, migration, SLI, SLO, alert, runbook, incident, deployment) to carry a real structural contract expressed in the shared semantic-core grammar
**So that** spec authors write one typed `## Properties` table per object, reviewers and generators read one declaration record per object, standing definitions stay separable from observed executions, and the same record validates identically in Quire, Quoin, and the compiler.

The story is stated from the maintainer's perspective and does not prescribe
the emitter, the file layout, or the extraction engine.

## Context

Today every object type in `manifest.yaml` carries `data_schema: {type: object}`,
which types nothing: an SLI and an incident are indistinguishable to a consumer,
`## Configuration` is a free table whose Scope column is checked only by an
advisory lint rule, and no cross-reference between two operational objects is
checked. The semantic-core grammar (`agent-ix/filament-core-data#35`) and the
semantic-module contract (`agent-ix/quoin#293`, `agent-ix/quire-rs#388`) now
exist and are merged, and the sibling business module
(`agent-ix/spec-objects-business#4`) has already taken this shape.

Operational modelling adds a distinction the business module did not have to
make: a *standing definition* (what the system is configured to do, what it
promises, how it is remediated) is not the same object as an *observed
execution* (what actually happened). The evidence programme
(`agent-ix/quoin#267`) already owns the observed-execution record family, so
this module maps to it rather than minting a second one.

## Acceptance Examples (Illustrative)

These examples clarify the maintainer's expectations. They are illustrative
only, not test cases and not verification criteria.

### US-001-EX-1: A configuration skeleton extracts to typed parameters

- **Given** the `configuration` skeleton with a `| Field | Type | Multiplicity | Constraints |` table
- **When** Quire extracts it under this module
- **Then** the record carries one `FieldDecl` per row, at least one row declares a default, and the record validates against the shipped `Configuration.json`

### US-001-EX-2: A migration that records when it ran is refused

- **Given** a migration artifact whose `## Properties` table carries an `applied_at` `Timestamp` row
- **When** Quire validates it
- **Then** validation fails naming the migration schema, because a migration declares change intent and safety, and when it ran belongs to the execution that applied it

### US-001-EX-3: The module installs into Quoin

- **Given** the packaged module directory
- **When** an operator runs `quoin module install path:<dir>`
- **Then** the install succeeds, every exported schema digest matches, and the module is listed

## Options (Exploratory)

Approaches discussed: hand-authoring one JSON Schema per type; generating the
schemas from a TypeSpec package that imports `@agent-ix/semantic-core`;
deriving the schemas from the skeletons; duplicating the `agent-ix/quoin#267`
evidence-record fields onto `incident`. Only the TypeSpec route keeps one
source for the grammar and its vocabulary, and only a reference (rather than a
copy) of the evidence record keeps one record family; both are the routes the
authoring contract on the ticket already names.

## Constraints (Contextual)

No corpus repository may be edited; existing `body_extraction` locators stay
as they are so current artifacts keep extracting; the change is advisory until
corpus promotion. This context is not binding here and is refined in the
functional and non-functional requirements.

## Dependencies (Contextual)

Upstream: semantic-core 0.3.0 on GitHub Packages, the module-manifest schema
with the `semantic` block, Quire 0.47.1 with `extract_semantic`, and the
`agent-ix/quoin#267` evidence-record family this module maps to. Downstream:
the frontends that read this module's skeletons as fixtures.

## Priority and Risk (Informative)

P1 on the Track A programme. The risk if unmet is that operational specs stay
untyped prose, that SLI/SLO objectives cannot be checked, and that a second,
incompatible operational evidence record family is minted beside
`agent-ix/quoin#267`.

## Notes (Informative)

Open question captured for later analysis: which sections beyond
`## Properties`, `## Invariants`, and `## Operations` the extraction engine
should read (`## Configuration`, `## Steps`, `## Timeline`, the mermaid
topology and flow fences). The schemas declare the corresponding keys;
extraction of them is an engine concern.

## Traceability (Informative)

Traces to [StR-001](../stakeholder/StR-001-module-activation.md); implemented
by [FR-002](../functional/FR-002-emitted-json-schemas.md),
[FR-003](../functional/FR-003-semantic-manifest-contract.md),
[FR-004](../functional/FR-004-role-schemas.md), and
[FR-005](../functional/FR-005-executable-skeletons.md).
