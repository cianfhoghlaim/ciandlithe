# CIANDLITHE — Law & Medicine Malpractice Research Synthesis

> **Per the cianchosaint `web-stack-best-practices-v0.md` precedent** — the canonical synthesis of the 60+ leabharlann Gemini Deep Research outputs that informed the ciandlithe composite pilot.

## §1 — Why this document exists

The `leabharlann/gemini_deep_research/law/` + `leabharlann/gemini_deep_research/medical/` directories at `/Users/cianmacandeisigh/dev/cianfhoghlaim/leabharlann/gemini_deep_research/` contain ~60+ PDF files (~5 MB total) that informed every ciandlithe BAML schema + every ciandlithe DLT source + every ciandlithe FunctionTool + the entire composite pilot. These PDFs are the canonical source-of-truth for the entities + events + jurisdictions covered by ciandlithe.

This document synthesises the findings into the 7 BLIP v1 cohorts + the 7 composite-pilot parties.

## §2 — The 7 BLIP v1 cohorts (from the law + medical PDFs)

### Cohort 1 — civil_litigation_forms (Circuit / District / High Court forms)

**Key PDFs:**
- `law/uk_ireland_court_forms_procedures.pdf` — the canonical procedure guide
- `law/cross_border_legal_action_research.pdf` — cross-border NI ↔ ROI
- `law/comprehensive_jurisprudential_analysis_of_dual_irish_british_citizenship_statutory_acquisition_by_descent_and_procedures_for_renunciation.pdf`
- `law/cross_border_medical_malpractice_and_data_breach.pdf`

**Cohort entities:** Courts Service of Ireland (courts.ie) · NICTS · Scottish Courts · HMCTS · Jersey Royal Court · Guernsey Royal Court · Isle of Man High Court.

### Cohort 2 — medical_malpractice (clinical negligence + misdiagnosis)

**Key PDFs:**
- `law/brother_misdiagnosis_malpractice_grievous_bodily_harm_2017_2026.pdf`
- `law/ciara_meehan_sean_o_gradaigh_malpractice.pdf`
- `law/irish_high_court_echr_medical_cannabis.pdf`
- `law/maximizing_civil_suit_damages_against_qub.pdf`
- `law/medical_malpractice_and_legal_investigation.pdf`
- `law/medical_malpractice_brain_damage_legal_action.pdf`
- `law/medical_malpractice_lawsuit_against_irish_psychiatrist.pdf`
- `law/medical_malpractice_legal_strategy_outline.pdf`
- `law/qub_royal_victoria_malpractice.pdf`
- `medical/irish_sodium_valproate_inquiry_and_healthcare.pdf`
- `medical/sodium_valproate_lawsuits_and_inquiries.pdf`
- `medical/sodium_valproate_legalities_and_risks.md`
- `medical/essential_tbi_medication.pdf`
- `medical/misdiagnosis_brain_damage_recovery.pdf`
- `medical/ireland_mental_health_law_inquiry.pdf`
- `medical/mental_health_misdiagnosis_and_damages.pdf`
- `medical/mental_health_commission_oversight_inquiry.pdf`

**Cohort entities:** HSE + HPSC + Medical Council Ireland + GMC + NICTS (NI malpractice jurisdiction) · Royal Victoria Hospital Belfast.

### Cohort 3 — personal_injury_piab_nhs

**Key PDFs:**
- `law/irish_passport_name_rights_complaint.pdf`
- `law/landlord_eviction_and_discrimination_dispute.pdf`
- `law/legal_avenues_for_music_removal.pdf`
- `law/disability_allowance_and_medical_records_dispute.pdf`

**Cohort entities:** PIAB · HSE · NHS Resolution · NHS England + NHS Scotland + NHS Wales + Health & Social Care NI.

### Cohort 4 — workplace_relations_wrc_et

**Key PDFs:**
- `law/discrimination_case_strategy_university_of_galway.pdf`
- `law/cbd_discrimination_lawsuit_preparation.pdf`
- `law/cbd_dispensary_manager_discrimination_lawsuit.pdf`
- `law/challenging_university_rejection_and_ombudsman_decision.pdf`

**Cohort entities:** WRC · Industrial Tribunal NI · Employment Tribunals Scotland / Wales / England.

### Cohort 5 — hse_nhs_complaints

**Key PDFs:**
- `medical/counselling_notes_some_errors.pdf`
- `medical/disability_data_access_request_emails.pdf`
- `medical/hse_malpractice.pdf`
- `medical/hse_trauma.pdf`
- `medical/medical_advocacy_sleep_study.pdf`
- `medical/mental_health_care_request_and_complaint.pdf`

**Cohort entities:** HSE + NHS England + NHS Scotland + NHS Wales + CQC + HIS + HIW + RQIA.

### Cohort 6 — statutes_si_court_rules

**Key PDFs:**
- `law/elder_abuse_and_inheritance_in_ireland.pdf`
- `law/navigating_abuse_legal_orders_and_family.pdf`
- `law/parental_rights_group_tactics_analysis.pdf`

**Cohort entities:** Irish Statute Book · Courts.ie Rules of Court · NICTS Rules · Scottish Court Rules · Crown Dependencies legislation.

