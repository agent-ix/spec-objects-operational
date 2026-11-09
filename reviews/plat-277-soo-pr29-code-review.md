---
id: SR-102
title: "Code review — spec-objects-operational PR #29 (PLAT-277 F1 optional record keys)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-operational; typespec/main.tsp, spec_objects_operational/schemas/*.json, tests/test_role_schemas.py, tests/test_skeletons_semantic.py, tests/fixtures/negative/"
review_set: subset
---
# Code review — spec-objects-operational PR #29 (PLAT-277 F1)

## Summary

Ticket: PLAT-277 (finding F1). Diff `origin/main...adaac81`: eight TypeSpec
models drop `required` on `fields` / `clauses` / `operations`, the eight
emitted schemas lose their `required` arrays, one negative fixture is deleted,
and the role-schema tests flip their absent-key assertions and gain TC-092.

Verified independently:

- Every relaxed key is fed only by a `required: false` locator in
  `spec_objects_operational/manifest.yaml` (properties/invariants/operations
  for all eight types, lines 93-331). No locator or construct is touched.
- Item rules (`minItems`, `contains`, the occurrence `allOf`) are unchanged in
  every schema; only the `required` arrays are removed.
- Regeneration: fetched the real pinned `@agent-ix/semantic-core@0.3.2` from
  GitHub Packages (sha512 equals `package-lock.json` integrity), ran `npm ci`,
  then `node scripts/generate-schemas.mjs --check` (27 match) and a full
  regenerate with clean `git status`, on both the PR head and `origin/main`.
  The coder's 0.3.3-relabelled emission is therefore confirmed byte-for-byte
  against the real toolchain.
- Tests (quire 0.54.0 wheel, the only one reachable): PR head 145 passed /
  6 failed; `origin/main` 144 passed / 6 failed. The 6 failing tests are the
  same set with identical error lines on both trees (incident skeleton
  `semantic.record-invalid`, alert-with-properties detail mismatch, unhashable
  dict, empty extraction). Pre-existing engine skew, not introduced here.
- FCD construct consistency (filament-core-data
  `crates/extraction-frontend/src/constructs.rs` `shape()`): the construct a
  type lowers to comes from its manifest `object_types[].construct` block
  (`bundle.rs` `archetype.construct()`). `spec_objects_operational/manifest.yaml`
  declares no `construct:` for any type, on `origin/main`, on the PR head, or
  on any remote branch. For all eight types (configuration, migration, sli,
  slo, alert, runbook, incident, deployment), `shape()` therefore takes its
  "object type with no declaration keeps the record" path. No
  `min_clauses` / `identity_field_required` / `occurrence_field_required` /
  `min_operations` rule applies, so the relaxation does not let `quire validate`
  pass a document that FCD lowering then refuses. Consistent for every type,
  no finding. If a construct is added later with one of those rules, the
  matching locator must become `required: true` at the same time.
- With quire 0.54.0, `runbook-no-operations` still fails with its
  `at operations: [] has less than 1 item` detail, and the deleted
  `migration-no-invariants` fixture no longer yields `semantic.record-invalid`.

## Verdict

**CONDITIONAL** — no high finding. Two mediums (stale schema descriptions,
TC-092 asserting different cases than its ACs) and one low ceremony item.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | The TypeSpec doc comments, which the emitter copies into each shipped schema's `description`, still state the removed rule: Migration "`clauses` is required because…", Slo "`clauses` is required because…", Alert "`clauses` is required and carries the condition", Runbook "`operations` is required". The file header (line 12, "type-specific required keys") and line 20 / 256 / 455 ("the only model that requires…") also describe a required set that no longer exists. Shipped `Migration.json`, `Slo.json`, `Alert.json`, `Runbook.json` now contradict their own `required`-free bodies. | typespec/main.tsp:12, typespec/main.tsp:291, typespec/main.tsp:352, typespec/main.tsp:383, typespec/main.tsp:401 | wrong-requirement |
| FND-002 | medium | TC-092 does not assert what its two tagged ACs say. FR-006-AC-2 names "an `Incident` without an occurrence field", but the test sends `{"fields": [OCCURRENCE]}` — an occurrence field with no identity — so it fails on the identity rule, not the occurrence rule. FR-006-AC-1's "a record lacking `fields`, `clauses` or `operations` validates" half is never exercised in TC-092: it only checks `schema.get("required")` is falsy; the validating calls live in TC-041..049 tagged to FR-004. | tests/test_role_schemas.py:488-501 | correct-requirement-no-evidence |
| FND-003 | low | Ceremony: `assert len(fixtures) >= 9` is a file count. It does not prove the nine named cases exist (any nine files pass), and the real checks — `seen == expected_codes` and the unique-`detail` assertion — already carry the value. The PR re-tuned the number from 10 to 9 instead of removing it. | tests/test_skeletons_semantic.py:155 | wrong-requirement |
