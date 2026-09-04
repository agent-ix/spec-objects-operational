---
id: CFG-001
title: "ArtifactStoreConfiguration"
type: configuration
object: configuration
---
<!-- configuration authoring skeleton (spec-objects-operational). Fill every
     section with substantive content. Contract (manifest body_extraction):
     - Frontmatter MUST carry id, title, type: configuration, AND
       object: configuration (the `object:` key is what makes Quire run the
       semantic layer on the document).
     - "## Properties" (H2): the typed declaration. Header exactly
       `Field | Type | Multiplicity | Constraints`, one row per parameter.
       Configuration.json admits ZERO identity rows: a parameter set is keyed
       by the object it configures, not by itself.
     - "## Configuration" (H2, REQUIRED): the human-facing table with headers
       exactly Name | Scope | Type | Default | Description and at least one
       data row. Scope carries the semantic as data:
         creation — fixed when the instance/object is created (reloptions,
                    deploy values); changing it means rebuild/redeploy.
         runtime  — tunable on a running system (GUCs, admin toggles).
         session  — per-session/per-request overrides.
       Scope values are checked by the `configuration-scope` lint rule
       (`quire lint`). This table is a derived view of "## Properties"; the
       typed table is the authority.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one `ocl` fence.
     - "## Behavior" (H2, optional): load/reload semantics, validation,
       precedence rules.
     - Keep headings unique per level; never leave a section empty. -->
# [CFG-001] ArtifactStoreConfiguration

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| storage_root | String | 1..1 | minLength: 1 |
| max_upload_size_mb | Integer | 1..1 | min: 1, max: 4096 |
| checksum_algorithm | String | 1..1 | enumValues: sha256\|sha512 |
| retention_days | Integer | 1..1 | min: 1 |
| log_level | String | 1..1 | enumValues: debug\|info\|warn\|error |

## Configuration

| Name | Scope | Type | Default | Description |
|------|-------|------|---------|-------------|
| storage_root | creation | string | /var/lib/artifact-store | Filesystem root for blob storage |
| max_upload_size_mb | runtime | integer | 512 | Reject uploads larger than this size |
| checksum_algorithm | creation | string | sha256 | Digest algorithm used to verify imports |
| retention_days | runtime | integer | 90 | Days before unreferenced blobs are pruned |
| log_level | session | string | info | Per-connection log verbosity override |

## Invariants

The clauses the ArtifactStoreConfiguration declaration enforces. Each clause
owns one `ocl` fence under its own `### <clauseId>` heading; the fence text is
carried verbatim and never evaluated here.

### UploadLimitExceedsNoRetention

```ocl
context ArtifactStoreConfiguration
inv UploadLimitExceedsNoRetention:
  self.retention_days > 0 and self.max_upload_size_mb > 0
```

### CreationScopedValuesNeedRestart

```ocl
context ArtifactStoreConfiguration
inv CreationScopedValuesNeedRestart:
  self.storage_root->notEmpty() implies self.checksum_algorithm->notEmpty()
```

## Behavior

The service loads its configuration once at startup and re-reads it on
`SIGHUP`. A reload that fails validation is rejected atomically: the previous
configuration stays active and the failure is logged at `error` with the
offending parameter name. Changing any `creation`-scoped value requires a
full restart because open blob handles cannot be migrated in place.
