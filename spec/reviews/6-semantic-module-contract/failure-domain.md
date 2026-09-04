---
id: SR-006
title: "Failure-domain review of the #6 semantic module contract spec"
type: SpecReview
analysis: failure-domain
scope: "spec/spec.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/non-functional/NFR-001-additive-compatibility.md"
review_set: all
---
# SR-006: Failure-domain review of the #6 semantic module contract spec

## Summary

Failure-domain analysis (extension-point failure policy, entity identity,
evaluation purity, topological robustness) of the issue #6 semantic-module
contract, read against the shipped `spec_objects_operational/manifest.yaml`
(version 0.2.0, eight object types, `allowed_links`, `lint_rules`, `lexicon`),
the eight 0.2.0 skeletons, the module's own `spec/tests.md`, and the sibling
review `agent-ix/spec-objects-business` SR-002, whose dispositions this spec
has already absorbed (title identity, `--check` purity, `.gitattributes`,
fail-not-skip, refusal granularity, `quire-rs#391`).

Fourteen findings: two high, six medium, six low. Both highs sit on the
identity/purity axis the module exists to establish. The module's separation
of seven standing definitions from one observed execution is enforced only at
the level of *record keys*, and the seal that enforces it is tested with a key
(`observations`) that the seal refuses trivially; an accumulated observation,
a consumed error budget, or an applied-migration timestamp authored as an
ordinary `## Properties` row on `Configuration`, `Migration`, `Sli`, `Slo` or
`Deployment` validates today, and no criterion in the spec can fail on it.
Separately, FR-005's "typed section is the authority" rule enumerates three
overlap pairs and omits the three where the typed key is *optional* and the
kernel form *required* — alert thresholds and severities, the SLO target and
window, and the incident occurrence time — which are precisely the values the
ticket's acceptance criteria name.

## Verdict

