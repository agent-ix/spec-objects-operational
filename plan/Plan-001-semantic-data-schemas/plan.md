---
id: Plan-001
title: "spec-objects-operational — semantic data schemas (issue #6)"
type: Plan
status: active
relationships:
  - target: ix://agent-ix/spec-objects-operational/StR-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/US-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/FR-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-operational/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-operational/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-operational/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-operational/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/IT-001
    type: references
  - target: ix://agent-ix/spec-objects-operational/IT-002
    type: references
---
# Implementation Plan: semantic data schemas

## Requirements Summary

### Stakeholder Requirements
- [x] **StR-001**: Operational specifications yield extractable graph entities; every operational object carries one typed structural contract downstream frontends can read, and a standing definition is distinguishable from an observed execution without reading the prose (VC-1..VC-3).

### User Stories
- [x] **US-001**: Declare every operational object type against the shared semantic-core grammar, so one declaration record per object validates identically in Quire, Quoin and the compiler, and operational evidence is referenced rather than duplicated.

### Functional Requirements
- [x] **FR-001**: The manifest conforms to the FR-035 module-manifest schema and activates idempotently; the registered `data_schema` is the reference object as posted.
- [x] **FR-002**: Emit one JSON Schema 2020-12 document per model from `typespec/main.tsp` with the official `@typespec/json-schema` emitter at a pinned toolchain; normalize `$id`/`$ref`; gate drift; package the schemas into the wheel and the npm tarball; version-embedded `$id` with an atomic bump procedure.
- [x] **FR-003**: `manifest.yaml` at version 0.3.0 carries the quoin FR-070 `semantic` block and a reference-form `data_schema` (path + digest) per exported object type, with every 0.2.0 locator, the `configuration-scope` lint rule and the lexicon term set unchanged.
- [x] **FR-004**: One role-distinct model per operational object type — required, forbidden and item rules — separating the seven standing definitions from the one observed execution, with a single canonical `evidence` mapping and every grammar item by `$ref` to semantic-core 0.1.0.
- [x] **FR-005**: Every skeleton is an executable typed fixture in the quoin FR-071/FR-072 Markdown forms, with three `sysml` alternates and ten negative fixtures; the semantic suite fails rather than skips when the engine is absent.

### Non-Functional Requirements
- [x] **NFR-001**: Additive compatibility — the checked-in 0.2.0 skeleton set still validates at 0.3.0, every 0.2.0 locator definition and lint rule is unchanged, the lexicon term set is intact, and each required 0.2.0 section yield is byte-identical.

### Integration Test Requirements
- [ ] **IT-001**: Activation roundtrip against a running filament-core-service (environment-gated).
- [ ] **IT-002**: `quoin module install path:<dir>` accepts the semantic contract and the prior module state is restored unconditionally (blocked on a Quoin carrying the semantic installer).

## Dependency Graph

### Core dependency edges
- `FR-002 (toolchain half) -> FR-004`
  Reason: the models cannot be authored until `tsp compile` runs against `@agent-ix/semantic-core` 0.1.0 and the generator normalizes what it emits.
- `FR-004 -> FR-002 (emitted-set half)`
  Reason: FR-002-AC-1/AC-2/AC-3 assert the emitted file set, its `$id`s and its `$ref`s, none of which exist before FR-004 declares the models. The apparent cycle is broken by splitting FR-002 into an enablement half (generator, drift gate, packaging) that precedes FR-004 and an emitted-set half that follows it.
- `FR-002 (emitted set) + FR-001 -> FR-003`
  Reason: the manifest references the emitted files by path and digest, and the 0.3.0 manifest must still be an FR-035-valid manifest.
- `FR-003 + FR-004 -> FR-005`
  Reason: a skeleton validates only once the archetype loads with its schema, and the negative fixtures pin refusals the FR-004 rules define.
- `FR-005 -> FR-003 (added locators)`
  Reason: the `required: false` locators the manifest gains exist to assert sections the skeletons introduce, so the section lands before its locator.
