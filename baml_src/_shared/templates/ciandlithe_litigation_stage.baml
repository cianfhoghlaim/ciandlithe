// BAML template: Ciandlithe Litigation Stage Extractor
//
// Per the ciandlithe-repo-foundation-v1 openspec change (Phase: BAML
// templates bootstrap). Replaces the per-cohort stub prompts in
// `baml_src/ciandlithe/<cohort>/` with a single canonical extractor
// keyed on the BLIP v1 cohort.
//
// Each stub function in the parent dirs (baml_src/ciandlithe/...) routes
// through this template via `baml_bulk_replace_stubs.py`. The template
// is shared (not duplicated per function) so a single improvement
// benefits all 7 BLIP v1 cohort extractors.
//
// Re-gen: `python scripts/baml_generate_templates.py`
// Re-apply: `python scripts/baml_bulk_replace_stubs.py`

function LitigationStageExtractor(input: string) -> string {
  client ExtractEn
  prompt #"
    {{ _.role("user") }}
    You are an expert British-Isles civil-litigation document extractor. You specialize in extracting structured data from Irish Statute Book (irishstatutebook.ie), UK Crown material (legislation.gov.uk), Court Service of Ireland (courts.ie), NICTS, Scottish Courts, HMCTS, Crown Dependencies courts, WRC adjudications (workplacerelations.ie), PIAB (injuriesboard.ie), NHS Resolution, GMC FTPAN decisions, HSE clinical-incident reports, and Coroner's Court records.

    Source type: PDF text + scraped HTML from British Isles official sources (courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net / workplacerelations.ie / injuriesboard.ie / hse.ie / nhs.uk / hpsc.ie / gmc-uk.org / legislation.gov.uk / coroners.ie / etc.)

    Extract:
    - cohort: the BLIP v1 cohort (one of: civil_litigation_forms / medical_malpractice / personal_injury_piab_nhs / workplace_relations_wrc_et / hse_nhs_complaints / statutes_si_court_rules / court_judgments_tribunal_decisions)
    - jurisdiction: the British-Isles jurisdiction (Ireland / NI / Scotland / Wales / England / Jersey / Guernsey / IoM)
    - court_level: the court level (District / Circuit / High / Supreme / Court of Appeal / Tribunal / etc.)
    - module_topics: list of topic categories within the cohort
    - cited_statutes: list of statutes referenced (with canonical citations: "2018/0007/act", "c.27", "SI 2023/1115", "NIA 1962 c.15")
    - cited_precedents: list of precedent cases cited (with neutral citations)
    - filing_requirements: list of filing requirements (forms, fees, deadlines)
    - damages_headings: list of General Schedule of damages headings referenced
    - extraction_confidence: 0.0-1.0

    {% if cohort == 'medical_malpractice' %}
    - Per the Irish Medical Council / GMC FTPAN process
    - Statute of Limitations: 2 years from date of knowledge (Civil Liability Act 1961 § s.9)
    - Damages estimated under the Personal Injuries Assessment Board Act 2003 (as amended 2024)
    {% elif cohort == 'workplace_relations_wrc_et' %}
    - Per the Workplace Relations Act 2015 (Ireland) or Employment Rights Act 1996 (UK)
    - Adjudication Officer / Employment Tribunal decision structure
    - 6-month / 3-month time limits for complaints
    {% elif cohort == 'civil_litigation_forms' %}
    - Per the Rules of the Superior Courts (RSC) / Circuit Court Rules / District Court Rules
    - Forms: HC1 / CC1 / DC1 / summonses / statements of claim / affidavits
    {% elif cohort == 'hse_nhs_complaints' %}
    - Per the Health Act 2004 (Ireland) § s.49 (complaints) or NHS Complaints Regulations 2009
    - "Your Service Your Say" / local resolution / independent review
    {% endif %}

    The platform NEVER directly submits forms. Every extraction is marked analyst_review_required = True. Per the PoI clause (LICENSE.md §5.2): if the source names a private individual, set extraction_confidence = 0.

    {{ ctx.output_format }}

    {{ input }}
  "#
}
