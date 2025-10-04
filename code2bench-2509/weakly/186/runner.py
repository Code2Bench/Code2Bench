import json
import os
import copy
import numpy as np
from helper import deep_compare
from tested import post_process_sampled_indices as func1

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases")
TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

# Ground truth function
def post_process_sampled_indices(*, sampled_inds_list, attn_map, image_size):
    inds = np.array(sampled_inds_list).flatten()
    inds = np.array(np.unravel_index(inds, attn_map.shape)).T

    inds_normalised = np.zeros(inds.shape)
    inds_normalised[:, 0] = inds[:, 1] / image_size
    inds_normalised[:, 1] = inds[:, 0] / image_size
    inds_normalised = inds_normalised.tolist()

    return inds, inds_normalised

def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)
    return test_cases

def compare_outputs(expected, actual):
    # Handle third-party library types (e.g., NumPy arrays)
    if isinstance(expected, tuple) and isinstance(actual, tuple):
        if len(expected) != len(actual):
            return False
        return all(compare_outputs(exp, act) for exp, act in zip(expected, actual))
    elif isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
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
            sampled_inds_list = inputs["sampled_inds_list"]
            attn_map = np.array(inputs["attn_map"], dtype=np.float32)
            image_size = inputs["image_size"]

            try:
                expected_output = post_process_sampled_indices(
                    sampled_inds_list=sampled_inds_list,
                    attn_map=attn_map,
                    image_size=image_size
                )
                actual_output = func1(
                    sampled_inds_list=sampled_inds_list,
                    attn_map=attn_map,
                    image_size=image_size
                )

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": [arr.tolist() if isinstance(arr, np.ndarray) else arr for arr in expected_output],
                        "actual": [arr.tolist() if isinstance(arr, np.ndarray) else arr for arr in actual_output]
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