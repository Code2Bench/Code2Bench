from typing import List

from typing import List

def _get_manual_recommendations(operation: str, failed_components: List[str]) -> List[str]:
    recommendations = []

    base_recommendations = {
        "network_discovery": [
            "Manually test common ports using telnet or nc",
            "Check for service banners manually",
            "Use online port scanners as alternative"
        ],
        "web_discovery": [
            "Manually browse common directories",
            "Check robots.txt and sitemap.xml",
            "Use browser developer tools for endpoint discovery"
        ],
        "vulnerability_scanning": [
            "Manually test for common vulnerabilities",
            "Check security headers using browser tools",
            "Perform manual input validation testing"
        ],
        "subdomain_enumeration": [
            "Use online subdomain discovery tools",
            "Check certificate transparency logs",
            "Perform manual DNS queries"
        ]
    }

    recommendations.extend(base_recommendations.get(operation, []))

    # Add specific recommendations based on failed components
    for component in failed_components:
        if component == "nmap":
            recommendations.append("Consider using online port scanners")
        elif component == "gobuster":
            recommendations.append("Try manual directory browsing")
        elif component == "nuclei":
            recommendations.append("Perform manual vulnerability testing")

    return recommendations