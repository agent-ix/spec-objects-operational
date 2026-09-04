---
id: SR-100
title: "Code review — spec-objects-operational issue #6 semantic data schemas"
type: SpecReview
analysis: code-review
scope: "typespec/, scripts/, spec_objects_operational/, tests/"
review_set: subset
---
# Code review — spec-objects-operational issue #6 semantic data schemas

## Summary

Reviewed the 115-file diff of `spec/6-semantic-module-contract` against
`origin/main`: the TypeSpec source and its 27 emitted schemas, the schema
generator and drift gate, the 0.3.0 manifest, the eleven skeletons, the ten
negative fixtures, and the twelve test modules. `make lint` and `make test`
are green (162 passed, 7 skipped, 3 strict xfails, 100% branch coverage of the
Python package), `quire validate --scope . "spec/**/*.md"` is structurally
clean with zero warnings, and `quire coverage --scope .` reports 125/125 rows
backed with zero unbacked rows and zero untracked symbols.

## Verdict

**CONDITIONAL** — no high finding. Six mediums and lows, all recorded; two are
inherited from the sibling module's generator and one is an upstream engine
constraint this module records rather than works around.

## Findings

Two mediums were fixed in this branch rather than carried; the rows say so.


| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | `readIfPresent` mapped every read failure to "file absent", so a `PermissionError` or an `EISDIR` on a committed schema was reported by `--check` as a content difference rather than as the real cause. **Fixed**: both catches now match `ENOENT` and rethrow the rest. | scripts/generate-schemas.mjs:243 |
| FND-002 | medium | `test_the_npm_tarball_ships_the_schemas_beside_the_manifest` unconditionally `rmtree`s `REPO_ROOT/schemas` and `REPO_ROOT/skeletons` in its `finally`. Correct today — those paths hold only the pack-time staged copies, and the test asserts they are absent before packing — but the guard is an assertion at the top rather than a check inside the cleanup. **Fixed**: the pre-existing set is captured before the pack and the cleanup skips anything that was already there. | tests/test_schema_emission.py:281 |
| FND-003 | medium | `test_the_three_cross_key_reader_rules_are_refused` is a strict xfail because JSON Schema cannot relate one key of a record to another. FR-004-AC-15 therefore has one passing half (the rules are stated and expressible by no shipped schema) and one expected-failure half. The refusal itself has no evidence until `agent-ix/quoin#335` lands. Recorded, not worked around; the schema is not relaxed to fake it. | tests/test_role_schemas.py:390, FR-004-AC-15 |
| FND-004 | low | `test_engine_provisioning` patches `builtins.__import__` and `sys.modules`. That is Python's import machinery, not a third-party edge — but the behaviour under test *is* the absence of a third-party package, and no other seam exposes it. `monkeypatch` restores both. No change. | tests/test_engine_provisioning.py:32 |
| FND-005 | low | The repository's tests are module-level functions, not `class TestFeature` classes, and their docstrings carry prose rather than an Assumptions/Criteria block. This is the shape the sibling module `agent-ix/spec-objects-business` established for these Filament object modules and that `quire coverage` binds through `@pytest.mark.trace`; the repo idiom outranks the generic Python lane. No change. | tests/ |
| FND-006 | low | Seven rows skip rather than run: four need a running `filament-core-service` and three a Quoin built from `agent-ix/quoin` main. None is a semantic row — those fail rather than skip (FR-005-AC-10, asserted by TC-071) — and each `skipif` reason names the missing environment and the matrix row that stays `🚧`. Recorded so the gap analysis does not read them as this issue's debt. | tests/test_activation_and_stakeholder.py:44, tests/test_quoin_install_roundtrip.py:30 |

## Checks Run

