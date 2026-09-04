---
id: FR-002
title: "Emit the module's JSON Schemas from a TypeSpec package importing semantic-core"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-operational/US-001"
    type: "implements"
  - target: "ix://agent-ix/filament-core-data/FR-033"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-operational/FR-004"
    type: "depends_on"
---
# FR-002: Emit the module's JSON Schemas from a TypeSpec package importing semantic-core

## Description

The module build SHALL emit one JSON Schema 2020-12 document per operational
object type from a TypeSpec source that imports `@agent-ix/semantic-core`
0.1.0, using the official `@typespec/json-schema` emitter at a pinned
toolchain, into `spec_objects_operational/schemas/`, so that the shipped
schema is the compiled one and any drift between source and shipped bytes
fails the build.

## Inputs

- `typespec/main.tsp`: namespace `AgentIx.SpecObjects.Operational`, decorated
  `@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-operational/<version>/")`
  where `<version>` is the manifest `version`.
- `@agent-ix/semantic-core` 0.1.0 from npm.ix (`FieldDecl`, `TypeRef`,
  `Multiplicity`, `ConstraintDecl`, `RelationDecl`, `OperationDecl`,
  `ClauseRef`, `EnumValue`, `DefaultDecl`, `KernelScalar`, `Identifier`,
  `SemanticId`, `UnitSymbol`).
- `@typespec/compiler` 1.15.0, `@typespec/json-schema` 1.15.0 and
  `@agent-ix/semantic-core` 0.1.0 as exact `devDependencies` in `package.json`,
  resolved through `package-lock.json`: all three are build inputs of the
  emission step, and the published artifact is Markdown and JSON, so none is a
  runtime dependency of a consumer.
- `scripts/generate-schemas.mjs` (the generator) and `scripts/stage-npm.mjs`
  (the npm staging script), both Node built-ins only.
- Node 20 or later, the runtime `@typespec/compiler` 1.15.0 requires.

## Outputs

- `spec_objects_operational/schemas/<Model>.json`, one per model of the module
  namespace, rendered as two-space JSON with a trailing newline.
- `spec_objects_operational/schemas/toolchain.json`: compiler and emitter names
  and versions, the `$id` base, the emitted file list, the normalization record
  (name, version, applied, rewritten files), and `sha256:<hex>` over the
  emitted files.
- The `data_schema.digest` of every exported object type in `manifest.yaml`,
  rewritten to the SHA-256 of the shipped file bytes.

## Behavior

