# OpenSpec — Agent Routing

> **OpenSpec workflow** for the `ciandlithe` repo. Mirrors the Cianfhoghlaim + Cianchosaint `openspec/` convention. Every non-trivial change lives in `openspec/changes/<id>/` as a 3-artifact bundle (`proposal.md` + `tasks.md` + spec deltas) before any code is written.

## Priority quick reference

### Priority commands

```bash
openspec list --specs                   # list all capability specs
openspec list                           # list all pending changes
openspec view                           # interactive dashboard
openspec show <change-id|spec-id>       # formatted view
openspec status <change-id>             # artifact completion check
openspec validate <change-id> --strict  # MUST pass before commit
openspec validate --all --strict       # validate every change + every spec
openspec archive <change-id> --yes      # after deploy
```

### Priority mise tasks

```bash
mise run openspec:validate-all          # CI gate — every change + every spec (strict)
mise run openspec:validate <id>        # validate one change (--strict)
mise run openspec:archive <id>          # archive a deployed change
mise run openspec:view                  # interactive dashboard
mise run ciandlithe:provider:health-check  # ping the 4-tier provider chain
mise run lint:license                   # verify every DLT source URL is in the OSINT allowlist
```

### Priority specs

| Spec | One-liner |
|:--|:--|
| [`ciandlithe-pipeline`](./specs/ciandlithe-pipeline/spec.md) | The umbrella — British Isles civil-litigation pipeline (BLIP v1) |

## The 6-file change bundle

Every openspec change MUST contain:

```
openspec/changes/<change-id>/
├── proposal.md              # why + what + impact + dependencies
├── tasks.md                 # the ordered checklist
├── cross-repo-sync.md       # ONLY if change touches >1 repo
└── specs/
    └── <spec-name>/
        └── spec.md          # ADDED/MODIFIED/REMOVED Requirements + Scenarios
```

For the canonical capability spec, the per-spec directory contains:

```
openspec/specs/<spec-name>/
├── spec.md                  # the END STATE (what the system looks like post-archive)
└── AGENTS.md                # per the repo-hygiene-agent-routing convention
```

## Spec delta format

```markdown
## ADDED Requirements

### Requirement: <title>

The system SHALL ...

#### Scenario: <scenario name>

- **WHEN** ...
- **THEN** ...
- **AND** ...

## MODIFIED Requirements

### Requirement: <title> (modified)

[the full updated requirement body, prefixed with the original]

## REMOVED Requirements

### Requirement: <title> (removed)

**Reason:** ...
**Migration:** ...
```

## Cross-repo sync

If the change touches >1 repo (cianfhoghlaim + ciandlithe, OR cianchosaint + ciandlithe), the change MUST include a `cross-repo-sync.md` file listing:

1. The commit plan for each repo
2. The branch name + remote URL for each push target
3. The order of operations (which repo MUST be committed first)

The canonical pattern lives at `openspec/changes/ciandlithe-repo-foundation-v1/cross-repo-sync.md`.

## Repo hygiene

Per the cianfhoghlaim / cianchosaint convention:

- Every `openspec/specs/<spec-name>/` directory MUST contain both `spec.md` AND `AGENTS.md`.
- The `AGENTS.md` MUST be ≤30 lines. Anything longer belongs in `docs/`.
- Every openspec change MUST validate with `openspec validate <id> --strict` before commit. The CI gate is `mise run openspec:validate-all`.

## OpenSpec validation gates

| Gate | When | Tool |
|---|---|---|
| `openspec validate <change-id> --strict` | Before commit | Local CLI |
| `mise run openspec:validate-all` | CI gate | mise task |
| `mise run lint:license` | CI gate | mise task (verify OSINT allowlist) |

## Cross-references

- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../docs/USAGE-GUIDELINES.md`](../../docs/USAGE-GUIDELINES.md) — the OSINT ceiling + no-auto-submit constraint in operational terms
- [`./specs/ciandlithe-pipeline/spec.md`](./specs/ciandlithe-pipeline/spec.md) — the umbrella spec
- [`./specs/ciandlithe-pipeline/AGENTS.md`](./specs/ciandlithe-pipeline/AGENTS.md) — the per-spec agent routing