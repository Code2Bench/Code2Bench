import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import parse_specific_attributes as func1
import urllib.parse

# Ground truth function (func0), keep its original implementation and name
def parse_specific_attributes(specific_attributes):
    assert isinstance(specific_attributes, str), "Specific attributes must be a string"
    parsed_specific_attributes = urllib.parse.parse_qsl(specific_attributes)
    return (
        {key: value for (key, value) in parsed_specific_attributes}
        if parsed_specific_attributes
        else dict()
    )

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
            specific_attributes = inputs["specific_attributes"]

            try:
                expected_output = parse_specific_attributes(specific_attributes)
                actual_output = func1(specific_attributes)

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