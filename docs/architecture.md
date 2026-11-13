# ciandlithe — Architecture Overview (1-page)

> **Per the repo-hygiene-agent-routing spec**, this 1-page architecture overview is the entry point for the per-sister canonical spec at [`../openspec/specs/ciandlithe-architecture/spec.md`](../openspec/specs/ciandlithe-architecture/spec.md).

## What is ciandlithe?

**Ciandlíthe** = Irish Gaelic "cian" (long/far/longing) + "dlíthe" (laws / statutes) → "distant laws / far statutes". Mirrors *Cianfhoghlaim* = "cian" + "fhoghlaim" (learning).

**Scope (per `LICENSE.md`)**: OSINT-only British-Isles civil-litigation data platform. Strictly restricted to courts, tribunals, regulators, ombudsmen, law societies, bar councils, legal-aid bodies, coroners, health-service complaints bodies, and registered claimant-representation clinics of the Republic of Ireland, the United Kingdom of Great Britain and Northern Ireland (including the devolved administrations of Scotland, Wales, and Northern Ireland), and the Crown Dependencies (Jersey, Guernsey, Isle of Man). Foreign use requires satisfaction of the 3-step gate (Explain → Do us a favour → Maybe).

## Sister-repo position (per the multi-repo scaffold)

Per the `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` parent change, ciandlithe is the BI legal-system sister repo:

| Repo | Owns |
|---|---|
| `cianfhoghlaim` | Cross-cutting hub (`common/`, `lakehouse/`, `jobs/`) + the BIEP flagship (`british_isles/_cross/`, `british_isles/ireland/education/`) |
| `tuatha` | BI Educational MMO — 8 NCCA subject agents + 40 per-subject tools + 3 educational + 4 BIEP hackathon + 1 media_intel pipeline |
| **`ciandlithe`** | **BI legal-system vertical — WRC + UK statute + courts + tribunals + regulators + ombudsmen + law societies + bar councils + legal-aid bodies + coroners + health-service complaints bodies + claimant-representation clinics** |
| `cianchosaint` | BI law-enforcement + civil protection — evidence-collection for law-enforcement purposes |
| `ciancheiltis` | Pure Irish-language datasets + non-educational Celtic-language pipelines (deferred — Phase 4) |

## The 6 cascade contracts (per parent change §15-§19)

1. **`dlt-sister-sync-reusable-workflow`** — `.github/workflows/dlt-sister-sync-call.yml` calls cianfhoghlaim's reusable workflow
2. **`cognee-twin-clusters`** — 6 ciandlithe_* Cognee clusters
3. **`dlt-nightly-mirror-merge`** — ciandlithe emits `_sister_refs/ciandlithe/...` diffs
4. **`dlt-destination-versioning-contract`** — pins `cianfhoghlaim >=<minor>,<<next-minor`
5. **`agent-observability-ciandlithe`** — `ciandlithe_*` Langfuse project + project-scoped API key
6. **`openspec-per-sister-sync`** — per-sister `openspec/AGENTS.md` + `openspec/specs/`

## Skeleton shape

```
ciandlithe/
├── pyproject.toml          # uv workspace member, depends on cianfhoghlaim (FUTURE)
├── mise.toml               # ciandlithe:<verb>:* task namespace
├── README.md
├── AGENTS.md
├── LICENSE.md              # BUSL-1.1
├── openspec/
│   ├── AGENTS.md           # per-repo openspec conventions
│   ├── specs/
│   │   ├── ciandlithe-architecture.md  # per-sister canonical spec (NEW)
│   │   ├── ciandlithe-pipeline/        # BLIP v1 umbrella spec
│   │   └── ...
│   └── changes/
│       └── 2026-08-24-ciandlithe-init-v1/   # this init change
├── dlt_sources/
│   ├── _cross/             # JurisdictionPipelineBase re-export + cross-repo helpers
│   ├── common/             # 4 canonical helpers (endpoint_recovery, firecrawl_source, http_client, destinations_cianfhoghlaim)
│   └── ciandlithe/         # the BI legal-system vertical (per-jurisdiction)
│       ├── ireland/
│       ├── uk/
│       ├── ni/
│       ├── scotland/
│       ├── wales/
│       ├── england/
│       ├── crown_dependencies/
│       └── common/         # the per-sister OSINT allowlist
├── baml_src/               # the BAML extraction contracts (per-sister schemas)
├── orchestration/          # the Dagster asset groups
├── cocoindex_flows/        # the CocoIndex v1 Apps
├── notebooks/              # the per-jurisdiction marimo dives
├── ci/                     # the CI conventions README
└── docs/
    ├── AGENTS.md           # per-directory conventions
    └── architecture.md     # this file
```

## Cross-references

- [`../openspec/specs/ciandlithe-architecture/spec.md`](../openspec/specs/ciandlithe-architecture/spec.md) — the per-sister canonical spec
- [`../openspec/specs/ciandlithe-pipeline/spec.md`](../openspec/specs/ciandlithe-pipeline/spec.md) — the BLIP v1 umbrella spec
- [`../openspec/changes/2026-08-24-ciandlithe-init-v1/proposal.md`](../openspec/changes/2026-08-24-ciandlithe-init-v1/proposal.md) — the init change
- [`../openspec/AGENTS.md`](../openspec/AGENTS.md) — the per-repo openspec conventions
- [`../AGENTS.md`](../AGENTS.md) — the canonical agent routing
- [`../LICENSE.md`](../LICENSE.md) — the load-bearing legal document