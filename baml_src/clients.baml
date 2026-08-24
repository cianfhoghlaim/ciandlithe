// BAML Client Configuration for Ciandlithe (the 4-tier ModelProviderRouter)
//
// ====== Architecture: Unsloth Studio primary -> LiteLLM -> MiniMax Token Plan -> Gemini ======
//
// Per the ciandlithe-repo-foundation-v1 + ciandlithe-baml-schemas-v1 + ciandlithe-provider-router-v1
// openspec changes, Ciandlithe routes every LLM
// call through a 4-tier fallback chain (per the baml_src/_shared/provider_router.py
// module that ships with the ciandlithe-repo-foundation-v1 openspec change):
//
//   Tier 1 (PRIMARY)   — Unsloth Studio    (local API at unsloth-serve:8889/api/v1)
//   Tier 2             — LiteLLM Proxy     (litellm.cianfhoghlaim.ie)
//   Tier 3             — MiniMax Token Plan (direct API at api.minimax.io/v1)
//   Tier 4 (LAST RESORT) — Gemini API      (generativelanguage.googleapis.com)
//
// Each BAML function below declares its PREFERRED client (`Primary`,
// `Fallback`, `Emergency`) — these are the 3 named clients the
// ModelProviderRouter recognises. The router itself dynamically
// picks the active provider based on circuit-breaker state, latency,
// and per-deployment config (deployment-choice.yaml).

// ====== PRIMARY: Unsloth Studio (Tier 1) ======
// Local self-hosted inference (BAAI/bge-m3, Qwen2.5-VL-7B-Instruct,
// etc.). Default for every cianchosaint LLM call.

client<llm> Primary {
  provider "openai-generic"
  options {
    base_url env.UNSLOTH_STUDIO_BASE_URL
    api_key env.UNSLOTH_STUDIO_API_KEY
    model "minimax-m3"
    temperature 0.0
    max_tokens 8192
    timeout 30
  }
}

// ====== FALLBACK: LiteLLM Proxy (Tier 2) ======
// Routes through the existing litellm.cianfhoghlaim.ie proxy.
// Activated when Unsloth Studio is unavailable (5xx, timeout, or
// circuit-breaker open).

client<llm> Fallback {
  provider "openai-generic"
  options {
    base_url env.LITELLM_BASE_URL
    api_key env.LITELLM_MASTER_KEY
    model "minimax-m3"
    temperature 0.0
    max_tokens 8192
    timeout 30
  }
}

// ====== EMERGENCY: MiniMax Token Plan (Tier 3) ======
// Direct API to api.minimax.io/v1 (the user holds a MiniMax coding
// plan). Activated when both Unsloth Studio AND LiteLLM are down.

client<llm> Emergency {
  provider "openai-generic"
  options {
    base_url env.MINIMAX_BASE_URL
    api_key env.MINIMAX_TOKEN_PLAN_KEY
    model "minimax-m3"
    temperature 0.0
    max_tokens 8192
    timeout 30
  }
}

// ====== LAST RESORT: Gemini API (Tier 4) ======
// Direct API to generativelanguage.googleapis.com. Activated when
// all 3 prior tiers are down. NOT used for cianchosaint default —
// only for last-resort fallback.

client<llm> LastResort {
  provider "openai-generic"
  options {
    base_url env.GEMINI_BASE_URL
    api_key env.GEMINI_API_KEY
    model "gemini-2.5-pro"
    temperature 0.0
    max_tokens 8192
    timeout 30
  }
}

// ====== Function-role client assignments ======
// Each BAML function declares its preferred client. The
// ModelProviderRouter picks the active provider dynamically based on
// circuit-breaker state + latency + per-deployment config.

class CivilLitigationForm {
  court_level CourtLevel
  form_number string
  form_title string
  category enum<PersonalInjury, Family, Criminal, Civil, Probate, Licensing, Taxation, Other>
  jurisdiction Jurisdiction
  source_url string
  fee_eur float?
  downloadable_url string?
  content_hash string?
}

function ExtractCivilLitigationForm(input: string) -> CivilLitigationForm {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured civil-litigation form metadata from the
    following British Isles official source content (courts.ie /
    NICTS / scotcourts.gov.uk / judiciary.uk / courtserve.net).
    {{ input }}
  "#
}

class CourtJudgment {
  court enum<UKSupremeCourt, UKCourtOfAppeal, UKHighCourt, UKCrownCourt, UKMagistrates, NICrownCourt, NICounty, NIHighCourt, ROIHighCourt, ROICircuitCourt, ROIDistrictCourt, ROISupremeCourt, ROICourtOfAppeal, ScotCourtOfSession, ScotHighCourtJusticiary, ScotSheriffCourt, JerseyRoyalCourt, GuernseyRoyalCourt, IoMHighCourt>
  neutral_citation string
  case_name string
  judges string[]
  parties string[]
  judgment_date date?
  subject_matter string[]
  police_powers_invoked string[]
  legislation_referenced StatuteRef[]
  precedential_value enum<Binding, Persuasive, FirstInstance, Obiter>
  reporting_restriction enum<None, AnonymisationOrder, Section_4_2_Contempt, GDPR>
  pdf_url string
}

function ExtractCourtJudgment(input: string) -> CourtJudgment {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured court judgment metadata from the
    following British Isles official source content.
    {{ input }}
  "#
}

class StatuteReference {
  jurisdiction enum<Ireland, UK, Scotland, Wales, NI, Jersey, Guernsey, IoM>
  statute_id string
  canonical_citation string
  title string
  section_references string[]
  effective_date date?
  source_url string
}

function ExtractStatuteReference(input: string) -> StatuteReference {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured statute reference from the following
    British Isles statute book / legislation.gov.uk / irishstatutebook.ie
    content.
    {{ input }}
  "#
}

function ExtractWRCAdjudication(input: string) -> string {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Workplace Relations Commission adjudication
    decision from the following workplacerelations.ie page.
    {{ input }}
  "#
}

function ExtractPIABApplication(input: string) -> string {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Personal Injuries Assessment Board application
    from the following injuriesboard.ie page.
    {{ input }}
  "#
}

function ExtractHSEIncidentReport(input: string) -> string {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Health Service Executive clinical incident
    report from the following hse.ie / hpsc.ie page.
    {{ input }}
  "#
}

function ExtractCrossBorderFinding(input: string) -> string {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Reconcile the structured findings from the following multiple
    British-Isles sources (NI + ROI / Scotland + England / Crown Dependencies).
    The reconciliation MUST respect the CTA (Common Travel Area) data-sharing
    constraints + the PoI clause (LICENSE.md §5.2).
    {{ input }}
  "#
}
