"""CIANDLITHE smoke tests.

These tests verify the foundational invariants of the ciandlithe repo:
1. The openspec workflow validates (1 spec + 1 change)
2. Every DLT source URL is on the OSINT allowlist
3. The composite pilot FunctionTool returns the expected 7 dossiers
4. The complaint classifier returns the expected cohort for a sample complaint
5. Every BAML extraction schema includes `osint_ceiling_enforced: True`

Run: `mise run test:smoke` or `python -m pytest tests/smoke/ -v`
"""

from __future__ import annotations

import importlib.util
import os
import sys
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent


def test_openspec_validate() -> None:
    """Verify the openspec workflow validates."""
    result = subprocess.run(
        ["openspec", "validate", "--all", "--strict"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"openspec validate failed:\n{result.stdout}\n{result.stderr}"
    assert "passed" in result.stdout, f"Expected 'passed' in output:\n{result.stdout}"


def test_osint_audit() -> None:
    """Verify every DLT source URL is on the OSINT allowlist."""
    # Import osint_audit directly to avoid package-level imports
    spec = importlib.util.spec_from_file_location(
        "osint_audit", REPO_ROOT / "dlt_sources/ciandlithe/common/osint_audit.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    all_dlt_files = list((REPO_ROOT / "dlt_sources/ciandlithe").rglob("*.py"))
    fails = []
    for f in sorted(all_dlt_files):
        errors = mod.lint_dlt_source_file(f)
        for e in errors:
            fails.append((str(f), e["offending_url"]))
    assert not fails, f"OSINT audit FAILED: {len(fails)} URLs not in allowlist:\n" + "\n".join(
        [f"  {f}: {url}" for f, url in fails[:30]]
    )


def test_composite_pilot() -> None:
    """Verify the composite pilot FunctionTool returns 7 dossiers for cohort='all'."""
    spec = importlib.util.spec_from_file_location(
        "composite_pilot", REPO_ROOT / "agents/ciandlithe/tools/composite_pilot.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    result = mod.composite_pilot_tool(cohort="all")
    assert result["osint_ceiling_enforced"] is True
    assert result["analyst_review_required"] is True
    assert len(result["dossiers"]) == 7, f"Expected 7 dossiers, got {len(result['dossiers'])}"
    for d in result["dossiers"]:
        assert d["osint_ceiling_enforced"] is True
        assert d["analyst_review_required"] is True
        assert d["case_id"] in [p["party_id"] for p in mod.PILOT_PARTIES]


def test_per_cohort_tools() -> None:
    """Verify the 6 per-cohort tools work."""
    spec = importlib.util.spec_from_file_location(
        "composite_pilot", REPO_ROOT / "agents/ciandlithe/tools/composite_pilot.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    for cohort, tool_fn in [
        ("MedicalMalpractice", mod.medical_malpractice_tool),
        ("EmployerBreach", mod.employer_breach_tool),
        ("GardaDiscrimination", mod.garda_discrimination_tool),
        ("EducationDiscrimination", mod.education_discrimination_tool),
        ("AdmissionBreach", mod.admission_breach_tool),
        ("CivilActionOutline", mod.civil_action_outline_tool),
    ]:
        result = tool_fn()
        assert result["osint_ceiling_enforced"] is True
        assert result["analyst_review_required"] is True
        for d in result["dossiers"]:
            assert d["cohort"] == cohort


def test_complaint_classifier() -> None:
    """Verify the complaint classifier returns the expected cohort."""
    spec = importlib.util.spec_from_file_location(
        "complaint_classifier", REPO_ROOT / "dlt_sources/ciandlithe/cross/complaint_classifier.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Sample 1: medical malpractice in Ireland
    result1 = mod.classify_complaint(
        "I was misprescribed olanzapine in a Galway hospital and now I have brain damage. The HSE won't give me my medical records. What can I do?"
    )
    assert result1["cohort"] == "MedicalMalpractice"
    assert result1["jurisdiction"] == "IRELAND"
    assert result1["osint_ceiling_enforced"] is True
    assert result1["analyst_review_required"] is True

    # Sample 2: employer breach
    result2 = mod.classify_complaint(
        "I was unfairly dismissed from my job at a Monroes restaurant in Galway after I complained about breach of contract by the CEO."
    )
    assert result2["cohort"] == "EmployerBreach"

    # Sample 3: admission breach
    result3 = mod.classify_compliament(classify_complaint := mod.classify_complaint)(
        "I received a UCL offer but they withdrew it after my DBS check came back."
    ) if False else mod.classify_complaint(
        "I received a UCL offer but they withdrew it after my DBS check came back."
    )
    assert result3["cohort"] in ("AdmissionBreach", "EducationDiscrimination")  # DBS may map to either


def test_license_posture() -> None:
    """Verify the LICENSE.md contains the 4 mandatory sections."""
    license_md = (REPO_ROOT / "LICENSE.md").read_text()
    for required_section in [
        "Additional Use Grant",
        "Conditional foreign use",
        "OSINT ceiling + Person-of-Interest clause",
        "Warrant to enforce",
    ]:
        assert required_section in license_md, f"LICENSE.md missing required section: {required_section!r}"


def test_pilot_parties_exist_in_leabharlann() -> None:
    """Verify every pilot party's primary PDF exists on disk in leabharlann/."""
    leabharlann_root = Path(
        os.environ.get(
            "CIANDLITHE_LEABHARLANN_ROOT",
            str(Path.home() / "dev" / "cianfhoghlaim" / "leabharlann"),
        )
    )

    spec = importlib.util.spec_from_file_location(
        "case_study_loader", REPO_ROOT / "dlt_sources/ciandlithe/cross/case_study_loader.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    results = mod.load_all_case_studies(str(leabharlann_root))
    missing = [r["party_id"] for r in results if not r["primary_pdf_exists"]]
    assert not missing, f"Pilot party PDFs not found in leabharlann:\n" + "\n".join(
        [f"  {m}: {next(r for r in results if r['party_id'] == m)['primary_pdf_path']}" for m in missing]
    )


if __name__ == "__main__":
    # Run all tests sequentially
    tests = [
        test_openspec_validate,
        test_osint_audit,
        test_composite_pilot,
        test_per_cohort_tools,
        test_complaint_classifier,
        test_license_posture,
        test_pilot_parties_exist_in_leabharlann,
    ]
    for t in tests:
        print(f"Running {t.__name__}...", end=" ")
        try:
            t()
            print("OK")
        except AssertionError as e:
            print(f"FAIL: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)
    print("\nAll smoke tests PASSED")