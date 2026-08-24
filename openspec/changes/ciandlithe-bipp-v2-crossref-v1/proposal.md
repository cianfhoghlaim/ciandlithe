# Change: ciandlithe-bipp-v2-crossref-v1

## Why

Three problems converged on 2026-08-24:

1. **The ciandlithe composite pilot (per `ciandlithe-repo-foundation-v1`) covers 7 medical-malpractice + employer-breach + discrimination cases.** These cases have political-accountability dimensions that should be cross-referenced with the new cianchosaint BIPP v2 vertical.

2. **The cianchosaint BIPP v2 vertical** (`cianchosaint-bipp-v2-spec-v1`) introduces 7 thematic cohorts that cover the political-accountability dimensions.

3. **The new BLIG v1 spec (`ciandlithe-blig-v1-spec-v1`) defines the cross-domain intelligence graph** that composes both verticals. The cross-reference is the load-bearing data that the BLIG v1 graph queries.

## What changes

- **NEW module** at `baml_src/ciandlithe/processing/bipp_v2_crossref.py` (~150 LOC) — the `BippV2CrossrefResolver` class
  - `resolve_related_cohort(ciandlithe_cohort_id) -> BippV2CohortReference`
  - The 7 ciandlithe composite pilots → the 7 BIPP v2 cohort references

## Impact

- Affected specs: **1 NEW spec** (`ciandlithe-blig-v1` + the cross-reference requirement)

## Out of scope (follow-up changes)

- The full BLIG v1 graph implementation (the BFS cross-reference query) — follow-up `ciandlithe-blig-v1-graph-v1`
- The web UI for the BLIG v1 graph — follow-up `ciandlithe-blig-web-v1`

## Dependencies

`Blocked by: ciandlithe-blig-v1-spec-v1`.
`Blocked by (soft): cianchosaint/cianchosaint@cianchosaint-bipp-v2-spec-v1` (the BIPP v2 vertical — published in cianchosaint).
`Affected repos: ciandlithe.`

## Cross-repo sync

This change touches ONLY the `ciandlithe` repo.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
openspec validate ciandlithe-bipp-v2-crossref-v1 --strict
# Expected: pass

python3 -c "
from baml_src.ciandlithe.processing.bipp_v2_crossref import BippV2CrossrefResolver
r = BippV2CrossrefResolver()
ref = r.resolve_related_cohort('pilot-sodium-valproate')
print(f'ciandlithe pilot: {ref.ciandlithe_pilot_id}')
print(f'BIPP v2 cohort: {ref.bipp_v2_cohort_id}')
print(f'leabharlann PDFs: {len(ref.leabharlann_pdf_urls)}')
"
# Expected: ciandlithe pilot: pilot-sodium-valproate, BIPP v2 cohort: roi_political_accountability, leabharlann PDFs: 6
```