Not ready for `spec-to-plan` until FND-200 and FND-201 are dispositioned.
FND-200 is a rule the spec states four times (spec.md Out of Scope, FR-004
Behavior, FR-004-CON-4, US-001-EX-2) and verifies nowhere in the direction an
author would actually breach it; FND-201 leaves the typed contract subordinate
to untyped prose for thresholds, windows, severities and occurrence times.
Both have a one-paragraph fix that adds rules rather than relaxing any.
FND-202..FND-207 are medium and each has a stated fix; the six low findings
are proposed additions, not blockers.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-200 | high | Purity is enforced only over record *keys*, not over `fields` items: nothing forbids an occurrence, sample, or execution-state row inside `fields` on the seven standing definitions, so `applied_at: Timestamp` on `Migration`, `consumed_budget: Decimal [1]` on `Slo`, or `last_value: Duration [ms]` on `Sli` all validate. FR-004-CON-4 constrains what a *model declares*; FR-004-AC-10 tests a record carrying `observations`, which every sealed schema refuses whatever its rules — so the criterion cannot fail and the constraint has no evidence. | FR-004 Behavior (l. 80, 85), FR-004-CON-4, FR-004-AC-10, spec.md Out of Scope, US-001-EX-2, TC-049 | correct-requirement-no-evidence |
| FND-201 | high | FR-005's typed-is-authority rule names three overlap pairs (configuration, runbook, deployment) and omits the three where the *typed* key is optional and the *kernel* form required: alert `## Flow` (the shipped skeleton's mermaid carries 14x/6x burn thresholds, 5m/1h windows and page/ticket severities) vs optional `conditions: AlertCondition[]`; the `slo` frontmatter `target`/`window` pair (asserted by FR-005 Behavior) vs optional `objective: ObjectiveDecl`; the incident `## Timeline` vs the required occurrence field. For thresholds, windows, severities and occurrence times the untyped form is the only asserted one, which inverts the rule and defeats the ticket AC. | FR-005 Behavior (kernel-section bullet, typed-authority bullet), FR-004 table rows alert/slo/incident, FR-004 Behavior (l. 86), skeletons `alert.md`, `slo.md`, `incident.md` | wrong-requirement |
| FND-202 | medium | "Occurrence identity" is used to divide the roles but is never defined, and the table contradicts it: `Deployment` is listed as a standing definition yet is the only standing definition *requiring* an identity field ("the release identity"), while `Sli` and `Slo` carry no identity rule at all, so an SLI record with an identity field validates. The stated dividing line (identity + occurrence = observed execution) therefore holds for five of the eight types. | FR-004 Behavior (l. 85), FR-004 table rows sli, slo, deployment, FR-004 Description | wrong-requirement |
| FND-203 | medium | The semantic reference keys re-declare edges the manifest `allowed_links` already types (`configures: [configurable]`, `references: [configuration]`, `migrates: [data_schema]`) with no authority rule and no rule that a semantic key's target role matches the typed link, so the two edge sets can disagree silently — the same dual-authority defect FR-005 fixes for sections, left open for links. | FR-004 Behavior (l. 84, 86), FR-003 Behavior (locators unchanged), `manifest.yaml` `object_types[].allowed_links` | missing-requirement |
| FND-204 | medium | No reference key states its admissible target type, and no key forbids self-reference or cycles. `dependsOn` (migration, slo, deployment) is an ordering edge and `escalatesTo` (alert) an escalation edge: a `dependsOn` cycle is an unorderable migration set and an `escalatesTo` cycle is a paging loop. Only `AlertCondition.sli` has a target-type reader rule; `breaches`, `remediates`, `configures`, `measures`, `constrains`, `correlates`, `triggers`, `deploys` have none. | FR-004 table (optional-key columns), FR-004 Behavior (l. 88-91) | missing-requirement |
| FND-205 | medium | Unit and window coherence is unstated: `ObjectiveDecl.unit` is optional, so a `target: 99.9` is unresolvable between percent and ratio; `AlertCondition` carries a bare `threshold: float64` with no unit at all while comparing against a united SLI; no rule ties either to the referenced SLI's measured-field `type.unit`; and the ISO 8601 duration form admits `PT0S` (a zero window) and `P1M`/`P1Y` (calendar-relative, not a fixed duration). | FR-004 Behavior (`ObjectiveDecl`, `AlertCondition`), FR-004 table rows sli, slo, alert | missing-requirement |
| FND-206 | medium | "An `EvidenceRef.record` SHALL be a `SemanticId` naming a record of the `agent-ix/quoin#267` operational evidence family" has no verification in the direction that matters: `SemanticId` admits any `ix://` URI, so FR-004-AC-11 (bare token rejected, `kind` in set) passes for a `record` naming anything at all. The issue AC "operational evidence has one canonical semantic mapping" is asserted structurally (`evidence` on one model) but unmeasured referentially. | FR-004 Behavior (l. 78-79), FR-004-AC-11, FR-004-CON-3, TC-050 | correct-requirement-no-evidence |
| FND-207 | medium | Six of the nine named negative fixtures expect the single code `semantic.record-invalid`, and FR-005-AC-5 matches on the message *containing* that code, so a fixture that fails for the wrong schema rule (or for a rule belonging to another type) still passes. The negative suite pins the eight schemas only in aggregate. | FR-005 Behavior (negative fixture bullet), FR-005-AC-5, TC-064 | correct-requirement-no-evidence |
| FND-208 | low | Skeleton `title` is overloaded: it is the artifact's human name (required locator, rendered in the H1) and, per FR-005, the semantic type token every `Type` cell resolves through. The eight shipped 0.2.0 titles are sentences, so all eight must be retitled to bare `Identifier`s; and because the token is a mutable title, any later retitle silently dangles every `Type` cell that named it, with no stability rule. | FR-005 Behavior (l. 60-61), FR-005-AC-8, skeletons `alert.md`, `deployment.md` | missing-requirement |
| FND-209 | low | This module's own lexicon defines two of its eight type names as observed executions: `deployment` as "a released, running instance of a service" and `alert` as "a fired condition requiring attention", while `Deployment` and `Alert` are classified as standing definitions. FR-003 freezes both definitions byte-identical (`deployment` is one of the three issue #5 restorations), so the module ships a vocabulary that contradicts its own role split. | FR-003 Behavior (lexicon bullets), FR-003-CON-3, FR-004 Behavior (l. 85), `manifest.yaml` `lexicon` | missing-requirement |
| FND-210 | low | Uniqueness keys inside the declaration models are unstated: two `ScopeAssignment` entries may assign `creation` and `runtime` to one `parameter`; two `RunbookStep`s may share `order: 1` or `name`; nothing says whether a runbook's procedure is ordered by `order` or by array position. A runbook is a procedure whose value is its order, yet the ordered `steps[]` is optional while the unordered `operations` is required. | FR-004 Behavior (`ScopeAssignment`, `RunbookStep`), FR-004 table row runbook | missing-requirement |
| FND-211 | low | Contradictory strategy combinations are admitted: a `RolloutDecl` whose nested `rollback.strategy` is `forward_only` declares a rollout that cannot roll back, and `canary`/`rolling` carry no step, budget, or bake-time field, so the strategy enum names an intent no consumer can act on. | FR-004 Behavior (`RollbackDecl`, `RolloutDecl`) | missing-requirement |
| FND-212 | low | `make dev-quire` has no version floor, no source pin, and no purity statement: FR-005 Inputs say "0.46.0 or later", and the fail-not-skip rule triggers only on a *missing* `extract_semantic`, so a later wheel that renames or re-severities a diagnostic silently changes what the nine negative fixtures assert, with every row still green. | FR-005 Inputs, FR-005 Behavior (`make dev-quire`, fail-not-skip bullets), tests.md Test Environment | missing-requirement |
| FND-213 | low | The marker models' discriminating keys are unstated in the spec. `@contains(IdentityField)` and `@minContains(0) @maxContains(0)` are only correct if `IdentityField` *requires* `identity` as `const: true` and `MeasuredField`/`OccurrenceField` require `type`; an open marker with an optional discriminator makes every `contains` vacuous and every `maxContains: 0` unsatisfiable against a non-empty `fields`. The emitted markers on this branch do require them, so the encoding is right today by the implementer's judgement rather than by a rule, and no AC pins it. | FR-004 Outputs (open marker schemas), FR-004 Behavior (l. 83) | missing-requirement |
| FND-214 | low | NFR-001 measures "the checked-in 0.2.0 skeleton set" and the checked-in 0.2.0 locator, lint-rule and lexicon baselines, but names no location, no capture mechanism, and no rule that the baseline is captured from the 0.2.0 tag rather than hand-written; FR-005-CON-1 places skeletons in `spec_objects_operational/skeletons/`, which is the set being rewritten. | NFR-001 Statement, NFR-001 Verification, NFR-001-AC-1..4, FR-003-AC-3 | missing-requirement |

