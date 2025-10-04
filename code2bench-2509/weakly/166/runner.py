import json
import copy
import numpy as np
from helper import deep_compare, load_test_cases_from_json
from tested import first_order_rotation as func1

# Ground truth function (func0), keep its original implementation and name
def first_order_rotation(rotvec):
    R = np.zeros((3, 3), dtype=np.float64)
    R[0, 0] = 1.0
    R[1, 0] = rotvec[2]
    R[2, 0] = -rotvec[1]
    R[0, 1] = -rotvec[2]
    R[1, 1] = 1.0
    R[2, 1] = rotvec[0]
    R[0, 2] = rotvec[1]
    R[1, 2] = -rotvec[0]
    R[2, 2] = 1.0
    return R

# Compare outputs for NumPy arrays
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
            # Convert JSON list to NumPy array
            rotvec = np.array(inputs["rotvec"], dtype=np.float64)

            try:
                expected_output = first_order_rotation(rotvec)
                actual_output = func1(rotvec)

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
        print("No test cases loaded. Exiting.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)