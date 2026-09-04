---
id: SR-002
title: "Integrity review of the #6 semantic module contract spec"
type: SpecReview
analysis: integrity
scope: "spec/spec.md, spec/stakeholder/StR-001-module-activation.md, spec/usecase/US-001-declare-operational-objects-against-semantic-core.md, spec/functional/FR-001-module-manifest-activates.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/non-functional/NFR-001-additive-compatibility.md, spec/integration/IT-001-manifest-activation-roundtrip.md, spec/integration/IT-002-quoin-module-install.md, spec/tests.md"
review_set: all
---
# SR-002: Integrity review of the #6 semantic module contract spec

## Summary

Integrity gate (completeness, consistency, atomicity/testability) over the
twelve artifacts that deliver `agent-ix/spec-objects-operational#6`, grounded
against the shipped `spec_objects_operational/manifest.yaml` (0.3.0), the 26
emitted schemas plus `toolchain.json`, the eleven skeletons, `package.json`,
`pyproject.toml`, the `Makefile`, `.gitattributes`, the repository's CI
workflows, and the sibling `agent-ix/spec-objects-business#4` integrity review
(SR-003), whose dispositions this spec has largely absorbed. Every referenced
neighbour issue was checked and exists open: `agent-ix/quoin#335`,
`agent-ix/quoin#340`, `agent-ix/quire-rs#221`, `#391`, `#392`, `#394`,
`agent-ix/filament-core-service#23`. No dangling issue reference was found.

Two conditions on reading this review. First, the artifacts were being edited
while it was written: `FR-001`, `FR-002`, `FR-004`, `FR-005`, `StR-001` and
`tests.md` changed at 14:22–14:24 as the base (SR-001) and failure-domain
(SR-006) dispositions were applied. Every finding below is grounded on the tree
as it stood after those edits, and several completeness gaps that were real
earlier in the review (no matrix row for `FR-004-AC-14`/`CON-5`; a
`TC-064` naming nine fixtures against an eleven-case rule) closed during it and
are **not** recorded as findings. Second, the peer reviews are now partly stale
against the text: SR-006 FND-200, FND-201 and FND-207, and SR-001 FND-001,
FND-002, FND-003, FND-005 and FND-006, read as applied.

Completeness now holds at the level the gate measures: every acceptance
criterion, named constraint and NFR metric of FR-001..FR-005 and NFR-001 has at
least one test case, and the traceability matrix below has no orphan criterion
and no orphan `TC`. `quire validate --scope . "spec/**/*.md"` exits 0.

Fifteen findings: no high, eight medium, seven low. The mediums cluster in three
places — the stakeholder layer still validates against artifacts the module does
not ship, the matrix's own status bookkeeping now contradicts the engine's
reading of the same tree, and three obligations added by the newest edits
arrived without an owning criterion.

## Verdict

**CONDITIONAL — the integrity gate passes; `spec-to-plan` may start once the
eight mediums are dispositioned.** No finding blocks tasking: FND-100, FND-104
and FND-108 are one-line edits, FND-101 and FND-113 are frontmatter, FND-102 and
FND-106 are matrix bookkeeping, and FND-103, FND-105 and FND-107 are one added
criterion each. Nothing here requires a schema, a rule or a gate to be relaxed.

## Traceability Matrix

Completeness deliverable: US → FR → StR → verification. "StR (via US)" means the
only stakeholder link is transitive through `US-001`.

