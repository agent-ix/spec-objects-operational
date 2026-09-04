---
id: SR-007
title: "Risk & complexity review of the issue #6 semantic module contract"
type: SpecReview
analysis: risk-complexity
scope: "spec/spec.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/non-functional/NFR-001-additive-compatibility.md, spec/tests.md"
review_set: all
---
# SR-007: Risk & complexity review of the issue #6 semantic module contract

## Summary

Scored every requirement of the issue #6 set on technical risk and volatility
and ground each score against the landed implementation on this worktree
(`bd48e9a`), not against the spec text alone: `typespec/main.tsp`, the 27
emitted schemas plus `toolchain.json`, `spec_objects_operational/manifest.yaml`
at `version: 0.3.0`, `package-lock.json`, `tests/conftest.py`, the role-schema
and semantic test modules, the `Makefile`, and the repository's two workflows.
`make test` is green and `quire coverage --scope .` reports 125/125 rows
backed, so this review is about residual risk in what shipped and volatility in
what it is coupled to, rather than about buildability.

Two structural facts dominate the register. First, the evidence mapping the
ticket's own merge gate names was changed during implementation — the shipped
`EvidenceRef` is `{ shape: EvidenceRecordShape, record: EvidenceRecordId }`
over quoin FR-059's own vocabulary and bare-token identity pattern — while
FR-004 Outputs, FR-004 Behavior and FR-004-AC-11 still describe
`{ kind: EvidenceKind, record: SemanticId }`, and TC-050 reads green over an
assertion the shipped schema now inverts. Second, every gate that protects the
contract (the `schemas-check` drift gate, the 15 FR-004 record criteria, every
semantic row) runs only on a machine that carries `node_modules` from npm.ix
and a Quire 0.46.0 wheel from pypi.ix; the repository's CI is dispatch-only and
provisions neither, so 125 backed rows are backed on exactly one host.

The rest of the set is low-to-medium risk by construction: the module is
advisory-only, ships no runtime behaviour, holds no secret, coordinates no
writer, and states no latency or availability bound — so the classical
high-risk drivers are absent and the risk that remains is coupling and churn.

## Verdict

