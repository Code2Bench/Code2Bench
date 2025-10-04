import json
import copy
from typing import Dict
from helper import deep_compare, load_test_cases_from_json
from tested import _deep_merge_dicts as func1

# Ground truth function (func0), keep its original implementation and name
def _deep_merge_dicts(source: Dict, destination: Dict) -> Dict:
    """
    Recursively merges the 'source' dictionary into the 'destination' dictionary.
    Keys from 'source' will overwrite existing keys in 'destination'.
    If a key in 'source' corresponds to a dictionary, a recursive merge is performed.
    The 'destination' dictionary is modified in place.
    """
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            if isinstance(
                node, dict
            ):  # Ensure the destination node is a dict for merging
                _deep_merge_dicts(value, node)
            else:  # If destination's node is not a dict, overwrite it entirely
                destination[key] = copy.deepcopy(value)
        else:
            destination[key] = value
    return destination

# Define compare_outputs function
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
            source = inputs["source"]
            destination = inputs["destination"]

            try:
                expected_output = _deep_merge_dicts(source, destination)
                actual_output = func1(source, destination)

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