- `FR-003 + FR-005 -> NFR-001`
  Reason: the compatibility metrics compare 0.2.0 locators, lint rules, lexicon terms and skeletons against the finished 0.3.0 manifest and its loader behaviour.
- `FR-003 -> IT-002`
  Reason: the Quoin install exercises the finished `semantic` block and digests.
- `FR-003 -> FR-001 / IT-001 (re-verification)`
  Reason: the manifest changed, so activation must be re-verified against the pinned schema revision.

### Shared dependencies
- **The generator** (`scripts/generate-schemas.mjs`) is the single writer of
  `spec_objects_operational/schemas/` and of `manifest.yaml`'s `data_schema.digest`
  values. It is needed by FR-002, FR-003, FR-004 and NFR-001; it is extracted as
  Task-001 and no other task writes those bytes.
- **The Quire test harness** (module registry construction, `validate_document`,
  `extract_semantic`, the hard-fail-on-missing-engine rule) is needed by FR-003,
  FR-004, FR-005 and NFR-001; it is extracted as Task-007.
- **The 0.2.0 baseline** (a checked-in copy of the 0.2.0 `body_extraction`, the 0.2.0
  `lint_rules`, the 0.2.0 lexicon term set and the eight 0.2.0 skeletons) is needed by
  FR-003-AC-3/AC-7/AC-8 and by all four NFR-001 criteria; it is captured once in
  Task-007 and read by Task-004 and Task-008.

### Cross-cutting constraints
- `NFR-001` applies to every write to `manifest.yaml`'s `body_extraction`,
  `lint_rules` and `lexicon`, and to the skeleton rewrite: a locator may be added
  (`required: false`) but never changed, and no lexicon term may be removed or renamed.
- `FR-004-CON-3`/`CON-4`/`CON-5` (one `evidence` key, no observation key, no occurrence
  row on a standing definition) apply to every model in `typespec/main.tsp`.
- `FR-002-CON-1` (official emitter only, no hand-edited emitted file) applies to every
  byte under `spec_objects_operational/schemas/`.
- `FR-002-CON-2`/`CON-4` (no `.npmrc`, no `file:`/`link:`, exact pins, npm.ix only for
  `@agent-ix/semantic-core`) apply to `package.json` and `package-lock.json`.
- `FR-005-CON-1` (no corpus repository and no vendored fixture edited) applies to the
  whole branch and is checked as a diff inspection.

### The seams

The module already ships `spec_objects_operational/manifest.yaml` (0.2.0, eight object
types, `data_schema: {type: object}` on every one, one advisory `configuration-scope`
lint rule and a 25-term FR-043 lexicon) and eight skeletons. This plan adds
`typespec/main.tsp` and `scripts/generate-schemas.mjs` beside the existing
`scripts/stage-npm.mjs`, which gains the `--clean` postpack half; `pyproject.toml`'s
`include` list gains `schemas/*.json`. The existing
`tests/test_skeletons_and_validate.py` holds the skeleton/locator parity assertions
and the "quire is intentionally NOT a dependency" skip that FR-005 replaces with a
hard failure — a skip that was hiding a broken locator lookup for `configuration`.

## Test Plan

