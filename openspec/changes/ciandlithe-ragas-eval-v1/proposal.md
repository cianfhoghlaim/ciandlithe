# Change: ciandlithe-ragas-eval-v1

## Why

Three problems converged on 2026-08-24:

1. **The cianchosaint RAGAS eval pipeline** (`cianchosaint-ragas-eval-pipeline-v1`) was just shipped. Ciandlithe needs the same infrastructure for the ciandlithe composite pilots + the per-cohort BAML extraction schemas.

2. **The ciandlithe BLIG v1 graph** (per `ciandlithe-blig-v1-spec-v1`) needs RAGAS evaluation gates for every cross-domain dossier composition query.

3. **The user explicitly requested RAGAS evals for the Garda self-hosted prompt workflow** — the ciandlithe composite pilot needs the same RAGAS gates.

## What changes

- **NEW module** at `baml_src/_shared/ragas_evaluator.py` (~150 LOC) — the ciandlithe mirror evaluator
  - `CiandlitheRAGASEvaluator` class
  - `evaluate_composite_pilot()` method
  - `report_to_langfuse()` method (uses the cianchosaint langfuse_client)

## Impact

- Affected specs: **1 NEW spec delta** for the ciandlithe BLIG v1 spec

## Out of scope (follow-up changes)

- The full ciandlithe RAGAS eval dashboard — follow-up `ciandlithe-eval-web-v1`
- The per-pilot gold-standard Q/A datasets — follow-up `ciandlithe-ragas-eval-datasets-v1`

## Dependencies

`Blocked by: ciandlithe-blig-v1-spec-v1`.
`Blocked by (soft): cianchosaint/cianchosaint@cianchosaint-ragas-eval-pipeline-v1`.
`Affected repos: ciandlithe.`

## Cross-repo sync

This change touches ONLY the `ciandlithe` repo.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/ciandlithe
python3 -c "
from baml_src._shared.ragas_evaluator import CiandlitheRAGASEvaluator
e = CiandlitheRAGASEvaluator()
scores = e.evaluate_composite_pilot(
    pilot_id='pilot-qub-rvh',
    cohort='medical_malpractice',
    input_text='The QUB brain injury case ...',
    output_text='{pilot_id: pilot-qub-rvh, ...}',
)
print(f'Passed: {scores.passed_threshold}')
print(f'Scores: {scores.scores}')
"
```