| US | FR | StR | Verification (AC / CON → TC) | Gap |
|---|---|---|---|---|
| — | FR-001 | none in frontmatter; asserted in `tests.md` prose only | AC-1..4 → TC-001..TC-004; IT-001-SC-01..03 → TC-002..TC-004 | FND-101, FND-104 |
| US-001 | FR-002 | StR-001 (via US) | AC-1..9 → TC-010..TC-018; AC-2 → TC-023; AC-10..12 → TC-024..TC-026; CON-1 → TC-020; CON-2 → TC-021; CON-3 → TC-019; CON-4 → TC-022; CON-5 → TC-017 | FND-103, FND-108, FND-111 |
| US-001 | FR-003 | StR-001 (via US) | AC-1..4, AC-6..8 → TC-030..TC-032, TC-034, TC-035, TC-037, TC-038; AC-5 → TC-036; CON-1 → TC-030; CON-2 → TC-033; CON-3 → TC-037; IT-002-SC-01..06 → TC-091 | FND-110, FND-113 |
| US-001 | FR-004 | StR-001 (via US) | AC-1..15 → TC-040..TC-054; CON-1 → TC-052; CON-2, CON-4 → TC-049; CON-3 → TC-050; CON-5 → TC-053 | FND-105, FND-113 |
| US-001 | FR-005 | StR-001 (via US) | AC-1..9 → TC-060..TC-068; AC-10, AC-11 → TC-071, TC-072; CON-1 → TC-069; CON-2 → TC-070 | FND-107 |
| — | NFR-001 (constrains FR-003, FR-004, FR-005) | — | AC-1..4 → TC-080..TC-083, over the five declared metrics | FND-113 |
| StR-001-VC-1 | — | — | TC-005 (Demonstration) | environment-bound, SR-001 FND-013 |
| StR-001-VC-2 | — | — | TC-006 (Manual) | FND-100 |
| StR-001-VC-3 | — | — | TC-007 (Demonstration) | FND-106 |
| US-001-EX-1..3 (illustrative) | FR-002..FR-005 | — | TC-060, TC-049, TC-091 | FND-109 |

Every NFR is explicitly scoped (NFR-001 Scope names `manifest.yaml`, the shipped
schemas and the skeletons) and its `constrains` relationships name the three FRs
it bounds; the back-reference is one-directional (FND-113).

## Hidden Assumption Probes

| FR | Pattern | Result |
|---|---|---|
| FR-002 | Delegates to external CLIs (`node`, `tsp`) | Version floor (Node 20) and the user-facing error when absent are both stated; **provisioning is not** — `make install` runs Poetry only and no requirement obliges an `npm ci`, while `make lint` is required to run `make schemas-check` (FND-103) |
| FR-002 | Depends on a registry-scoped package (`@agent-ix/semantic-core` on npm.ix) | FR-002-CON-4 states the routing discipline and excludes the GitHub workflow; no rule states what a registry auth failure or an unreachable npm.ix produces (folded into FND-103) |
| FR-002 | Generation command | Build (`make schemas`) and check (`--check`) modes are both specified, `--check` is write-free, stale files are named. No interactive mode is needed. OK |
| FR-003 | Lookup over two consumers (Quire loader, Quoin installer) | No tie-break needed — both refuse; refusal granularity is stated per class and both silent-refusal defects are named (`quire-rs#221`, `#394`) with FR-003-AC-6's naming half carried as an expected failure. OK |
| FR-004 | Depends on an emitter capability | The decorator recipe is stated for every item rule, including the `@extension("allOf", …)` route for the two-`contains` cases, all official-emitter decorators under FR-002-CON-1. OK |
| FR-004 | References a record family not yet published (`agent-ix/quoin#267`) | Referenced by `SemanticId`, never resolved; the dangling-reference policy is SR-006 FND-206's, not restated here |
| FR-005 | Depends on a package version not on any committable index (Quire 0.46.0) | Fail-not-skip, `make dev-quire`, the `pyproject.toml` prohibition and the blocking issue are all stated and now carry FR-005-AC-10/AC-11; the version floor is unpinned (SR-006 FND-212) |
| FR-001 | Calls an external service with a changed payload | `spec.md` states the reference-form `data_schema` is stored verbatim until `filament-core-service#23` and attributes that assertion to FR-001-AC-4 and IT-001-SC-03 — neither of which mentions `data_schema`, and IT-001-SC-03 is the idempotency criterion (FND-104) |

## Failure Domain Check

