---
id: MIG-001
title: "AddArtifactChecksum"
type: migration
object: migration
---
<!-- migration authoring skeleton (spec-objects-operational). Fill the SQL
     with the real, runnable migration. Contract (manifest body_extraction):
     - Frontmatter MUST carry id, title, type: migration, object: migration.
     - "## Properties" (H2): the typed declaration of what the migration
       changes. Header exactly `Field | Type | Multiplicity | Constraints`.
       Migration.json admits ZERO identity rows and declares NO execution
       state: no applied-at timestamp, no row count, no database status. A
       consumer needing execution state reads it through the `migrates`
       reference or through an incident that references this migration.
     - "## Invariants" (H2, REQUIRED by Migration.json): at least one clause.
       A migration that states no safety condition states nothing a reviewer
       can check. One `### <clauseId>` per clause, each owning one `ocl`
       fence.
     - "## Migration" (H2, REQUIRED) MUST contain a fenced `sql` code
       block; its content is extracted as `sql`.
     - Keep the migration idempotent or guarded so reruns are safe. -->
# [MIG-001] AddArtifactChecksum

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| migration_version | String | 1..1 | pattern: /^[0-9]{14}$/ |
| target_table | String | 1..1 | minLength: 1 |
| added_column | String | 1..1 | minLength: 1 |
| backfills_existing_rows | Boolean | 1..1 | |
| rollback_strategy | String | 1..1 | enumValues: reversible\|forward_only\|compensating |

## Invariants

The safety conditions this migration preserves. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### BackfillPrecedesConstraint

```ocl
context AddArtifactChecksum
inv BackfillPrecedesConstraint:
  self.backfills_existing_rows = true
```

### RollbackIsDeclaredBeforeApply

```ocl
context AddArtifactChecksum
inv RollbackIsDeclaredBeforeApply:
  self.rollback_strategy <> 'forward_only' or self.backfills_existing_rows = true
```

## Migration

```sql
ALTER TABLE artifacts
    ADD COLUMN IF NOT EXISTS checksum_sha256 CHAR(64);

UPDATE artifacts
   SET checksum_sha256 = encode(digest(payload, 'sha256'), 'hex')
 WHERE checksum_sha256 IS NULL;

ALTER TABLE artifacts
    ALTER COLUMN checksum_sha256 SET NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_artifacts_checksum
    ON artifacts (checksum_sha256);
```

Backfills the digest for existing rows before tightening the constraint, so
the migration is safe to run against a populated production table.
