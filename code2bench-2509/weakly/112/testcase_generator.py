from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from datetime import datetime
from typing import Any, Dict, List

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def generate_test_report(
    test_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    total_tests = len(test_results)
    passed_tests = sum(
        1 for result in test_results if result["success"]
    )
    failed_tests = total_tests - passed_tests
    total_time = sum(
        result["execution_time"] for result in test_results
    )

    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "total_execution_time": total_time,
            "average_execution_time": (
                total_time / total_tests if total_tests > 0 else 0
            ),
        },
        "test_results": test_results,
    }

    return report

# Strategies for generating inputs
def test_result_strategy():
    return st.fixed_dictionaries({
        "success": st.booleans(),
        "execution_time": st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
        "details": st.text(max_size=50)
    })

def test_results_strategy():
    return st.lists(test_result_strategy(), min_size=0, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(test_results=test_results_strategy())
@example(test_results=[])
@example(test_results=[{"success": True, "execution_time": 0.0, "details": ""}])
@example(test_results=[{"success": False, "execution_time": 1.0, "details": "error"}])
@example(test_results=[{"success": True, "execution_time": 0.5, "details": "test1"}, {"success": False, "execution_time": 1.5, "details": "test2"}])
def test_generate_test_report(test_results: List[Dict[str, Any]]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    test_results_copy = copy.deepcopy(test_results)

    # Call func0 to verify input validity
    try:
        expected = generate_test_report(test_results_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "test_results": test_results_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)