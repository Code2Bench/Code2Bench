from typing import Dict, Any

def generate_summary(report_data: Dict[str, Any]) -> Dict[str, Any]:
    total_tools = len(report_data)
    tools_completed = 0
    critical_issues = 0
    
    for tool in report_data:
        if report_data[tool]['status'] == 'completed':
            tools_completed += 1
        if report_data[tool]['status'] == 'critical':
            critical_issues += 1
    
    recommendations = []
    if critical_issues > 0:
        recommendations.append("⚠️ Critical issues found. Please address them immediately.")
    
    if tools_completed == total_tools:
        overall_status = "✅ PASS"
    elif critical_issues > 0:
        overall_status = "❌ CRITICAL ISSUES FOUND"
    else:
        overall_status = "❓ NO RESULTS"
    
    return {
        'total_tools': total_tools,
        'tools_completed': tools_completed,
        'critical_issues': critical_issues,
        'recommendations': recommendations,
        'overall_status': overall_status
    }