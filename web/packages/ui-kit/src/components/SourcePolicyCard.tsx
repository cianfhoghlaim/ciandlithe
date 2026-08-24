/**
 * CIANDLITHE per-source context-aware React component.
 *
 * Per the
 * openspec/changes/ciandlithe-source-policy-v1/specs/ciandlithe-source-policy/spec.md,
 * Requirement: The SourcePolicyCard React component.
 *
 * Renders a per-source policy card that adapts to the source's
 * unique context (jurisdiction, body, category, OSINT ceiling,
 * gaps, BAML function, milestone gate). Reads from the Convex
 * `sourcePolicyIndex` table, embeds the 4 existing AG-UI event
 * types as action buttons (+ a "Run milestone" button that emits
 * the new `source-policy-view` event), and shows the OSINT
 * ceiling + the BUSL-1.1 v2 licence posture as a banner.
 *
 * The component is intentionally runtime-driven (per Q32 + Q36 +
 * Q42 of the locked plan) — the per-source configuration lives
 * in the Convex `sourcePolicyIndex` table + the CocoIndex
 * `ciandlithe.source_policy_index` LanceDB table, NOT in the
 * component itself.
 */
import * as React from "react";
import { useQuery } from "convex/react";
import type {
  FormFillRequest,
  OSINTEvidenceCitation,
  JurisdictionDisambiguation,
} from "../ag-ui-events";
import type { SourcePolicyView } from "../source-policy-view";

export type SourcePolicyCardProps = {
  jurisdiction: SourcePolicyView["jurisdiction"];
  source_id: string;
  on_run_milestone?: (milestone_gate: SourcePolicyView["milestone_gate"]) => void;
  on_form_fill?: (form_data: Record<string, string>, jurisdiction: SourcePolicyView["jurisdiction"]) => void;
  on_search_statute?: (jurisdiction: SourcePolicyView["jurisdiction"]) => void;
  on_citation?: (citation: OSINTEvidenceCitation) => void;
  on_jurisdiction_disambiguation?: (disambiguation: JurisdictionDisambiguation) => void;
};

const LICENSE_MARKER = "BUSL-1.1 v2 (British-Isles-only)" as const;

