---
id: Task-007
title: "FR-005 / FR-002 — Quire provisioning, the no-vacuous-skip gate and the 0.2.0 baseline"
type: Task
status: done
track: B
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-operational/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-operational/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-021
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-022
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-023
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-027
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-069
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-071
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-072
    type: verifies
---
# Task-007: FR-005 / FR-002 — Quire provisioning, the no-vacuous-skip gate and the 0.2.0 baseline

## Scope

Make the engine a hard dependency of the semantic rows, and freeze the 0.2.0 surface
the compatibility criteria measure against — both before anything else changes it.

## Subtasks

- [x] **`make dev-quire`.** Installs the wheel exposing `extract_semantic` from the dev-only `pypi.ix`; `quire` is declared in no dependency group while `agent-ix/quire-rs#392` is open.
- [x] **Fail, never skip.** `conftest.require_quire` fails the test naming `extract_semantic`, `make dev-quire` and quire-rs#392; the pre-existing `pytest.skip` in `tests/test_skeletons_and_validate.py` is replaced by it.
- [x] **The 0.2.0 baseline.** `tests/fixtures/baseline-0.2.0/` holds the 0.2.0 `body_extraction`, `lint_rules`, lexicon term set and all eight 0.2.0 skeletons, plus the 0.2.0 manifest itself so the truncated lexicon can be read as YAML actually parsed it.
- [x] **The schema registry fixture.** A 2020-12 validator factory resolving every `$ref` locally — module models from the committed tree, grammar models from the installed semantic-core package.
- [x] **Packaging inspections.** No `.npmrc`, no `file:`/`link:`, exact pins, npmjs-only lockfile, no hard-coded `$id` version segment, no corpus or vendored-fixture edit on the branch.

## Deliverables

- `tests/conftest.py`, `tests/test_engine_provisioning.py`
- `tests/fixtures/baseline-0.2.0/`, `tests/fixtures/module-manifest.schema.json`
- `Makefile` / `pyproject.toml` `dev-quire` target
- Tests for TC-021, TC-022, TC-023, TC-027, TC-069, TC-071, TC-072

## Notes

- Replacing the skip immediately surfaced a defect it had been hiding: the
  `configuration` branch of `test_mutated_skeleton_fails_validation` read
  `after_heading` from a `table_row` locator, which names its heading with
  `under_section`. A skipped row is not coverage.
- The baseline is captured from `git show main:` so it is the 0.2.0 bytes, not a
  re-description of them.
- Unblocks: Task-004, Task-008. Runs in parallel with Track A from the start.
