import json
import copy
import numpy as np
import math
from helper import deep_compare, load_test_cases_from_json
from tested import S_inv_eulerZYX_body_deriv as func1

# Ground truth function (func0), keep its original implementation and name
def S_inv_eulerZYX_body_deriv(euler_coordinates, omega):
    y = euler_coordinates[1]
    z = euler_coordinates[2]

    J_y = np.zeros((3, 3))
    J_z = np.zeros((3, 3))

    J_y[0, 1] = math.tan(y)/math.cos(y)*math.sin(z)
    J_y[0, 2] = math.tan(y)/math.cos(y)*math.cos(z)
    J_y[2, 1] = math.sin(z)/(math.cos(y))**2
    J_y[2, 2] = math.cos(z)/(math.cos(y))**2

    J_z[0, 1] = math.cos(z)/math.cos(y)
    J_z[0, 2] = -math.sin(z)/math.cos(y)
    J_z[1, 1] = -math.sin(z)
    J_z[1, 2] = -math.cos(z)
    J_z[2, 1] = math.cos(z)*math.tan(y)
    J_z[2, 2] = -math.sin(z)*math.tan(y)

    J = np.zeros((3, 3))
    J[:, 1] = np.dot(J_y, omega)
    J[:, 2] = np.dot(J_z, omega)

    return J

# Compare outputs
def compare_outputs(expected, actual):
    return np.allclose(expected, actual, atol=1e-6)

# Diagnostic runner
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            # Type conversion for inputs
            euler_coordinates = np.array(inputs["euler_coordinates"], dtype=np.float64)
            omega = np.array(inputs["omega"], dtype=np.float64)

            try:
                expected_output = S_inv_eulerZYX_body_deriv(euler_coordinates, omega)
                actual_output = func1(euler_coordinates, omega)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output.tolist(),
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
        print("No test cases found.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)