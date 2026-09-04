---
id: SR-005
title: "Evidence review of the issue #6 semantic module contract specification"
type: SpecReview
analysis: evidence
scope: "spec/functional/FR-001..FR-005, spec/non-functional/NFR-001, spec/stakeholder/StR-001, spec/integration/IT-001..IT-002, spec/tests.md"
review_set: all
---
# SR-005: Evidence review of the issue #6 semantic module contract specification

## Summary

Every `Verification` cell in FR-001..FR-005, every `Validation` cell in the
constraint and StR-001 tables, every NFR-001 `Method` cell, and every Test
Matrix `Type` was checked against the declared catalog in
`spec-artifacts-process/manifest.yaml` (33 method ids across the classes
`Analysis`, `Demonstration`, `Inspection`, `Test`; matrix `Type` vocabulary
with `no_source_symbol: [Eval, Manual, Inspection, Analysis]`). `quoin advise`
was run over the 60 obligations `quire coverage --json` derives (55 acceptance
criteria plus the 5 NFR-001 measurement rows): **2 mismatch, 0 uncatalogued,
0 inconclusive**. Context: agent-ix/spec-objects-operational#6.

Unlike the sibling `agent-ix/spec-objects-business#4`, this spec set has no
`uncatalogued-verification-method` diagnostic — every cell is a declared class
— and every obligation the advisor could see matched at least one applicability
rule. The engine's own findings are narrow: FR-002-AC-12 (`Inspection`) and
FR-003-AC-5 (`Demonstration`) are the two mismatches, and
`catch-all-universal` fires on 6 of 7 documents (`coverage.specific_shaped` is
1 of 58), so most `property-based-testing` recommendations name no property to
write.

What judgement adds is about the *shape of the evidence that exists*, not
about missing tests. This module is implemented: `quire coverage --scope .`
reports 125 of 125 minted targets backed and `make test` runs 162 passed,
7 skipped, 3 xfailed. Three things about that evidence disagree with the
declared methods. First, eight obligations are authored `Inspection` or
`Demonstration` — methods the catalog defines as producing no source symbol —
and every one of them is nevertheless discharged by a tagged pytest symbol that
shells out, diffs the tree, or greps a file. Second, three obligations are
discharged only by a strict-xfail, which is evidence that the system does *not*
satisfy the criterion, and the binder cannot read those three symbols at all
(`authoring.tag_rate` is 85 of 88 over 88 test definitions each carrying a
`@pytest.mark.trace` marker). Third, the five NFR-001 measurement rows are
obligations `quoin advise` carries and `minted_targets` does not, so the
module's only quantified thresholds sit outside the 125/125 denominator.

Two things were checked and found honest, and are recorded here rather than as
findings. The seven skips are all environment gates (`@needs_filament_core`,
`@needs_quoin`) backing the eight `🚧` rows — TC-004 and TC-005 share one
symbol — and none is a semantic test, so FR-005-AC-10's fail-not-skip rule is
not violated by them. And `tests.md` states plainly that 125/125 is a
traceability figure and not a pass rate, which is the distinction the rest of
this review turns on.

## Verdict

**CONDITIONAL** — the method vocabulary is clean and no obligation is
unverified for want of a test. What must be settled before the matrix is
treated as the verification contract is the eight rows whose authored method
says no source symbol can exist while a source symbol backs them (FND-500,
FND-501, FND-502), the three obligations whose only evidence is an expected
failure the binder cannot see (FND-503), and the five metric obligations
outside the coverage denominator (FND-504). The remaining findings are method
refinements and residue the author can accept or decline in the `Verification`
cell, which is the obligation's method (quire-rs FR-053).

