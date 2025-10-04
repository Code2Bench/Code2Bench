import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import iso8601_to_epoch_ms as func1
from datetime import datetime

# Ground truth function (func0), keep its original implementation and name
def iso8601_to_epoch_ms(iso8601_string: str) -> int:
    """
    Convert ISO 8601 string to epoch milliseconds (matches Java iso8601StringToEpochLong).

    Args:
        iso8601_string: ISO 8601 formatted datetime string

    Returns:
        Time as epoch milliseconds
    """
    dt = datetime.fromisoformat(iso8601_string.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)

# Compare outputs function
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
            iso8601_string = inputs["iso8601_string"]

            try:
                expected_output = iso8601_to_epoch_ms(iso8601_string)
                actual_output = func1(iso8601_string)

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
        print("No test cases loaded. Exiting.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)