### Unit Tests
- [x] **TC-001** (FR-001-AC-1): the manifest validates through `quire.validate_manifest` against the vendored FR-035 schema.
- [x] **TC-010** (FR-002-AC-1): the emitted set equals the twenty-seven files `toolchain.json` lists, with compiler and emitter 1.15.0 recorded.
- [x] **TC-011** (FR-002-AC-2): every shipped schema declares the 2020-12 `$schema` and an `$id` under the base whose version segment is read from `manifest.yaml`.
- [x] **TC-012** (FR-002-AC-3): every `$ref` resolves to a shipped sibling or to semantic-core 0.1.0.
- [x] **TC-022** (FR-002-CON-4): `package-lock.json` resolves every package from npmjs except `@agent-ix/semantic-core`.
- [x] **TC-023** (FR-002-AC-2): no test hard-codes the `$id` version segment.
- [x] **TC-027** (FR-002-AC-13): `make install` provisions the TypeSpec toolchain.
- [x] **TC-030** (FR-003-AC-1, FR-003-CON-1): the `semantic` block equals the nine admitted keys and `exports` equals the eight object-type names.
- [x] **TC-031** (FR-003-AC-2): every exported type's `data_schema` is the reference form and the referenced file hashes to the recorded digest.
- [x] **TC-032** (FR-003-AC-3): every 0.2.0 locator is unchanged against the checked-in baseline.
- [x] **TC-033** (FR-003-CON-2): every locator added after 0.2.0 is `required: false`.
- [x] **TC-037** (FR-003-AC-7, FR-003-CON-3): every lexicon definition is one whole scalar and the three issue #5 definitions carry their restored wording.
- [x] **TC-038** (FR-003-AC-8): the `configuration-scope` lint rule is unchanged.
- [x] **TC-040** (FR-004-AC-1): the eight object-type schemas differ pairwise in a required, forbidden or item rule; none is `type: object` only.
- [x] **TC-052** (FR-004-AC-13, FR-004-CON-1): no module schema redeclares a semantic-core model; every grammar item is a `$ref`.
- [x] **TC-065** (FR-005-AC-6): every skeleton's H2 set is asserted by the manifest and includes every `required: true` heading.
- [x] **TC-066** (FR-005-AC-7): every skeleton is placeholder-free with non-empty asserted sections.
- [x] **TC-067** (FR-005-AC-8): skeleton titles are distinct `Identifier`s outside `KernelScalar`, and `object` equals `type` in every frontmatter.
- [x] **TC-080** (NFR-001-AC-1): zero 0.2.0 locator or lint-rule definitions changed.
- [x] **TC-082** (NFR-001-AC-3): the 0.2.0 lexicon term set is intact and only the three issue #5 definitions differ, each by restoration.

### Integration Tests
- [x] **TC-013** (FR-002-AC-4): `make schemas-check` exits zero on the committed tree and non-zero naming a mutated schema or digest.
- [x] **TC-014** (FR-002-AC-5): a `@jsonSchema` base version differing from the manifest version fails the generator naming both.
- [x] **TC-015** (FR-002-AC-6): the built wheel and sdist contain every exported schema file.
- [x] **TC-016** (FR-002-AC-7): the packed npm tarball ships `manifest.yaml` beside `schemas/<Model>.json`.
- [x] **TC-017** (FR-002-AC-8, FR-002-CON-5): a coordinated version bump re-emits every `$id`/`$ref` with matching digests; half a bump fails the check.
- [x] **TC-018** (FR-002-AC-9): `make schemas-check` names a stale committed schema and writes nothing.
- [x] **TC-019** (FR-002-CON-3): two generator runs over one source are byte-identical.
- [x] **TC-024** (FR-002-AC-10): the generator writes only under `schemas/` and only at `data_schema.digest`.
- [x] **TC-025** (FR-002-AC-11): `make lint` runs the drift gate.
- [x] **TC-034** (FR-003-AC-4): `quire.Registry.load_from` lists all eight archetypes and `validate_document` on every skeleton reports no `semantic.*` load failure.
- [x] **TC-035** (FR-003-AC-6): an unknown `semantic` key and an altered digest are each refused by the loader; the naming half is an expected failure on quire-rs#221 and #394.
- [x] **TC-041..TC-051, TC-053** (FR-004-AC-2..AC-14): the per-type positive and negative record fixtures — configuration identity refusal, migration safety clause, SLI unit, SLO objective, alert fields refusal, runbook operations, incident occurrence identity, deployment lifecycle, the empty record, the single `evidence` declaration, the unresolved placeholder, the occurrence-row ban.
- [x] **TC-054** (FR-004-AC-15): the three cross-key reader rules — a passing half asserting they are stated and expressible by no shipped schema, and a strict-xfail half asserting the refusal, blocked on quoin#335.
- [x] **TC-060** (FR-005-AC-1): every skeleton (eight plus three alternates) validates with no error.
- [x] **TC-061** (FR-005-AC-2, FR-005-CON-2): table and `sysml` skeletons extract to identical normalized fields with the recorded forms.
- [x] **TC-062** (FR-005-AC-3): under the skeleton bundle index every skeleton extracts with zero errors and zero unresolved tokens.
- [x] **TC-063** (FR-005-AC-4): availability states per skeleton match the type's declared set.
- [x] **TC-064** (FR-005-AC-5): every negative fixture fails with its `expect:` code and its `detail:` substring, and the ten named cases exist.
- [x] **TC-068** (FR-005-AC-9): the sli/slo skeletons extract a unit-bearing field and the incident skeleton an identity and a `Timestamp` field.
- [x] **TC-070** (FR-005-CON-2): a Properties section holding both a table and a fence is refused at the second form.
- [x] **TC-071** (FR-005-AC-10): with the engine absent the semantic rows fail rather than skip, naming the provisioning path.
- [x] **TC-083** (NFR-001-AC-4): each required 0.2.0 section yield is byte-identical under 0.2.0 and 0.3.0.