| Check | Result |
|---|---|
| Test standards | Function-style tests per the repo idiom (FND-005); `pytest` throughout; no database interaction. |
| Mock compliance | No `unittest.mock`, no `@patch`, no `mocker.` anywhere. The only patching is `monkeypatch` over the import machinery (FND-004). |
| Completeness (source) | No `TODO`/`FIXME`/`XXX` outside the placeholder-token list a test asserts against. No stub module, no placeholder return, no empty class. The generator is 320 lines of real logic; `typespec/main.tsp` declares 27 models. |
| Completeness (tests) | No empty test, no `pytest.skip` inside a body, no import-only test. The one bare `pass` is a two-line stub class standing in for an engine that lacks `extract_semantic` — the object under test. |
| Integrity | Coverage threshold unchanged at `--cov-fail-under=100` and met. `filterwarnings = ["error"]` unchanged. No `pragma: no cover` added except one on an unreachable detached-clone branch, which the sibling carries too. |
| Spec-code faithfulness | Every FR-002..FR-005 and NFR-001 criterion has a test that asserts the criterion's own claim; the four criteria that cannot be asserted today are three strict xfails and one environment-gated demonstration, each naming its blocking issue. |
| Code-test alignment | Rows over keys the extractor does not populate are verified against hand-built JSON records and say so in their docstrings; no row claims extraction evidence it does not have. |
| Edge cases | Input validation: the generator refuses a failed compile, an empty emitted set, Node < 20, and a half-bumped version, each without touching committed output. Boundaries: zero/one identity field, unit present/absent, empty/one-item arrays, the empty record. Resource: the compile scratch directory is removed in a `finally`. |

## Gap Analysis

Two behaviours exist in the change with no owning requirement, and both are
now owned:

- **`make install` running `npm ci`.** `make lint` chains `make schemas-check`,
  which needs a TypeSpec toolchain nothing provisioned. Added as FR-002-AC-13
  with TC-027 rather than left as an undeclared convenience.
- **The bundle-index identity rule.** The three `sysml` alternates share an
  `id` and `title` with their table skeletons by intent, and the resolver
  matches entries rather than distinct ids, so a per-file index raises
  `semantic.ambiguous-type`. Stated in FR-005 Behavior rather than left as a
  fixture detail.

Two defects found in neighbours were filed rather than absorbed:

- `agent-ix/filament-core-service#26` — three divergent copies of the FR-035
  module-manifest schema; the service's own admits neither the `semantic`
  block nor the `lexicon` block, so this manifest cannot validate against it.
  The pin names the copy Quoin and Quire actually load.
- `agent-ix/quoin#340` — `quire coverage` skips status classification because
  its declaration reads `Status` while the `TestMatrix` archetype asserts
  `Coverage Status`. It affects `agent-ix/spec-objects-business` identically.

One defect was found *by* the change and fixed in place: replacing the
`pytest.skip` in `tests/test_skeletons_and_validate.py` with a hard failure
immediately surfaced a broken locator lookup — the `configuration` branch read
`after_heading` from a `table_row` locator, which names its heading with
`under_section`. The row had been passing as a skip since the file was
written. That is the FR-005-AC-10 rule earning its place.


## Dispositions

| Finding | Disposition |
|---|---|
| FND-001 | Applied: `readIfPresent` and the `readdirSync` guard now match `ENOENT` only and rethrow every other error. |
| FND-002 | Applied: the npm-pack cleanup captures the pre-existing staged set and removes only what the pack created. |
| FND-003 | Recorded as an explicit expected failure naming `agent-ix/quoin#335`; the schema is not relaxed and the row is not skipped. |
| FND-004..FND-006 | Recorded, no change. |

## Findings Raised by the Peer Reviews and Applied Here

The eight-analysis spec review ran against the landed code, not only the spec
text, and three of its findings were code-affecting:

- **SR-006 FND-200 (high, failure-domain)** — purity was enforced over record
  *keys* only, so a `Migration` could declare `applied_at: Timestamp` and be an
  observed execution wearing a standing definition's schema. Fixed in
  `typespec/main.tsp`: every standing definition that admits `fields` carries
  an `allOf` clause banning occurrence rows (FR-004-CON-5, TC-053), with a
  tenth negative fixture pinning it. The unenforceable half — purity over field
  *names* — is now stated as unenforceable rather than claimed.
- **SR-004 FND-400 (high, dependency)** — `EvidenceRef.record` was a
  `SemanticId`, but quoin FR-059 identifies its records with a bare token, so
  the "mapping" could not name most of the family it mapped to. Fixed:
  `EvidenceRecordId` carries FR-059's own `$defs/identity` pattern and
  `EvidenceRecordShape` its own `record_shape` enum.
- **SR-005 FND-503 (medium, evidence)** — `@pytest.mark.xfail` sitting between
  a `@pytest.mark.trace` marker and its `def` made the binder skip the marker:
  `authoring.tag_rate` read 85/88 while all 88 symbols carried a tag. Fixed by
  moving each trace marker adjacent to its `def`; the rate is now 88/88.
