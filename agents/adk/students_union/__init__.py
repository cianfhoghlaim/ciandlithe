"""ciandlithe — Students' Union (USG / Ollscoil na Gaillimhe) Google ADK agents.

Per openspec/changes/ciandlithe-students-union-adk-v1/.

5 specialist agents + 1 root orchestrator covering the 5 most common
Students' Union workflows:

  1. Clubs & Societies Registration (clubs_socs_agent)
  2. Grants & Funding Triage (grants_funding_agent)
  3. Class Rep Feedback Aggregator (class_rep_aggregator_agent)
  4. Complaints & Welfare Triage (complaints_welfare_agent)
  5. Election & Referendum Workflow (elections_agent)

Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md).
"""
from .root_agent import root_agent, students_union_app

__all__ = [
    "root_agent",
    "students_union_app",
    "clubs_socs_agent",
    "grants_funding_agent",
    "class_rep_aggregator_agent",
    "complaints_welfare_agent",
    "elections_agent",
]