Run against `spec-failure-domain-analysis` and deferred to SR-006 where it
already holds the ground: extension-point failure policy, entity identity,
evaluation purity and topological robustness are that review's fourteen
findings. Two items on this axis belong to the integrity gate and are recorded
here instead: the purity fix (SR-006 FND-200) arrived complete in FR-004 —
occurrence-row bans on all five standing definitions that admit `fields`,
FR-004-CON-5, FR-004-AC-14, TC-053 and a `migration-applied-timestamp` negative
fixture — but it left `US-001-EX-2` illustrating the superseded key-level
refusal (FND-109); and the cross-key reader rules (SR-006 FND-204, SR-001
FND-007) were dispositioned into FR-004-AC-15, a criterion that states no
required system behaviour (FND-105).

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-100 | medium | The stakeholder layer validates against templates the module does not ship: StR-001-VC-2 reads "the templates and schemas this module ships", the Rationale and Stakeholders paragraphs repeat it, and `spec.md` Purpose and Intended Users say "with their templates and schemas". The package ships `manifest.yaml`, `schemas/` and `skeletons/`; `manifest.yaml` contains no `template` key and no `templates/` directory exists. TC-006 (Manual, P2) therefore demonstrates a criterion over a non-existent artifact. The sibling module corrected the identical wording (SR-003 FND-130, "templates" → "skeletons and schemas"); the fix is not carried here. | StR-001-VC-2, StR-001 Rationale, StR-001 Stakeholders, spec.md Purpose, spec.md Intended Users, TC-006, `spec_objects_operational/` | wrong-requirement |
| FND-101 | medium | FR-001 carries no `traces_to` or `implements` relationship to StR-001 or US-001 — its only frontmatter relationship is `implements` on `filament-core-service/FR-035` — yet `tests.md` credits StR-001 with "US-001, FR-001..FR-005" and StR-001 Dependencies names FR-001 as downstream. The completeness rule "every FR maps to ≥ 1 StR" holds for FR-001 in prose only, and holds for FR-002..FR-005 transitively through US-001. StR-001 Downstream is separately stale: it names FR-001 and US-001 while VC-3, added for this issue, is discharged by FR-002..FR-005. | FR-001 frontmatter, StR-001 Dependencies, StR-001-VC-3, spec/tests.md StR row | missing-requirement |
| FND-102 | medium | The matrix status column contradicts the engine's reading of the same tree. `tests.md` states "a row is `🚧` until a tagged test asserts it", every one of the 66 rows reads `🚧`, and the FR rows read "pending implementation" — while `quire coverage --scope .` on this worktree reports 53/123 rows backed (43%), with FR-004 at 15/15 (100%) and FR-002 at 9/12 (75%) from 29 bound symbols across 45 candidates. Either the matrix is stale against tests that have landed, or the rows are backed by symbols the matrix does not credit; both readings make the status column unusable as the coverage signal it declares itself to be. | spec/tests.md Overview, spec/tests.md Test Case Summary, `quire coverage --scope .`, `tests/test_role_schemas.py` | correct-requirement-no-evidence |
| FND-103 | medium | The TypeSpec toolchain is wired into the default lint gate with no provisioning obligation. FR-002 Behavior and FR-002-AC-11 require `make lint` to run `make schemas-check`; `poe lint` on this branch is `[ruff-check, black-check, schemas-check]`; the generator is required to exit non-zero when `tsp` is unresolvable; and `make install` runs `poetry install` only. No requirement obliges an `npm ci`, names `node_modules` as a precondition, or provides the counterpart to FR-005's `make dev-quire` — so on a clean checkout the repository's lint gate fails for a reason unrelated to lint. FR-002-CON-4 states the check does not run in the GitHub workflow without saying what discharges the drift gate there (the repository's `lib-ci` reusable workflow runs `pytest`, `black --check` and `ruff check` directly, never `poe lint`). | FR-002 Behavior (`make lint`, `tsp` bullets), FR-002-AC-11, FR-002-CON-4, `Makefile`, `pyproject.toml` `[tool.poe.tasks.lint]`, `.github/workflows/ci.yml`, `python-service-actions/.github/workflows/lib-ci.yml` | missing-requirement |
| FND-104 | medium | `spec.md` Out of Scope states that until `agent-ix/filament-core-service#23` lands "the service stores the reference verbatim, which is what FR-001-AC-4 and IT-001-SC-03 assert". Neither does. FR-001-AC-4 reads "each declared archetype/object_type/artifact_type appears in the corresponding filament-core table" with no mention of `data_schema`; IT-001-SC-03 is the idempotency criterion (same `modules.id`, same content hash), and the contribution-presence criterion is IT-001-SC-02. FR-001 and IT-001 are unchanged from the 0.2.0 era and are silent on the reference form and on the minimum service revision, so FR-001-AC-4 has two valid readings and the spec's own claim of coverage is unbacked. The sibling dispositioned the same gap by amending FR-001 Behavior and IT-001-SC-03 (SR-003 FND-126). | spec.md Out of Scope, FR-001-AC-4, IT-001-SC-02, IT-001-SC-03, FR-003 Inputs (revision `a77f31e`) | correct-requirement-no-evidence |
| FND-105 | medium | FR-004-AC-15 states no required behaviour of the system: it asserts that the three cross-key reader rules "are asserted by no shipped schema" and that "a record violating any of the three validates today". TC-054 therefore passes for exactly as long as nothing implements the rules and turns red the day `agent-ix/quoin#335` publishes the mapping — the inverse of a criterion. The spec has an established form for precisely this shape (an explicit expected failure naming the blocking issue, as FR-003-AC-6 and NFR-001-AC-2 carry) and AC-15 does not use it, so no artifact tells a future reader that a red TC-054 is the success signal. | FR-004-AC-15, TC-054, FR-004 Behavior (three reader-rule bullets), FR-003-AC-6, NFR-001-AC-2 | correct-requirement-no-evidence |
| FND-106 | medium | The rows with no declared discharge mechanism grew and their inventory did not. `quire coverage` reports `archetype-matches-nothing` for both the `inspection` (`Inspections`) and `suite` (`SuiteRegistry`) declarations — neither scans any document, so no `Inspection`, `Manual` or `Demonstration` row can be minted or discharged. The matrix's Coverage Gaps enumerates eight such rows (TC-005, TC-006, TC-007, TC-020, TC-021, TC-036, TC-069, TC-091); the newest edits added TC-026 and TC-072, both `Inspection`, bringing the count to ten, and the enumeration was not updated. Ten of 66 rows (15%) are carried by the plan rather than the matrix. | spec/tests.md Coverage Gaps, TC-026, TC-072, `quire coverage --scope .` | correct-requirement-no-evidence |
| FND-107 | medium | Three normative bullets added to FR-005 by the SR-006 FND-201 disposition arrived with no owning criterion and no matrix row: the typed-section-is-authority rule, the kernel-form-is-authority rule for the three inverted overlaps (alert `## Flow`, slo frontmatter `target`/`window`, incident `## Timeline`), and "where the kernel form is the authority, no test SHALL assert agreement". The fourth unowned bullet SR-001 FND-004 named — "only a criterion this specification names as blocked SHALL be exempt" — also remains unowned; that disposition landed as FR-005-AC-10 and AC-11, which cover `make dev-quire`, fail-not-skip and the `pyproject.toml` prohibition, three of its four parts. Authority rules are the module's answer to dual-authority drift and are the least self-enforcing text in the spec. | FR-005 Behavior (typed-authority, kernel-authority, no-agreement-test, exemption bullets), FR-005-AC-1..11, spec/tests.md TC-060..TC-072 | correct-requirement-no-evidence |
| FND-108 | low | FR-002-AC-12 requires `.gitattributes` to mark `*.json`, `*.tsp`, `*.yaml` and `*.md` as `eol=lf` (which the shipped `.gitattributes` does), while the FR-002 Behavior bullet the criterion verifies still names `*.json` and `*.tsp` only. The criterion asserts more than the behaviour it is the evidence for. | FR-002 Behavior (`.gitattributes` bullet), FR-002-AC-12, `.gitattributes` | wrong-requirement |
| FND-109 | low | US-001-EX-2 illustrates the module's purity rule with an SLI carrying an `observations` key, refused "because an SLI declares a measurement, not the values measured". FR-004-AC-10 now records that this refusal "holds for any unknown key, so it is evidence of the seal only", and points to FR-004-AC-14 for the type-specific evidence. The story's one purity example therefore illustrates a refusal the spec has since classified as non-diagnostic; the occurrence-row case (a `Timestamp` row on a standing definition) is the example that now carries the rule. | US-001-EX-2, FR-004-AC-10, FR-004-AC-14, spec.md Out of Scope | wrong-requirement |
| FND-110 | low | FR-003 Behavior's closing bullet — "If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or schemas rather than relax the contract keys, the digests, or the `$id` rules" — is a process obligation on the maintainers, not externally observable system behaviour, and carries no criterion and no row. The sibling dispositioned the same sentence by rewording the subject from a person to the module (SR-003 FND-135), which is the wording here; the testability objection survives the rewording. | FR-003 Behavior (last bullet), spec/tests.md TC-030..TC-038 | wrong-requirement |
| FND-111 | low | FR-002 is not atomic: it owns schema emission, the drift gate, the `make lint` wiring, the manifest digest rewrite, wheel packaging (AC-6), npm tarball staging (AC-7) and the `.gitattributes` line-ending rule (AC-12) — twelve acceptance criteria and five constraints over obligations that fail independently. The packaging half (AC-6, AC-7, `scripts/stage-npm.mjs`) has no dependency on the emission half beyond consuming its output and would carry cleanly as its own requirement. | FR-002 Description, FR-002 Behavior, FR-002-AC-6, FR-002-AC-7, FR-002-AC-12 | wrong-requirement |
| FND-112 | low | FR-005-AC-7 requires that "the skeleton for each of the eight types has no placeholder token"; no artifact defines "placeholder token". `spec.md` and FR-004 use "placeholder" for an untyped `{type: object}` schema, which is a different subject. An implementer must invent the predicate (`TODO`, `TBD`, `FIXME`, `<...>`, `XXX`?), so two correct implementations of TC-066 can disagree. | FR-005-AC-7, TC-066, FR-004 Description, spec.md In Scope | missing-requirement |
| FND-113 | low | NFR-001 declares `constrains` on FR-003, FR-004 and FR-005, and only FR-005 names it back (one Behavior bullet). FR-003 and FR-004 Dependencies list their upstream and downstream FRs but not the NFR that bounds them, so a reader of FR-004 — which owns the schemas NFR-001 measures — is not told that additive compatibility constrains it. | NFR-001 frontmatter, FR-003 Dependencies, FR-004 Dependencies, FR-005 Behavior | missing-requirement |
| FND-114 | low | The npm package version and the manifest version are decoupled: `package.json` carries `0.0.0-managed` (set by the release pipeline) while FR-002's whole rationale is that the `$id` base embeds the manifest `version` so "one schema URL names exactly one immutable byte sequence". FR-002-AC-7 checks the tarball's *contents*; nothing ties the version a consumer pins on npm to the schema version inside it, so `@agent-ix/spec-objects-operational@X` does not name a schema generation. Either state that the manifest `version` is the only version axis a consumer may read, or bind the two. | FR-002 Behavior (`$id` base bullet), FR-002-AC-7, `package.json`, `scripts/stage-npm.mjs` | missing-requirement |

## Finding Details

### FND-100 (medium) — the stakeholder layer validates against an artifact that does not exist

`StR-001-VC-2` is one of the three criteria by which stakeholder satisfaction is
judged, and TC-006 is its only row. It reads: "Agent CLI generators
(minijinja-cli) can produce valid artifacts using the **templates** and schemas
this module ships." The shipped package is `manifest.yaml`, `schemas/` (26
models plus `toolchain.json`) and `skeletons/` (eight types plus three alternate
forms). `grep template spec_objects_operational/manifest.yaml` returns nothing.
The word survives in five places across `spec.md` and `StR-001`.