## Finding Detail

### FND-200 (high): purity is a key rule, and its test cannot fail

The module states the purity rule four times, each time over *keys*:

- `spec.md` Out of Scope: "Accumulated observations of any kind — measured
  samples, consumed error budgets, applied-migration timestamps, database
  execution state … are refused by every model's seal".
- FR-004 Behavior: "No model SHALL declare a key for an accumulated
  observation, a measured sample, a consumed error budget, an
  applied-migration timestamp, or a database execution state".
- FR-004-CON-4: "No model SHALL declare a key holding an observation, sample,
  consumed budget, or execution timestamp."
- US-001-EX-2: an SLI carrying an `observations` key is refused.

Every one of those is true and none of them binds an author. The seal
(`unevaluatedProperties: {not: {}}`) refuses *any* undeclared key, so
`observations` is refused by all eight schemas for a reason that has nothing to
do with observations; FR-004-AC-10 and TC-049 therefore assert a property that
holds for `zzz` equally well. The criterion cannot fail while the schemas are
sealed, which is the definition of a test with no diagnostic power.

The key an author actually reaches for is a `## Properties` row, and `fields`
is declared, required, and shape-unconstrained on five of the seven standing
definitions. Under the table as written all of the following validate:

| Record | Schema | Rule that would have caught it |
|---|---|---|
| `Migration` with `applied_at : Timestamp` | `Migration.json` | none — `fields` ≥ 1, 0 identity: satisfied |
| `Slo` with `consumed_budget : Decimal(5,4) [1]` | `Slo.json` | none — it is a measured field, which `Slo` *requires* |
| `Sli` with `last_value : Duration [ms]` and `observed_at : Timestamp` | `Sli.json` | none |
| `Configuration` with `applied_at : Timestamp` | `Configuration.json` | none — 0 identity fields: satisfied |
| `Deployment` with `deployed_at : Timestamp` | `Deployment.json` | none |

The emitted schemas on this branch confirm the reading: `Migration.json`
constrains `fields` with `minItems: 1` plus `contains: IdentityField` /
`maxContains: 0` and nothing else; `Sli.json` with `minItems: 1` plus
`contains: MeasuredField`; `Slo.json` the same; neither names
`OccurrenceField`, which exists and is referenced by `Incident.json` alone.
`Migration.json`'s own `description` states "never execution state: no
applied-at timestamp, no row count, no database status" — a rule the schema
beside it does not enforce.

