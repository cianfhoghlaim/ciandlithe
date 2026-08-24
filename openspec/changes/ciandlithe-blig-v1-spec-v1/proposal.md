# Change: ciandlithe-blig-v1-spec-v1

## Why

Two problems converged on 2026-08-24:

1. **The ciandlithe composite pilot (per `ciandlithe-repo-foundation-v1`) covers 7 medical-malpractice + employer-breach + discrimination cases.** But there's no cross-reference to the political-accountability context that drives these cases (e.g. the sodium-valproate HSE investigation is politically covered up).

2. **The cianchosaint BIPP v2 vertical** (`cianchosaint-bipp-v2-spec-v1`) introduces 7 thematic cohorts that cover the political-accountability dimensions of the ciandlithe cases. The BLIG v1 composes both verticals.

## What changes

- **NEW spec** `openspec/specs/ciandlithe-blig-v1/spec.md` — the British Isles Law Intelligence Graph umbrella
- **NEW spec** `openspec/specs/ciandlithe-blig-v1/AGENTS.md` — the per-spec agent routing

## Impact

- Affected specs: **1 NEW spec** (`ciandlithe-blig-v1`)

## Out of scope (follow-up changes)

- The actual graph implementation (the BFS cross-reference query) — follow-up `ciandlithe-blig-v1-graph-v1`
- The Convex schema for the BLIG v1 graph — follow-up `ciandlithe-convex-blig-v1`

## Dependencies

`Blocked by: cianlithe-repo-foundation-v1` (archived 2026-08-24).
`Blocked by (soft): cianchosaint/cianchosaint@cianchosaint-bipp-v2-spec-v1` (the BIPP v2 vertical — published in cianchosaint; cross-repo reference).
`Affected repos: ciandlithe.`

## Cross-repo sync

This change touches ONLY the `ciandlithe` repo.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
openspec validate ciandlithe-blig-v1-spec-v1 --strict
# Expected: pass

openspec validate ciandlithe-blig-v1 --strict
# Expected: pass
```