The correction is the sibling's: read "skeletons and schemas" throughout, since
those are what a generator targets and what FR-005 makes executable. This is
also what makes VC-2 discharge-able at all — a demonstration against skeletons
and schemas is possible today; one against templates is not.

### FND-102 (medium) — the matrix and the engine disagree about the same tree

`tests.md` declares its own rule in the Overview: "A row is `🚧` until a tagged
test asserts it; the rows that stay `🚧` after implementation are the ones whose
evidence needs an environment this repository cannot provision". All 66 rows
read `🚧`, and the five FR rows read "pending implementation" or an environment
note. Run on the same worktree:

```
Coverage: 53/123 rows backed (43%)
python: 29/29/45 bound/tagged/candidates
spec/functional/FR-004-role-schemas.md: 15/15 (100%)
spec/functional/FR-002-emitted-json-schemas.md: 9/12 (75%)
```

FR-004's fifteen criteria are fully bound by tagged symbols, and FR-002's are
three-quarters bound, while the matrix reports both as pending. This is a
bookkeeping lag, not a defect in the requirements — but the matrix is the
artifact `spec-to-plan` reads to decide what remains, and in its current state
it would task work that is done. Refresh the status column against
`quire coverage` before the plan is cut, and state in the Overview which of the
two documents is authoritative when they disagree.

