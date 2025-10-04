import json
import copy
import numpy as np
from scipy.spatial.transform import Rotation as R
from helper import deep_compare, load_test_cases_from_json
from tested import align_vector_sets as func1

# Ground truth function (func0), keep its original implementation and name
def align_vector_sets(vec_set1, vec_set2):
    """
    Computes a single quaternion representing the rotation that best aligns vec_set1 to vec_set2.

    Args:
        vec_set1 (np.array): (N, 3) tensor of N 3D vectors
        vec_set2 (np.array): (N, 3) tensor of N 3D vectors

    Returns:
        np.array: (4,) Normalized quaternion representing the overall rotation
    """
    rot, _ = R.align_vectors(vec_set1, vec_set2)
    return rot.as_quat()

# Define compare_outputs function
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
            # Convert JSON lists to numpy arrays
            vec_set1 = np.array(inputs["vec_set1"], dtype=np.float64)
            vec_set2 = np.array(inputs["vec_set2"], dtype=np.float64)

            try:
                expected_output = align_vector_sets(vec_set1, vec_set2)
                actual_output = func1(vec_set1, vec_set2)

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
        print("No test cases loaded.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)