from typing import List

def _get_manual_recommendations(operation: str, failed_components: List[str]) -> List[str]:
    # Base recommendations for the operation
    base_recommendations = []
    if operation == 'network_discovery':
        base_recommendations = [
            "Manually test common ports using telnet or nc",
            "Check for service banners manually",
            "Use online port scanners as alternative"
        ]
    elif operation == 'web_discovery':
        base_recommendations = [
            "Manually browse common directories",
            "Check robots.txt and sitemap.xml",
            "Use browser developer tools for endpoint discovery",
            "Consider using online port scanners"
        ]
    elif operation == 'vulnerability_scanning':
        base_recommendations = [
            "Manually test for common vulnerabilities",
            "Check security headers using browser tools",
            "Perform manual input validation testing",
            "Try manual directory browsing",
            "Perform manual vulnerability testing"
        ]
    elif operation == 'subdomain_enumeration':
        base_recommendations = [
            "Use online subdomain discovery tools",
            "Check certificate transparency logs",
            "Perform manual DNS queries"
        ]
    
    # Additional recommendations for failed components
    additional_recommendations = []
    if 'nmap' in failed_components:
        additional_recommendations.append("Use nmap for network discovery and port scanning")
    if 'gobuster' in failed_components:
        additional_recommendations.append("Use gobuster for web vulnerability scanning")
    if 'nuclei' in failed_components:
        additional_recommendations.append("Use nuclei for automated vulnerability scanning")
    
    return base_recommendations + additional_recommendations