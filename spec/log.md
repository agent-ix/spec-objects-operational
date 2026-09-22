---
type: log
title: "Update Log"
description: "Chronological log of structural changes to this bundle."
---
# Update Log

## History

* **2026-06-15** — Adopted OKF-compatible bundle structure with directory indexes.
* **2026-09-04** — Added the semantic-module contract (issue #6): US-001, FR-002..FR-005, NFR-001, IT-002, and the `usecase/` and `non-functional/` directories.
* **2026-09-22** — PLAT-974: quire 0.47.1 on `internal-pypi`. FR-005 declares `quire` as a dev dependency pinned to the `internal-pypi` source and drops the `make dev-quire` target and every `pypi.ix` reference; the quire 0.47.1 wheel is published to internal-pypi, so the `agent-ix/quire-rs#392` Out of Scope bullet in spec.md is dropped. US-001's Dependencies line is corrected to the semantic-core version and registry this module already ships (0.3.0 on GitHub Packages) and Quire 0.47.1. CI's `ci` job now calls `python-service-actions/semantic-module-ci.yml`, which runs `npm ci` before the Python suite, and `publish-to-pypi` becomes opt-in behind a `workflow_dispatch` input. No engine-gate xfail or model-table locator rename was needed here: the full local gate (pytest, schemas-check, black, ruff) was green on the first run under quire 0.47.1 and semantic-core 0.3.0.
