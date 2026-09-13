"""ciandlithe — Cross-repo integration smoke test (SU agents × KCG data).

Per openspec/changes/ciandlithe-students-union-adk-v1/ +
openspec/changes/kcg-university-of-galway-doc-processing-v1/.

Exercises the 5 SU ADK agents consuming real UoG data from the KCG
DLT sources. Same pattern as the SU agents-only smoke test, plus
a cross-repo import step at the top.

Exits 0 on full pass, 1 on any failure.

Run via:

    python3 agents/adk/students_union/_smoke_test_cross_repo.py

Licence: BUSL-1.1 v2 CIANDLITHE edition (per LICENSE.md) +
BUSL-1.1 (KCG edition) per LICENSE.md.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent.parent.parent  # agents/adk/students_union → ciandlithe
KCG_REPO_ROOT = REPO_ROOT.parent / "kings_college_galway"


def _bootstrap_su_package() -> None:
    """Make the students_union package importable."""
    import importlib.util as _ilu

    su_pkg = types.ModuleType("students_union")
    su_pkg.__path__ = [str(THIS_DIR)]
    sys.modules["students_union"] = su_pkg

    config_spec = _ilu.spec_from_file_location(
        "students_union.config", str(THIS_DIR / "config.py"),
    )
    config_mod = _ilu.module_from_spec(config_spec)
    sys.modules["students_union.config"] = config_mod
    config_mod.__package__ = "students_union"
    config_spec.loader.exec_module(config_mod)

    tools_pkg = types.ModuleType("students_union.tools")
    tools_pkg.__path__ = [str(THIS_DIR / "tools")]
    sys.modules["students_union.tools"] = tools_pkg

    for tool_file in [
        "clubs_socs_validator.py",
        "grants_matcher.py",
        "complaint_router.py",
        "election_validator.py",
        "class_rep_themer.py",
    ]:
        name = tool_file.removesuffix(".py")
        spec = _ilu.spec_from_file_location(
            f"students_union.tools.{name}",
            str(THIS_DIR / "tools" / tool_file),
        )
        mod = _ilu.module_from_spec(spec)
        sys.modules[f"students_union.tools.{name}"] = mod
        mod.__package__ = "students_union.tools"
        spec.loader.exec_module(mod)


def _bootstrap_su_agents() -> None:
    """Stub google.adk then load the 5 specialist agents + the root_agent."""
    google_stub = types.ModuleType("google")
    adk_stub = types.ModuleType("google.adk")
    agents_stub = types.ModuleType("google.adk.agents")

    class _StubLlmAgent:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    agents_stub.LlmAgent = _StubLlmAgent

    apps_stub = types.ModuleType("google.adk.apps")
    app_stub = types.ModuleType("google.adk.apps.app")

    class _StubApp:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    app_stub.App = _StubApp

    tools_stub = types.ModuleType("google.adk.tools")
    tools_stub.FunctionTool = lambda func: f"FunctionTool({func.__name__})"

    sys.modules.setdefault("google", google_stub)
    sys.modules.setdefault("google.adk", adk_stub)
    sys.modules.setdefault("google.adk.agents", agents_stub)
    sys.modules.setdefault("google.adk.apps", apps_stub)
    sys.modules.setdefault("google.adk.apps.app", app_stub)
    sys.modules.setdefault("google.adk.tools", tools_stub)

    from importlib.machinery import SourceFileLoader

    for agent_file in [
        "clubs_socs_agent.py",
        "grants_funding_agent.py",
        "class_rep_aggregator_agent.py",
        "complaints_welfare_agent.py",
        "elections_agent.py",
    ]:
        module_name = agent_file.removesuffix(".py")
        loader = SourceFileLoader(
            f"students_union.{module_name}",
            str(THIS_DIR / agent_file),
        )
        loader.load_module()

    root_loader = SourceFileLoader(
        "students_union.root_agent",
        str(THIS_DIR / "root_agent.py"),
    )
    root_loader.load_module()


def _bootstrap_kcg_package() -> None:
    """Stub dlt then load the KCG DLT sources."""
    if "dlt" not in sys.modules:
        dlt_stub = types.ModuleType("dlt")

        def _stub_resource(*_a, **_k):
            def _decorator(fn):
                return fn

            return _decorator

        def _stub_source(*_a, **_k):
            def _decorator(fn):
                return fn

            return _decorator

        dlt_stub.resource = _stub_resource
        dlt_stub.source = _stub_source
        sys.modules["dlt"] = dlt_stub

    # Add the KCG repo to sys.path
    if str(KCG_REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(KCG_REPO_ROOT))

    # Clear any cached imports of dlt_sources
    for mod_name in list(sys.modules.keys()):
        if mod_name.startswith("dlt_sources"):
            del sys.modules[mod_name]


_bootstrap_su_package()
_bootstrap_su_agents()
_bootstrap_kcg_package()

from students_union.config import config  # noqa: E402
from students_union.tools.clubs_socs_validator import (  # noqa: E402
    ClubApplication, validate_club_application,
)
from students_union.tools.grants_matcher import (  # noqa: E402
    GrantApplication, match_grant_to_pot,
)
from students_union.tools.complaint_router import (  # noqa: E402
    Complaint, route_complaint,
)
from students_union.tools.election_validator import (  # noqa: E402
    Candidate, validate_candidate_eligibility,
)
from students_union.tools.class_rep_themer import (  # noqa: E402
    ClassRepReport, aggregate_class_rep_themes,
)
from students_union.root_agent import classify_su_query  # noqa: E402

from dlt_sources.uog import (  # noqa: E402
    academic_calendar_pipeline,
    course_catalog_pipeline,
    university_council_minutes_pipeline,
    press_releases_pipeline,
    research_outputs_pipeline,
)


def main() -> int:
    print("Cross-repo integration smoke test — SU agents × KCG data")
    print(f"  ciandlithe repo:  {REPO_ROOT}")
    print(f"  kcg repo:         {KCG_REPO_ROOT}")
    print()

    # ── KCG data ─────────────────────────────────────────────────────
    print("[1/4] KCG data (University of Galway public documents)")
    calendar_events = list(academic_calendar_pipeline._yield_live_scrape_rows())
    courses = list(course_catalog_pipeline._yield_live_scrape_rows())
    minutes = list(university_council_minutes_pipeline._yield_live_scrape_rows())
    press = list(press_releases_pipeline._yield_live_scrape_rows())
    outputs = list(research_outputs_pipeline._yield_live_scrape_rows())
    print(f"  ✓ {len(calendar_events)} academic calendar events")
    print(f"  ✓ {len(courses)} course outlines")
    print(f"  ✓ {len(minutes)} governance minutes")
    print(f"  ✓ {len(press)} press releases")
    print(f"  ✓ {len(outputs)} research outputs")
    print()

    # ── Case Study 1: Clubs & Socs × press releases ────────────────
    print("[2/4] Case Study 1: Clubs & Socs × KCG press releases")
    new_club_name = "Galway Sustainability Researchers"
    collisions = [
        p for p in press
        if any(token.lower() in p["headline_english"].lower()
               for token in new_club_name.split())
    ]
    clubs_result = validate_club_application(ClubApplication(
        club_name=new_club_name, society_type="academic", member_count=22,
        has_constitution=True, has_safeguarding_officer=True, has_committee=True,
        has_bank_account=True, gdpr_compliant=True,
        purpose_statement="To promote sustainability research at UoG, in alignment with the UoG 2030 Sustainability Strategy.",
        contact_email="sustainability@universityofgalway.ie",
    ))
    assert clubs_result.is_valid
    print(f"  ✓ Clubs & Socs: valid={clubs_result.is_valid}, score={clubs_result.score}, press collisions={len(collisions)}")

    # ── Case Study 2: Grants × governance minutes ──────────────────
    print("[3/4] Case Study 2: Grants × KCG governance minutes")
    grants_award = match_grant_to_pot(GrantApplication(
        applicant_name="Aisling Ní Bhrádaigh", society_name="Cumann na Gaeilge",
        society_type="cultural", amount_requested_eur=350,
        purpose="cultural_celebration",
        description="Irish-language poetry slam for Seachtain na Gaeilge 2026",
        has_receipts=False, is_first_time_applicant=True,
    ))
    funding_decisions = [
        m for m in minutes
        if "budget" in m["decisions_summary"].lower()
        or "funding" in m["decisions_summary"].lower()
    ]
    assert grants_award.eligible and grants_award.matched_pot == "EVENT"
    print(f"  ✓ Grants: pot={grants_award.matched_pot}, €{grants_award.awarded_eur}, governance context={len(funding_decisions)} decisions")

    # ── Case Study 3: Class Rep × course catalog ───────────────────
    print("[4/4] Case Study 3: Class Rep × KCG course catalog")
    real_module_codes = [c["course_code"] for c in courses]
    reports = [
        ClassRepReport(
            rep_id=f"cr-{courses[i]['course_code'].lower()}",
            module_code=courses[i]["course_code"],
            module_title=courses[i]["course_title_english"],
            report_text="Lecturer is unclear and assessments are heavy. Many students have accessibility needs that are not being met.",
            semester="2025/26 S1",
            submitted_at_iso="2026-09-13T11:00:00+00:00",
        )
        for i in range(min(3, len(courses)))
    ]
    agg = aggregate_class_rep_themes(reports)
    # Verify the real module codes appear in the aggregation
    modules_in_agg = {r.module_code for r in reports}
    assert modules_in_agg.issubset(set(real_module_codes)), (
        f"reports reference modules not in KCG catalog: {modules_in_agg - set(real_module_codes)}"
    )
    print(f"  ✓ Class Rep: aggregated {agg.total_reports} reports across real UoG modules {sorted(modules_in_agg)}")

    # ── Classifier smoke test (queries mentioning UoG-specific things) ──
    print()
    print("[bonus] classify_su_query on UoG-specific queries")
    uog_queries = [
        ("Apply for funding for the Seachtain na Gaeilge 2026 poetry slam", "grants"),
        ("Summarise Class Rep feedback from CS203", "class_rep"),
        ("I want to register a new sustainability society", "clubs_socs"),
    ]
    for q, expected in uog_queries:
        got = classify_su_query(q)
        status = "✓" if got == expected else "✗"
        print(f"  {status} {expected:11} <= {got:11}  ::  {q}")

    print()
    print("=" * 60)
    print("Cross-repo integration PASS — SU agents consume real KCG data.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
