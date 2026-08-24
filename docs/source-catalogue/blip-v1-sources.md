# CIANDLITHE — BLIP v1 Source Catalogue

> **Per `docs/case-study/composite-pilot.md` + `openspec/specs/ciandlithe-pipeline/spec.md`** — the canonical list of ~70 DLT source URLs that populate the British Isles Litigation Pipeline (BLIP v1).

## Cohort — × 6-8 sub-nations

Each cell = 1 DLT source URL.

### Cohort 1: civil_litigation_forms

| Sub-nation | URL | DLT source file |
|---|---|---|
| ROI | https://www.courts.ie/forms | `dlt_sources/ciandlithe/ireland/law/courts_ie.py` |
| ROI | https://www.citizensinformation.ie/ | `dlt_sources/ciandlithe/ireland/law/citizensinformation.py` |
| ROI | https://www.legalaidboard.ie/ | `dlt_sources/ciandlithe/ireland/law/` (NEW) |
| NI | https://www.courtsni.gov.uk/ | `dlt_sources/ciandlithe/northern_ireland/law/` (NEW) |
| NI | https://www.nidirect.gov.uk/ | `dlt_sources/ciandlithe/northern_ireland/law/nidirect.py` (NEW) |
| Scotland | https://www.scotcourts.gov.uk/ | `dlt_sources/ciandlithe/scotland/law/scotcourts.py` (NEW) |
| Wales | https://www.lawsocwales.co.uk/ | `dlt_sources/ciandlithe/wales/law/` (NEW) |
| England | https://www.judiciary.uk/ | `dlt_sources/ciandlithe/england/law/judiciary_uk.py` (NEW) |
| England | https://www.courtserve.net/ | `dlt_sources/ciandlithe/england/law/` (NEW) |
| Jersey | https://www.courts.je/ | `dlt_sources/ciandlithe/crown_dependencies/jersey/law/` (NEW) |
| Guernsey | https://www.guernseyroyalcourt.gg/ | `dlt_sources/ciandlithe/crown_dependencies/guernsey/law/` (NEW) |
| IoM | https://www.courts.im/ | `dlt_sources/ciandlithe/crown_dependencies/isle_of_man/law/` (NEW) |

### Cohort 2: medical_malpractice

| Sub-nation | URL | DLT source file |
|---|---|---|
| ROI | https://www.medicalcouncil.ie/ | `dlt_sources/ciandlithe/ireland/medicine/medical_council.py` |
| ROI | https://www.hse.ie/ | `dlt_sources/ciandlithe/ireland/medicine/hse.py` |
| ROI | https://www.hpsc.ie/ | `dlt_sources/ciandlithe/ireland/medicine/hpsc.py` |
| ROI | https://coroners.ie/ | `dlt_sources/ciandlithe/ireland/medicine/coroners_ie.py` (NEW) |
| NI | https://www.nidirect.gov.uk/ | `dlt_sources/ciandlithe/northern_ireland/medicine/nidirect.py` |
| NI | https://www.rqia.org.uk/ | `dlt_sources/ciandlithe/northern_ireland/medicine/rqia.py` (NEW) |
| Scotland | https://www.nhsinform.scot/ | `dlt_sources/ciandlithe/scotland/medicine/nhs_scotland.py` |
| Scotland | https://www.healthcareimprovementscotland.org/ | `dlt_sources/ciandlithe/scotland/medicine/his.py` (NEW) |
| Wales | https://phw.nhs.wales/ | `dlt_sources/ciandlithe/wales/medicine/phw.py` (NEW) |
| England | https://www.gmc-uk.org/ | `dlt_sources/ciandlithe/england/medicine/gmc.py` |
| England | https://www.nice.org.uk/ | `dlt_sources/ciandlithe/england/medicine/nice.py` |
| England | https://resolution.nhs.uk/ | `dlt_sources/ciandlithe/england/medicine/nhs_resolution.py` (NEW) |

### Cohort 3: personal_injury_piab_nhs

| Sub-nation | URL | DLT source file |
|---|---|---|
| ROI | https://www.injuriesboard.ie/ (also https://www.injuries.ie/) | `dlt_sources/ciandlithe/ireland/law/injuries_ie.py` |
| UK | https://www.england.nhs.uk/ | `dlt_sources/ciandlithe/england/medicine/nhs_england.py` |

### Cohort 4: workplace_relations_wrc_et

| Sub-nation | URL | DLT source file |
|---|---|---|
| ROI | https://www.workplacerelations.ie/ | `dlt_sources/ciandlithe/ireland/law/workplace_relations.py` |
| NI | https://www.employmenttribunalsni.org.uk/ | `dlt_sources/ciandlithe/northern_ireland/law/` (NEW) |
| Scotland | https://www.employmenttribunals.scot/ | `dlt_sources/ciandlithe/scotland/law/` (NEW) |
| Wales | https://www.employmenttribunals.wales/ | `dlt_sources/ciandlithe/wales/law/` (NEW) |
| England | https://www.gov.uk/employment-tribunal | `dlt_sources/ciandlithe/england/law/` (NEW) |

### Cohort 5: hse_nhs_complaints

