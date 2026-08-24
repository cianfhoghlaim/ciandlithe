// =============================================================================
// BAML context: reform_civil_suit_dossier.baml
//
// Ciandlithe COMPOSITE PILOT — the 6+1 case-study dossier schema + extraction
// function. Mirrors the cianchosaint `reform_uk_pilot_extraction.baml` precedent.
//
// Composite pilot parties (one per leabharlann PDF, read-only context):
//   1. QUB / Royal Victoria Hospital brain-injury  (medical_malpractice, NI)
//   2. Eric employer / breach of contract          (employer_breach, cross-border NI ↔ ROI)
//   3. Garda discrimination / data-access         (garda_discrimination, ROI)
//   4. DkIT disability / education complaint      (education_discrimination, ROI)
//   5. NUIG / UoG rejection + abuse of power       (education_discrimination, ROI)
//   6. UCL offer / DBS                            (admission_breach, England)
//   7. Sodium valproate / HSE misprescription      (medical_malpractice, ROI)
//
// Constraints (per LICENSE.md §3.8 + §5.2):
//   - osint_ceiling_enforced = True (every extraction gated by the OSINT allowlist)
//   - analyst_review_required = True (every result marked for manual review)
//   - PoI clause: extractions naming non-public individuals fail
//   - No automated form submission to courts.ie / irishstatutebook.ie / nidirect.gov.uk
// =============================================================================

class CaseParty {
  party_id           string
  display_name       string
  role               enum<Claimant, Defendant, Respondent, Applicant, InterestedParty, PublicOfficial>
  is_public_official bool                       @description("True if the party is a public official; False for private individuals (PoI clause applies if False)")
  jurisdiction       Jurisdiction
  source_pdf_url     string
  extraction_confidence float                   @description("0.0-1.0")
}

class TimelineEvent {
  event_date         date
  event_type         enum<Filing, Hearing, Judgment, Order, Settlement, Appeal, Discovery, Mediation>
  description        string
  jurisdiction       Jurisdiction
  source_pdf_url     string?
  extraction_confidence float
}

class DamagesEstimate {
  general_damages_eur float?
  special_damages_eur float?
  aggravated_damages_eur float?
  punitive_damages_eur float?
  costs_eur          float?
  notes              string?
  jurisdiction       Jurisdiction
  source_pdf_url     string
  extraction_confidence float
}

class CompositePilotDossier {
  case_id            string
  cohort             enum<MedicalMalpractice, EmployerBreach, GardaDiscrimination, EducationDiscrimination, AdmissionBreach, CivilActionOutline>
  jurisdiction       Jurisdiction
  court_level        CourtLevel
  parties            CaseParty[]
  timeline           TimelineEvent[]
  statute_references StatuteReference[]
  precedent_judgments JudgmentReference[]
  damages_estimate   DamagesEstimate?
  burden_of_proof    enum<BalanceOfProbabilities, BeyondReasonableDoubt, BeyondReasonableDoubt_Criminal>
  limitation_period_years float?
  filing_form        string?                 @description("e.g. 'Form 1', 'Form 5A', 'HC1', 'CC1', 'DC1', 'ET1'")
  filing_fee_eur     float?
  next_steps         string[]
  osint_ceiling_enforced   bool               @description("Always True. Per LICENSE.md §5.1.")
  analyst_review_required  bool               @description("Always True. Per LICENSE.md §5.2 + §3.8.")
  source_pdf_urls    string[]
  extraction_confidence float
  @@stream.done
}

enum Jurisdiction {
  IRELAND
  NI
  SCOTLAND
  WALES
  ENGLAND
  JERSEY
  GUERNSEY
  IOM
  CROSS_BORDER
}

enum CourtLevel {
  DISTRICT
  CIRCUIT
  HIGH
  SUPREME
  COURT_OF_APPEAL
  TRIBUNAL
  SHERIFF
  CORONER
  INQUEST
}

class StatuteReference {
  jurisdiction Jurisdiction
  statute_id   string                      @description("e.g. '2018/0007/act' (Ireland), 'c.27' (UK), 'NIA 1962 c.15' (NI), 'SI 2023/1115' (UK SI), 'asp 5' (Scotland Act of Scottish Parliament)")
  canonical_citation string
  title string
  section_references string[]
  effective_date date?
  source_url string
}

class JudgmentReference {
  jurisdiction Jurisdiction
  neutral_citation string                  @description("e.g. '[2024] IESC 5', '[2024] NICA 1', '[2024] EWCA Civ 5'")
  case_name string
  judges string[]
  judgment_date date?
  ratio string?                 @description("The headnote / ratio decidendi")
  precedential_value enum<Binding, Persuasive, FirstInstance, Obiter>
  source_url string
}

function ExtractCompositePilotDossier(
  cohort: string,
  page_url: string,
  page_html: string,
  source_pdf_url: string,
) -> CompositePilotDossier {
  client ExtractEn
  prompt #"
    {{ _.role("user") }}
    You are an expert British-Isles civil-litigation extractor. From the input below, extract every field
    in the return type according to the @description decorators on the
    class definition. Preserve the canonical field names + types.

    For the COMPOSITE PILOT, the cohort MUST be one of:
    MedicalMalpractice | EmployerBreach | GardaDiscrimination | EducationDiscrimination |
    AdmissionBreach | CivilActionOutline.

    For every party, set is_public_official = True ONLY if the party is a named government official
    (e.g. a named judge, named WRC adjudicator, named PSNI officer). For named private individuals
    (claimants, defendants, employees, students, patients), set is_public_official = False — the PoI
    clause (LICENSE.md §5.2) requires manual review for these.

    osint_ceiling_enforced MUST be True. analyst_review_required MUST be True.

    {{ ctx.output_format }}

    {{ input }}
  "#

  catch_all (err) {
    CompositePilotDossier {
      case_id "ERROR",
      cohort CivilActionOutline,
      jurisdiction CROSS_BORDER,
      court_level TRIBUNAL,
      parties [],
      timeline [],
      statute_references [],
      precedent_judgments [],
      damages_estimate null,
      burden_of_proof BalanceOfProbabilities,
      limitation_period_years 2.0,
      filing_form null,
      filing_fee_eur null,
      next_steps ["manual review required (BAML extraction failed)"],
      osint_ceiling_enforced true,
      analyst_review_required true,
      source_pdf_urls [source_pdf_url],
      extraction_confidence 0.0,
    }
  }
}