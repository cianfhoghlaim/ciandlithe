/**
 * CIANDLITHE Convex schema definitions.
 *
 * Per the openspec/changes/ciandlithe-convex-schemas-v1/
 * specs/ciandlithe-convex-schemas/spec.md (6 canonical tables)
 * + the
 * openspec/changes/ciandlithe-source-policy-v1/specs/ciandlithe-source-policy/spec.md
 * (the 7th table — `sourcePolicyIndex`).
 *
 * Defines the canonical Convex tables for the 7 per-persona apps + the
 * Reform UK pilot app + the per-source context-aware UI.
 */

import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

import { sourcePolicyIndex } from "./source-policy-schemas";

// ============================================================================
// Shared tables (used by all 8 apps)
// ============================================================================

const chatSessions = defineTable({
  session_id: v.string(),
  user_id: v.string(),
  constituency: v.union(
    v.literal("ga"),
    v.literal("met"),
    v.literal("psni"),
    v.literal("reform_uk_pilot"),
  ),
  started_at: v.string(),  // ISO 8601
  ended_at: v.optional(v.string()),
  provider_used: v.string(),
  model_used: v.string(),
}).index("by_session_id", ["session_id"]);

const citationChains = defineTable({
  session_id: v.string(),
  source_url: v.string(),
  source_body: v.string(),
  excerpt: v.string(),
  relevance_score: v.number(),
  cited_at: v.string(),
}).index("by_session_id", ["session_id"]);

// ============================================================================
// GA-specific tables (An Garda Síochána public-facing + internal-facing)
// ============================================================================

const gardaFormFillDrafts = defineTable({
  session_id: v.string(),
  form_type: v.string(),  // "traffic_violation" | "foi_request" | etc.
  form_data: v.any(),  // The pre-filled form contents
  citation_chain: v.array(v.id("citationChains")),
  submitted_at: v.optional(v.string()),  // Always null (OSINT ceiling)
}).index("by_session_id", ["session_id"]);

// ============================================================================
// MET-specific tables (Metropolitan Police public-facing + internal-facing)
// ============================================================================

const metCrimeQueries = defineTable({
  session_id: v.string(),
  force_id: v.string(),  // e.g. "metropolitan"
  query: v.string(),
  results: v.any(),
  queried_at: v.string(),
}).index("by_force_id", ["force_id"]);

// ============================================================================
// PSNI-specific tables (Police Service of Northern Ireland)
// ============================================================================

const psniCrossBorderQueries = defineTable({
  session_id: v.string(),
  query: v.string(),
  psni_results: v.any(),
  garda_results: v.any(),  // Cross-border with An Garda Síochána
  queried_at: v.string(),
}).index("by_session_id", ["session_id"]);

// ============================================================================
// Reform UK pilot-specific tables
// ============================================================================

const reformUkPilotDossiers = defineTable({
  dossier_id: v.string(),
  target_entity: v.string(),  // e.g. "Richard Tice"
  focus: v.string(),  // e.g. "2024 election debt fraud"
  jurisdiction: v.literal("uk_hoc"),
  mentions_entities: v.array(v.string()),
  mentions_donors: v.array(v.any()),
  mentions_companies_house: v.array(v.any()),
  mentions_investigatory_powers: v.array(v.any()),
  osint_ceiling_enforced: v.literal(true),
  licence_posture: v.literal("BUSL-1.1 v2 (British-Isles-only)"),
  analyst_review_required: v.literal(true),
  created_at: v.string(),
}).index("by_dossier_id", ["dossier_id"]);

// ============================================================================
// Canonical schema export
// ============================================================================

export default defineSchema({
  chatSessions,
  citationChains,
  gardaFormFillDrafts,
  metCrimeQueries,
  psniCrossBorderQueries,
  reformUkPilotDossiers,
  sourcePolicyIndex,
});
