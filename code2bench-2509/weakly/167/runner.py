import json
import copy
import numpy as np
from helper import deep_compare, load_test_cases_from_json
from tested import logmap_so3 as func1

# Ground truth function (func0)
def logmap_so3(R):
    R11 = R[0, 0]
    R12 = R[0, 1]
    R13 = R[0, 2]
    R21 = R[1, 0]
    R22 = R[1, 1]
    R23 = R[1, 2]
    R31 = R[2, 0]
    R32 = R[2, 1]
    R33 = R[2, 2]
    tr = np.trace(R)
    omega = np.empty((3,), dtype=np.float64)

    if(np.abs(tr + 1.0) < 1e-10):
        if(np.abs(R33 + 1.0) > 1e-10):
            omega = (np.pi / np.sqrt(2.0 + 2.0 * R33)) * np.array([R13, R23, 1.0+R33])
        elif(np.abs(R22 + 1.0) > 1e-10):
            omega = (np.pi / np.sqrt(2.0 + 2.0 * R22)) * np.array([R12, 1.0+R22, R32])
        else:
            omega = (np.pi / np.sqrt(2.0 + 2.0 * R11)) * np.array([1.0+R11, R21, R31])
    else:
        magnitude = 1.0
        tr_3 = tr - 3.0
        if tr_3 < -1e-7:
            theta = np.arccos((tr - 1.0) / 2.0)
            magnitude = theta / (2.0 * np.sin(theta))
        else:
            magnitude = 0.5 - tr_3 * tr_3 / 12.0

        omega = magnitude * np.array([R32 - R23, R13 - R31, R21 - R12])

    return omega

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
            R = np.array(inputs["R"], dtype=np.float64)

            try:
                expected_output = logmap_so3(R)
                actual_output = func1(R)

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
    if test_cases:
        run_tests_with_loaded_cases_diagnostic(test_cases)
    else:
        print("No test cases found.")