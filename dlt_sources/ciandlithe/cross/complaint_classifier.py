"""CIANDLITHE complaint classifier.

Maps an uploaded complaint to its BLIP v1 cohort + jurisdiction.

The classifier is intentionally conservative — it NEVER auto-files the
complaint (per LICENSE.md §3.8). It only classifies the complaint and
returns the cohort + jurisdiction for downstream FunctionTool routing.

Per LICENSE.md §5.2 (PoI clause): the classifier NEVER includes the
name of any non-public individual in its output.
"""

from __future__ import annotations

from typing import Any


COHORT_KEYWORDS: dict[str, list[str]] = {
    "MedicalMalpractice": [
        "misdiagnosis", "malpractice", "clinical negligence", "wrong prescription",
        "wrong dose", "misprescription", "olanzapine", "sodium valproate",
        "brain injury", "TBI", "PTSD", "cPTSD", "treatment injury",
        "wrong-site surgery", "hospital negligence",
    ],
    "EmployerBreach": [
        "breach of contract", "unfairlyaw", "constructive dismissal", "wrongful dismissal",
        "wages theft", "holiday pay", "redundancy", "breach of duty",
        "discrimination at work", "harassment at work",
    ],
    "GardaDiscrimination": [
        "garda", "gardaí", "an garda síochána", "psni", "police discrimination",
        "police misconduct", "false arrest", "wrongful detention",
        "data access request", "FOI request", "section 4", "data protection",
    ],
    "EducationDiscrimination": [
        "education", "university", "college", "school", "admissions",
        "registration", "matriculation", "exam", "marking", "academic misconduct",
        "reasonable accommodation", "disability", "DSA", "student",
    ],
    "AdmissionBreach": [
        "offer", "admission", "DBS", "criminal record", "disclosure",
        "fitness to practise", "professional registration",
    ],
    "CivilActionOutline": [
        "civil action", "civil suit", "statement of claim", "damages",
        "negligence", "duty of care", "breach", "loss", "injury",
    ],
}


JURISDICTION_KEYWORDS: dict[str, list[str]] = {
    "IRELAND": ["ireland", "irish", "dublin", "cork", "galway", "limerick", "waterford", "ROI", "éire", "gaelic"],
    "NI": ["northern ireland", "belfast", "derry", "lisburn", "newry", "NI"],
    "SCOTLAND": ["scotland", "edinburgh", "glasgow", "aberdeen", "dundee", "scottish"],
    "WALES": ["wales", "cardiff", "swansea", "newport", "welsh", "cymru"],
    "ENGLAND": ["england", "london", "manchester", "birmingham", "bristol", "liverpool", "leeds", "english"],
    "JERSEY": ["jersey"],
    "GUERNSEY": ["guernsey"],
    "IOM": ["isle of man", "iom", "manx"],
}


def classify_complaint(complaint_text: str) -> dict[str, Any]:
    """Classify an uploaded complaint into a BLIP v1 cohort + jurisdiction.

    Args:
        complaint_text: the raw text of the complaint (free-form)

    Returns:
        A dict with:
          - cohort: the BLIP v1 cohort (best match)
          - cohort_score: 0.0-1.0 (the keyword overlap score)
          - jurisdiction: the British-Isles sub-nation
          - jurisdiction_score: 0.0-1.0
          - all_cohorts: list of all cohorts ranked by score
          - all_jurisdictions: list of all sub-nations ranked by score
          - osint_ceiling_enforced: True (always)
          - analyst_review_required: True (always)
          - next_steps: list of next-step actions for the per-persona web app
    """
    text_lower = complaint_text.lower()

    # Score each cohort by keyword overlap
    cohort_scores: dict[str, int] = {}
    for cohort, keywords in COHORT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        cohort_scores[cohort] = score

    best_cohort = max(cohort_scores, key=cohort_scores.get)
    best_cohort_score = cohort_scores[best_cohort]
    cohort_score_normalised = min(1.0, best_cohort_score / 3.0)  # normalise

    # Score each jurisdiction
    jur_scores: dict[str, int] = {}
    for jur, keywords in JURISDICTION_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        jur_scores[jur] = score

    best_jur = max(jur_scores, key=jur_scores.get)
    best_jur_score = jur_scores[best_jur]
    jur_score_normalised = min(1.0, best_jur_score / 2.0)

    # Determine next steps based on cohort + jurisdiction
    next_steps = _determine_next_steps(best_cohort, best_jur)

    return {
        "cohort": best_cohort,
        "cohort_score": cohort_score_normalised,
        "jurisdiction": best_jur,
        "jurisdiction_score": jur_score_normalised,
        "all_cohorts": sorted(cohort_scores.items(), key=lambda x: x[1], reverse=True),
        "all_jurisdictions": sorted(jur_scores.items(), key=lambda x: x[1], reverse=True),
        "osint_ceiling_enforced": True,
        "analyst_review_required": True,
        "next_steps": next_steps,
    }


def _determine_next_steps(cohort: str, jurisdiction: str) -> list[str]:
    """Determine the appropriate next steps for a cohort + jurisdiction."""
    base_steps = [
        "Read the relevant OSINT-allowlisted sources for the cohort + jurisdiction",
        "Identify the appropriate court / tribunal / regulator (per the cohort)",
        "Generate the relevant form (Statement of Claim / WRC complaint / HSE complaint / PIAB form)",
        "Manual review by a qualified solicitor or barrister before filing",
    ]

    cohort_specific = {
        "MedicalMalpractice": [
            "Compile the medical record + clinical-incident reports",
            "Obtain an independent medical expert report",
            "Statute of Limitations check (2 years from date of knowledge)",
        ],
        "EmployerBreach": [
            "Compile the employment contract + payslips + correspondence",
            "Identify the relevant WRC / ET / Labour Court",
            "Time limit check (6 months for WRC; 3 months for ET)",
        ],
        "GardaDiscrimination": [
            "Submit a data access request under the GDPR / Data Protection Acts",
            "Identify the relevant Garda station + Garda Inspectorate",
            "Compile the timeline of the discrimination / data-access denial",
        ],
        "EducationDiscrimination": [
            "Compile the academic record + admissions / registration correspondence",
            "Identify the relevant university + the Equality Tribunal",
            "Time limit check (6 months for WRC; 2 months for university appeal)",
        ],
        "AdmissionBreach": [
            "Compile the offer letter + DBS / disclosure + correspondence",
            "Identify the relevant admissions body + the Equality Tribunal",
            "Time limit check (3 months for university appeal)",
        ],
        "CivilActionOutline": [
            "Identify the Statement of Claim form for the court level",
            "Compile the witness statement + exhibits of",
        ],
    }

    return cohort_specific.get(cohort, []) + base_steps


__all__ = ["classify_complaint", "COHORT_KEYWORDS", "JURISDICTION_KEYWORDS"]


if __name__ == "__main__":
    import json
    sample = "I was misprescribed olanzapine in a Galway hospital and now I have brain damage. The HSE won't give me my medical records. What can I do?"
    print(json.dumps(classify_complaint(sample), indent=2))