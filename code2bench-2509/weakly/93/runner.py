import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import encode_url_params as func1
import base64

# Ground truth function (func0), keep its original implementation and name
def encode_url_params(decoded_map, apply_on_keys=None):
    """Code taken from comments in vizro-core/src/vizro/static/js/models/page.js file."""
    encoded_map = {}
    for key, value in decoded_map.items():
        if key in apply_on_keys:
            # This manual base64 encoding could be simplified with base64.urlsafe_b64encode.
            # It's kept here to match the javascript implementation.
            json_str = json.dumps(value, separators=(",", ":"))
            encoded_bytes = base64.b64encode(json_str.encode("utf-8"))
            encoded_str = encoded_bytes.decode("utf-8").replace("+", "-").replace("/", "_").rstrip("=")
            encoded_map[key] = "b64_" + encoded_str
    return encoded_map

# Define compare_outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Define diagnostic runner
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            decoded_map = inputs["decoded_map"]
            apply_on_keys = inputs["apply_on_keys"]

            try:
                expected_output = encode_url_params(decoded_map, apply_on_keys)
                actual_output = func1(decoded_map, apply_on_keys)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output,
                        "actual": actual_output
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