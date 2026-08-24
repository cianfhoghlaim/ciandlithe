# CIANDLITHE — Composite Pilot Case Study

> Per the openspec/changes/ciandlithe-composite-pilot-workflow-v1/
> specs/ciandlithe-composite-pilot-workflow/spec.md, this case study
> is the canonical narrative for the composite pilot workflow.

## Why the composite pilot?

The CIANDLITHE composite pilot exercises **all 7 BLIP v1 cohorts × 4 jurisdictions** via 7 leabharlann PDFs (one per pilot party). Each pilot party is **single-entity, allowlist-bounded**, mirroring how the Reform UK pilot was single-entity in cianchosaint (per `cianchosaint/docs/case-study/reform-uk-pilot.md`).

**The verified user use case.** On 2026-08-24 the user explicitly requested a law-focused sibling repo to cianfhoghlaim + cianchosaint, citing the Gemini Deep Research output documents in `leabharlann/gemini_deep_research/law/` + `medical/` as the canonical source-of-truth for case-study material covering:

- Medical malpractice (QUB / Royal Victoria Hospital brain injury, sodium valproate / HSE misprescription)
- Employer / breach of contract (Eric case)
- Garda discrimination / data-access
- Education discrimination (DkIT disability, NUIG rejection)
- Admission breach (UCL offer / DBS)

The composite pilot elevates these 7 case studies into the canonical pilot set. Other British-Isles litigation bodies (courts, tribunals, law societies, legal-aid clinics) may use the platform for any civil-litigation preparation within the OSINT ceiling + the no-auto-submit constraint.

**The OSINT allowlist.** Every leabharlann PDF cited in this case study is a read-only reference — the pilot does NOT generate new factual claims from the PDFs; it only references them in the `source_pdf_urls` field of the `CompositePilotDossier` record. The `osint_ceiling_enforced: True` + `analyst_review_required: True` flags are enforced at every layer.

**The no-automated-form-submission constraint.** Per LICENSE.md §3.8, the platform NEVER directly submits forms to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk. The pilot generates a dossier (PDF + JSON) for manual review by the claimant or their solicitor.

**The Person-of-Interest clause.** Per LICENSE.md §5.2, every extraction that names a private individual (not a public official) is marked `analyst_review_required: True` and is NOT auto-rendered in any shared view. The composite pilot's FunctionTool response includes a `[redacted per PoI clause]` placeholder for any named private claimant/defendant; the full name appears ONLY in the leabharlann PDF source-of-truth (which the user has separate, more private access to via the `stedding/private_case_evidence/` volume — NOT in the open repo).

## The 7 composite-pilot parties

| # | Pilot party | Cohort | Sub-nation | Leabharlann PDF (read-only context) |
|--:|---|---|---|---|
| 1 | QUB / Royal Victoria Hospital brain-injury | MedicalMalpractice | NI | `law/qub_royal_victoria_malpractice.pdf` + `medical/misdiagnosis_brain_damage_recovery.pdf` + `law/maximizing_civil_suit_damages_against_qub.pdf` |
| 2 | Eric (employer / breach of contract) | EmployerBreach | Cross-border NI ↔ ROI | `law/suing_ceo_for_breach_abuse_damages.pdf` + `law/cross_border_legal_action_research.pdf` + `law/monroes.pdf` |
| 3 | Garda discrimination / data-access | GardaDiscrimination | ROI | `law/garda_corruption_and_data_access.pdf` + `law/garda_data_and_accommodation_request.pdf` + `law/garda_brutality_dual_citizenship_and_justice.pdf` |
| 4 | DkIT disability / education complaint | EducationDiscrimination | ROI | `law/discrimination_case_strategy_university_of_galway.pdf` + `law/cbd_discrimination_lawsuit_preparation.pdf` + `law/challenging_university_rejection_and_ombudsman_decision.pdf` |
| 5 | NUIG / UoG rejection + abuse of power | EducationDiscrimination | ROI | `law/discrimination_case_strategy_university_of_galway.pdf` + `law/cbd_dispensary_manager_discrimination_lawsuit.pdf` |
| 6 | UCL offer / DBS | AdmissionBreach | England | `law/ucl_sar_equality_act_claim.pdf` |
| 7 | Sodium valproate / HSE misprescription | MedicalMalpractice | ROI | `medical/irish_sodium_valproate_inquiry_and_healthcare.pdf` + `medical/sodium_valproate_lawsuits_and_inquiries.pdf` + `medical/essential_tbi_medication.pdf` |

## Inputs to the workflow

The composite pilot workflow consumes three input layers, in order of increasing breadth.

### Layer 1 — The leabharlann PDF (read-only context)
For each pilot party, the canonical leabharlann PDF is the source-of-truth. The FunctionTool NEVER modifies the PDF; it only references the PDF's URL in the `source_pdf_urls` field of the `CompositePilotDossier` record.

### Layer 2 — The BAML extraction (`ExtractCompositePilotDossier`)
The `baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml` file defines:
- `CompositePilotDossier` (the umbrella record)
- `CaseParty` (with `is_public_official: bool` for the PoI clause)
- `TimelineEvent`
- `DamagesEstimate`
- `StatuteReference` + `JudgmentReference`
- The `ExtractCompositePilotDossier` extraction function