### FND-103 (medium) — the lint gate depends on a toolchain nothing provisions

Three rules interlock:

- FR-002 Behavior: "`make lint` SHALL run `make schemas-check`, so a `typespec/`
  edit that was never regenerated fails before push rather than at review", now
  carried by FR-002-AC-11.
- FR-002 Behavior: "If `node` is older than 20 or `tsp` is not resolvable, then
  the generator SHALL exit non-zero naming the required Node version or the
  missing binary."
- `make install` → `poetry install`. There is no `npm ci` target, and no
  requirement names `node_modules` as a precondition of `make lint`.

So on a clean checkout the repository's own lint gate fails, correctly and by
design, for a missing binary. FR-005 solved the identical problem for the Quire
wheel by specifying a provisioning target (`make dev-quire`), stating what
happens when it has not been run (fail, not skip), and naming the blocking
issue. FR-002 states only the third of those three.

FR-002-CON-4 compounds it by asserting where the check does *not* run — "not in
the GitHub workflow" — without saying what discharges the drift gate there. The
repository's CI is `workflow_dispatch`-only and delegates to
`agent-ix/python-service-actions/.github/workflows/lib-ci.yml`, whose jobs run
`poetry run pytest`, `poetry run black --check .` and `poetry run ruff check .`
directly; `poe lint` is never invoked, so CON-4 is true today by accident of the
shared workflow's shape rather than by any rule this module states. Add the
provisioning obligation and a criterion for it, and state the drift gate's CI
discharge (or its explicit absence, with the reason).

