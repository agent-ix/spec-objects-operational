---
id: Task-001
title: "FR-002 — TypeSpec toolchain, schema generator and drift gate"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-operational/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-013
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-014
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-017
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-018
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-019
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-020
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-024
    type: verifies
---
# Task-001: FR-002 — TypeSpec toolchain, schema generator and drift gate

## Scope

Stand up the emission half of FR-002: the pinned TypeSpec toolchain, the generator
that runs the official emitter and normalizes what it emits, and the drift gate that
makes a hand edit or a stale file red before push.

## Subtasks

- [x] **Toolchain pins.** `@typespec/compiler` 1.15.0, `@typespec/json-schema` 1.15.0 and `@agent-ix/semantic-core` 0.1.0 as exact `devDependencies`; `package-lock.json` resolving every public package from npmjs and `@agent-ix/semantic-core` from npm.ix; no `.npmrc` in the repository.
- [x] **`scripts/generate-schemas.mjs`.** Node built-ins only. Compiles `typespec/` with `tsp compile`, keeps only the files whose `$id` starts with the module base, rewrites any relative `$id`/`$ref` to the module base or the semantic-core base, records the rewrite in `toolchain.json`, and writes the manifest digests textually so anchors and comments survive.
- [x] **Refusals.** A failed compile, an empty emitted set, Node older than 20, or a `@jsonSchema` base whose version segment differs from the manifest `version` each exit non-zero without touching the committed output.
- [x] **`--check` mode.** Writes nothing, and names every differing, stale or digest-mismatched file.
- [x] **Wiring.** `make schemas`, `make schemas-check`, `make lint` chaining the gate, and `make install` running `npm ci` so the gate has a toolchain to run.

## Deliverables

- `typespec/tspconfig.yaml`, `scripts/generate-schemas.mjs`, `.gitattributes`
- `package.json`, `package-lock.json`, `Makefile`, `pyproject.toml` poe tasks
- Tests for TC-013, TC-014, TC-017, TC-018, TC-019, TC-020, TC-024

## Notes

- The generator resolves its own repo root from its file location, so a throwaway
  tree must run its own copy — every test that mutates the tree copies it first.
- This task is the only writer of `spec_objects_operational/schemas/` and of the
  manifest's `data_schema.digest` values.
- Unblocks: Task-002.
