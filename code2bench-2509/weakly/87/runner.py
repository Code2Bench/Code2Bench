import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import metadata_url_for_resource as func1
from urllib.parse import urlunsplit, urlsplit

# Ground truth function (func0), keep its original implementation and name
def metadata_url_for_resource(resource_url: str) -> str:
    """
    RFC 9728: insert '/.well-known/oauth-protected-resource' between host and path.
    If the resource has a path (e.g., '/mcp'), append it after the well-known suffix.
    """
    u = urlsplit(resource_url)
    path = u.path.lstrip("/")
    suffix = "/.well-known/oauth-protected-resource"
    if path:
        suffix += f"/{path}"
    return urlunsplit((u.scheme, u.netloc, suffix, "", ""))

# Define compare_outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Define diagnostic runner
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            resource_url = inputs["resource_url"]

            try:
                expected_output = metadata_url_for_resource(resource_url)
                actual_output = func1(resource_url)

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
    if not test_cases:
        print("No test cases loaded.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)