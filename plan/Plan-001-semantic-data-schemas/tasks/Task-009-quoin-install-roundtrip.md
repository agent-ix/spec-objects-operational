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

- **Blocked on operator consent, not on a build.** The Quoin on this machine is
  `0.23.1-2-g3e842ce` — exactly the revision IT-002 pins — so the build half of the
  original blocker is cleared. What remains is that the install writes to the
  machine-global `quoin module` store, so the test is double-gated and runs only
  when such a Quoin is on `PATH` *and* `QUOIN_INSTALL_ROUNDTRIP=1` says that store
  may be touched. No agent sets that variable on an operator's behalf; clearing this
  task is an operator action, not engineering work.
- This is the one row that mutates state outside the repository, which is why the
  restore is in a `finally` and is itself a criterion (IT-002-SC-06).
