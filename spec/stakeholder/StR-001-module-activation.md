---
id: StR-001
title: "Tier-2 operational objects"
type: StR
---
# [StR-001] Tier-2 operational objects

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

This need is considered satisfied when a Module activation against filament-core
registers all the contents this module declares, and when agent CLI generators
(minijinja-cli) can produce valid artifacts using the templates and schemas this
module ships. Satisfaction is judged by demonstrating both outcomes against a
filament-core instance.

## Stakeholders

The primary stakeholders are the Filament platform and spec authors, who depend
on the operational graph, and agent CLI generators, which consume the shipped
schemas and templates.

## Dependencies

- **Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035) (Module Manifest Schema)
- **Downstream**: [FR-001](../functional/FR-001-module-manifest-activates.md) (Module manifest activates against filament-core)
