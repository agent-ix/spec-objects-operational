---
id: IT-001
title: "Manifest activation roundtrip against filament-core"
type: IT
relationships:
  - target: "ix://agent-ix/spec-objects-operational/FR-001"
    type: "verifies"
---
# IT-001: Manifest activation roundtrip

## Objective

Verify the integration boundary between this Module's published manifest and a
clean `filament-core-service` instance: activating `manifest.yaml` shall land all
declared contributions in the database, and re-activating the same manifest shall
be an idempotent no-op. This test verifies [FR-001](../functional/FR-001-module-manifest-activates.md).

## Target Integration

The service under test is `filament-core-service` and the external artifact is
this repo's `spec_objects_operational/manifest.yaml`. The integration type
exercised is HTTP: a `POST` to the module activation endpoint followed by `GET`
reads of the contribution catalog endpoints, against the service's database.

## Preconditions

A `filament-core-service` instance is running and reachable on a clean database
(or kind dev cluster) so that the absence or presence of contributed rows is
meaningful, and this repo's `manifest.yaml` is built and available to submit.

## Inputs

This repo's `spec_objects_operational/manifest.yaml` (the tier-2 operational
ObjectTypes module). The same manifest bytes are submitted twice to exercise the
idempotency path.

## Test Procedure

Each step performs one discrete action and declares its success criterion.

1. `POST spec_objects_operational/manifest.yaml` to `/api/v1/modules/activate`.
   - IT-001-SC-01: the endpoint returns 200 OK and a `modules` row is created.
2. `GET` `/api/v1/archetypes`, `/api/v1/object-types`, `/api/v1/grammars`, and
   `/api/v1/artifact-types`.
   - IT-001-SC-02: each item declared by the manifest is present with the
     correct attributes.
3. Re-`POST` the same manifest to `/api/v1/modules/activate`.
   - IT-001-SC-03: the activation is an idempotent no-op — same `modules.id`,
     same SHA-256 content hash, and no row duplication.

## Expected Results

Activation against a clean `filament-core-service` succeeds with 200 OK, every
declared archetype, object type, grammar, and artifact type appears in its
corresponding catalog endpoint, and re-activation yields the same SHA-256 content
hash with no duplicated rows. The test passes only when every per-step success
criterion holds.

## Traceability

This integration test verifies [FR-001](../functional/FR-001-module-manifest-activates.md) (Module manifest activates against
filament-core).
