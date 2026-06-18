# spec-objects-operational

> Filament Module: tier-2 operational ObjectTypes (configuration, migration, hook, job, sli, slo)

Agent-IX Filament module loaded by [`quire-cli`](https://github.com/agent-ix/quire-cli) and [`ix-spec`](https://github.com/agent-ix/ix-spec).

## Installing quire-cli

The module is consumed by `quire-cli`, published to GitHub Packages. Create an `.npmrc` so the `@agent-ix` scope resolves there:

```ini
@agent-ix:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

```bash
npm install -g @agent-ix/quire-cli
```

See https://github.com/agent-ix/quire-cli#install for details.

## Object types provided

| Object | `type:` | Description |
|--------|---------|-------------|
| Configuration | `configuration` | A service's tunable settings as a required `## Configuration` table (Name, Scope, Type, Default, Description), where Scope ∈ creation \| runtime \| session, plus optional load/reload Behavior. |
| Migration | `migration` | A database migration carrying its runnable, idempotent/guarded change in a required `## Migration` SQL code block. |
| SLI | `sli` | A service-level indicator defining what is measured (e.g. the success ratio) via a required `## Query` code block. |
| SLO | `slo` | A service-level objective with frontmatter `target` and `window` fields, describing the reliability goal and its error budget. |
| Alert | `alert` | A burn-rate/monitoring alert whose escalation logic is a required `## Flow` mermaid diagram. |
| Runbook | `runbook` | An ordered, executable response procedure captured as a required `## Steps` list with the exact operator commands. |
| Incident | `incident` | A post-incident record with a required `## Timeline` of timestamped (UTC), ordered, factual events. |
| Deployment | `deployment` | A deployment topology rendered as a required `## Topology` mermaid diagram of replicas, services, and dependencies. |

## How this module is used

### With ix-spec (recommended)

```bash
ix-spec plugin install path:../spec-objects-operational
ix-spec catalog list
ix-spec write . --types configuration,slo
ix-spec review
```

See https://github.com/agent-ix/ix-spec.

### With quire-cli directly

```bash
quire schema configuration --module ./spec_objects_operational
quire validate spec/**/*.md --module ./spec_objects_operational
quire extract SLO-001.md --module ./spec_objects_operational
```

See https://github.com/agent-ix/quire-cli#usage-instructions.

## Development

Python 3.13+ package (`spec_objects_operational`, flat layout) managed with Poetry. CI runs on GitHub Actions and publishes to Google Artifact Registry (PyPI-compatible) on `tag v*.*.*`.

```bash
make install          # install dependencies in Poetry venv
make test             # run pytest
make lint             # ruff + black check
make format           # ruff + black format
make build            # build wheel and sdist under dist/
make update-lock      # update poetry.lock
make use-local p=<name>     # switch dep to local pypi.ix
make use-upstream p=<name>  # switch dep back to upstream
make local-publish    # build and publish to local pypi.ix
```

Install from local PyPI:

```bash
pip install --index-url http://pypi.ix/root/dev/+simple/ spec_objects_operational
```

CI requires the `GCP_SERVICE_ACCOUNT_KEY` secret and the `GCP_REGION`, `GCP_PROJECT_NAME`, and `GCP_PYPI` variables for Artifact Registry publishing. Versioning is dynamic from the Git tag.