The last row is the sharpest: `Incident`'s occurrence rule is "≥ 1 field whose
`type.target` is `Timestamp`", and `Deployment` already requires an identity
field, so a deployment record with one timestamp row is byte-for-byte an
observed execution and validates as a standing definition. FR-004's own
Description claim — "a standing definition is refused where an observed
execution is required and the reverse" — holds in one direction only.

Fix (adds rules, relaxes none). The encoding already exists in the spec: the
zero-identity rule is written `@contains(IdentityField) @minContains(0)
@maxContains(0)`. Apply the same shape to occurrence:

1. Add to the FR-004 table's Item rules for `configuration`, `migration`,
   `sli`, `slo` and `deployment`: "0 occurrence fields". Because JSON Schema
   admits one `contains` per array, express it the way FR-004 already
   expresses the incident rule — an `@extension("allOf", …)` clause whose
   `contains` references `OccurrenceField.json` with `maxContains: 0`.
2. Add an AC per affected type asserting the *escape*, not the seal: "a
   `Migration` record whose `fields` carry a `Timestamp` row fails
   `Migration.json`", and likewise for configuration, sli, slo, deployment.
   Add the matching negative fixture (`migration-applied-timestamp.md`) to the
   FR-005 list, since this is the case an author will actually author.
3. Restate FR-004-CON-4 so it constrains the *record*, not the model: "No
   standing-definition schema SHALL accept a record whose `fields` carry an
   occurrence field", and keep the declared-key sentence as a second,
   separately-verified clause with an AC that enumerates each schema's
   declared key set against the banned list — an inspection of the emitted
   `properties` maps, which is a test that can fail.
4. Note the residual: a consumed error budget authored as a *measured* field
   (`Slo` requires ≥ 1) is indistinguishable from the objective's own
   measurement by shape alone. Either state that residual explicitly in
   FR-004 as a limit of the schema layer with the reader rule that closes it
   (`Slo.fields` declares the measured quantity, never its accumulated value),
   or bind `Slo`'s measurement to `ObjectiveDecl.sli` so the objective names
   the SLI rather than restating it.

### FND-201 (high): the typed-is-authority rule stops short of the optional keys

FR-005 Behavior states: "Where a typed section and a kernel section describe
the same declarations (the configuration `## Properties` table and its
`## Configuration` table; the runbook `## Operations` and its `## Steps`
prose; the deployment `## Operations` and its `## Topology` diagram), the
typed section SHALL be the authority". Three pairs are omitted, and in each
the typed side is an *optional* key while the kernel side is asserted by a
`required: true` locator FR-003 freezes:

- **alert**: the shipped `alert.md` `## Flow` mermaid encodes `14x`/`6x` burn
  thresholds, `5m`/`1h` windows, and page-vs-ticket severity — every field of
  `AlertCondition`. `conditions: AlertCondition[]` is optional; `## Flow` is
  required. The typed contract therefore carries none of the alert's actual
  numbers, and a `conditions` entry disagreeing with the diagram is not a
  finding anywhere.
- **slo**: FR-005 requires the skeleton keep "the frontmatter `target`/`window`
  pair" — the same two values `ObjectiveDecl` declares, with
  `objective: ObjectiveDecl` optional. Two authorities for one objective, the
  untyped one required.
- **incident**: `## Timeline` is required and carries the occurrence times in
  prose beside the one required `Timestamp` field, with no rule that they
  agree or that the field is the authority.

The ticket's own deliverable list names "thresholds, units, windows, alert
conditions, runbook steps, incident references" — the three omitted pairs are
where those live.

Fix: extend the FR-005 authority bullet to name the three pairs; add to FR-004
that `Alert` requires `conditions` with ≥ 1 item (an alert without a typed
firing condition is the placeholder the ticket forbids) and that `Slo`
requires `objective`, or, if they must stay optional while
`agent-ix/quoin#335` settles the mapping, say so in the same sentence with the
issue named, the way FR-005 already does for the `scopes` mapping. Add one
negative fixture per pair where the two forms disagree, and record in FR-005
that disagreement is unverified until the extractor reads the kernel section
(owner: `agent-ix/quoin#335`).

