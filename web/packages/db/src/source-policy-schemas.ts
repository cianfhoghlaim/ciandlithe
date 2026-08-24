/**
 * CIANDLITHE 7th canonical Convex table — `sourcePolicyIndex`.
 *
 * Per the
 * openspec/changes/ciandlithe-source-policy-v1/specs/ciandlithe-source-policy/spec.md,
 * Requirement: The AG-UI source-policy-view event + Convex
 * sourcePolicyIndex table.
 *
 * The `sourcePolicyIndex` table is the per-source context-aware
 * mirror of the CocoIndex `ciandlithe.source_policy_index`
 * LanceDB table. The Convex table is the live state for the
 * per-persona web apps; the CocoIndex table is the semantic-search
 * index that the Hono API gateway queries for similar sources.
 *
 * The BUSL-1.1 v2 licence posture on the table (per the
 * `ciandlithe-convex-schemas` spec) applies: the `milestone_gate`
 * field is the literal British Isles pipeline gate.
 */

import { defineTable } from "convex/server";
import { v } from "convex/values";

// The 8 British Isles sub-nations (per the canonical jurisdiction enum).
const jurisdictionLiteral = v.union(
  v.literal("ireland"),
  v.literal("uk"),
  v.literal("ni"),
  v.literal("scotland"),
  v.literal("wales"),
  v.literal("jersey"),
  v.literal("guernsey"),
  v.literal("iom"),
);

// The 6-value source category enum.
const categoryLiteral = v.union(
  v.literal("intelligence"),
  v.literal("military"),
  v.literal("policing"),
  v.literal("emergency_service"),
  v.literal("agency"),
  v.literal("political_party"),
);

// The milestone gate enum (the 10 canonical British Isles pipeline gates).
const milestoneGateLiteral = v.union(
  v.literal("BIPP v1 m1"),
  v.literal("BIPP v1 m2"),
  v.literal("BIPP v1 m3"),
  v.literal("BIDP v1 m1"),
  v.literal("BIDP v1 m2"),
  v.literal("BIDP v1 m3"),
  v.literal("BIIP v1 m1"),
  v.literal("BIIP v1 m2"),
  v.literal("BIIP v1 m3"),
  v.literal("reform-uk-pilot-workflow"),
);

export const sourcePolicyIndex = defineTable({
  jurisdiction: jurisdictionLiteral,
  source_id: v.string(),
  body: v.string(),
  category: categoryLiteral,
  osint_ceiling: v.string(),
  gaps: v.array(v.string()),
  baml_function: v.string(),
  milestone_gate: milestoneGateLiteral,
  last_updated: v.string(),
}).index("by_jurisdiction_source", ["jurisdiction", "source_id"]);

export default sourcePolicyIndex;
