import json
import copy
from typing import Dict, Tuple
from helper import deep_compare, load_test_cases_from_json
from tested import validate_channel_info as func1

# Ground truth function (func0), keep its original implementation and name
def validate_channel_info(channel_info: Dict) -> Tuple[bool, str]:
    """Validate channel information before processing."""
    required_fields = ['channel_name', 'channel_niche', 'target_audience', 'key_topics', 'unique_points']

    # Check for missing required fields
    for field in required_fields:
        if not channel_info.get(field):
            return False, f"Missing required field: {field}"

    # Validate field lengths
    if len(channel_info['channel_name']) < 3:
        return False, "Channel name must be at least 3 characters long"

    if len(channel_info['target_audience']) < 10:
        return False, "Target audience description must be at least 10 characters long"

    if len(channel_info['key_topics']) < 10:
        return False, "Key topics must be at least 10 characters long"

    if len(channel_info['unique_points']) < 10:
        return False, "Unique selling points must be at least 10 characters long"

    return True, ""

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

            try:
                expected_output = validate_channel_info(inputs)
                actual_output = func1(inputs)

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