| Sub-nation | URL | DLT source file |
|---|---|---|
| ROI | https://www.hse.ie/ | `dlt_sources/ciandlithe/ireland/medicine/hse.py` |
| ROI | https://www.hpsc.ie/ | `dlt_sources/ciandlithe/ireland/medicine/hpsc.py` |
| NI | https://www.nidirect.gov.uk/ | `dlt_sources/ciandlithe/northern_ireland/medicine/nidirect.py` |
| Scotland | https://www.nhsinform.scot/ | `dlt_sources/ciandlithe/scotland/medicine/nhs_scotland.py` |
| Wales | https://phw.nhs.wales/ | `dlt_sources/ciandlithe/wales/medicine/nhs_wales.py` (NEW) |
| England | https://www.nhs.uk/ | `dlt_sources/ciandlithe/england/medicine/nhs_england.py` |
| England | https://www.cqc.org.uk/ | `dlt_sources/ciandlithe/england/medicine/cqc.py` (NEW) |

### Cohort 6: statutes_si_court_rules

| Sub-nation | URL | DLT source file |
|---|---|---|
| ROI | https://www.irishstatutebook.ie/eli/{year}/act/{number}/enacted/en/xml | `dlt_sources/ciandlithe/ireland/law/irish_statute_book.py` |
| ROI | https://www.justice.ie/ | `dlt_sources/ciandlithe/ireland/law/doj.py` |
| ROI | https://www.lawreform.ie/ | `dlt_sources/ciandlithe/ireland/law/lawreform.py` |
| UK_WIDE | https://www.legislation.gov.uk/ | `dlt_sources/ciandlithe/england/law/legislation.py` |
| Scotland | https://www.legislation.gov.uk/scot | `dlt_sources/ciandlithe/scotland/law/legislation.py` |
| Wales | https://www.legislation.gov.uk/wales | `dlt_sources/ciandlithe/wales/law/legislation.py` |
| NI | https://www.legislation.gov.uk/ (NI-specific) | `dlt_sources/ciandlithe/northern_ireland/law/legislation.py` |

### Cohort 7: court_judgments_tribunal_decisions

| Sub-nation | URL | DLT source file |
|---|---|---|
| ROI | https://www.courts.ie/judgements | `dlt_sources/ciandlithe/ireland/law/courts_ie.py` (judgements sub-tree) |
| ROI | https://coroners.ie/ | `dlt_sources/ciandlithe/ireland/courts/coroners_ie.py` (NEW) |
| UK_WIDE | https://www.bailii.org/ | `dlt_sources/ciandlithe/england/law/bailii.py` (NEW) |
| UK_WIDE | https://www.casemine.com/ | `dlt_sources/ciandlithe/england/law/casemine.py` (NEW) |
| NI | https://www.courtsni.gov.uk/ | `dlt_sources/ciandlithe/northern_ireland/courts/` (NEW) |
| Scotland | https://www.scotlawreports.com/ | `dlt_sources/ciandlithe/scotland/law/scot_law_reports.py` (NEW) |
| Jersey | https://www.courts.je/ | `dlt_sources/ciandlithe/crown_dependencies/jersey/courts/` (NEW) |
| Guernsey | https://www.guernseyroyalcourt.gg/ | `dlt_sources/ciandlithe/crown_dependencies/guernsey/courts/` (NEW) |
| IoM | https://www.courts.im/ | `dlt_sources/ciandlithe/crown_dependencies/isle_of_man/courts/` (NEW) |

## Cohort counts

| Cohort | ROI | NI | Scotland | Wales | England | Crown Deps | TOTAL |
|---|---:|---:|---:|---:|---:|---:|---:|
| civil_litigation_forms | 3 | 2 | 1 | 1 | 2 | 3 | 12 |
| medical_malpractice | 4 | 2 | 2 | 1 | 3 | 0 | 12 |
| personal_injury_piab_nhs | 1 | 0 | 0 | 0 | 1 | 0 | 2 |
| workplace_relations_wrc_et | 1 | 1 | 1 | 1 | 1 | 0 | 5 |
| hse_nhs_complaints | 2 | 1 | 1 | 1 | 2 | 0 | 7 |
| statutes_si_court_rules | 3 | 1 | 1 | 1 | 1 | 0 | 7 |
| court_judgments_tribunal_decisions | 2 | 1 | 1 | 0 | 2 | 3 | 9 |
| **TOTAL** | **16** | **8** | **7** | **5** | **12** | **6** | **54** |

## Cohort milestones

- **m1 (Republic of Ireland)**: 16 cohorts minimum
- **m2 (United Kingdom)**: 32 cohorts (NI + Scotland + Wales + England = 8 + 7 + 5 + 12)
- **m3 (Crown Dependencies)**: 6 cohorts (Jersey + Guernsey + IoM)
- **v1 GA**: ~54 cohorts

## OSINT allowlist integration

Every URL in this catalogue is in `dlt_sources/ciandlithe/common/osint_allowlist.yaml` (the canonical OSINT allowlist). The CI gate `mise run lint:license` verifies every DLT source URL is in the allowlist. Adding new URLs requires a PR + openspec change (the `ciandlithe-dlt-source-policy-v1` follow-up).

## Cross-references

- [`dlt_sources/ciandlithe/common/osint_allowlist.yaml`](../../dlt_sources/ciandlithe/common/osint_allowlist.yaml) — the canonical OSINT allowlist
- [`docs/case-study/composite-pilot.md`](../case-study/composite-pilot.md) — the canonical pilot narrative
- [`docs/research/law-med-malpractice-research.md`](../research/law-med-malpractice-research.md) — the 60+ leabharlann PDFs synthesis