### Cohort 7 — court_judgments_tribunal_decisions

**Key PDFs:**
- `law/perjury_destroyed_my_life_and_future.pdf`
- `law/irish_high_court_echr_medical_cannabis.pdf`

**Cohort entities:** Courts.ie Judgements · BAILII · ICLR CaseMine · NICTS judgments · Scot Law Reports.

## §3 — The 7 composite-pilot parties (from the law + medical PDFs)

Per `docs/case-study/composite-pilot.md` + `agents/ciandlithe/tools/composite_pilot.py`:

| # | Pilot party | Cohort | Sub-nation | Primary leabharlann PDF | Companion PDFs |
|--:|---|---|---|---|---|
| 1 | QUB / Royal Victoria Hospital brain-injury | medical_malpractice | NI | `law/qub_royal_victoria_malpractice.pdf` | `medical/misdiagnosis_brain_damage_recovery.pdf` + `law/maximizing_civil_suit_damages_against_qub.pdf` |
| 2 | Eric employer / breach of contract | employer_breach | CROSS_BORDER | `law/suing_ceo_for_breach_abuse_damages.pdf` | `law/cross_border_legal_action_research.pdf` + `law/monroes.pdf` |
| 3 | Garda discrimination / data-access | garda_discrimination | IRELAND | `law/garda_corruption_and_data_access.pdf` | `law/garda_data_and_accommodation_request.pdf` + `law/garda_brutality_dual_citizenship_and_justice.pdf` |
| 4 | DkIT disability / education complaint | education_discrimination | IRELAND | `law/discrimination_case_strategy_university_of_galway.pdf` | `law/cbd_discrimination_lawsuit_preparation.pdf` + `law/challenging_university_rejection_and_ombudsman_decision.pdf` |
| 5 | NUIG / UoG rejection + abuse of power | education_discrimination | IRELAND | `law/discrimination_case_strategy_university_of_galway.pdf` | `law/cbd_dispensary_manager_discrimination_lawsuit.pdf` |
| 6 | UCL offer / DBS | admission_breach | ENGLAND | `law/ucl_sar_equality_act_claim.pdf` | (none) |
| 7 | Sodium valproate / HSE misprescription | medical_malpractice | IRELAND | `medical/irish_sodium_valproate_inquiry_and_healthcare.pdf` | `medical/sodium_valproate_lawsuits_and_inquiries.pdf` + `medical/essential_tbi_medication.pdf` |

## §4 — The key entities mentioned across the PDFs

**Institutions (public-sector):**
- Courts Service of Ireland (courts.ie)
- An Garda Síochána (garda.ie)
- HSE / HPSC / Medical Council Ireland
- NICTS (Northern Ireland Courts and Tribunals Service)
- GMC (General Medical Council)
- NHS England + NHS Scotland + NHS Wales + nidirect
- The National Archives (legislation.gov.uk)
- BAILII (British and Irish Legal Information Institute)
- WRC (Workplace Relations Commission)
- PIAB (Personal Injuries Assessment Board)
- Coroner Service of Ireland
- NHS Resolution
- Law Society of Ireland / NI / Scotland / England & Wales
- Faculty of Advocates (Scotland)
- Bar of Northern Ireland / England & Wales

**Institutions (education):**
- DkIT (Dundalk Institute of Technology)
- NUI Galway / University of Galway
- University College London (UCL)
- Queen's University Belfast (QUB)
- Royal College of Surgeons in Ireland

**Individuals (in named cases — PoI clause applies):**
- The pilot parties who are named (Eric; the QUB/RVH patient; the DkIT student; the NUIG applicant; the UCL offer holder; the sodium valproate patient) are NOT named in the open repo. The FunctionTool response uses `[redacted per PoI clause]` placeholders. The full names are only in the leabharlann PDFs (read-only context).

## §5 — Cross-references

- [`../case-study/composite-pilot.md`](../case-study/composite-pilot.md) — the canonical pilot narrative
- [`../../dlt_sources/ciandlithe/cross/case_study_loader.py`](../../dlt_sources/ciandlithe/cross/case_study_loader.py) — the case-study loader
- [`../../dlt_sources/ciandlithe/cross/case_party_registry.py`](../../dlt_sources/ciandlithe/cross/case_party_registry.py) — the canonical pilot-party registry
- [`../../agents/ciandlithe/tools/composite_pilot.py`](../../agents/ciandlithe/tools/composite_pilot.py) — the composite pilot FunctionTool
- [`../../baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml`](../../baml_src/ciandlithe/case_studies/reform_civil_suit_dossier.baml) — the BAML extraction schema
- [`/Users/cianmacandeisigh/dev/cianfhoghlaim/leabharlann/gemini_deep_research/law/`](https://github.com/cianfhoghlaim/leabharlann/tree/main/gemini_deep_research/law/) — the law PDFs
- [`/Users/cianmacandeisigh/dev/cianfhoghlaim/leabharlann/gemini_deep_research/medical/`](https://github.com/cianfhoghlaim/leabharlann/tree/main/gemini_deep_research/medical/) — the medical PDFs