### FND-202 (medium): "occurrence identity" is undefined and unevenly applied

FR-004 closes its Behavior with: "`Configuration`, `Migration`, `Sli`, `Slo`,
`Alert`, `Runbook`, and `Deployment` are standing definitions and carry no
occurrence identity; `Incident` is the one observed execution and is the only
model that requires one." The table says otherwise for three of those seven:

- `deployment` requires "≥ 1 identity field (the release identity)" — a
  release identity is an occurrence identity under any reading the spec
  offers, and none is offered.
- `sli` and `slo` state no identity rule in either direction, so an SLI
  declaring `sample_id` with `identity: true` validates.

Fix: define "occurrence identity" once (an identity field co-occurring with an
occurrence field is the reading the incident row implies), then either add
"0 identity fields" to the `sli` and `slo` rows and justify the deployment
exception in the same sentence, or drop `Deployment` from the standing list
and say what makes a release identity admissible on a standing definition.
FND-200's occurrence rule and this one are the same fix applied to two axes;
disposition them together.

### FND-203 (medium): two edge layers, no agreement rule

`manifest.yaml` already types this module's links per object
(`configuration.allowed_links.configures: [configurable]`,
`references: [configuration]`, `migration.allowed_links.migrates:
[data_schema]`), and FR-003 freezes every 0.2.0 locator and rule. FR-004 adds
semantic keys of the same names (`configures`, `references`, `migrates`)
carrying `SemanticId[]`. Nothing states which layer is authoritative, that the
target of a semantic key must satisfy the `allowed_links` role for that key,
or that the two sets must agree. A future consumer reading `allowed_links`
and one reading `configures` can see different graphs from one artifact.

Fix: add to FR-004 Behavior "Where a semantic reference key shares a name with
an `allowed_links` edge, the semantic key SHALL name a target whose object
type carries the role that edge admits, and the two SHALL agree; the check is
a reader rule until `agent-ix/quoin#335` publishes the mapping", plus an AC
that the key names and the edge names are the same set.

### FND-204 (medium): the reference graphs have no target types and no cycle rules

Ten of the optional keys are `SemanticId[]` with no admissible target type;
only `AlertCondition.sli` is constrained, as a reader rule. Two of the ten are
graphs whose cycles are the classic failure of their domain:

- `dependsOn` on `migration`, `slo` and `deployment` is the ordering edge. A
  cycle makes the migration set unorderable, and nothing forbids
  `migration A dependsOn A`.
- `escalatesTo` on `alert` is the escalation edge. A cycle is a paging loop,
  which is an operational-safety failure, not a modelling nicety.

Fix: add to FR-004's reader-rule block, beside the three already there: each
reference key's admissible target object type (a one-column addition to the
table is enough), and "`dependsOn` and `escalatesTo` SHALL be acyclic and SHALL
NOT name their own artifact; JSON Schema cannot express either, so both are
reader rules for the extractor that first populates them", with a negative
fixture for a self-referencing `dependsOn` once populated.

### FND-205 (medium): thresholds and windows are numbers without units

`ObjectiveDecl` is `{ sli, target: float64, unit?: UnitSymbol, window }` and
`AlertCondition` is `{ …, threshold: float64, window, severity }`. The SLI
they reference is required to carry a measured field — a field whose
`type.unit` is present. Nothing ties the three units together, `AlertCondition`
has no unit slot at all, and `ObjectiveDecl.unit` is optional, so `target:
99.9` against an SLI measured in `[1]` is a 9,990 % objective that validates.
The window strings are "the ISO 8601 duration form", which admits `PT0S` and
the calendar-relative `P1M`/`P1Y`; a zero-length SLO window and a
month-relative burn window both pass.

Fix: make `ObjectiveDecl.unit` required, add `unit: UnitSymbol` to
`AlertCondition`, add the reader rule "`ObjectiveDecl.unit` and
`AlertCondition.unit` SHALL equal the `type.unit` of the referenced SLI's
measured field", and constrain the window pattern to the fixed-duration subset
(`PnDTnHnMnS`, non-zero), naming the exclusion of `Y`/`M` designators as the
decision it is.

### FND-206 (medium): the canonical evidence mapping is structural only

