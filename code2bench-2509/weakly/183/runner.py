import json
import os
import copy
import numpy as np
from helper import deep_compare
from tested import _first_divided_difference as func1

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases")
TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

# Ground truth function
def _first_divided_difference(d, fct, fctder, atol=1e-12, rtol=1e-12):
    dif = np.repeat(d[None, :], len(d), axis=0)
    close_ = np.isclose(dif, dif.T, atol=atol, rtol=rtol)
    dif[close_] = fctder(dif[close_])
    dif[~close_] = (fct(dif[~close_]) - fct(dif.T[~close_])) / \
                   (dif[~close_] - dif.T[~close_])
    return dif

# Function to map function names to actual functions
def get_function_from_name(name):
    if name == "sin":
        return np.sin
    elif name == "cos":
        return np.cos
    elif name == "exp":
        return np.exp
    elif name == "lambda":
        return lambda x: -np.sin(x)
    else:
        return lambda x: 1.0

def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)
    return test_cases

def compare_outputs(expected, actual):
    # Handle third-party library types (e.g., NumPy arrays)
    if isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
        return np.allclose(expected, actual, rtol=1e-05, atol=1e-08)
    # Handle basic types and combinations (int, float, str, list, dict, etc.)
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
            # Type conversion here if needed (e.g., list → np.array)
            d = np.array(inputs["d"], dtype=np.float64)
            fct = get_function_from_name(inputs["fct"])
            fctder = get_function_from_name(inputs["fctder"])
            atol = inputs["atol"]
            rtol = inputs["rtol"]

            try:
                expected_output = _first_divided_difference(d, fct, fctder, atol, rtol)
                actual_output = func1(d, fct, fctder, atol, rtol)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output.tolist(),  # serialize if it can be serialized
                        "actual": actual_output.tolist()
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