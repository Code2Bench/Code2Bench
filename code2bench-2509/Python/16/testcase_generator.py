from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def generate_summary(report_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate executive summary of fuzzing results."""
    summary = {
        "total_tools": 0,
        "tools_completed": 0,
        "critical_issues": 0,
        "recommendations": [],
        "overall_status": "unknown"
    }

    tools = ["hypothesis", "atheris", "schemathesis", "security_tests"]
    summary["total_tools"] = len(tools)

    completed_tools = 0
    critical_issues = 0

    for tool in tools:
        if tool in report_data and report_data[tool].get("status") == "completed":
            completed_tools += 1

        # Check for critical issues
        if tool == "atheris" and report_data.get(tool, {}).get("crashes_found", 0) > 0:
            critical_issues += 1
            summary["recommendations"].append(f"🚨 Atheris found {report_data[tool]['crashes_found']} crashes - investigate immediately")

        if tool == "schemathesis" and report_data.get(tool, {}).get("failures", 0) > 0:
            critical_issues += 1
            summary["recommendations"].append(f"⚠️ API fuzzing found {report_data[tool]['failures']} failures")

    summary["tools_completed"] = completed_tools
    summary["critical_issues"] = critical_issues

    # Determine overall status
    if completed_tools == len(tools) and critical_issues == 0:
        summary["overall_status"] = "✅ PASS"
    elif critical_issues > 0:
        summary["overall_status"] = "❌ CRITICAL ISSUES FOUND"
    elif completed_tools > 0:
        summary["overall_status"] = "⚠️ PARTIAL"
    else:
        summary["overall_status"] = "❓ NO RESULTS"

    # Add general recommendations
    if not summary["recommendations"]:
        summary["recommendations"].append("✅ No critical issues found in fuzzing")
        summary["recommendations"].append("🔄 Continue regular fuzzing as part of CI/CD")

    summary["recommendations"].append("📊 Review detailed results below for optimization opportunities")

    return summary

# Strategy for generating report data
def report_data_strategy():
    return st.dictionaries(
        keys=st.sampled_from(["hypothesis", "atheris", "schemathesis", "security_tests"]),
        values=st.one_of([
            st.fixed_dictionaries({
                "status": st.sampled_from(["completed", "failed", "running"]),
                "crashes_found": st.integers(min_value=0, max_value=10),
                "failures": st.integers(min_value=0, max_value=10)
            }),
            st.none()
        ]),
        min_size=0,
        max_size=4
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(report_data=report_data_strategy())
@example(report_data={})
@example(report_data={"atheris": {"status": "completed", "crashes_found": 1}})
@example(report_data={"schemathesis": {"status": "completed", "failures": 1}})
@example(report_data={"hypothesis": {"status": "completed"}, "atheris": {"status": "completed"}, "schemathesis": {"status": "completed"}, "security_tests": {"status": "completed"}})
@example(report_data={"hypothesis": {"status": "failed"}, "atheris": {"status": "running"}, "schemathesis": {"status": "completed"}, "security_tests": {"status": "completed"}})
def test_generate_summary(report_data: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    report_data_copy = copy.deepcopy(report_data)
    try:
        expected = generate_summary(report_data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"report_data": report_data},
        "Expected": expected
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)