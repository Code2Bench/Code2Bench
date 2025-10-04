import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import modify_url as func1
import urllib.parse
from typing import List

# Ground truth function (func0), keep its original implementation and name
def modify_url(url: str, remove: List[str]) -> str:
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
    params = urllib.parse.parse_qs(query)
    for param_key in remove:
        if param_key in params:
            del params[param_key]
    query = urllib.parse.urlencode(params, doseq=True)
    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))

# Define compare_outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Diagnostic runner structure
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            # No type conversion needed here as inputs are JSON-native

            try:
                expected_output = modify_url(inputs["url"], inputs["remove"])
                actual_output = func1(inputs["url"], inputs["remove"])

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output,
                        "actual": actual_output
                    })
            except Exception as e:
                failed_count += 1
                failures.append({
                    "case_id": i+1,
                    "type": "ExecutionError",
                    "inputs": inputs,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })

    except Exception as e:
        execution_error = {
            "type": "CriticalExecutionError",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }

    summary = {
        "passed": passed_count,
        "failed": failed_count,
        "total": len(test_cases),
        "failures": failures[:10],
        "execution_error": execution_error
    }

    print("\n---DIAGNOSTIC_SUMMARY_START---")
    print(json.dumps(summary, indent=2))
    print("---DIAGNOSTIC_SUMMARY_END---")

# Main block
if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    if test_cases:
        run_tests_with_loaded_cases_diagnostic(test_cases)
    else:
        print("No test cases found.")