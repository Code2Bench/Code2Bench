from typing import Any, Dict

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