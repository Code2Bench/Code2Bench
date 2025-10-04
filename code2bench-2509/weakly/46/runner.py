import json
import copy
from datetime import date
from helper import deep_compare, load_test_cases_from_json
from tested import gregorian_date as func1

# Ground truth function (func0), keep its original implementation and name
def gregorian_date(jdn):
    f = jdn + 1401 + (4 * jdn + 274277) // 146097 * 3 // 4 - 38
    e = 4 * f + 3
    h = e % 1461 // 4
    h = 5 * h + 2
    d = (h % 153) // 5 + 1
    m = (h // 153 + 2) % 12 + 1
    y = e // 1461 - 4716 + (14 - m) // 12
    return date(y, m, d)

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
            jdn = inputs["jdn"]

            try:
                expected_output = gregorian_date(jdn)  # Compute dynamically
                actual_output = func1(jdn)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output.isoformat(),  # serialize date
                        "actual": actual_output.isoformat()
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