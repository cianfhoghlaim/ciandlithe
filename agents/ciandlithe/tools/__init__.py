"""CIANDLITHE per-cohort FunctionTool registry.

Mirrors the cianchosaint pattern at `agents/cianchosaint/tools/`.
Each tool wraps `composite_pilot_tool` with a default cohort.

Every tool's response MUST include the `osint_ceiling_enforced: True`
and `analyst_review_required: True` flags (per LICENSE.md §3.8 + §5.2).
"""

from __future__ import annotations

from .composite_pilot import (
    PILOT_PARTIES,
    admission_breach_tool,
    civil_action_outline_tool,
    composite_pilot_tool,
    education_discrimination_tool,
    employer_breach_tool,
    garda_discrimination_tool,
    medical_malpractice_tool,
)

__all__ = [
    "PILOT_PARTIES",
    "composite_pilot_tool",
    "medical_malpractice_tool",
    "employer_breach_tool",
    "garda_discrimination_tool",
    "education_discrimination_tool",
    "admission_breach_tool",
    "civil_action_outline_tool",
]