### FND-104 (medium) — a coverage claim the cited criteria do not make

`spec.md` Out of Scope, on `agent-ix/filament-core-service#23`:

> Until it lands the service stores the reference verbatim, which is what
> FR-001-AC-4 and IT-001-SC-03 assert.

FR-001-AC-4: "Each declared archetype/object_type/artifact_type appears in the
corresponding filament-core table after activation." IT-001-SC-03: "the
activation is an idempotent no-op — same `modules.id`, same SHA-256 content
hash, and no row duplication." Neither names `data_schema`, the reference form,
or a minimum service revision; the contribution-presence criterion is
IT-001-SC-02, not SC-03, so the citation is wrong on both halves.

The consequence is a real ambiguity, not only a citation error: FR-001-AC-4 can
be read as "the row exists" or as "the row's `data_schema` equals the reference
object as posted", and the two readings diverge exactly when `#23` lands. FR-003
Inputs already pins the manifest schema revision (`a77f31e`, CR-003); FR-001
should pin the service revision the same way and state the expected registered
value, and IT-001-SC-02 should say what "the correct attributes" means for
`data_schema`.

### FND-105 (medium) — a criterion that asserts the system does nothing

FR-004-AC-15 was added to discharge SR-001 FND-007 (three `SHALL` reader rules
JSON Schema cannot express). Of the two dispositions that review offered —
restate as informative notes, or give each a criterion naming the consumer that
discharges it — the applied text does neither cleanly: the rules stay `SHALL` in
Behavior, and AC-15 asserts their *non-enforcement*.

A criterion whose predicate is "no shipped schema asserts this" cannot fail
while the gap exists and can only fail once the gap closes. The spec already has
the right instrument for a known-open gap and uses it twice: FR-003-AC-6's
naming half is carried as an explicit expected failure against `quire-rs#221`
and `#394`, and NFR-001-AC-2's legacy-`object:` case against `#391`. Restate
AC-15 in that form — an expected-flip row naming `agent-ix/quoin#335`, so that a
red TC-054 reads as the mapping having landed rather than as a regression — or
demote the three rules to informative notes and drop the criterion.

### FND-107 (medium) — the authority rules govern nothing that is checked

FR-005 now carries six overlap statements: three pairs where the typed section
is the authority, three where the kernel form is, and one rule forbidding any
test from asserting agreement between the two while the mapping is open. None of
the six has a criterion, and none has a row. The last one is self-consistent
(it forbids a test rather than requiring one), but the first five are the
module's entire answer to the dual-authority problem the ticket exists to solve,
and they are enforced today only by review.

The verifiable residue is small but real and should be claimed: that the typed
section exists in every skeleton whose type admits it (close to FR-005-AC-6),
that the kernel sections named as authoritative are present and non-empty (close
to FR-005-AC-7), and that the typed keys said to be unpopulated are in fact
absent from every extracted record — which is the assertion that makes "no test
shall assert agreement" honest rather than convenient. One criterion covering
the third of those, plus a row, converts a prose rule into a measurement.

## Consistency and Atomicity Notes

Checked and clean, recorded so a later reader need not re-derive them:

