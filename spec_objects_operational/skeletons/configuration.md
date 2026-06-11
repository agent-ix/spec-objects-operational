---
id: CFG-001
title: "Artifact-store service configuration"
artifact_type: configuration
---
<!-- configuration authoring skeleton (spec-objects-operational). Fill every
     section with substantive content. Contract (manifest body_extraction):
     - Frontmatter MUST carry id, title, and artifact_type: configuration.
     - "## Parameters" (H2) is REQUIRED; its body is extracted as `parameters`.
     - "## Settings" and "## Behavior" (H2) are optional locators; when present
       their bodies are extracted as `settings` / `behavior`.
     - Keep headings unique per level; never leave a section empty. -->
# [CFG-001] Artifact-store service configuration

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| storage_root | string | /var/lib/artifact-store | Filesystem root for blob storage |
| max_upload_size_mb | integer | 512 | Reject uploads larger than this size |
| checksum_algorithm | string | sha256 | Digest algorithm used to verify imports |
| retention_days | integer | 90 | Days before unreferenced blobs are pruned |

## Settings

| Setting | Dev | Production |
|---------|-----|------------|
| log_level | debug | info |
| replica_count | 1 | 2 |
| prune_schedule | manual | daily at 03:00 UTC |

## Behavior

The service loads its configuration once at startup and re-reads it on
`SIGHUP`. A reload that fails validation is rejected atomically: the previous
configuration stays active and the failure is logged at `error` with the
offending parameter name. Changing `storage_root` requires a full restart
because open blob handles cannot be migrated in place.