### Verification (NFRs)
- [x] **TC-081** (NFR-001-AC-2): every checked-in 0.2.0 skeleton validates under 0.3.0 with zero errors; the `object:`-declaring case is an explicit expected failure while `agent-ix/quire-rs#391` is open.

### Environment-gated and inspection rows
- [ ] **TC-002..TC-005** (FR-001-AC-2..AC-4, IT-001, StR-001-VC-1): activation, re-activation and registry reads against a running filament-core-service.
- [ ] **TC-006** (StR-001-VC-2): the generator demonstration.
- [x] **TC-007** (StR-001-VC-3): a standing definition and an observed execution are distinguishable by schema alone.
- [x] **TC-020** (FR-002-CON-1), **TC-021** (FR-002-CON-2), **TC-026** (FR-002-AC-12), **TC-069** (FR-005-CON-1), **TC-072** (FR-005-AC-11): inspections over the emitter path, the packaging surface, the line-ending pins, the branch diff, and the dependency groups.
- [ ] **TC-036, TC-091** (FR-003-AC-5, IT-002-SC-01..SC-06): the Quoin install roundtrip with unconditional state restore.

## Remaining Work

### Track A: Critical Path (serial)
- **A1 = Task-001** TypeSpec toolchain, generator and drift gate — Hard; exit: `make schemas` compiles and `make schemas-check` exits zero on the committed tree and non-zero on any mutation, stale file, or half-bumped version.
- **A2 = Task-002** The eight role-distinct models and nineteen support models — Hard; exit: each type accepts the records its role admits and refuses the records its role forbids, with every grammar item resolved by `$ref` to semantic-core.
- **Gate = Task-011** Migration, Sli and Incident end-to-end — measures whether the emitter's `contains`/`minContains`/`maxContains` recipe, the `@extension("allOf", …)` second predicate, and `unevaluatedProperties` survive the real 2020-12 validator for the zero-identity, unit-bearing and occurrence-identity rules; pass: all three accept their positive record and refuse their negatives. If it fails, the item-rule encoding is wrong and the remaining five types must not be authored against it.
- **A3 = Task-003** Emitted set, `toolchain.json`, digests and packaging — Medium; exit: twenty-seven schema files ship in the wheel and the npm tarball with digests the manifest agrees with.
- **A4 = Task-004** Manifest 0.3.0, `semantic` block, reference-form `data_schema`, lexicon repair — Medium; exit: Quire's loader lists all eight archetypes, refuses an unknown key or an altered digest, and issue #5's three truncated definitions are whole.
- **A5 = Task-005** Skeleton rewrite, three `sysml` alternates, ten negative fixtures — Hard; exit: every skeleton validates clean under the module and every negative fails for its named reason and detail.
- **A6 = Task-006** Added `required: false` locators for the sections the skeletons introduced — Easy; exit: every new section is asserted by the manifest and no existing artifact is invalidated.