FR-004 says an `EvidenceRef.record` names a record of the `agent-ix/quoin#267`
family and that no model redeclares any field of it. The second half is
verified (AC-11, CON-3, the seal). The first half is not: `SemanticId` is a
URI pattern, so `ix://agent-ix/anything/at/all` satisfies it, and AC-11 tests
only that a *bare token* fails and that `kind` is in `EvidenceKind`. Because
the evidence family is out of scope here and not yet published, every
`EvidenceRef` in the shipped fixtures will dangle by construction, with no
diagnostic, no reader rule, and no test.

Fix: state the shape a `quoin#267` record id takes (org/repo prefix at
minimum) as a reader rule with the pattern the schema *can* express, add an AC
that the incident skeleton's `EvidenceRef.record` matches it, and record in
FR-004 Dependencies that full resolution waits on the evidence family's own
publication — so the gap is carried rather than implied.

### FND-207 (medium): the negative suite collapses onto one code

Of the nine named cases, six expect `semantic.record-invalid`: configuration
with an identity row, migration with no `## Invariants`, SLI with no unit,
alert with a `## Properties` table, runbook with no operation, incident with
no `Timestamp` row. FR-005-AC-5 requires only that the error message
*contains* that code. A fixture that fails because its frontmatter `object:`
is wrong, or because it violates a different type's rule, satisfies the
criterion. The sibling module recorded the same defect (SR-002 FND-107) and
dispositioned it by asserting the failing schema path per fixture; that
disposition is not carried here.

Fix: restate FR-005-AC-5 as "each negative fixture fails with its `expect:`
code *and* the failing schema keyword path (or the diagnostic detail) the
fixture names", and give each fixture an `expect_detail:` naming the rule it
is meant to trip.

## Checklist Coverage

### Extension points (trust boundaries)

- `make schemas` / `scripts/generate-schemas.mjs`: strict and well specified
  (compile failure, zero module models, Node floor, `--check` writes nothing,
  stale-file naming, `eol=lf`). No finding — the sibling's dispositions landed.
- `make dev-quire` and the Quire wheel: fail-not-skip is specified, the
  version floor and the diagnostic contract are not (FND-212).
- Negative fixtures' `expect:` frontmatter: strict, but the match is
  code-only and six of nine share one code (FND-207).
- Quire/Quoin refusing the manifest: strict, granularity stated per refusal
  class, both refusals silent with the engine issues named (`quire-rs#221`,
  `#394`). No finding.
- The `agent-ix/quoin#267` evidence family: referenced, never resolved; no
  failure policy for a dangling record (FND-206).

### Entity identity

- Object types: keyed by manifest `name`, eight, unique. No finding.
- Standing definition vs observed execution: the module's central identity
  claim, enforced over keys only (FND-200) and unevenly over identity fields
  (FND-202).
- Skeleton cross-references: keyed by `title`, which is overloaded and mutable
  (FND-208).
- `ScopeAssignment.parameter`, `RunbookStep.name`/`order`: no uniqueness key
  (FND-210).
- Lexicon terms vs object-type names: two collide in meaning (FND-209).
- NFR-001 baseline: population named, location not (FND-214).

### Evaluation purity

- Generator `--check` mode: declared write-free. No finding.
- Occurrence, sample, budget and execution state inside `fields`: unconstrained
  (FND-200).
- Typed section vs kernel section: rule stated, three pairs omitted (FND-201).
- Semantic reference keys vs manifest `allowed_links`: two authorities
  (FND-203).
- Clause fences carried verbatim, never evaluated (quoin FR-071-CON-1): no
  finding.
- `make dev-quire` mutates the module's Python environment with no idempotency
  statement (FND-212).

### Topological robustness

- `$ref` graph: `RolloutDecl` → `RollbackDecl` → `ClauseRef` and the eight
  object models onto semantic-core form a DAG; FR-002-AC-3 pins every `$ref`
  to a shipped sibling or semantic-core 0.1.0. No finding.
- `dependsOn` (migration, slo, deployment) and `escalatesTo` (alert): ordering
  and escalation graphs with no acyclicity or self-reference rule (FND-204).
- `RunbookStep.order`: no total-order, contiguity, or uniqueness rule, and the
  ordered form is the optional one (FND-210).
- `correlates` (incident↔incident): symmetry and self-correlation unstated;
  folded into FND-204.
- Bundle index over skeletons: lookup, not traversal. No finding.

## Proposed Additions

- **FR** (FR-004): "0 occurrence fields" item rule on the five standing
  definitions that admit `fields`, with the `allOf`/`maxContains` encoding the
  incident rule already uses; a record-level restatement of CON-4; per-type
  ACs asserting the escape rather than the seal (FND-200).
