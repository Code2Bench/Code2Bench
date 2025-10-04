import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import _parse_json_fields as func1

from typing import Any, Dict
# Ground truth function (func0), keep its original implementation and name
def _parse_json_fields(field: Any) -> Dict[str, Any]:
    """Parse a JSON field from the database, handling potential errors.

    Args:
        field: The field to parse, can be a string or dict

    Returns:
        Parsed dictionary or error dictionary if parsing fails
    """
    if isinstance(field, dict):
        return field
    if isinstance(field, str):
        try:
            return json.loads(field)
        except Exception as e:
            return {"error": f"Unable to parse {field}: {e}"}
    return {"error": f"Invalid {field} format"}

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
            field = inputs["field"]

            try:
                expected_output = _parse_json_fields(field)
                actual_output = func1(field)

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