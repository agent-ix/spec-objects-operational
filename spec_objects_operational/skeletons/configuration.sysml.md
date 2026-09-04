---
id: CFG-001
title: "ArtifactStoreConfiguration"
type: configuration
object: configuration
---
<!-- configuration authoring skeleton, alternate Properties form. Declares
     exactly the same fields as configuration.md, authored as one `sysml`
     fence instead of the typed table (FR-005-AC-2). One artifact carries one
     form; the alternate is a separate file, never a second block in the same
     artifact. -->
# [CFG-001] ArtifactStoreConfiguration

## Properties

```sysml
attribute storage_root : String[1..1] { minLength: 1 }
attribute max_upload_size_mb : Integer[1..1] { min: 1, max: 4096 }
attribute checksum_algorithm : String[1..1] { enumValues: sha256|sha512 }
attribute retention_days : Integer[1..1] { min: 1 }
attribute log_level : String[1..1] { enumValues: debug|info|warn|error }
```

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
