import json
import copy
from typing import List, Dict, Any
from datetime import datetime
from helper import deep_compare, load_test_cases_from_json
from tested import generate_test_report as func1

# Ground truth function (func0), keep its original implementation and name
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
            test_results = inputs["test_results"]

            try:
                expected_output = generate_test_report(test_results)
                actual_output = func1(test_results)

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