import json
import copy
import numpy as np
from scipy import sparse
from helper import deep_compare, load_test_cases_from_json
from tested import _build_dispersed_image_of_source as func1

# Ground truth function (func0), keep its original implementation and name
def _build_dispersed_image_of_source(x, y, flux):
    minx = int(min(x))
    maxx = int(max(x))
    miny = int(min(y))
    maxy = int(max(y))
    a = sparse.coo_matrix(
        (flux, (y - miny, x - minx)), shape=(maxy - miny + 1, maxx - minx + 1)
    ).toarray()
    bounds = [minx, maxx, miny, maxy]
    return a, bounds

# Compare outputs
def compare_outputs(expected, actual):
    if isinstance(expected, tuple) and isinstance(actual, tuple):
        if len(expected) != len(actual):
            return False
        return all(compare_outputs(e, a) for e, a in zip(expected, actual))
    elif isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
        return np.allclose(expected, actual, atol=1e-6)
    else:
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
            # Convert inputs to numpy arrays
            x = np.array(inputs["x"], dtype=np.int32)
            y = np.array(inputs["y"], dtype=np.int32)
            flux = np.array(inputs["flux"], dtype=np.float32)

            try:
                expected_output = _build_dispersed_image_of_source(x, y, flux)
                actual_output = func1(x, y, flux)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": [expected_output[0].tolist(), expected_output[1]],
                        "actual": [actual_output[0].tolist(), actual_output[1]]
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