**CONDITIONAL — plannable, not mergeable, until FND-700 is dispositioned.** The
evidence-mapping divergence sits on the ticket's own safety gate ("evidence-record
incompatibility blocks merge rather than creating a second record family") and
on a matrix row that is green while asserting the opposite of what ships;
restating FR-004 over the shipped mapping is a spec edit, not a code change.
FND-701 needs an owning issue before the copied vocabulary can be relied on.
The four remaining mediums are plan inputs (provisioning, version churn,
forward-guessed keys, blast radius); the three lows are recorded.
Counts: 2 high, 4 medium, 3 low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|----|----------|---------|------|--------------|
| FND-700 | high | The spec and the shipped schema disagree about the one thing the ticket gates on. FR-004 Outputs names the enum `EvidenceKind`, FR-004 Behavior specifies `EvidenceRef` as `{ kind: EvidenceKind, record: SemanticId }` with the closed set `exercise`/`execution`/`observation`/`review`, and FR-004-AC-11 requires that a `record` that is "a bare token rather than a `SemanticId`" fails. What shipped is `EvidenceRef.json` requiring `{ shape, record }` where `shape` is `EvidenceRecordShape` (two values, `standing_capability` and `exercise`) and `record` is `EvidenceRecordId`, a string with pattern `^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$` — so `artifact-store-capability` validates, which AC-11 says must fail. `EvidenceKind` is emitted nowhere; `EvidenceRecordShape` and `EvidenceRecordId` are emitted and are named by no requirement. FR-002-AC-1 ties the emitted file set to "the support models named by FR-004": that is 18 support models against the 19 `toolchain.json` lists, and TC-023/TC-040's evidence uses `tests/conftest.py::SUPPORT_MODELS`, which carries the shipped 19. TC-050 ("a bare-token `record` and an out-of-set `kind` each fail") reads ✅ while its test asserts something else — that `"has spaces"` and `shape: "vibes"` fail. The change is the right one on the merits (dependency.md FND-400 argued exactly this), but it landed in code and never reached the spec. | FR-004 Outputs, FR-004 Behavior (EvidenceRef bullets), FR-004-AC-11, FR-002-AC-1, spec/tests.md TC-050, `typespec/main.tsp` l.129-145 l.244-245, `schemas/EvidenceRef.json`, `schemas/EvidenceRecordId.json`, `tests/test_role_schemas.py::test_evidence_is_declared_by_incident_alone_and_is_typed` | wrong-requirement |
| FND-701 | high | The evidence vocabulary is a copy of a neighbour's closed enum and identity pattern, taken from a programme that has no open owner and no version this module can pin. `EvidenceRecordShape` reproduces quoin FR-059's `record_shape` and `EvidenceRecordId` reproduces its `$defs/identity` regex; `main.tsp` states "FR-059 owns the values; a change there is a breaking change to this module", but nothing detects such a change — no digest covers quoin's schema, no test reads it, `agent-ix/quoin#267` is CLOSED, and no issue is filed for the reconciliation. The widened identity also removes the only handle a resolver had: an `EvidenceRecordId` names no repository and no bundle, so an `evidence` entry cannot be resolved, cross-checked, or reported dangling by any engine — the "one canonical semantic mapping" acceptance criterion is satisfied structurally (one key on one model) and is unmeasurable referentially. Volatility here is not this module's to control and its blast radius is a manifest version bump plus full regeneration. | FR-004 Behavior (EvidenceRef bullets), FR-004-CON-3, spec.md Out of Scope (quoin#267 paragraph), `typespec/main.tsp` l.118-145, quoin FR-059 | missing-requirement |
| FND-702 | medium | Every gate that protects this contract is single-host. The drift gate (`make lint` → `make schemas-check`) needs `tsp` and `@agent-ix/semantic-core` from `node_modules`, installed by `make install`'s `npm ci` against npm.ix; the 15 FR-004 record criteria resolve their semantic-core `$ref`s out of `node_modules/@agent-ix/semantic-core/generated/json-schema` (`tests/conftest.py`); every semantic row needs a Quire 0.46.0 wheel that exists only on pypi.ix (`agent-ix/quire-rs#392`). The repository's CI is `workflow_dispatch`-only and delegates to `python-service-actions/lib-ci`, which runs `pytest`, `ruff` and `black` after a `poetry install` — no `make install`, no `npm ci`, no `make dev-quire` — so if that workflow is ever dispatched it fails wholesale, and if it is not, nothing re-verifies the 125 rows anywhere. FR-002-CON-4 states the check does not run in the workflow; no requirement states what does, and the FR-004/FR-005 halves are not covered by CON-4 at all. Integrity FND-103 raised the clean-checkout half of this before the tests existed; post-implementation the exposure is the whole matrix, not the lint target. | FR-002-CON-4, FR-002-AC-13, FR-005 Inputs, FR-005 Behavior (`make dev-quire`), spec/tests.md Test Environment, `Makefile`, `.github/workflows/ci.yml`, `tests/conftest.py` | correct-requirement-no-evidence |
| FND-703 | medium | Version churn is coupled across four artifact classes and two of its statements are already hard-pinned. FR-002 accepts by decision that the `$id` base embeds the manifest `version`, and forbids any criterion, test or fixture from hard-coding the version segment (FR-002-CON-5) — but FR-003's Description ("at manifest `version` 0.3.0"), FR-003 Behavior ("The manifest `version` SHALL be `0.3.0`") and FR-003 Outputs all hard-code it, so a 0.4.0 bump makes three FR-003 statements false while FR-002's rule reads satisfied. The mechanical cost of that bump is 27 `$id` values, every sibling `$ref` across the emitted set, 8 manifest digests, the `toolchain.json` base and aggregate digest, and the npm/wheel payloads — one commit that touches nearly every shipped byte, with `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` reading these files as fixtures keyed by that URL. The procedure is specified; the FR-003 pins and the downstream notification are not. | FR-003 Description, FR-003 Behavior (version bullet), FR-003 Outputs, FR-002 Behavior (`$id` base, bump procedure), FR-002-CON-5, FR-004 Dependencies (Downstream) | wrong-requirement |
| FND-704 | medium | Nineteen declared-but-unpopulated keys plus `relations` are a forward guess at a mapping that does not exist yet, and nothing detects the guess going wrong. `scopes`, `configures`, `rollback`, `migrates`, `dependsOn`, `measures`, `objective`, `constrains`, `conditions`, `escalatesTo`, `references`, `steps`, `remediates`, `evidence`, `correlates`, `breaches`, `triggers`, `rollout`, `deploys` are declared optional so a future extractor can fill them without a schema change — but only if `agent-ix/quoin#335` names them identically and nests them identically. Their entire evidence is hand-built JSON records (`tests.md` Test Environment says so honestly, and TC-041..TC-050 and TC-054 carry it), so a mismatch is invisible until the mapping publishes, at which point the correction is a schema change, a version bump, and the full regeneration of FND-703. Nothing in the spec or the suite subscribes to `agent-ix/quoin#335`, and the shapes with the most invented structure (`AlertCondition`, `ObjectiveDecl`, `RunbookStep`, `ScopeAssignment`) are the ones the mapping is least likely to match term-for-term. | FR-004 Behavior (unpopulated-key bullet, support-model bullets), FR-004 table (optional-key columns), spec/tests.md Test Environment, spec.md Out of Scope (quoin#335 paragraph) | correct-requirement-no-evidence |
| FND-705 | medium | There is no slice boundary below the whole module, and no requirement says so. A one-character correction to any single schema re-emits that file, flips its digest in `manifest.yaml`, flips the aggregate digest in `toolchain.json`, invalidates any Quoin-installed copy (IT-002), and changes the wheel and the npm tarball — while FR-002 owns emission, the drift gate, the manifest digest rewrite, the `make lint` wiring, wheel packaging and npm staging across 13 acceptance criteria, and FR-004 owns 8 object-type models plus 19 support models across 15. The bump procedure covers a version change; nothing states the equivalent for a content fix, and the plan therefore has no task granularity smaller than "regenerate everything" and no rollback smaller than reverting the whole regeneration. Integrity FND-111 proposed splitting FR-002's packaging half; this is the same shape measured as blast radius rather than atomicity. | FR-002 Description, FR-002-AC-1, FR-002-AC-4, FR-002-AC-6, FR-002-AC-7, FR-003-AC-2, FR-004 Outputs, IT-002-SC-02 | missing-requirement |
| FND-706 | low | The `$id`/`$ref` base `https://schemas.agent-ix.org/...` is a naming convention that no requirement states is or is not dereferenceable, and three consumers already resolve it three ways: the test harness maps the semantic-core base onto `node_modules/@agent-ix/semantic-core/generated/json-schema`, Quire resolves module-bundle siblings and its vendored semantic-core bundle, and the downstream fixture readers (`agent-ix/quire-contract-ir#52`, `agent-ix/filament-core-data#36`) will choose their own. FR-002-AC-3 only requires that every `$ref` names one of the two bases. A consumer that assumes the URL fetches gets nothing, with no requirement to point at. | FR-002 Behavior (normalization bullets), FR-002-AC-3, `tests/conftest.py` (`SEMANTIC_CORE_BASE`) | missing-requirement |
| FND-707 | low | Ten of 125 rows are held green or amber by a neighbour's unreleased state, and the matrix column cannot say so: three strict xfails (`agent-ix/quire-rs#391` beside NFR-001-AC-2, `agent-ix/quire-rs#221`/`#394` beside FR-003-AC-6, `agent-ix/quoin#335` beside FR-004-AC-15) and seven environment-gated rows (TC-002..TC-006, TC-036, TC-091). The xfails are strict by design — they turn red when the neighbour lands, which is the intended signal — but the repository has no subscription to those five issues and no CI that would notice, and FR-005 Inputs pin the engine as "0.46.0 or later", so an upgrade can flip an xfail, re-severity a diagnostic, or change a message tail under a green suite. Failure-domain FND-212 raised the floor; this is the flip-notification half. | FR-005 Inputs, FR-005 Behavior (exemption bullet), NFR-001-AC-2, FR-003-AC-6, FR-004-AC-15, spec/tests.md Test Environment | correct-requirement-no-evidence |
| FND-708 | low | Recorded so the register's low scores are auditable rather than assumed: this module has no novel-technology, concurrency, security or performance driver. It ships declarations only (`spec.md` Out of Scope forbids runtime control), holds no credential, coordinates no writer, states no latency, throughput or availability bound, and processes no regulated data; `security_critical: false` in `spec.md` frontmatter is correct. The one privileged act in the set is IT-002's `quoin module install`, which mutates operator-global state and is restored by hand (IT-002-SC-06), and the one supply-chain surface is `package-lock.json`, whose 75 entries now resolve 74 from `registry.npmjs.org` and only `@agent-ix/semantic-core` from npm.ix with an `integrity` hash — the state FR-002-CON-4 requires, and a correction of what dependency.md FND-403 found. | spec.md Out of Scope, spec.md frontmatter, FR-002-CON-4, IT-002-SC-06, `package-lock.json` | correct-requirement-no-evidence |

## Risk Register

| Req | Tech Risk | Volatility | Drivers | Mitigation |
|-----|-----------|------------|---------|------------|
| StR-001 | Low | Low | Stakeholder need over eight shipped types; no technology of its own | None needed on this axis; the wording defects are base.md FND-002 and integrity.md FND-100 |
| US-001 | Low | Medium | Downstream fixture readers (`quire-contract-ir#52`, `filament-core-data#36`) may reshape what a declaration record must carry | Keep the story free of layout; let FR-004 absorb the change |
| FR-001 | Medium | Low | Live `filament-core-service`, content-hash idempotency, a manifest schema no released service accepts | Leave as-is; TC-002..TC-004 stay environment-gated (dependency.md FND-404 pins the revision) |
| FR-002 | Medium | High | Version-embedded `$id`, digest coupling across 27 schemas + manifest + `toolchain.json` + two distribution channels, drift gate that runs on one host only, npm.ix-only build input | Name what discharges the gate outside that host (FND-702); state the content-fix regeneration procedure beside the bump procedure (FND-705); de-pin `0.3.0` from FR-003 so the version axis has one home (FND-703) |
| FR-003 | Medium | High | Manifest version hard-pinned in three statements, digests churn on every schema edit, two vendored copies of the FR-035 schema, a global `quoin module` install as the only Quoin evidence | Sequence as build step then verify step (dependency.md FND-405); derive the version rather than pin it; keep the Quoin roundtrip Manual until it can run in a temp Quoin home |
| FR-004 | High | High | Shipped evidence mapping diverges from the requirement text; a copied closed enum and identity pattern owned by a closed epic; 19 unpopulated keys guessing at `quoin#335`; `contains`/`minContains`/`maxContains` plus `unevaluatedProperties` encodings behind `@extension` escape hatches; 15 criteria on one requirement | Restate FR-004 over the shipped `EvidenceRef` and re-word TC-050 (FND-700); file the FR-059 reconciliation issue and record what detects a change there (FND-701); mark the 19 keys as reserved-pending-`quoin#335` with the churn cost stated (FND-704) |
| FR-005 | Medium | Medium | Engine floor "0.46.0 or later" on a wheel published to one dev index; message-tail `detail:` matching; two extraction paths; strict xfails that flip on a neighbour's release | Pin the wheel exactly and name the flip owners for the five gating issues (FND-707); dependency.md FND-406/FND-407 carry provisioning and the `detail:` substring source |
| NFR-001 | Medium | Low | Zero-error legacy metric over a checked-in 0.2.0 baseline; one engine defect (`quire-rs#391`) carried as a strict xfail rather than worked around | Keep the xfail; name the revision the baseline was captured from (failure-domain FND-214, dependency FND-410) |
| IT-001 | Medium | Low | Needs a `filament-core-service` built from main; no release accepts the 0.3.0 manifest | Carry the service build as an enablement task; row stays gated |
| IT-002 | Medium | Medium | Manual, mutates operator-global Quoin state, needs a Quoin built from main that no tag carries | Parameterise against a temp Quoin home; keep as Demonstration until then |

## Top hazards

1. **FR-004's evidence mapping (FND-700, FND-701).** The requirement text, the
   acceptance criterion, the matrix row and the shipped schema describe three
   different contracts, on the one obligation the ticket's merge gate names.
   Restating the spec is cheap; deciding who owns quoin FR-059's vocabulary
   for this module is not, and no open issue holds it.
2. **Single-host evidence (FND-702).** 125 rows are backed on one machine, by a
   toolchain from a local npm registry and a wheel from a local PyPI, with a
   dispatch-only CI that provisions neither. Every other risk in this register
   is discovered by re-running that suite somewhere else.
3. **Version and digest churn (FND-703, FND-705).** One shipped byte moves
   eight manifest digests, two `toolchain.json` fields, a wheel and an npm
   tarball; a version bump moves nearly every byte, and three FR-003 statements
   go stale when it does. There is no slice smaller than the module.
4. **Forward-guessed keys (FND-704).** Nineteen optional keys and four invented
   support shapes are betting on `agent-ix/quoin#335` naming things the same
   way; the bet is verified only against hand-built records and pays out as a
   schema change plus a full regeneration.
5. **Neighbour-release flips (FND-707).** Five open engine issues gate three
   strict xfails and seven environment rows; the design is right and the
   notification path does not exist.

## Mitigation order

1. Disposition FND-700 with the architect: restate FR-004 Outputs, the
   `EvidenceRef` Behavior bullets and FR-004-AC-11 over the shipped
   `{ shape, record }` form, and re-word TC-050 to the rule its test asserts.
   No schema, test, or digest changes; this is the spec catching up with a
   decision already taken and defended in `main.tsp`.
2. File the FR-059 reconciliation issue FND-701 asks for (quoin#267 is closed),
   and record in FR-004 which side owns the identity and what detects a change
   to `record_shape` — a pinned copy under `tests/fixtures/`, or an explicit
   statement that nothing does.
3. State the CI answer FND-702 needs: either a workflow that runs `make install`
   and `make dev-quire` before `pytest`, or an explicit statement in
   FR-002-CON-4 and `tests.md` Test Environment that the whole matrix is
   discharged on a developer host while `agent-ix/quire-rs#392` is open.
4. Remove the `0.3.0` pins from FR-003 (Description, Behavior, Outputs) so the
   manifest version has exactly one home, and add the content-fix regeneration
   procedure beside FR-002's bump procedure.
5. Label the 19 unpopulated keys and the four invented support shapes as
   reserved pending `agent-ix/quoin#335`, stating the cost of a mismatch, so a
   later reader does not read them as ratified.
6. Pin the Quire wheel exactly in FR-005 Inputs and name, per gating issue, the
   row that flips when it lands.

## Failure-domain gaps

`spec/reviews/6-semantic-module-contract/failure-domain.md` (SR-006 in that
directory's numbering) is current and its dispositions FND-200, FND-201 and
FND-202 read as applied in the landed FR-004 table and FR-005 Behavior. This
review adds no new failure domain and defers to it for identity, purity,
topology and edge-case gaps; FND-204 (reference-key target types and cycles),
FND-205 (unit and window coherence) and FND-213 (marker discriminators) remain
the open ones and are scored above as FR-004 volatility drivers rather than
restated. The one domain this review touches that failure-domain does not is
referential: FND-701's unresolvable `EvidenceRecordId`, which arrived with the
implementation after that review was written. Open gaps: FR-004.

## Proposed Dispositions

No spec artifact and no implementation file was edited by this review. Every
disposition below is proposed for the parent agent to apply.

| Finding | Proposed disposition |
|---|---|
| FND-700 | Restate FR-004 Outputs (`EvidenceRecordShape`, `EvidenceRecordId`, drop `EvidenceKind`), the two `EvidenceRef` Behavior bullets, and FR-004-AC-11 over the shipped `{ shape, record }` contract with FR-059's identity pattern; re-word TC-050 to the assertion its test makes. Do not narrow the shipped schema back to `SemanticId` — dependency.md FND-400 established why it was widened. |
| FND-701 | File the reconciliation issue against the quoin evidence programme, name it in FR-004 Dependencies, and state in FR-004 Behavior what detects a change to FR-059's `record_shape` or identity pattern (a pinned fixture copy, or nothing, said plainly). |
| FND-702 | Add a CI job that runs `make install` and `make dev-quire` before `pytest`, or state in FR-002-CON-4 and `tests.md` Test Environment that the drift gate and every semantic row are discharged on a developer host only while `agent-ix/quire-rs#392` is open, and that the dispatch-only workflow cannot run them. |
| FND-703 | Remove `0.3.0` from FR-003 Description, Behavior and Outputs, deriving it from FR-002's rule; add a line to FR-002 Behavior naming the downstream fixture readers a bump notifies. |
| FND-704 | Mark the 19 declared-but-unpopulated keys and the four invented support shapes as reserved pending `agent-ix/quoin#335` in FR-004 Behavior, stating that a name or nesting mismatch is a schema change plus a version bump, and that no artifact detects it today. |
| FND-705 | Add a content-fix regeneration procedure to FR-002 Behavior beside the bump procedure (which files move for a single-schema correction), and note in FR-002 Description that it owns emission, the gate and two distribution channels — integrity.md FND-111's proposed split remains the cleaner option. |
| FND-706 | State in FR-002 Behavior whether the `$id` base is dereferenceable, and that a consumer resolves it against a local bundle. |
| FND-707 | Pin the Quire wheel exactly in FR-005 Inputs, and add to `tests.md` Test Environment a line per gating issue (`quire-rs#391`, `#221`, `#394`, `#392`, `quoin#335`) naming the row that flips when it lands. |
| FND-708 | Recorded, no change. Verification result only. |