The extraction function ALWAYS sets:
- `osint_ceiling_enforced = True`
- `analyst_review_required = True`

### Layer 3 — The per-persona web app
The 7 personas (self-rep / WRC / HSE-NHS / PIAB / coroner / inquest / legal-aid) each have a `web/apps/ciandlithe-<persona>/` TanStack Start + Convex + AG-UI + CopilotKit app that renders the dossier for manual review. NONE of the apps offer an "auto-submit to court" affordance.

## Composite pilot outputs

The FunctionTool `composite_pilot_tool` returns a dict with:

```python
{
  "dossiers": [<list of CompositePilotDossier dicts>],
  "osint_ceiling_enforced": True,
  "analyst_review_required": True,
  "source_pdf_urls": [<list of leabharlann PDF URLs>],
  "extraction_confidence": 0.0,
  "composite_pilot_metadata": {
    "total_pilot_parties": 7,
    "selected_pilot_parties": <int>,
    "valid_cohorts": [...],
    "lineage": "ciandlithe-repo-foundation-v1 + ciandlithe-composite-pilot-workflow-v1",
  },
}
```

Each `CompositePilotDossier` has the schema:

```python
{
  "case_id": "pilot-qub-rvh" / "pilot-eric" / etc.,
  "cohort": "MedicalMalpractice" / "EmployerBreach" / etc.,
  "jurisdiction": "IRELAND" / "NI" / "SCOTLAND" / "WALES" / "ENGLAND" / "JERSEY" / "GUERNSEY" / "IOM" / "CROSS_BORDER",
  "court_level": "DISTRICT" / "CIRCUIT" / "HIGH" / "SUPREME" / "COURT_OF_APPEAL" / "TRIBUNAL" / "SHERIFF" / "CORONER" / "INQUEST",
  "parties": [<list of CaseParty dicts>],
  "timeline": [<list of TimelineEvent dicts>],
  "statute_references": [<list of StatuteReference dicts>],
  "precedent_judgments": [<list of JudgmentReference dicts>],
  "damages_estimate": <DamagesEstimate dict or None>,
  "burden_of_proof": "BalanceOfProbabilities" / "BeyondReasonableDoubt" / "BeyondReasonableDoubt_Criminal",
  "limitation_period_years": <float>,
  "filing_form": "Form 1" / "HC1" / "CC1" / etc. or None,
  "filing_fee_eur": <float or None>,
  "next_steps": [<list of strings>],
  "osint_ceiling_enforced": True,  # ALWAYS True
  "analyst_review_required": True,  # ALWAYS True
  "source_pdf_urls": [<list of leabharlann PDF URLs>],
  "extraction_confidence": <float>,
}
```

## Validation criteria (manual review)

Per the OSINT ceiling + the no-auto-submit constraint + the PoI clause, the composite pilot is NOT valid for any automated downstream action. The composite pilot generates a structured dossier for **manual review by a qualified solicitor or barrister** who verifies:

1. The leabharlann PDFs cited in `source_pdf_urls` are the canonical source-of-truth for the pilot party (the pilot does NOT generate new factual claims from the PDFs).

2. The `statute_references` + `precedent_judgments` cited are from the BAML extraction (which itself cites the OSINT-allowlisted British-Isles official sources).

3. The `parties[*].is_public_official` flag is correctly set (per the PoI clause).

4. The `next_steps` are appropriate for the cohort (e.g. for `MedicalMalpractice` in NI, the next steps are: "Read the leabharlann PDF for full procedural detail; Identify the relevant court (District / Circuit / High / Tribunal); Generate the Statement of Claim / WRC complaint / HSE complaint / PIAB form using the BAML Extract functions; Manual review by a qualified solicitor or barrister before filing").

5. The dossier's `analyst_review_required = True` flag is respected — no automated downstream action is taken without human sign-off.

## Pilot scope

- **7 pilot parties** (one per leabharlann PDF cluster).
- **7 BLIP v1 cohorts** covered (one per pilot party; some cohorts are covered by 2 pilots).
- **6 sub-nations** covered (Ireland / NI / Scotland / Wales / England / Cross-border).

The pilot validates the workflow end-to-end before any expansion. A follow-up `ciandlithe-composite-pilot-workflow-v2` change would expand to multi-party dossiers (e.g. all 7 Reform UK politicians analogue for ciandlithe), full courts.ie daily-list scraping, or Companies House bulk-data cross-referencing — but only after the v1 composite pilot has been validated by a public-sector analyst.

## Dependencies

`Blocked by: ciandlithe-repo-foundation-v1` (must archive first; archived 2026-08-24).
`Blocked by: ciandlithe-baml-schemas-v1` (must archive first; lands 2026-09).
`Blocked by: ciandlithe-blip-v1` (must archive first; lands 2026-09).
`Affected repos: ciandlithe.` (Cianfhoghlaim + Cianchosaint + leabharlann are unchanged — the leabharlann PDFs are read-only context.)

## Cross-repo sync

This change touches **ONLY the `ciandlithe` repo**. Cianfhoghlaim + Cianchosaint + leabharlann remain **completely unchanged**.