---
id: StR-001
title: "Tier-2 operational objects"
type: StR
---
# StR-001: Tier-2 operational objects

## Stakeholder Need

The Filament platform, spec authors, and agent CLI generators require that
operational specs **shall** yield extractable graph entities for configuration,
migrations, hooks, jobs, SLIs, and SLOs, so that runtime operational concerns are
first-class, queryable objects rather than free prose.

## Rationale

Operational concerns — configuration, migrations, hooks, jobs, SLIs, and SLOs —
are today expressed only as prose and cannot be queried, validated, or generated
against. Without a shared module of tier-2 ObjectTypes, each consumer reinvents
the structure and agent generators have no schemas or templates to target, which
fragments the operational graph and blocks downstream automation.

## Validation Criteria


| ID | Criteria | Validation |
|----|----------|------------|
| StR-001-VC-1 | A Module activation against filament-core registers all the contents this module declares. | Inspection |
| StR-001-VC-2 | Agent CLI generators (minijinja-cli) can produce valid artifacts using the templates and schemas this module ships. | Demonstration |
| StR-001-VC-3 | Every operational object type carries one typed structural contract that the downstream frontends (`agent-ix/quire-contract-ir#52`, `agent-ix/filament-core-data#36`) can consume read-only, so a standing definition and an observed execution are distinguishable to a consumer without reading the prose. | Demonstration |

Satisfaction is judged by demonstrating the first two outcomes against a
filament-core instance, and the third against the shipped schemas and skeletons
read as fixtures.

## Stakeholders

The primary stakeholders are the Filament platform and spec authors, who depend
on the operational graph, and agent CLI generators, which consume the shipped
schemas and templates.

## Dependencies

- **Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035) (Module Manifest Schema)
- **Downstream**: [FR-001](../functional/FR-001-module-manifest-activates.md) (Module manifest activates against filament-core), [US-001](../usecase/US-001-declare-operational-objects-against-semantic-core.md) (Declare operational object types against semantic-core)
