/**
 * CIANDLITHE — PipelineGraph component
 *
 * Per the canonical spec at
 * `openspec/specs/ciandlithe-pipeline-graph/spec.md`.
 *
 * Visualises the 5-stage Ciandlithe pipeline (DLT source → BAML
 * extraction → CocoIndex v1 embedding → LanceDB / DuckLake target →
 * AG-UI consumer) as an interactive per-persona graph for analysts,
 * lawyers, judges, and oversight officers.
 *
 * Migrated wholesale-copy pattern: cianfhoghlaim/cianfhoghlaim @
 * main branch (per the openspec/changes/ciandlithe-repo-bootstrap-v2
 * change). Licence: BUSL-1.1 (per LICENSE.md).
 */

import * as React from "react"

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type Persona = "analyst" | "lawyer" | "judge" | "oversight"

export type StageId = "dlt" | "baml" | "embedding" | "target" | "agui"

export interface PipelineStage {
  id: StageId
  label: string
}

export interface SourceNode {
  id: string
  label: string
  stageId: StageId
  vlmModel: string
  ocrConfidence: number
  extractionPassRate: number
  costCredits: number
  latencyMs: number
}

export interface EdgeBadge {
  sourceStageId: StageId
  targetStageId: StageId
  totalCostCredits: number
  avgLatencyMs: number
}

export interface PipelineGraphData {
  stages: PipelineStage[]
  sources: SourceNode[]
  edges: EdgeBadge[]
}

// ---------------------------------------------------------------------------
// Constants (5-stage pipeline layout)
// ---------------------------------------------------------------------------

const STAGES: PipelineStage[] = [
  { id: "dlt", label: "DLT source" },
  { id: "baml", label: "BAML extraction" },
  { id: "embedding", label: "CocoIndex v1 embedding" },
  { id: "target", label: "LanceDB / DuckLake target" },
  { id: "agui", label: "AG-UI consumer" },
]

const PERSONA_HIGHLIGHT: Record<Persona, string> = {
  analyst: "#0ea5e9",   // sky-500
  lawyer: "#a855f7",    // purple-500
  judge: "#f59e0b",     // amber-500
  oversight: "#ef4444", // red-500
}

// ---------------------------------------------------------------------------
// Layout helpers (pure CSS / SVG, no d3-force dependency)
// ---------------------------------------------------------------------------

const STAGE_WIDTH = 160
const STAGE_HEIGHT = 60
const STAGE_GAP = 20
const SVG_WIDTH = 960
const SVG_HEIGHT = 360

function stageX(index: number): number {
  return index * (STAGE_WIDTH + STAGE_GAP) + 20
}

function stageY(): number {
  return SVG_HEIGHT / 2 - STAGE_HEIGHT / 2
}

// ---------------------------------------------------------------------------
// Convex query stub (the vlmPipelineDashboard table is owned by the sibling
// ciandlithe-vlm-ocr-pipeline-v1 change)
// ---------------------------------------------------------------------------

export type DashboardQueryFn = () => PipelineGraphData | undefined

function stubDashboardQuery(): PipelineGraphData {
  return {
    stages: STAGES,
    sources: [],
    edges: STAGES.slice(0, -1).map((s, i) => ({
      sourceStageId: s.id,
      targetStageId: STAGES[i + 1]!.id,
      totalCostCredits: 0,
      avgLatencyMs: 0,
    })),
  }
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export interface PipelineGraphProps {
  persona: Persona
  /** Optional override for the Convex useQuery hook. */
  useDashboardQuery?: DashboardQueryFn
  className?: string
}

export function PipelineGraph({
  persona,
  useDashboardQuery,
  className,
}: PipelineGraphProps): React.JSX.Element {
  const data = useDashboardQuery ? useDashboardQuery() : stubDashboardQuery()

  const sourceByStage = React.useMemo(() => {
    const map = new Map<StageId, SourceNode[]>()
    if (!data) return map
    for (const s of data.sources) {
      const list = map.get(s.stageId) ?? []
      list.push(s)
      map.set(s.stageId, list)
    }
    return map
  }, [data])

  if (!data) {
    return (
      <div
        data-slot="pipeline-graph"
        data-persona={persona}
        data-state="loading"
        className={className}
      >
        <p>Loading pipeline graph…</p>
      </div>
    )
  }

  // `data` is non-null from here onwards (the guard above is the only
  // early-return). Re-bind to a narrowed type for the rest of the render.

  return (
    <div
      data-slot="pipeline-graph"
      data-persona={persona}
      className={className}
    >
      <svg
        viewBox={`0 0 ${SVG_WIDTH} ${SVG_HEIGHT}`}
        role="img"
        aria-label={`Ciandlithe pipeline graph for ${persona} persona`}
        style={{ width: "100%", height: "auto", maxWidth: SVG_WIDTH }}
      >
        {/* Stage nodes */}
        <g data-slot="pipeline-graph-stages">
          {STAGES.map((stage, i) => (
            <g key={stage.id} transform={`translate(${stageX(i)},${stageY()})`}>
              <rect
                width={STAGE_WIDTH}
                height={STAGE_HEIGHT}
                rx={8}
                fill="#1e293b"
                stroke={PERSONA_HIGHLIGHT[persona]}
                strokeWidth={2}
              />
              <text
                x={STAGE_WIDTH / 2}
                y={STAGE_HEIGHT / 2 + 4}
                textAnchor="middle"
                fill="#f8fafc"
                fontSize={12}
              >
                {stage.label}
              </text>
            </g>
          ))}
        </g>

        {/* Edge badges (per-stage cost + latency) */}
        <g data-slot="pipeline-graph-edges">
          {data.edges.map((edge) => {
            const sIdx = STAGES.findIndex((st) => st.id === edge.sourceStageId)
            const tIdx = STAGES.findIndex((st) => st.id === edge.targetStageId)
            const x = (stageX(sIdx) + STAGE_WIDTH + stageX(tIdx)) / 2
            const y = stageY() + STAGE_HEIGHT + 18
            return (
              <text
                key={`${edge.sourceStageId}-${edge.targetStageId}`}
                x={x}
                y={y}
                textAnchor="middle"
                fill="#94a3b8"
                fontSize={10}
              >
                {`${edge.totalCostCredits.toFixed(1)} cr · ${edge.avgLatencyMs}ms`}
              </text>
            )
          })}
        </g>

        {/* Source nodes (per-source hover cards) */}
        <g data-slot="pipeline-graph-sources">
          {data.sources.map((source) => {
            const stageIdx = STAGES.findIndex((st) => st.id === source.stageId)
            const siblings: SourceNode[] = sourceByStage.get(source.stageId) ?? []
            const idxInStage = siblings.findIndex((s: SourceNode) => s.id === source.id)
            const baseX = stageX(stageIdx) + STAGE_WIDTH / 2
            const baseY = stageY() - 30 - idxInStage * 14
            const tooltip = [
              source.label,
              `VLM: ${source.vlmModel}`,
              `OCR confidence: ${(source.ocrConfidence * 100).toFixed(1)}%`,
              `Pass rate: ${(source.extractionPassRate * 100).toFixed(1)}%`,
              `Cost: ${source.costCredits.toFixed(2)} credits`,
              `Latency: ${source.latencyMs}ms`,
            ].join("\n")
            return (
              <g key={source.id} transform={`translate(${baseX},${baseY})`}>
                <circle r={5} fill={PERSONA_HIGHLIGHT[persona]} />
                <title>{tooltip}</title>
              </g>
            )
          })}
        </g>
      </svg>
    </div>
  )
}