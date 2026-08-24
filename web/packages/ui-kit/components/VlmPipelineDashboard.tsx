/**
 * CIANDLITHE — VlmPipelineDashboard component
 *
 * Per the canonical spec at
 * `openspec/specs/ciandlithe-vlm-ocr-pipeline/spec.md`.
 *
 * Reads the Convex `vlmPipelineDashboard` table (populated by
 * `cocoindex_flows/ciandlithe/vlm_pipeline_aggregator.py`) and
 * renders per-source cards with the VLM model + OCR confidence +
 * extraction pass-rate + cost + a status badge (`ok` / `warn` /
 * `critical`).
 *
 * Wholesale-copy pattern: cianfhoghlaim/cianfhoghlaim @ main branch
 * (per the openspec/changes/ciandlithe-repo-bootstrap-v2 change).
 * Licence: BUSL-1.1 (per LICENSE.md).
 */

import * as React from "react"

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type SourceStatus = "ok" | "warn" | "critical"

export interface VlmPipelineRow {
  source_id: string
  source_label: string
  vlm_model: string
  ocr_confidence: number
  extraction_pass_rate: number
  cost_credits: number
  latency_ms: number
  status: SourceStatus
  last_extraction_at: number
}

export interface VlmPipelineDashboardProps {
  /** The per-source rows to render. In production this comes from
   * `useQuery(api.vlmPipelineDashboard.list)`. For Storybook / tests,
   * pass an explicit array. */
  rows: VlmPipelineRow[]
  className?: string
}

// ---------------------------------------------------------------------------
// Status colour map (driven by the per-source `status` badge)
// ---------------------------------------------------------------------------

const STATUS_COLOUR: Record<SourceStatus, { bg: string; fg: string; label: string }> = {
  ok: { bg: "#16a34a", fg: "#ffffff", label: "ok" },          // green-600
  warn: { bg: "#f59e0b", fg: "#ffffff", label: "warn" },       // amber-500
  critical: { bg: "#dc2626", fg: "#ffffff", label: "critical" }, // red-600
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export function VlmPipelineDashboard({
  rows,
  className,
}: VlmPipelineDashboardProps): React.JSX.Element {
  if (rows.length === 0) {
    return (
      <div
        data-slot="vlm-pipeline-dashboard"
        data-state="empty"
        className={className}
      >
        <p>No VLM extraction data yet — run the aggregator App.</p>
      </div>
    )
  }

  return (
    <div
      data-slot="vlm-pipeline-dashboard"
      data-row-count={rows.length}
      className={className}
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
        gap: "16px",
      }}
    >
      {rows.map((row) => {
        const colour = STATUS_COLOUR[row.status]
        return (
          <article
            key={row.source_id}
            data-slot="vlm-pipeline-dashboard-card"
            data-source-id={row.source_id}
            data-status={row.status}
            style={{
              border: "1px solid #1e293b",
              borderRadius: 8,
              padding: 16,
              background: "#0f172a",
              color: "#f8fafc",
            }}
          >
            <header
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: 12,
              }}
            >
              <h3 style={{ margin: 0, fontSize: 14, fontWeight: 600 }}>
                {row.source_label}
              </h3>
              <span
                data-slot="vlm-pipeline-dashboard-badge"
                style={{
                  background: colour.bg,
                  color: colour.fg,
                  padding: "2px 8px",
                  borderRadius: 4,
                  fontSize: 11,
                  fontWeight: 600,
                  textTransform: "uppercase",
                }}
              >
                {colour.label}
              </span>
            </header>
            <dl
              style={{
                margin: 0,
                display: "grid",
                gridTemplateColumns: "1fr auto",
                gap: "4px 12px",
                fontSize: 12,
              }}
            >
              <dt style={{ color: "#94a3b8" }}>VLM model</dt>
              <dd style={{ margin: 0, fontFamily: "monospace" }}>
                {row.vlm_model}
              </dd>
              <dt style={{ color: "#94a3b8" }}>OCR confidence</dt>
              <dd style={{ margin: 0 }}>
                {(row.ocr_confidence * 100).toFixed(1)}%
              </dd>
              <dt style={{ color: "#94a3b8" }}>Pass rate</dt>
              <dd style={{ margin: 0 }}>
                {(row.extraction_pass_rate * 100).toFixed(1)}%
              </dd>
              <dt style={{ color: "#94a3b8" }}>Cost</dt>
              <dd style={{ margin: 0 }}>{row.cost_credits.toFixed(2)} cr</dd>
              <dt style={{ color: "#94a3b8" }}>Latency</dt>
              <dd style={{ margin: 0 }}>{row.latency_ms}ms</dd>
            </dl>
          </article>
        )
      })}
    </div>
  )
}