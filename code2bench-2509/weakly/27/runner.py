import json
import copy
from typing import Dict, Optional
from helper import deep_compare, load_test_cases_from_json
from tested import get_docstring_description_input as func1

# Ground truth function (func0), keep its original implementation and name
def get_docstring_description_input(func) -> Dict[str, Optional[str]]:
    """Extract parameter descriptions from function docstring.

    Parses the function's docstring to extract descriptions for each parameter.
    Looks for lines that start with parameter names followed by descriptions.

    Args:
        func: The function to extract parameter descriptions from.

    Returns:
        Dictionary mapping parameter names to their descriptions.
        Parameters without descriptions are omitted.

    Example:
        For a function with docstring containing "param1: Description of param1",
        returns {"param1": "Description of param1"}.
    """
    doc = func.__doc__
    if not doc:
        return {}
    descriptions = {}
    for line in map(str.strip, doc.splitlines()):
        for param in inspect.signature(func).parameters:
            if param == "self":
                continue
            if line.startswith(param):
                descriptions[param] = line.split(param, 1)[1].strip()
    return descriptions

# Define the comparison function
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
            # No type conversion needed here as the input is a function name

            try:
                # Compute expected output using ground truth function
                expected_output = get_docstring_description_input(inputs["func"])
                # Compute actual output using the tested function
                actual_output = func1(inputs["func"])

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
        print("No test cases loaded.")