"""CIANDLITHE DLT sources.

The ciandlithe DLT sources are organised as:
- ireland/law/         — Republic of Ireland law (courts.ie, irishstatutebook.ie, etc.)
- ireland/medicine/    — Republic of Ireland medicine (hse.ie, hpsc.ie, medical_council.ie)
- ireland/courts/      — Republic of Ireland courts (Circuit Court Dublin, High Court, etc.)
- northern_ireland/law/    — NI law (NICTS, nidirect.gov.uk)
- northern_ireland/medicine/ — NI medicine (nidirect, BSO, RQIA)
- northern_ireland/courts/  — NI courts (Royal Courts of Justice Belfast)
- scotland/law/        — Scotland law (scotcourts.gov.uk)
- scotland/medicine/   — Scotland medicine (NHS Scotland)
- scotland/courts/     — Scotland courts (Sheriff Court, Court of Session)
- wales/law/           — Wales law (Senedd, Casemine Wales)
- wales/medicine/      — Wales medicine (NHS Wales, PHW)
- wales/courts/        — Wales courts (Cardiff Crown Court)
- england/law/         — England law (legislation.gov.uk, BAILII, ICLR CaseMine)
- england/medicine/    — England medicine (NHS England, GMC, NICE, CQC)
- england/courts/      — England courts (Royal Courts of Justice London)
- crown_dependencies/{jersey,guernsey,isle_of_man}/{law,medicine,courts}/

The cross/ helpers at dlt_sources/ciandlithe/cross/ provide:
- case_study_loader.py    — loads the 7 leabharlann case-study PDFs
- case_party_registry.py  — canonical registry of the 7 pilot parties
- complaint_classifier.py — maps an uploaded complaint → cohort + jurisdiction

The common/ helpers at dlt_sources/ciandlithe/common/ provide:
- osint_allowlist.yaml    — the canonical OSINT allowlist
- osint_audit.py          — the CI gate (verify every DLT source URL is on the allowlist)
"""

from .common.osint_audit import osint_audit  # noqa: F401
from .cross import load_case_study, load_all_case_studies, PILOT_PARTIES, classify_complaint  # noqa: F401