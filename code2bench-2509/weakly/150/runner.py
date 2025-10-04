import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import find_github_issues as func1
import re
from urllib.parse import urlparse

# Ground truth function (func0), keep its original implementation and name
def find_github_issues(message: str):
    # Look for urls first
    urls = [urlparse(e) for e in re.findall(r"https?://[^\s^\)]+", message)]

    issue_urls = [e for e in urls if e.hostname == 'github.com' and e.path.lower().startswith('/microsoft/wsl/issues/')]

    issues = set(['#' + e.path.split('/')[-1] for e in issue_urls])

    # Then add issue numbers
    for e in re.findall(r"#\d+", message):
        issues.add(e)

    return issues

# Compare outputs
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Diagnostic runner
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            message = inputs["message"]

            try:
                expected_output = find_github_issues(message)
                actual_output = func1(message)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": list(expected_output),  # serialize set to list
                        "actual": list(actual_output)  # serialize set to list
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
    if not test_cases:
        print("No test cases loaded. Exiting.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)