# Tasks: ciandlithe-bipp-v2-crossref-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.4.1 installed
- [x] Verify ciandlithe-blig-v1-spec-v1 has archived

## 1. Write the cross-reference resolver

- [x] Write `baml_src/ciandlithe/processing/bipp_v2_crossref.py` (~150 LOC) — the `BippV2CrossrefResolver` class
  - `PILOT_TO_BIPP_V2_MAP` — the canonical mapping of 7 ciandlithe pilots → 7 BIPP v2 cohorts
  - `resolve_related_cohort(ciandlithe_pilot_id) -> BippV2CohortReference`
  - `resolve_all()` method

## 2. OpenSpec artifacts

- [x] Write `openspec/changes/ciandlithe-bipp-v2-crossref-v1/proposal.md` (DONE)
- [x] Write `openspec/changes/ciandlithe-bipp-v2-crossref-v1/tasks.md` (this file)
- [x] Write `openspec/changes/ciandlithe-bipp-v2-crossref-v1/cross-repo-sync.md` (DONE)
- [x] Write `openspec/changes/ciandlithe-bipp-v2-crossref-v1/specs/ciandlithe-blig-v1/spec.md` (DONE)
- [ ] Run `openspec validate ciandlithe-bipp-v2-crossref-v1 --strict`
- [ ] Run `openspec validate ciandlithe-blig-v1 --strict`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
python3 -c "
from baml_src.ciandlithe.processing.bipp_v2_crossref import BippV2CrossrefResolver
r = BippV2CrossrefResolver()
ref = r.resolve_related_cohort('pilot-sodium-valproate')
print(f'BIPP v2 cohort: {ref.bipp_v2_cohort_id}')
print(f'leabharlann PDFs: {len(ref.leabharlann_pdf_urls)}')
"
# Expected: BIPP v2 cohort: roi_political_accountability, leabharlann PDFs: 4
```