- The `semantic` block's "nine admitted keys" (FR-003-AC-1) equals the nine keys
  FR-003 Behavior enumerates and the nine in the shipped `manifest.yaml`.
- The eight object types are eight in `spec.md`, `StR-001` (as amended),
  `US-001`, FR-003 `exports`, the FR-004 table and `manifest.yaml`
  `object_types`. No nine-versus-ten defect of the kind the sibling carried.
- FR-002-AC-1's emitted set ("the eight object-type models plus the support
  models named by FR-004") resolves against FR-004 Outputs to 5 markers, 7
  declaration models and 6 enums; 8 + 18 = 26 model files plus `toolchain.json`,
  which is exactly what `spec_objects_operational/schemas/` contains.
- Every negative-fixture case named in FR-005 Behavior (ten) matches
  FR-005-AC-5's count and TC-064's, and the `detail:` discipline is stated in
  Behavior, required by AC-5 and asserted by TC-064.
- No requirement duplicates another with different wording. The FR-004
  constraint table restates its acceptance criteria (CON-1/AC-13, CON-2/AC-10,
  CON-3/AC-11, CON-5/AC-14), but each is a distinct verification obligation and
  the matrix credits them jointly on one row, which is the intended shape.
- All seven neighbour issues cited across the spec exist and are open.

## Proposed Dispositions

No spec artifact was edited by this review. Every disposition below is proposed
for the parent agent to apply.

| Finding | Proposed disposition |
|---|---|
| FND-100 | Replace "templates" with "skeletons" in StR-001-VC-2, StR-001 Rationale, StR-001 Stakeholders, `spec.md` Purpose and `spec.md` Intended Users; TC-006's title follows. |
| FND-101 | Add a `traces_to` StR-001 relationship to FR-001's frontmatter so the `tests.md` StR row matches the frontmatter, and extend StR-001 Dependencies (Downstream) with FR-002..FR-005, which discharge VC-3. |
| FND-102 | Refresh the matrix status column against `quire coverage --scope .` before `spec-to-plan`, and state in the Overview that the engine's reading is authoritative where the two disagree. |
| FND-103 | Add to FR-002 an `npm ci` provisioning obligation (a `make node-deps` target or equivalent) with a criterion, and state in FR-002-CON-4 what discharges the drift gate in CI — or that nothing does and why. |
| FND-104 | Amend `spec.md` to cite IT-001-SC-02, and amend FR-001 Behavior and IT-001-SC-02 to state that, while `filament-core-service#23` is open, the registered `data_schema` is the reference object as posted; pin the minimum service revision the way FR-003 Inputs pins `a77f31e`. |
| FND-105 | Restate FR-004-AC-15 as an explicit expected-flip criterion naming `agent-ix/quoin#335` (the form FR-003-AC-6 and NFR-001-AC-2 already use), or demote the three reader rules to informative notes and drop the criterion and TC-054. |
| FND-106 | Add TC-026 and TC-072 to the Coverage Gaps enumeration, and record the count (ten of 66) so the plan inherits the full undischarged set. |
| FND-107 | Add one criterion (and row) asserting that the typed keys declared unpopulated are absent from every extracted record, and tie the authority bullets to it; keep the "no test SHALL assert agreement" rule as the stated limit it is. |
| FND-108 | Widen the FR-002 Behavior `.gitattributes` bullet to the four patterns FR-002-AC-12 and the shipped file carry. |
| FND-109 | Rewrite US-001-EX-2 over the occurrence-row case (a `Timestamp` row on an SLI or a migration), which is the refusal FR-004-AC-14 measures. |
| FND-110 | Move FR-003's "correct the manifest rather than relax the contract" bullet to Rationale, or restate it as a boundary constraint with an inspection row. |
| FND-111 | Recorded. Splitting the packaging half of FR-002 into its own FR is proposed, not required; if it stays, note in FR-002 Description that it owns emission, the gate and two distribution channels. |
| FND-112 | Define "placeholder token" in FR-005-AC-7 (the literal token set the test greps for). |
| FND-113 | Add NFR-001 to FR-003 and FR-004 Dependencies so the constraint is visible from the requirements it bounds. |
| FND-114 | State in FR-002 that the manifest `version` is the only version axis a schema consumer reads, and that the npm package version is a distribution artifact — or bind the two at pack time. |