### Track B: Parallel (independent agent, can start now)
- **B1 = Task-007** Test environment, provisioning and the 0.2.0 baseline — Medium; exit: the semantic suite fails loudly on a machine with no Quire and passes on one provisioned by `make dev-quire`; the 0.2.0 locators, lint rules, lexicon terms and skeletons are frozen as a fixture.
- **B2 = Task-010** FR-001 / StR-001 re-verification and trace tags — Easy; exit: the manifest still activates and every pre-existing test carries a trace tag that `quire coverage` binds.

### Track C: Post-critical-path
- **C1 = Task-008** NFR-001 additive-compatibility verification — Medium; exit: no 0.2.0 locator, lint rule or lexicon term changed except the three restorations, each required section yield is byte-identical, and the one blocked criterion is an expected failure naming its issue rather than a skip.
- **C2 = Task-009** IT-002 Quoin install demonstration — Medium; exit: the module installs, is listed, and the operator's prior module state is restored whether or not the install succeeded.

## Parallel Execution Summary

```
Track A  A1 ─── A2 ─── [Gate] ─── A3 ─── A4 ─── A5 ─── A6 ──┐
                                                            ├── C1
Track B  B1 ────────────────────────────────────┐           └── C2
         B2 ─────────────────────────(after A4)─┘
```

Track B starts immediately and independently of A1: neither the provisioning target
nor the 0.2.0 baseline touches the generator or the models. B2's re-verification half
waits on A4 because it re-posts the changed manifest. Track C begins once A6 lands.

## Task File Mapping

| Task     | Track | Owns (references)        | Verified by (verifies)                                | Status      |
| -------- | ----- | ------------------------ | ----------------------------------------------------- | ----------- |
| Task-001 | A     | FR-002                   | TC-013, TC-014, TC-017, TC-018, TC-019, TC-020, TC-024 | done |
| Task-002 | A     | FR-004, US-001           | TC-040…TC-054                                          | done |
| Task-011 | Gate  | FR-004                   | TC-042, TC-043, TC-047                                 | done |
| Task-003 | A     | FR-002                   | TC-010, TC-011, TC-012, TC-015, TC-016, TC-025, TC-026 | done |
| Task-004 | A     | FR-003                   | TC-030, TC-031, TC-032, TC-034, TC-035, TC-037, TC-038 | done |
| Task-005 | A     | FR-005, US-001           | TC-060…TC-070                                          | done |
| Task-006 | A     | FR-003, FR-005           | TC-033                                                 | done |
| Task-007 | B     | FR-005, FR-002           | TC-021, TC-022, TC-023, TC-027, TC-069, TC-071, TC-072 | done |
| Task-008 | C     | NFR-001                  | TC-080, TC-081, TC-082, TC-083                         | done |
| Task-009 | C     | FR-003, IT-002           | TC-036, TC-091                                         | blocked |
| Task-010 | B     | FR-001, StR-001          | TC-001…TC-007                                          | done |

## Quality Gates

1. **Gate (Task-011), before the remaining five types.** The item-rule encoding must
   survive the real 2020-12 validator, not just `tsp compile`. Passed on the first
   attempt.
2. **`make lint` before every push.** Runs ruff, black and the schema drift gate, so a
   `typespec/` edit that was never regenerated fails before review.
3. **`quire validate --scope . "spec/**/*.md"` structurally clean.** Warnings are
   acceptable; `failed structural validation` is not.
4. **`quire coverage --scope .` with zero unbacked rows.** A matrix row without a
   tagged symbol is not coverage.
5. **No skipped semantic row.** The engine is a hard dependency of the semantic tests
   (FR-005-AC-10); the only exemptions are the three named expected failures and the
   environment-gated non-semantic rows.
