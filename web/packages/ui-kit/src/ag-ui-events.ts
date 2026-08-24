/**
 * CIANDLITHE canonical AG-UI event types.
 *
 * Per the openspec/changes/ciandlithe-ag-ui-event-types-v1/
 * specs/ciandlithe-ag-ui-event-types/spec.md (4 canonical event
 * types) + the
 * openspec/changes/ciandlithe-source-policy-v1/specs/ciandlithe-source-policy/spec.md
 * (the 5th event — `SourcePolicyView`).
 *
 * The 5 canonical event types used across the 8 per-persona web apps
 * (ciafagent-ga-public, ciafagent-ga-internal, ciafagent-met-public,
 *  ciafagent-met-internal, ciafagent-psni-public,
 *  ciafagent-psni-internal, ciafagent-reform-uk-pilot, ciafagent-self-host)
 * + the Hono API gateway (web/apps/ciafagent-api/).
 *
 * BUSL-1.1 v2 licence posture: the FormFillResponse `user_next_step`
 * field is the literal `"copy_to_official_website"` — the agent NEVER
 * directly submits forms to operational systems.
 */

import type { SourcePolicyView } from "./source-policy-view";

// ============================================================================
// Type 1: FormFillRequest — the user initiated a non-emergency form fill
// ============================================================================

export interface FormFillRequest {
  type: "form-fill-request";
  /** ISO 8601 timestamp */
  timestamp: string;
  /** The constituency (ga | met | psni) */
  constituency: "ga" | "met" | "psni";
  /** The form schema URL (e.g. https://www.garda.ie/en/about-us/...) */
  form_schema_url: string;
  /** The pre-filled form data (from the BAML ExtractFormFields response) */
  pre_filled_data: Record<string, string>;
  /** The provider chain tier that generated this response (e.g. "unsloth_studio") */
  provider_used: string;
}

// ============================================================================
// Type 2: FormFillResponse — the agent's response to a FormFillRequest
// ============================================================================

export interface FormFillResponse {
  type: "form-fill-response";
  /** ISO 8601 timestamp */
  timestamp: string;
  /** The pre-filled form data, ready for the user to copy */
  form_data: Record<string, string>;
  /** The OSINT source URLs cited (per the OSINT allowlist) */
  source_urls: string[];
  /** The jurisdiction marker (per the BUSL-1.1 v2 licence posture) */
  jurisdiction: "ireland" | "uk" | "ni" | "scotland" | "wales" | "jersey" | "guernsey" | "iom";
  /** The license marker (always "BUSL-1.1 v2" for ciandlithe) */
  license_marker: "BUSL-1.1 v2";
  /** The user's next step — NEVER "submit", ALWAYS "copy to the official website" */
  user_next_step: "copy_to_official_website";
}

// ============================================================================
// Type 3: OSINTEvidenceCitation — the agent cited an OSINT source
// ============================================================================

export interface OSINTEvidenceCitation {
  type: "osint-evidence-citation";
  /** ISO 8601 timestamp */
  timestamp: string;
  /** The cited source URL (must be in the OSINT allowlist) */
  source_url: string;
  /** The source body (e.g. "An Garda Síochána", "UK Home Office", "HMCTS") */
  source_body: string;
  /** The published_at timestamp of the cited document */
  published_at: string;
  /** The excerpt from the document (max 500 chars) */
  excerpt: string;
  /** The relevance score (0-1, set by the BAML extraction) */
  relevance_score: number;
}

// ============================================================================
// Type 4: JurisdictionDisambiguation — when the agent needs to clarify the user's jurisdiction
// ============================================================================

export interface JurisdictionDisambiguation {
  type: "jurisdiction-disambiguation";
  /** ISO 8601 timestamp */
  timestamp: string;
  /** The candidate jurisdictions (the agent is asking the user to confirm) */
  candidate_jurisdictions: Array<{
    jurisdiction: "ireland" | "uk" | "ni" | "scotland" | "wales" | "jersey" | "guernsey" | "iom";
    reasoning: string;
  }>;
  /** The agent's confidence in each candidate (0-1) */
  confidence_scores: Record<string, number>;
}

// ============================================================================
// Union type for all AG-UI events
// ============================================================================

export type AGUIEvent =
  | FormFillRequest
  | FormFillResponse
  | OSINTEvidenceCitation
  | JurisdictionDisambiguation
  | SourcePolicyView;

export type { SourcePolicyView };
