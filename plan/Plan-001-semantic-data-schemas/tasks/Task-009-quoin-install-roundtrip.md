---
id: Task-009
title: "IT-002 — Quoin install roundtrip with unconditional restore"
type: Task
status: blocked
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-operational/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-operational/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-operational/IT-002
    type: references
  - target: ix://agent-ix/spec-objects-operational/TC-036
    type: verifies
  - target: ix://agent-ix/spec-objects-operational/TC-091
    type: verifies
---
# Task-009: IT-002 — Quoin install roundtrip with unconditional restore

## Scope

Verify the boundary between this module's shipped directory and the Quoin module
installer, and leave the operator's global module store exactly as it was found.

## Subtasks

- [ ] **Record.** Capture `quoin module` before anything is installed.
- [ ] **Install.** `quoin module install path:<module dir>` exits zero with no `semantic.*` error diagnostic.
- [ ] **List.** `quoin module` contains `spec-objects-operational` sourced from the path.
- [ ] **Derived manifest.** `semantic/package-manifest.json` names `agent-ix/spec-objects-operational` and one export per `semantic.exports` entry.
- [ ] **Restore, unconditionally.** The prior source and ref are re-installed whether or not any earlier step passed.

## Deliverables

- `tests/test_quoin_install_roundtrip.py`
- Tests for TC-036, TC-091

## Notes

- **Blocked.** No released Quoin carries the semantic installer — it needs a build
  from `agent-ix/quoin` main at or after `3e842ce`. The test is written and
  double-gated: it runs only when such a Quoin is on `PATH` *and*
  `QUOIN_INSTALL_ROUNDTRIP=1` says the operator's global module store may be touched.
- This is the one row that mutates state outside the repository, which is why the
  restore is in a `finally` and is itself a criterion (IT-002-SC-06).
