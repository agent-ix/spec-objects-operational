---
id: SR-101
title: "Gap analysis — Plan-001 semantic data schemas"
type: SpecReview
analysis: gap-analysis
scope: "plan/Plan-001-semantic-data-schemas/, spec/tests.md, typespec/, scripts/, spec_objects_operational/, tests/"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-operational/Plan-001"
    type: reviews
  - target: "ix://agent-ix/spec-objects-operational/TM-001"
    type: references
---
# Gap analysis — Plan-001 semantic data schemas

## Summary

Audited `plan/Plan-001-semantic-data-schemas/` (eleven tasks), the `TM-001` Test
Matrix in `spec/tests.md` (67 Test Case rows) and the branch's implementation on
`spec/6-semantic-module-contract` at `8c7f4c2`. Ten of eleven tasks are `done`;
`Task-009` is `blocked` on an operator consent gate. All 67 matrix Test Case ids
carry a real `@pytest.mark.trace` tag that the engine binds to a test function,
`quire coverage` reports 125/125 rows backed with zero unbacked rows, zero status
lies and zero untracked symbols, and **none of the three trace-tag binding traps
was found**: no black-wrapped marker, no trace id on a non-binding symbol, and no
bare TC id in a comment or docstring that mints a trace on the next symbol.

## Verdict

**CONDITIONAL** — no high finding; four mediums and four lows. The single
incomplete task (`Task-009`) is `blocked` with a named, non-code blocker: the
`QUOIN_INSTALL_ROUNDTRIP=1` operator opt-in that guards a write to the
machine-global `quoin module` store. Under the strict gap-analysis rule any
blocked task reads FAIL; it is recorded as CONDITIONAL here because the blocker
is declared in the task, in `plan.md` and in the matrix's Test Environment
section, and clearing it is an operator action rather than engineering work.

## Findings

| ID      | Severity | Summary                                                                                                                                                                       | Refs                                                                          | Escape Cause                    |
| ------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------- |
| FND-001 | medium   | `Task-009` is `blocked` (P1, track C), so IT-002 and rows TC-036 and TC-091 hold no execution evidence; the tests exist and are tagged, but only the operator opt-in can run them | Task-009, IT-002, TC-036, TC-091                                              | correct-requirement-no-evidence |
| FND-002 | medium   | `Task-009`'s named blocker is stale: it says no released Quoin carries the semantic installer, but `quoin --version` on this machine is `0.23.1-2-g3e842ce` — the revision IT-002 pins — and the real gate is operator consent, as `spec/tests.md` already records | Task-009 Notes, spec/tests.md Test Environment                                | wrong-requirement               |
| FND-003 | medium   | `quire coverage` skips status classification (`status-column-matches-nothing`, `agent-ix/quoin#340`), so the complete-but-unbacked half of matrix verification is unmeasured on this branch; the 125/125 backed figure stands, the "no status lies" claim is unverified | spec/tests.md:66, agent-ix/quoin#340                                          | correct-requirement-no-evidence |
| FND-004 | medium   | `scripts/stage-npm.mjs --clean` deletes root-staged `manifest.yaml`, `schemas/` and `skeletons/` at `postpack`; FR-002 Behavior states only the copy half, so this destructive step owns no acceptance criterion and rides on TC-016, whose criterion FR-002-AC-7 speaks about tarball contents | scripts/stage-npm.mjs::--clean, FR-002-AC-7, TC-016                           | missing-requirement             |
| FND-005 | low      | `plan.md` checks StR-001 and FR-001 as `[x]` while the matrix marks both `🚧` (StR-001-VC-1/VC-2 and FR-001-AC-2..AC-4 need a running filament-core-service) — the plan doc overstates against its own matrix | plan.md Requirements Summary, StR-001, FR-001                                 | wrong-requirement |
| FND-006 | low      | Two evidence-plan documents are absent — no `SuiteRegistry` and no `Inspections` document — so TC-005, TC-006, TC-007, TC-020, TC-036 and TC-091 have no declared evidence producer; `quire coverage` reports both as `archetype-matches-nothing` | TC-005, TC-006, TC-007, TC-020, TC-036, TC-091                                | missing-requirement             |
| FND-007 | low      | `quire validate --scope . "spec/**/*.md"` exits 0 with an empty stdout but 18 registry notices on stderr (`DuplicateModuleName` for this module at 2 paths, 13 `DuplicateArchetype`, 3 `DuplicateLexiconTerm`); the "zero warnings" claim holds for document diagnostics only, not for the module set the run assembled | quire validate stderr, spec_objects_operational/manifest.yaml                  | missing-requirement |
| FND-008 | low      | `catch-all-universal`: 6 of 7 criteria-binding documents name a specific property shape for none of their criteria (`specific_shaped` 1 of 58), so most acceptance criteria are not yet quantifiable by a generator — a `spec-correctness` handoff, not a coverage defect | spec/functional/FR-001-module-manifest-activates.md:39, coverage.specific_shaped | wrong-requirement |

## Coverage

- Reconciliation: `quire coverage` (quire 0.31.0, engine 0.46.0; module `spec-artifacts-process`) — engine path, not grep fallback.
- Tasks done: 10 / 11 (`Task-009` blocked; every `depends_on` of every `done` task is itself `done`).
- Rows backed by a tagged test: 125 / 125 (67 from `spec/tests.md`, 58 acceptance and validation criteria from the requirement documents); `unbacked_rows`, `status_lies` and `untracked_symbols` are all empty.
- Matrix Test Case ids reconciled by hand: 67 matrix rows, 67 distinct TC ids across 88 `@pytest.mark.trace` markers — the two sets are equal, with no row lacking a tag and no tag lacking a row.
- Symbol binding, from `quire symbols --scope .`: 167 extracted symbols, 88 tagged, 88 bound, every one a `test_*` function; no fixture, container, class or `conftest.py` symbol carries a trace.
- Trace-tag binding traps: none. (1) No marker is wrapped — all 88 are a single closed line, and commit `8c7f4c2` moved every marker adjacent to its `def`. (2) Every marker's bound symbol is the `def test_*` that follows it, allowing for an intervening `skipif` decorator; no marker binds a non-test symbol. (3) The bare ids in comments and docstrings all sit inside a function that already carries the matching marker, or in a module docstring or `conftest.py`, none of which minted a trace — `conftest.py` appears nowhere in the coverage report and all 17 of its extracted symbols are untagged.
- Gates re-run for this review: `make lint` green (ruff, black, 27 schemas match the committed output); `make test` 162 passed, 7 skipped, 3 xfailed, 100% coverage of the Python package; `quire validate --scope . "spec/**/*.md"` exit 0.
- Marker drift: none. The 7 skips are exactly the 7 rows marked `🚧` (TC-002..TC-006 need a running filament-core-service, TC-036 and TC-091 need the operator opt-in); the 3 xfails are the three declared expected failures (TC-035, TC-054, TC-081), each naming its blocking issue.
- Untraced behaviors / stubs: 1 untraced behavior (FND-004); 0 stubs. `spec_objects_operational/__init__.py` is a resource-path module owned by FR-001/TC-001; `scripts/generate-schemas.mjs` maps behavior-for-behavior onto FR-002 including the Node 20 guard and the normalization record; `scripts/build_tools.py` and the untouched Makefile targets are pre-existing cookiecutter golden-path scaffolding outside this plan's diff.
- Semantic review: skipped (not requested).
