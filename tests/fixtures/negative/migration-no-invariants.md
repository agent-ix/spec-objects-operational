---
id: negative-002
title: "MigrationWithoutSafetyClause"
type: migration
object: migration
expect: semantic.record-invalid
detail: 'at clauses: "clauses" is a required property'
because: "Migration.json requires at least one clause; a migration that states no safety condition states nothing a reviewer can check"
---
# [negative-002] MigrationWithoutSafetyClause

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| migration_version | String | 1..1 | pattern: /^[0-9]{14}$/ |
| target_table | String | 1..1 | minLength: 1 |