- `make install` SHALL install the TypeSpec toolchain with `npm ci` alongside the Python dependencies, so `make lint` — which runs `make schemas-check` — has the compiler and emitter it needs; without it the drift gate fails for a missing toolchain rather than for drift.
- `make schemas` SHALL run `node scripts/generate-schemas.mjs`.
- The generator SHALL compile `typespec/` with `tsp compile`, keep only the emitted files whose `$id` starts with the module base, and discard the re-emitted semantic-core files.
- If the emitter leaves any `$id` or `$ref` relative, then the generator SHALL rewrite it to `<base><file>` (module models) or `https://schemas.agent-ix.org/semantic-core/0.1.0/<file>` (semantic-core models) and record each rewrite in `toolchain.json`.
- When no `$id` or `$ref` is relative, the generator SHALL record the normalization as `applied: false`.
- If `tsp compile` fails or emits no module model, then the generator SHALL exit non-zero without touching the committed output.
- If `node` is older than 20 or `tsp` is not resolvable, then the generator SHALL exit non-zero naming the required Node version or the missing binary.
- In `--check` mode the generator SHALL write no file, neither under `spec_objects_operational/schemas/` nor in `manifest.yaml`.
- Every emitted schema SHALL declare `$schema: https://json-schema.org/draft/2020-12/schema` and `$id: https://schemas.agent-ix.org/agent-ix/spec-objects-operational/<manifest version>/<Model>.json`.
- The `$id` base SHALL embed the manifest `version`, which is the decision this module records rather than a side effect: it matches the semantic-core bundle convention (`https://schemas.agent-ix.org/semantic-core/0.1.0/`), and it makes one schema URL name exactly one immutable byte sequence, so a downstream fixture reader that pinned a version can never silently read a later version's bytes under the same URL. The cost — every bump rewrites every `$id`, `$ref`, digest and `toolchain.json` — is accepted and discharged by the bump procedure below, not avoided by a version-less base.
- If the manifest `version` changes, then the bump procedure SHALL be: edit the `@jsonSchema` base in `typespec/main.tsp` and the manifest `version` in the same commit, run `make schemas`, and commit the re-emitted schemas, the rewritten `$id` and `$ref` values, the regenerated `data_schema.digest` values and `toolchain.json` together; a commit that carries one half of the pair is refused by `make schemas-check`.
- No acceptance criterion, test, or fixture SHALL hard-code the version segment of the `$id` base.
- Each acceptance criterion, test, and fixture SHALL read the version segment of the `$id` base from the manifest `version`.
- Every `$ref` in an emitted schema SHALL name either a sibling `https://schemas.agent-ix.org/agent-ix/spec-objects-operational/<manifest version>/<File>.json` that ships in `schemas/`, or `https://schemas.agent-ix.org/semantic-core/0.1.0/<Model>.json`.
- If the `@jsonSchema` base version in `typespec/main.tsp` differs from the manifest `version`, then the generator SHALL fail naming both values.
- `make schemas-check` SHALL run the generator with `--check`.
- `make lint` SHALL run `make schemas-check`, so a `typespec/` edit that was never regenerated fails before push rather than at review.
- If any emitted file differs from the committed output, a committed file under `spec_objects_operational/schemas/` is stale (it has no emitted counterpart in this run), `toolchain.json` differs, or a manifest digest differs from the shipped bytes, then the check SHALL exit non-zero naming each such file.
- If nothing differs, then the check SHALL exit zero.
- The generator SHALL write files under `spec_objects_operational/schemas/` only.
- The generator SHALL edit `manifest.yaml` only at `data_schema.digest` values.
- The Python package SHALL include `spec_objects_operational/schemas/*.json` in the wheel and sdist.
- The repository SHALL mark `*.json`, `*.tsp`, `*.yaml` and `*.md` as `eol=lf` in `.gitattributes`, so a checkout with `autocrlf` cannot change the digested bytes of a schema, a source, the manifest, or a skeleton.
- `scripts/stage-npm.mjs` SHALL copy `schemas/` beside `manifest.yaml` at pack time, so the npm tarball ships the schemas the manifest references.
- `scripts/stage-npm.mjs --clean` SHALL run at `postpack` and remove the three staged paths it created at the repository root (`manifest.yaml`, `schemas/`, `skeletons/`), because a `manifest.yaml` left at the root makes every Filament tool discover the repository itself as a second module and an unrelated `quire validate` then fails with "no archetype registered".
- The clean step SHALL remove only the paths the pack staged, never the inner `spec_objects_operational/` sources it copied from.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-002-CON-1 | The build SHALL use the official `@typespec/json-schema` emitter only; no custom emitter and no hand-edited emitted file. | Architecture | Inspection |
| FR-002-CON-2 | The repository SHALL carry no `.npmrc`, no `file:` or `link:` dependency, and no upper version bound on the TypeSpec toolchain beyond the exact pin. | Packaging | Test |
| FR-002-CON-3 | Emission SHALL be deterministic: two runs over one source produce byte-identical files. | Integrity | Test |
| FR-002-CON-4 | `package-lock.json` SHALL resolve every public package from `registry.npmjs.org`; `@agent-ix/semantic-core` resolves from npm.ix until `agent-ix/filament-core-data#11` publishes it, so `make schemas`/`make schemas-check` run on a machine whose user-level npm config routes `@agent-ix` to npm.ix, not in the GitHub workflow. | Packaging | Inspection |
| FR-002-CON-5 | The `$id` base SHALL embed the manifest `version`, bumped as one atomic regeneration (source base, manifest version, schemas, digests, `toolchain.json` in one commit). | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-002-AC-1 | After `make schemas`, `spec_objects_operational/schemas/` holds exactly the twenty-seven files `toolchain.json` lists — the eight object-type models plus the nineteen support models [FR-004](./FR-004-role-schemas.md) names, with compiler 1.15.0 and emitter 1.15.0 recorded. | Test |
| FR-002-AC-2 | Every shipped schema declares the 2020-12 `$schema` and the `$id` `https://schemas.agent-ix.org/agent-ix/spec-objects-operational/<manifest version>/<Model>.json` matching its file name, with the version segment read from `manifest.yaml` rather than hard-coded. | Test |
| FR-002-AC-3 | Every `$ref` across the shipped schemas resolves to a shipped sibling or to semantic-core `0.1.0`; a `$ref` to any other host or version is absent. | Test |
| FR-002-AC-4 | `make schemas-check` on the committed tree exits zero; after one byte of any shipped schema or one manifest digest is changed, it exits non-zero naming that file. | Test |
| FR-002-AC-5 | A `@jsonSchema` base whose version segment differs from the manifest `version` makes the generator fail naming both versions. | Test |
| FR-002-AC-6 | The wheel built by `make build` contains `spec_objects_operational/schemas/<Model>.json` for every exported model. | Test |
| FR-002-AC-7 | The npm tarball produced by `npm pack` contains `manifest.yaml` and a sibling `schemas/<Model>.json` for every exported model, so a manifest-relative `schema:` path resolves inside the tarball. | Test |
| FR-002-AC-8 | Bumping the manifest `version` and the `@jsonSchema` base together and re-running the generator yields every `$id` and every sibling `$ref` at the new version, `toolchain.json` recording the new base, and manifest digests equal to the new bytes; `make schemas-check` then exits zero, while bumping only one of the pair exits non-zero. | Test |
| FR-002-AC-9 | `make schemas-check` on a committed tree carrying an extra `spec_objects_operational/schemas/Stale.json` with no emitted counterpart exits non-zero naming that file, and writes nothing. | Test |
| FR-002-AC-10 | A generator run over a scratch copy of the tree writes only under `spec_objects_operational/schemas/` and, in `manifest.yaml`, only at `data_schema.digest` lines: every other tracked file is byte-identical afterwards. | Test |
| FR-002-AC-11 | `make lint` runs `make schemas-check`: with one shipped schema mutated, `make lint` exits non-zero naming that file. | Test |
| FR-002-AC-12 | `.gitattributes` marks `*.json`, `*.tsp`, `*.yaml` and `*.md` `eol=lf`, so a checkout with `autocrlf` cannot change the digested bytes. | Test |
| FR-002-AC-13 | `make install` installs the TypeSpec toolchain: after it, `node_modules/@typespec/compiler` and `node_modules/@agent-ix/semantic-core` exist at the pinned versions and `make schemas-check` exits zero. | Test |
| FR-002-AC-14 | After `npm pack`, none of `manifest.yaml`, `schemas/` or `skeletons/` remains at the repository root, and `spec_objects_operational/manifest.yaml`, `spec_objects_operational/schemas/` and `spec_objects_operational/skeletons/` are byte-identical to their pre-pack state. | Test |

## Dependencies

- **Upstream**: [US-001](../usecase/US-001-declare-operational-objects-against-semantic-core.md); semantic-core FR-033 (`ix://agent-ix/filament-core-data/FR-033`); the generation pattern this module shares with `agent-ix/spec-objects-business`
- **Upstream (models)**: [FR-004](./FR-004-role-schemas.md) declares the models this build emits
- **Downstream**: [FR-003](./FR-003-semantic-manifest-contract.md)
