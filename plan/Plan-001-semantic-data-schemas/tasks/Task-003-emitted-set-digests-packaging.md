---
id: Task-003
title: "FR-002 — emitted set, toolchain.json, digests and packaging"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-operational/Task-011
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-010
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-011
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-012
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-015
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-016
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-025
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-026
    type: verifies
---
# Task-003: FR-002 — emitted set, toolchain.json, digests and packaging

## Scope

The emitted-set half of FR-002: assert what the generator actually produced, and
ship it in both distribution channels.

## Subtasks

- [x] **Emitted set.** Exactly the twenty-seven files `toolchain.json` lists — the eight object-type models plus nineteen support models — with compiler and emitter 1.15.0 and the module base recorded.
- [x] **`$id` and `$ref` shape.** Every schema declares the 2020-12 `$schema` and an `$id` matching its file name under the manifest-version base; every `$ref` names a shipped sibling or semantic-core 0.1.0.
- [x] **Python packaging.** `pyproject.toml` `include` gains `spec_objects_operational/schemas/*.json`, so the wheel and the sdist both carry them.
- [x] **npm packaging.** `scripts/stage-npm.mjs` gains the `--clean` postpack half, so the tarball ships `manifest.yaml` beside `schemas/` and the staged copies never survive at the repository root.
- [x] **Line endings.** `.gitattributes` marks `*.json`, `*.tsp`, `*.yaml` and `*.md` `eol=lf`, so a checkout with `autocrlf` cannot change digested bytes.

## Deliverables

- `spec_objects_operational/schemas/toolchain.json`
- `pyproject.toml` include list, `scripts/stage-npm.mjs`, `.gitattributes`
- Tests for TC-010, TC-011, TC-012, TC-015, TC-016, TC-025, TC-026

## Notes

- A leftover staged `manifest.yaml` at the repository root makes every Filament tool
  discover the repo root as a second module, which breaks an unrelated
  `quire validate`; the `--clean` half is asserted, not assumed.
- Unblocks: Task-004.
