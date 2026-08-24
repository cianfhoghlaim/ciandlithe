// BAML template: Ciandlithe Litigation Web Content Extractor
//
// Per the ciandlithe-repo-foundation-v1 openspec change (Phase: BAML
// templates bootstrap). Replaces the per-cohort stub prompts in
// `baml_src/ciandlithe/<cohort>/` with a single canonical extractor.
//
// Each stub function in the parent dirs (baml_src/ciandlithe/...) routes
// through this template via `baml_bulk_replace_stubs.py`. The template
// is shared (not duplicated per function) so a single improvement
// benefits all 7 BLIP v1 cohort extractors.
//
// Re-gen: `python scripts/baml_generate_templates.py`
// Re-apply: `python scripts/baml_bulk_replace_stubs.py`
//
// Ciandlithe-specific constraints (per LICENSE.md §3.8 + §5.2):
// - osint_ceiling_enforced: every extraction is gated by the OSINT
//   allowlist at dlt_sources/ciandlithe/common/osint_allowlist.yaml
// - analyst_review_required: every result is marked for manual review
// - PoI clause: extractions naming non-public individuals fail

function LitigationDomainExtractor(input: string) -> string {
  client ExtractEn
  prompt #"
    {{ _.role("user") }}
    You are an expert at extracting structured data from British Isles official legal sources (Irish Statute Book, Courts.ie, NICTS, Scottish Courts, HMCTS, Crown Dependencies courts, WRC decisions, PIAB decisions, NHS Resolution, GMC FTPAN decisions, HSE clinical-incident reports).

    Source type: markdown from a scraped web page (courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net / workplacerelations.ie / injuriesboard.ie / hse.ie / nhs.uk / hpsc.ie / gmc-uk.org / legislation.gov.uk / etc.)

    Extract:
    - title: the page title
    - publication_date: ISO 8601 publication date
    - jurisdiction: the British-Isles jurisdiction (Ireland / NI / Scotland / Wales / England / Jersey / Guernsey / IoM)
    - cohort: the BLIP v1 cohort (civil_litigation_forms / medical_malpractice / personal_injury_piab_nhs / workplace_relations_wrc_et / hse_nhs_complaints / statutes_si_court_rules / court_judgments_tribunal_decisions)
    - subject_area: the subject area covered (if any)
    - key_findings: list of key findings or facts
    - statutes_referenced: list of statute IDs referenced (e.g. "2018/0007/act", "c.27", "SI 2023/1115")
    - links: list of related URLs (MUST be from the OSINT allowlist)

    The platform NEVER directly submits forms to courts.ie / irishstatutebook.ie / nidirect.gov.uk / scotcourts.gov.uk / judiciary.uk / courtserve.net. This extractor generates structured output for manual review by the claimant or their solicitor ONLY.

    Per the PoI clause (LICENSE.md §5.2): if the source content names a private individual (not a public official), set extraction_confidence = 0 and return only the public procedural metadata.

    {{ ctx.output_format }}

    {{ input }}
  "#
}
