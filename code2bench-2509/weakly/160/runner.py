import json
import copy
import numpy as np
import math
from helper import deep_compare, load_test_cases_from_json
from tested import orthogonalization_matrix as func1

# Ground truth function (func0), keep its original implementation and name
def orthogonalization_matrix(lengths, angles):
    """Return orthogonalization matrix for crystallographic cell coordinates.

    Angles are expected in degrees.

    The de-orthogonalization matrix is the inverse.

    >>> O = orthogonalization_matrix([10, 10, 10], [90, 90, 90])
    >>> numpy.allclose(O[:3, :3], numpy.identity(3, float) * 10)
    True
    >>> O = orthogonalization_matrix([9.8, 12.0, 15.5], [87.2, 80.7, 69.7])
    >>> numpy.allclose(numpy.sum(O), 43.063229)
    True

    """
    a, b, c = lengths
    angles = np.radians(angles)
    sina, sinb, _ = np.sin(angles)
    cosa, cosb, cosg = np.cos(angles)
    co = (cosa * cosb - cosg) / (sina * sinb)
    return np.array([[a * sinb * math.sqrt(1.0 - co * co), 0.0, 0.0, 0.0], [-a * sinb * co, b * sina, 0.0, 0.0],
                        [a * cosb, b * cosa, c, 0.0], [0.0, 0.0, 0.0, 1.0]])

# Compare outputs
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
            lengths = np.array(inputs["lengths"], dtype=np.float64)
            angles = np.array(inputs["angles"], dtype=np.float64)

            try:
                expected_output = orthogonalization_matrix(lengths, angles)
                actual_output = func1(lengths, angles)

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