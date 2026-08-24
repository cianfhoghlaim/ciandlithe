# CIANDLITHE — Contributing

> **Per the cianchosaint `governance/CONTRIBUTING.md` precedent** — the canonical contribution guidelines for ciandlithe.

## §1 — How to contribute

### §1.1 — Add a new DLT source

1. **First**, add the URL to `dlt_sources/ciandlithe/common/osint_allowlist.yaml` via a PR + openspec change (`ciandlithe-dlt-source-policy-v1`).
2. **Then**, add the new DLT source at `dlt_sources/ciandlithe/<cohort>/<sub-nation>/<source>.py`. Mirror the existing pattern (e.g. `dlt_sources/ciandlithe/ireland/law/courts_ie.py`).
3. **Verify**, run `mise run lint:license` (the OSINT allowlist CI gate).
4. **Validate**, run `openspec validate --all --strict`.

### §1.2 — Add a new BAML extraction function

1. **First**, add a new openspec change (`ciandlithe-baml-schemas-v1` follow-up).
2. **Then**, add the new `.baml` file at `baml_src/ciandlithe/<cohort>/<file>.baml`. **Must include `osint_ceiling_enforced: bool = True` in every return schema.**
3. **Validate**, run `openspec validate --all --strict`.

### §1.3 — Add a new CocoIndex flow

1. **First**, add a new openspec change (`ciandlithe-cocoindex-flows-v1` follow-up).
2. **Then**, add the new flow file at `cocoindex_flows/ciandlithe/<cohort>_<sub_nation>_flow.py`.

### §1.4 — Add a new per-persona web app

1. **First**, add a new openspec change (`ciandlithe-per-persona-web-surfaces-v1` follow-up).
2. **Then**, add the new app at `web/apps/ciandlithe-<persona>/`. Use the TanStack Start + Convex + AG-UI + CopilotKit pattern (mirror `web/apps/ciandlithe-self-rep/`).
3. **Must** offer a "Download dossier (PDF + JSON)" button.
4. **Must NOT** offer any "Submit to court" / "File on my behalf" / "Send to court registry" affordance. Per `LICENSE.md §3.8`.

### §1.5 — Add a new FunctionTool

1. **First**, add a new openspec change.
2. **Then**, add the new FunctionTool at `agents/ciandlithe/tools/<cohort>_tool.py`.
3. **Must** include `osint_ceiling_enforced: True` + `analyst_review_required: True` flags in the response.

### §1.6 — Add a new openspec change

Per `openspec/AGENTS.md`:

```bash
openspec list --specs          # list all canonical specs
openspec list                  # list all pending changes
mkdir -p openspec/changes/<change-id>/specs/<spec-name>
# write proposal.md + tasks.md (+ cross-repo-sync.md if multi-repo) + specs/<spec-name>/spec.md
openspec validate <change-id> --strict
openspec archive <change-id> --yes  # after deploy
```

## §2 — Code style

- **Python:** ruff (line-length 100) + mypy (strict mode). See `pyproject.toml`.
- **TypeScript:** biome (the 7 web apps). See `package.json`.
- **BAML:** follow the existing per-cohort schema pattern. Always include `osint_ceiling_enforced` + `analyst_review_required` flags.
- **Markdown:** conventional commits style for PR titles. e.g. `feat(openspec): <change-id>`.

## §3 — Cross-references

- [`ROLES.md`](ROLES.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- [`../openspec/AGENTS.md`](../openspec/AGENTS.md)
- [`../LICENSE.md`](../LICENSE.md)
- [`../USAGE-GUIDELINES.md`](../USAGE-GUIDELINES.md)