Counts: 0 high, 6 medium, 4 low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|----|----------|---------|------|--------------|
| FND-500 | medium | FR-002-AC-12 is the advisor's first mismatch: authored `Inspection`, recommended `unit-testing`/`bdd-spec-by-example` on the `example` shape. The catalog defines `inspection` as "a person reads the artifact against the requirement and records a verdict — produces no source symbol, so it is discharged through the inspections registry rather than by a tagged test", and no inspections registry exists (FND-505). Meanwhile the criterion has a fully executable oracle (`.gitattributes` marks four globs `eol=lf`) and TC-026 already binds `tests/` symbols to it. Recommend `Test` in the cell and `unit-testing` (Unit) as the method; the matrix row should be typed `Unit` or `Static`, not `Inspection`. | FR-002-AC-12, TC-026 | wrong-requirement |
| FND-501 | medium | FR-003-AC-5 is the advisor's second mismatch: authored `Demonstration`, recommended `unit-testing`/`bdd-spec-by-example`. One obligation carries three different answers — the cell says `Demonstration`, matrix rows TC-036 and TC-091 are typed `Manual` (a `no_source_symbol` type), and the actual evidence is `tests/test_quoin_install_roundtrip.py`, two `@pytest.mark.integration @needs_quoin` functions with tagged trace ids that record, install, list, derive and restore exactly as IT-002 prescribes. The sibling `spec-objects-business` declined the equivalent finding (SR-005 FND-162) because no Quoin build carried the semantic installer; that reason no longer holds — the CLI on this machine reports `0.23.1-2-g3e842ce`, which is precisely the build IT-002 Preconditions pin. Recommend `Test` / `integration-testing` (Integration) and retype TC-036 and TC-091 `Integration`, leaving them `🚧` on the environment gate rather than on a method that forbids the symbol they have. | FR-003-AC-5, IT-002, TC-036, TC-091 | wrong-requirement |
| FND-502 | medium | Four more obligations are authored `Inspection` and discharged by an executable symbol: FR-002-CON-1 (TC-020 — asserts the generator shells out to the official compiler), FR-002-CON-2 (TC-021 — reads `package.json` and the tree for `.npmrc`, `file:`/`link:`, bounds), FR-005-CON-1 (TC-069 — runs a branch diff against `main`), FR-005-AC-11 (TC-072 — greps `pyproject.toml` for a `quire` dependency). Only FR-005-AC-11 is not an advisor mismatch, and only because `inspection (no-executable-oracle)` was offered beside `unit-testing`; the judgement is the same for all four. Each has a decidable oracle over checked-in bytes, which is what disqualifies `no-executable-oracle`. Recommend `Test` / `unit-testing` (Unit or Static) for FR-002-CON-2, FR-005-CON-1 and FR-005-AC-11; FR-002-CON-1's second half ("no emitted file is hand-edited") is genuinely judgement and should keep `Inspection` — which then needs the registry FND-505 names. | FR-002-CON-1, FR-002-CON-2, FR-005-CON-1, FR-005-AC-11, TC-020, TC-021, TC-069, TC-072 | wrong-requirement |
| FND-503 | medium | Three obligations are discharged only by a strict-xfail, and the catalog carries no method that produces "expected failure" as evidence: FR-003-AC-6's naming half (quire-rs#221, quire-rs#394), FR-004-AC-15's refusal half (quoin#335), NFR-001-AC-2's `object:`-declaring legacy case (quire-rs#391). An xfail records that the system does *not* satisfy the criterion; the criterion is pinned, not verified, and the honest evidence state for each is `undischarged`. Worse, the binder cannot see those three symbols: `authoring.tag_rate` is 85 of 88 while `grep -c 'def test_'` and `grep -c '@pytest.mark.trace'` over `tests/` both return 88, and the census's `unbound_example` is `test_a_legacy_form_artifact_that_declares_its_object_is_not_an_error`, one of the three. Judgement, not a rule: the three unread markers are exactly the three symbols where `@pytest.mark.xfail` sits between `@pytest.mark.trace` and the `def`, so the "attached annotation block" read stops at the intervening decorator. The consequence is that TC-035, TC-054 and TC-081 read `✅` on the strength of their passing half alone, and deleting the xfail would move no published number. Recommend: keep the xfails, record the three obligations as `undischarged` when the evidence store lands, and file the decorator-order binding gap against quire-rs. | FR-003-AC-6, FR-004-AC-15, NFR-001-AC-2, TC-035, TC-054, TC-081 | correct-requirement-no-evidence |
| FND-504 | medium | The five NFR-001 measurement rows are obligations with a `Method` cell (`Test`) that no coverage row and no test tag reaches. `quoin advise` carries NFR-001-M-1..M-5; `minted_targets` holds 125 entries and the only NFR ids among them are NFR-001-AC-1..AC-4; `grep -rn 'NFR-001-M' tests/ spec/` returns nothing. So the module's only quantified thresholds (`0` locators changed, `0` lint rules changed, `0` terms removed, `0` error findings, yields `identical`) are outside the 125/125 denominator entirely, and the advisor's per-metric recommendation is advice on obligations nothing can discharge. NFR-001-AC-1..AC-4 restate four of the five in prose — AC-1 covers M-1 and M-2 together, so there is no one-to-one mapping — but no id links them. Recommend either tagging the metric ids directly in `tests/test_additive_compatibility.py` beside the AC ids, or stating in NFR-001 Verification which acceptance criterion discharges which metric row, so the five obligations stop being invisible. | NFR-001, NFR-001-AC-1, NFR-001-AC-2, NFR-001-AC-3, NFR-001-AC-4, TC-080, TC-081, TC-082, TC-083 | correct-requirement-no-evidence |
| FND-505 | medium | The evidence store does not exist, and this analysis is what it costs. `quire coverage` reports `archetype-matches-nothing` for both the `suite` (`SuiteRegistry`) and `inspection` (`Inspections`) declarations — base.md FND-014 records the absence; recorded here are the three consequences for method selection. (a) No obligation is *discharged*, only *bound*: `quoin evidence` has no `suites.md`, no `bindings.json` and no run records, so there is no artifact of record for any of the 125 rows and the `✅` markers rest on a local `make test` nobody transcribed. (b) No `fault-detection-unmeasured` or `fault-detection-failed` characteristic can mint, because both are read from the evidence store — which is why `mutation-testing` was recommended for none of the 60 obligations, and why nothing in this repository says whether its 88 tests would catch a seeded fault. (c) The eight `Inspection`/`Manual` rows of FND-500, FND-501 and FND-502 have no registry to be discharged through if the author keeps those methods, which makes retyping them the cheaper of the two fixes. This is a gap in the plan, not in the spec. | TM-001, FR-002-CON-1, FR-002-AC-12, FR-003-AC-5, FR-005-AC-11 | correct-requirement-no-evidence |
| FND-506 | low | No obligation declares a criticality: `quoin advise --json` returns `criticality: null` for all 60. The two catalog rules keyed on `high-criticality` — `mutation-testing` (Static) and `concolic-execution` (Fuzz) — can therefore match nothing here, independently of the empty evidence store (FND-505), so the escalation ladder is unreachable by rule and reachable only by judgement. Judgement: FR-004-AC-1 ("each of the eight shipped schemas differs from every other in at least one required, forbidden, or item rule; a schema with only `type: object` is absent") is the module's central claim and the one place a fault-detection measurement pays — a mutant that relaxes one `contains` or drops one `required` should turn a test red. Recommend `mutation-testing` over the schema fixtures once a suite is recorded, taken *before* `concolic-execution`, which the advisor would tie with it on rule count and which nobody should reach for first (cost ordering, `agent-ix/quire-rs#190`). | FR-004-AC-1, FR-004-CON-2, FR-004-CON-5 | correct-requirement-no-evidence |
| FND-507 | low | Advisor residue, recorded as judgement rather than verdict. The `universal` catch-all drove roughly twenty `property-based-testing` recommendations: `coverage.specific_shaped` is 1 of 58 (the one specific shape is FR-004-AC-10's `invariant`) and `catch-all-universal` fires on 6 of 7 documents, so on those rows the advisor is saying "I could not tell you what to write", not "write a property test"; the authored `Test` stands. Named misfires the author should not follow: `dast`/`iast` (security) on FR-004-AC-11 and FR-005-AC-7 — a schema refusing an out-of-set `kind` and a skeleton having no placeholder token are not an attack surface; `fuzzing` (parser) on FR-003-AC-7 and NFR-001-AC-3 — the lexicon is authored YAML compared against a baseline, not an input surface; `demonstration` (stakeholder-acceptance) on FR-004-AC-12; `model-checking`/`runtime-monitoring` (temporal) on FR-002-AC-8 — the version bump is a two-file atomic edit, not a temporal property; `performance-benchmarking` (quantified-threshold) on all five NFR-001 metrics — the targets are `0` and `identical`, not latency or throughput. 0 obligations were inconclusive. | FR-004-AC-11, FR-005-AC-7, FR-003-AC-7, NFR-001-AC-3, FR-004-AC-12, FR-002-AC-8, NFR-001 | wrong-requirement |
| FND-508 | low | Four recommendations worth taking rather than setting aside, each sharpening the evidence kind the suite must produce. FR-002-AC-10 was recommended `golden-approval-testing` (Snapshot) on `stable-output` and the criterion is literally a whole-tree byte comparison ("every other tracked file is byte-identical afterwards"); TC-024 is typed `Integration`, and `Snapshot` names what it actually holds. FR-005-AC-2 (table and `sysml` skeletons extract to identical normalized `fields`) is the catalog's definition of `metamorphic-testing` (Property) — a relation between the outputs of two related executions with no independent oracle for either; the advisor offered `combinatorial-tway` on the same row and neither is the authored class's fault, but `metamorphic-testing` is the more specific reading. FR-004-AC-2 and FR-004-AC-14 were recommended `combinatorial-tway` (Property) on `configuration-matrix`, which is right: the purity rule is a matrix of 8 object types against 3 field kinds (identity, occurrence, measured) and the criteria enumerate a hand-picked subset. FR-002-CON-3 (two generator runs byte-identical) is not an obligation the advisor sees, and is `golden-approval-testing` or `metamorphic-testing` rather than the bare class `Test`. | FR-002-AC-10, FR-005-AC-2, FR-004-AC-2, FR-004-AC-14, FR-002-CON-3, TC-019, TC-024, TC-053, TC-061 | wrong-requirement |
| FND-509 | low | `coverage.implements` is 0 of 79: no implementation symbol in the module carries an `implements` trace to any requirement, so the reverse direction is unmeasured. The forward direction is complete — every obligation has a test — but nothing in the evidence programme can answer "what code exists that no requirement owns", which is the question that finds underspecified behaviour in `scripts/generate-schemas.mjs` and `spec_objects_operational/`. Not a matrix gap and not a blocker for issue #6; recorded so the 125/125 figure is not read as bidirectional traceability. | TM-001 | correct-requirement-no-evidence |

## Method recommendations per obligation

Only obligations whose authored method should change or be sharpened are
listed. The 45 acceptance criteria authored `Test` whose advisor
recommendation is a `Test`-class method match at class level and need no edit.

| Obligation | Authored | Advisor | Recommended | Basis |
|---|---|---|---|---|
| FR-002-AC-12 | Inspection | unit-testing, bdd-spec-by-example (mismatch) | `unit-testing` (Unit) | rule + judgement: decidable oracle over `.gitattributes`, TC-026 already binds a symbol |
| FR-003-AC-5 | Demonstration | unit-testing, bdd-spec-by-example (mismatch) | `integration-testing` (Integration) | judgement: CLI across a real filesystem boundary, exit-code oracle, restore is fixture work |
| FR-002-CON-2 | Inspection | not an obligation (constraint) | `unit-testing` (Unit) | judgement: executable over `package.json` and the tree |
| FR-005-CON-1 | Inspection | not an obligation (constraint) | `unit-testing` (Static) | judgement: TC-069 runs a branch diff |
| FR-005-AC-11 | Inspection | inspection, unit-testing, bdd-spec-by-example | `unit-testing` (Unit) | judgement: TC-072 greps `pyproject.toml`; `no-executable-oracle` does not hold |
| FR-002-CON-1 | Inspection | not an obligation (constraint) | `inspection` (Manual) for the hand-edit half, `unit-testing` for the emitter half | judgement: split obligation |
| FR-002-AC-10 | Test | golden-approval-testing, property-based-testing | `golden-approval-testing` (Snapshot) | rule: `stable-output`; whole-tree byte diff |
| FR-002-CON-3 | Test | not an obligation (constraint) | `golden-approval-testing` or `metamorphic-testing` | judgement: two runs byte-identical |
| FR-005-AC-2 | Test | bdd-spec-by-example, combinatorial-tway, unit-testing | `metamorphic-testing` (Property) | judgement: relation between two executions, no independent oracle |
| FR-004-AC-2, FR-004-AC-14 | Test | combinatorial-tway, property-based-testing | `combinatorial-tway` (Property) | rule: `configuration-matrix` over type × field kind |
| FR-004-AC-1 | Test | property-based-testing (universal) | `unit-testing` plus `mutation-testing` (Static) once a suite is recorded | judgement: discrimination claim needs a fault-detection measurement (FND-506) |
| FR-001-AC-4 | Test | golden-approval-testing, property-based-testing | `integration-testing` (Integration) | judgement: registry reads across a real HTTP boundary after activation |
| NFR-001-M-1..M-3, M-5 | Test | performance-benchmarking (misfire) | `golden-approval-testing` (Snapshot) | judgement: baseline diffs against the checked-in 0.2.0 copy |
| NFR-001-M-4 | Test | performance-benchmarking (misfire) | `integration-testing` (Integration) | judgement: Quire validates the legacy skeleton under 0.3.0 |
| FR-003-AC-6, FR-004-AC-15, NFR-001-AC-2 | Test | (various) | method unchanged; evidence state `undischarged` | judgement: an expected failure discharges nothing (FND-503) |

## Suite plan implied

The methods above imply these evidence kinds. No `SuiteRegistry` declares a
producer for any of them and no `Inspections` document exists (FND-505); the
rows below name what those documents would have to declare.

- `Unit` (pytest over `spec_objects_operational/`, `schemas/`, `manifest.yaml`, `package.json`, `pyproject.toml`): FR-002-AC-1..AC-3, FR-002-AC-12, FR-002-CON-2, FR-003-AC-1..AC-3, FR-003-AC-7, FR-003-AC-8, FR-004-AC-1, FR-004-AC-13, FR-005-AC-6..AC-8, FR-005-AC-11, NFR-001-AC-1, NFR-001-AC-3.
- `Integration` (pytest with the Quire wheel from `make dev-quire`): FR-002-AC-4..AC-9, FR-002-AC-11, FR-002-AC-13, FR-003-AC-4, FR-003-AC-6, FR-004-AC-2..AC-12, FR-004-AC-14, FR-005-AC-1, FR-005-AC-3..AC-5, FR-005-AC-9, FR-005-AC-10, FR-005-CON-2, NFR-001-AC-2, NFR-001-M-4.
- `Integration` (environment-gated, currently `🚧`): FR-001-AC-2..AC-4 and IT-001 need a running `filament-core-service` at `a77f31e`; FR-003-AC-5 and IT-002 need the Quoin build at or after `3e842ce` (FND-501).
- `Snapshot` (checked-in 0.2.0 baseline under `tests/fixtures/baseline-0.2.0/`): NFR-001-AC-4, NFR-001-M-1..M-3, M-5, FR-002-AC-10, FR-002-CON-3.
- `Property` (metamorphic and combinatorial): FR-005-AC-2, FR-004-AC-2, FR-004-AC-14.
- `Static` (fault-detection measurement over the schema fixtures, once a suite is recorded): FR-004-AC-1, FR-004-CON-2, FR-004-CON-5 (FND-506).
- `Manual` via an inspections registry: FR-002-CON-1's hand-edit half, StR-001-VC-2, and FR-003-AC-5 / FR-002-AC-12 / FR-005-AC-11 / FR-002-CON-2 / FR-005-CON-1 only if their authored method is kept.

## Diagnostics consulted

From `quoin advise` and `quoin advise --json` (quoin `0.23.1-2-g3e842ce`) over
60 obligations: 2 `mismatch` (FR-002-AC-12, FR-003-AC-5), 0 `uncatalogued`,
0 `inconclusive`, `criticality: null` on all 60.

From `quire coverage --scope . --json` (quire 0.31.0, engine 0.46.0@ca7362d4):
`coverage.backed` 125 of 125 over 88 examined evidence symbols with 85
matched; `authoring.tag_rate` 85 of 88; `coverage.property_shaped` 31 of 58;
`coverage.specific_shaped` 1 of 58; `coverage.no_symbol_rows` 0 of 125;
`coverage.implements` 0 of 79; `minting.section_hit_rate` 8 of 8;
`unbacked_rows` empty; `status_lies` empty; `untracked_symbols` empty. Four
diagnostics: `status-column-matches-nothing` (`functional-coverage`, already
base.md FND-008 and `agent-ix/quoin#340`), `archetype-matches-nothing` twice
(`SuiteRegistry`, `Inspections`), `catch-all-universal` (6 of 7 documents).
Binding census: 88 Python candidates, 85 tagged, 85 bound, unbound example
`tests/test_additive_compatibility.py:91`.

From `quoin catalog methods`: 33 methods across `Analysis`, `Demonstration`,
`Inspection`, `Test`; `no_source_symbol: [Eval, Manual, Inspection, Analysis]`
in `traceability.vocabularies.test_type`, with `Demonstration` deliberately
excluded because a demonstration is observed running and can carry a symbol.

## Proposed Dispositions

No spec artifact and no implementation file was edited by this review. The
dispositions below are proposals for the author.

| Finding | Proposed disposition |
|---|---|
| FND-500 | Apply: set FR-002-AC-12 `Verification` to `Test` and retype TC-026 `Unit`. The oracle is decidable over checked-in bytes and the symbol already exists. |
| FND-501 | Apply: set FR-003-AC-5 `Verification` to `Test` and retype TC-036 and TC-091 `Integration`, leaving both `🚧` on the Quoin build gate. The sibling's reason for declining no longer holds. |
| FND-502 | Apply in part: retype FR-002-CON-2, FR-005-CON-1 and FR-005-AC-11 as `Test`; keep `Inspection` on FR-002-CON-1's hand-edit half and carry it to the inspections registry when one exists. |
| FND-503 | Apply the disclosure, not a method change: keep the three strict-xfails, record the three obligations as `undischarged` rather than `✅` once the evidence store lands, and file the `@pytest.mark.xfail`-between-marker-and-`def` binding gap against `agent-ix/quire-rs` so the 85-of-88 tag rate is explained rather than tolerated. |
| FND-504 | Apply: state in NFR-001 Verification which acceptance criterion discharges each of M-1..M-5, or tag the metric ids alongside the AC ids in `tests/test_additive_compatibility.py`. Either closes the gap; leaving five obligations outside the denominator does not. |
| FND-505 | Carry to the plan, not to the spec. `tests.md` Coverage Gaps already publishes the two absent artifacts; the addition this finding asks for is that authoring `spec/evidence/suites.md` and `spec/evidence/inspections.md` is what turns 125 bound rows into 125 discharged obligations, and is the precondition for FND-506. |
| FND-506 | Record; act after FND-505. Declare a criticality on FR-004-AC-1 and run `mutation-testing` over the schema fixtures before considering any solver-based escalation. |
| FND-507 | Record, no change. The authored `Test` stands on every row named. |
| FND-508 | Author's choice. Each is a matrix `Type` sharpening rather than a class change; none of the four criteria is wrong as authored. |
| FND-509 | Record, no change for issue #6. The reverse direction belongs to the campaign's traceability work, not to this module's contract. |
