import json
import copy
import numpy as np
from helper import deep_compare, load_test_cases_from_json
from tested import k_mat as func1

# Ground truth function (func0), keep its original implementation and name
def k_mat(two_body_integrals):
    """
    Args:
        two_body_integrals: Numpy array of two-electron integrals with
            OpenFermion Ordering.

    Returns:
        k_matr : Numpy array of the exchange integrals K_{p,q} = (pq|qp)
            (in chemist notation).
    """
    chem_ordering = np.copy(two_body_integrals.transpose(0, 3, 1, 2), order='C')
    return np.einsum('ijji -> ij', chem_ordering)

# Define compare_outputs function
def compare_outputs(expected, actual):
    if isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
        return np.allclose(expected, actual, atol=1e-6)
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
            # Convert JSON list to numpy array
            two_body_integrals = np.array(inputs["two_body_integrals"], dtype=np.float64)

            try:
                expected_output = k_mat(two_body_integrals)  # Compute dynamically
                actual_output = func1(two_body_integrals)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output.tolist(),  # serialize numpy array
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
        print("No test cases loaded.")