export function SourcePolicyCard({
  jurisdiction,
  source_id,
  on_run_milestone,
  on_form_fill,
  on_search_statute,
  on_citation,
  on_jurisdiction_disambiguation,
}: SourcePolicyCardProps): React.ReactElement {
  // Read from the Convex `sourcePolicyIndex` table.
  // The `api` is imported lazily so the component remains
  // import-safe in CI stubs where the Convex codegen has not run.
  const api = (() => {
    try {
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      return require("../../../../apps/ciafagent-ga-public/convex/_generated/api").api;
    } catch {
      return null;
    }
  })();

  const row = useQuery(
    // The Convex query function (lazy import to keep CI import-safe).
    api?.sourcePolicyIndex?.get ?? (() => null),
    api ? { jurisdiction, source_id } : "skip",
  ) as
    | {
        jurisdiction: SourcePolicyView["jurisdiction"];
        source_id: string;
        body: string;
        category: SourcePolicyView["category"];
        osint_ceiling: string;
        gaps: string[];
        baml_function: string | null;
        milestone_gate: SourcePolicyView["milestone_gate"];
        last_updated: string;
      }
    | null
    | undefined;

  const handle_run_milestone = React.useCallback(() => {
    if (!row || !on_run_milestone) return;
    on_run_milestone(row.milestone_gate);
  }, [row, on_run_milestone]);

  const handle_form_fill = React.useCallback(() => {
    if (!row || !on_form_fill) return;
    const form_data: Record<string, string> = {
      jurisdiction: row.jurisdiction,
      source_id: row.source_id,
    };
    on_form_fill(form_data, row.jurisdiction);
  }, [row, on_form_fill]);

  const handle_search_statute = React.useCallback(() => {
    if (!row || !on_search_statute) return;
    on_search_statute(row.jurisdiction);
  }, [row, on_search_statute]);

  const handle_citation = React.useCallback(() => {
    if (!row || !on_citation) return;
    const citation: OSINTEvidenceCitation = {
      type: "osint-evidence-citation",
      timestamp: new Date().toISOString(),
      source_url: `ciandlithe://source-policy-index/${row.jurisdiction}/${row.source_id}`,
      source_body: row.body,
      published_at: row.last_updated,
      excerpt: `Per-source policy view: ${row.body} (${row.category})`,
      relevance_score: 1.0,
    };
    on_citation(citation);
  }, [row, on_citation]);

  const handle_jurisdiction_disambiguation = React.useCallback(() => {
    if (!row || !on_jurisdiction_disambiguation) return;
    const disambiguation: JurisdictionDisambiguation = {
      type: "jurisdiction-disambiguation",
      timestamp: new Date().toISOString(),
      candidate_jurisdictions: [
        {
          jurisdiction: row.jurisdiction,
          reasoning: `This source's OSINT allowlist entry explicitly states jurisdiction=${row.jurisdiction}`,
        },
      ],
      confidence_scores: { [row.jurisdiction]: 1.0 },
    };
    on_jurisdiction_disambiguation(disambiguation);
  }, [row, on_jurisdiction_disambiguation]);

  if (!row) {
    return (
      <div
        className="source-policy-card source-policy-card--loading"
        data-source-policy-loading="true"
      >
        Loading per-source policy for {jurisdiction}/{source_id}...
      </div>
    );
  }

  return (
    <div className="source-policy-card" data-source-policy-key={`${row.jurisdiction}:${row.source_id}`}>
      <header className="source-policy-header">
        <h2 className="source-policy-body">{row.body}</h2>
        <span className="source-policy-category" data-category={row.category}>
          {row.category}
        </span>
        <span className="source-policy-jurisdiction" data-jurisdiction={row.jurisdiction}>
          {row.jurisdiction}
        </span>
      </header>

      <div className="source-policy-banner" role="status">
        <strong>OSINT ceiling:</strong> {row.osint_ceiling}
        <br />
        <strong>Licence:</strong> {LICENSE_MARKER}
      </div>

      {row.gaps && row.gaps.length > 0 ? (
        <div className="source-policy-gaps">
          <h3>What's NOT covered</h3>
          <ul>
            {row.gaps.map((gap, idx) => (
              <li key={`${row.source_id}:gap:${idx}`}>{gap}</li>
            ))}
          </ul>
        </div>
      ) : null}

      {row.baml_function ? (
        <div className="source-policy-baml">
          <strong>BAML function:</strong>{" "}
          <code>{row.baml_function}</code>
        </div>
      ) : null}

      <div className="source-policy-milestone">
        <strong>Milestone gate:</strong>{" "}
        <span data-milestone-gate={row.milestone_gate}>{row.milestone_gate}</span>
        <br />
        <small>
          <strong>Last updated:</strong> {row.last_updated}
        </small>
      </div>

      <div className="source-policy-actions">
        <button
          type="button"
          onClick={handle_run_milestone}
          data-action="run-milestone"
        >
          Run milestone: {row.milestone_gate}
        </button>
        <button
          type="button"
          onClick={handle_form_fill}
          data-action="form-fill"
        >
          Fill non-emergency form
        </button>
        <button
          type="button"
          onClick={handle_search_statute}
          data-action="search-statute"
        >
          Search statute
        </button>
        <button
          type="button"
          onClick={handle_citation}
          data-action="cite-source"
        >
          Cite this source
        </button>
        <button
          type="button"
          onClick={handle_jurisdiction_disambiguation}
          data-action="jurisdiction-disambiguation"
        >
          Clarify jurisdiction
        </button>
      </div>
    </div>
  );
}

export default SourcePolicyCard;
