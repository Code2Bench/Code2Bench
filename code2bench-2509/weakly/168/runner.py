import json
import copy
import numpy as np
from helper import deep_compare, load_test_cases_from_json
from tested import S_inv_eulerZYX_body as func1

# Ground truth function (func0), keep its original implementation and name
def S_inv_eulerZYX_body(euler_coordinates):
    y = euler_coordinates[1]
    z = euler_coordinates[2]
    E = np.zeros((3, 3))
    E[0, 1] = np.sin(z)/np.cos(y)
    E[0, 2] = np.cos(z)/np.cos(y)
    E[1, 1] = np.cos(z)
    E[1, 2] = -np.sin(z)
    E[2, 0] = 1.0
    E[2, 1] = np.sin(z)*np.sin(y)/np.cos(y)
    E[2, 2] = np.cos(z)*np.sin(y)/np.cos(y)
    return E

# Define compare_outputs function
def compare_outputs(expected, actual):
    return np.allclose(expected, actual, rtol=1e-6, atol=1e-6)

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
            euler_coordinates = np.array(inputs["euler_coordinates"], dtype=np.float64)

            try:
                expected_output = S_inv_eulerZYX_body(euler_coordinates)
                actual_output = func1(euler_coordinates)

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