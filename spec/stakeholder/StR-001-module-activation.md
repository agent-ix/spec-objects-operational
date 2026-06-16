---
id: StR-001
title: "Tier-2 operational objects"
type: StR
---
# [StR-001] Tier-2 operational objects

## Stakeholder

Filament platform / spec authors / agent CLI generators.

## Need

Operational specs need extractable graph entities for configuration, migrations, hooks, jobs, SLIs, and SLOs.

## Acceptance Criteria

| ID | Criteria |
|----|----------|
| StR-001-AC-1 | A Module activation against filament-core registers the contents this module declares. |
| StR-001-AC-2 | Agent CLI generators (minijinja-cli) can produce valid artifacts using the templates and schemas this module ships. |

## Dependencies

- **Upstream**: filament-core-service FR-035 (Module Manifest Schema)
