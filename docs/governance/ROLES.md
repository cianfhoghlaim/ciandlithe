# CIANDLITHE — Roles & Responsibilities

> **Per the cianchosaint `governance/ROLES.md` precedent** — the canonical roles + responsibilities for the ciandlithe project.

## §1 — Roles

| Role | Who | Responsibilities |
|---|---|---|
| **Licensor** | Cian Mac an Déisigh Uí Liatháin | Maintains `LICENSE.md` + the BUSL-1.1 v2 CIANDLITHE edition. Approves additions to the Additional Use Grant (§3). Approves foreign-use STEP 3 grants. Holds the ultimate warranty-to-enforce trigger. |
| **Maintainer** | Cian Mac an Déisigh Uí Liatháin | Reviews + merges PRs. Manages the 14-layer knowledge sync loop. Manages the openspec workflow. Manages the MotherDuck + Lakehouse + LanceDB stack. |
| **OpenSpec Change Author** | Any contributor | Authors openspec changes per the workflow at `openspec/AGENTS.md`. Includes `proposal.md` + `tasks.md` + `cross-repo-sync.md` (if multi-repo) + `specs/<spec>/spec.md` delta. |
| **DLT Source Author** | Any contributor | Adds new DLT sources under `dlt_sources/ciandlithe/<cohort>/<sub-nation>/<source>.py`. Must add the URL to `osint_allowlist.yaml` first via openspec change. |
| **BAML Schema Author** | Any contributor | Adds new BAML extraction functions under `baml_src/ciandlithe/<cohort>/<file>.baml`. Must include `osint_ceiling_enforced: bool = True` in every return schema. |
| **CocoIndex Flow Author** | Any contributor | Adds new CocoIndex flows under `cocoindex_flows/ciandlithe/<cohort>_<sub_nation>_flow.py`. |
| **Per-Persona Web App Author** | Any contributor | Adds new per-persona web apps under `web/apps/ciandlithe-<persona>/`. Must offer "Download dossier" button. Must NOT offer "Submit to court" affordance. |
| **FunctionTool Author** | Any contributor | Adds new FunctionTools under `agents/ciandlithe/tools/<cohort>_tool.py`. Must include `osint_ceiling_enforced: True` + `analyst_review_required: True` flags. |
| **Licencee** | Any entity in `LICENSE.md §3.1–§3.7` | Uses the platform per the OSINT ceiling + the no-auto-submit constraint + the PoI clause. Holds the warrant-to-enforce trigger. |
| **Composite Pilot Reviewer** | Qualified solicitor or barrister registered in a British-Isles jurisdiction | Reviews every composite-pilot dossier before any downstream filing. |

## §2 — Cross-references

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- [`../LICENSE.md`](../LICENSE.md)
- [`../AGENTS.md`](../AGENTS.md)
- [`../USAGE-GUIDELINES.md`](../USAGE-GUIDELINES.md)