- **FR** (FR-005 and FR-004): extend the typed-is-authority bullet to the
  alert `## Flow`, slo frontmatter `target`/`window`, and incident
  `## Timeline` pairs; require `conditions` and `objective`, or name the issue
  that keeps them optional (FND-201).
- **FR** (FR-004): define "occurrence identity"; add the identity rule to the
  `sli` and `slo` rows; justify or remove the `deployment` exception
  (FND-202).
- **FR** (FR-004): agreement rule between semantic reference keys and manifest
  `allowed_links` (FND-203); admissible target object type per reference key,
  plus acyclicity and no-self-reference reader rules for `dependsOn` and
  `escalatesTo` (FND-204).
- **FR** (FR-004): required `unit` on `ObjectiveDecl` and `AlertCondition`, a
  unit-agreement reader rule against the referenced SLI, and a fixed-duration
  window pattern (FND-205); an expressible pattern and an AC for
  `EvidenceRef.record` (FND-206); uniqueness rules for `ScopeAssignment.
  parameter` and `RunbookStep.order`/`name` (FND-210); a refusal or a stated
  allowance for `forward_only` rollback inside a rollout (FND-211); the
  marker models' required discriminating keys (FND-213).
- **FR** (FR-005): per-fixture `expect_detail:` and a criterion that matches
  the failing rule, not only the code (FND-207); a title-stability rule, or a
  stable token separate from `title` (FND-208).
- **FR** (FR-005): a version floor and source pin for `make dev-quire`, and a
  statement of what a diagnostic rename does to the negative suite (FND-212).
- **FR** (FR-003) or **NFR** (NFR-001): the lexicon `deployment` and `alert`
  definitions reconciled with the role split, or the divergence recorded as
  intended (FND-209); the 0.2.0 baseline's location and capture rule
  (FND-214).

## Dispositions

| Finding | Disposition |
|---|---|
| FND-200 | PROPOSED — apply the four-part fix (occurrence item rule on the five standing definitions, escape-level ACs and fixtures, record-level restatement of CON-4 plus a declared-key inspection, and an explicit statement of the measured-field residual on `Slo`). Adds rules; relaxes none. |
| FND-201 | PROPOSED — extend the FR-005 authority bullet to the three omitted pairs and decide, per pair, whether the typed key becomes required or its optionality is carried against `agent-ix/quoin#335`. |
| FND-202 | PROPOSED — define "occurrence identity", add the `sli`/`slo` identity rule, and either justify or drop the `deployment` exception; disposition with FND-200. |
| FND-203 | PROPOSED — add the semantic-key ↔ `allowed_links` agreement rule and an AC over the key-name sets. |
| FND-204 | PROPOSED — add admissible target types per reference key and acyclicity/self-reference reader rules for `dependsOn` and `escalatesTo`. |
| FND-205 | PROPOSED — require `unit` on `ObjectiveDecl` and `AlertCondition`, add the unit-agreement reader rule, and narrow the window pattern to non-zero fixed durations. |
| FND-206 | PROPOSED — state the expressible pattern for a `quoin#267` record id, add the AC, and record full resolution as a carried dependency. |
| FND-207 | PROPOSED — adopt the sibling's SR-002 FND-107 disposition explicitly: per-fixture `expect_detail:` and a criterion over the failing rule. |
| FND-208 | PROPOSED — add a title-stability rule, or separate the semantic token from the human title. |
| FND-209 | PROPOSED — reconcile the `deployment` and `alert` lexicon definitions with the role split, or record the divergence as intended in FR-003. |
| FND-210 | PROPOSED — add uniqueness rules for `ScopeAssignment.parameter` and `RunbookStep.order`/`name`, and state the ordering authority for a runbook. |
| FND-211 | PROPOSED — refuse `forward_only` inside `RolloutDecl.rollback`, or state that the combination is admitted and what it means. |
| FND-212 | PROPOSED — pin the wheel version and source in FR-005 Inputs and state the diagnostic-rename exposure. |
| FND-213 | PROPOSED — state each marker model's required discriminating key in FR-004 Outputs. |
| FND-214 | PROPOSED — name the 0.2.0 baseline's location and require it be captured from the 0.2.0 tag. |

No spec artifact was edited by this review.
