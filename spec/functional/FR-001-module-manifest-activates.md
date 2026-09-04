---
id: FR-001
title: "Module manifest activates against filament-core"
type: FR
relationships:
  - target: "ix://agent-ix/filament-core-service/FR-035"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-operational/StR-001"
    type: "traces_to"
---
# FR-001: Module manifest activates against filament-core

## Description

The system **SHALL** publish a Filament Module manifest (`spec_objects_operational/manifest.yaml`) that conforms to filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035) v1.0.0 and activates idempotently against `POST /api/v1/modules/activate`.


## Inputs

- `manifest.yaml` (this repo's package)
- Activation endpoint: `POST /api/v1/modules/activate`

## Outputs

- Module row in `modules` table
- Contributed archetypes, object_types, grammars, artifact_types per the manifest

## Behavior

The manifest **SHALL** validate against `module-manifest.schema.json` v1.0.0. Re-activation **SHALL** be a no-op (idempotent by content hash per FR-026-AC-1).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-1 | Manifest validates against FR-035 JSON Schema | Test |
| FR-001-AC-2 | Activation against clean filament-core succeeds with 200 | Test |
| FR-001-AC-3 | Re-activation returns no-op (same content hash) | Test |
| FR-001-AC-4 | Each declared archetype/object_type/artifact_type appears in the corresponding filament-core table after activation, and each exported object type's registered `data_schema` equals the reference object as posted (`agent-ix/filament-core-service#23` has not yet resolved it into a stored snapshot) | Test |

## Dependencies

- **Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035), FR-026, FR-034
- **Downstream**: consumer agents/editors discovering this module's contributions
