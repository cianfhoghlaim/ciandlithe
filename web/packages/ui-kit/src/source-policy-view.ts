/**
 * CIANDLITHE 5th canonical AG-UI event type — the SourcePolicyView.
 *
 * Per the
 * openspec/changes/ciandlithe-source-policy-v1/specs/ciandlithe-source-policy/spec.md,
 * Requirement: The AG-UI source-policy-view event + Convex
 * sourcePolicyIndex table.
 *
 * The `SourcePolicyView` event is emitted by the Hono API gateway
 * after the Convex `sourcePolicyIndex` row is fetched for the
 * requested `(jurisdiction, source_id)` key. The per-persona web
 * apps (ciafagent-ga-public, ciafagent-met-public,
 * ciafagent-psni-public, ciafagent-reform-uk-pilot, etc.)
 * consume the event and render the
 * `<SourcePolicyCard>` component.
 *
 * The BUSL-1.1 v2 licence posture on every event (per the
 * `ciandlithe-ag-ui-event-types` spec) applies: the
 * `milestone_gate` field is the literal British Isles pipeline
 * gate (e.g. "BIPP v1 m2") and the `category` field is the
 * literal 6-value enum.
 */

export type SourceCategory =
  | "intelligence"
  | "military"
  | "policing"
  | "emergency_service"
  | "agency"
  | "political_party";

export type SourceMilestoneGate =
  | "BIPP v1 m1"
  | "BIPP v1 m2"
  | "BIPP v1 m3"
  | "BIDP v1 m1"
  | "BIDP v1 m2"
  | "BIDP v1 m3"
  | "BIIP v1 m1"
  | "BIIP v1 m2"
  | "BIIP v1 m3"
  | "reform-uk-pilot-workflow";

export interface SourcePolicyView {
  type: "source-policy-view";
  /** ISO 8601 timestamp */
  timestamp: string;
  /** The British Isles sub-nation (one of 8) */
  jurisdiction:
    | "ireland"
    | "uk"
    | "ni"
    | "scotland"
    | "wales"
    | "jersey"
    | "guernsey"
    | "iom";
  /** The canonical kebab-case source id (e.g. "data_police_uk") */
  source_id: string;
  /** The publishing authority (e.g. "UK Home Office") */
  body: string;
  /** The 6-value source category enum */
  category: SourceCategory;
  /** The OSINT ceiling text (what is in-scope vs out-of-scope) */
  osint_ceiling: string;
  /** The list of gaps (what is intentionally NOT covered) */
  gaps: string[];
  /** The BAML extraction function for this source (or null if N/A) */
  baml_function: string | null;
  /** The milestone gate that depends on this source */
  milestone_gate: SourceMilestoneGate;
  /** The ISO 8601 timestamp of the last per-source policy refresh */
  last_updated: string;
}
