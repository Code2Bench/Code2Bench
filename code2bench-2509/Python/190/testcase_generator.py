from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
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

# Strategy for generating operations
operation_strategy = st.one_of([
    st.just("network_discovery"),
    st.just("web_discovery"),
    st.just("vulnerability_scanning"),
    st.just("subdomain_enumeration"),
    st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
])

# Strategy for generating failed components
failed_components_strategy = st.lists(
    st.one_of([
        st.just("nmap"),
        st.just("gobuster"),
        st.just("nuclei"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
    ]),
    min_size=0, max_size=5
)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(operation=operation_strategy, failed_components=failed_components_strategy)
@example(operation="network_discovery", failed_components=[])
@example(operation="web_discovery", failed_components=["nmap"])
@example(operation="vulnerability_scanning", failed_components=["gobuster", "nuclei"])
@example(operation="subdomain_enumeration", failed_components=["nmap", "gobuster"])
@example(operation="unknown_operation", failed_components=["unknown_component"])
def test_get_manual_recommendations(operation: str, failed_components: List[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    operation_copy = copy.deepcopy(operation)
    failed_components_copy = copy.deepcopy(failed_components)
    try:
        expected = _get_manual_recommendations(operation_copy, failed_components_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if operation in ["network_discovery", "web_discovery", "vulnerability_scanning", "subdomain_enumeration"] or any(
        component in ["nmap", "gobuster", "nuclei"] for component in failed_components
    ):
        generated_cases.append({
            "Inputs": {"operation": operation, "failed_components": failed_components},
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