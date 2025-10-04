import json
import copy
from typing import Dict, Optional, Tuple
from helper import deep_compare, load_test_cases_from_json
from tested import get_contest_data_from_cache as func1

# Ground truth function (func0), keep its original implementation and name
def get_contest_data_from_cache(contest_id: int, cached_data: Dict) -> Tuple[Optional[Dict], Optional[Dict]]:
    contest_id_str = str(contest_id)

    if contest_id_str not in cached_data:
        print(f"Warning: Contest {contest_id} data not found in cache")
        return None, None

    contest_data = cached_data[contest_id_str]

    try:
        standings = contest_data["standings"]
        rating_changes = contest_data["rating_changes"]

        if standings.get("status") != "OK" or rating_changes.get("status") != "OK":
            print(f"Warning: Contest {contest_id} cached data status abnormal")
            return None, None

        return standings, rating_changes

    except KeyError as e:
        print(f"Warning: Contest {contest_id} cached data structure abnormal: {e}")
        return None, None

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
            contest_id = inputs["contest_id"]
            cached_data = inputs["cached_data"]

            try:
                expected_output = get_contest_data_from_cache(contest_id, cached_data)
                actual_output = func1(contest_id, cached_data)

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
        print("No test cases found.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)