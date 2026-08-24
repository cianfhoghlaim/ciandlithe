/**
 * CIANDLITHE wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/ciandlithe-repo-bootstrap-v2/specs/ciandlithe-bootstrap-v2/spec.md).
 * Migrated to ciandlithe: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
/**
 * @ciandlithe/ui-kit — the single canonical web UI surface
 *
 * Post-Phase A (2026-08-13-web-monorepo-consolidation-and-agent-integration-v1):
 * MERGES the 4 former packages (analytics / i18n / ui / config) into one
 * consolidated surface. The 4 sub-package directories still exist (for
 * code organization + re-exports), but the canonical entry point is this
 * file at the ui-kit root.
 */

// Re-export all 5 sub-surfaces
export * from "./analytics/src/index";
export * from "./i18n/src/index";
export * from "./components/src/index";
export * from "./config/src/index";
export { useIsMobile } from "./hooks/use-mobile";

// Re-export the per-source context-aware UI surface (per the
// openspec/changes/ciandlithe-source-policy-v1 change).
export { SourcePolicyCard } from "./components/SourcePolicyCard";
export type { SourcePolicyCardProps } from "./components/SourcePolicyCard";
