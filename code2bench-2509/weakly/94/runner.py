import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import decode_url_params as func1

# Ground truth function (func0), keep its original implementation and name
def decode_url_params(encoded_map, apply_on_keys=None):
    """Code taken from comments in vizro-core/src/vizro/static/js/models/page.js file."""
    decoded_map = {}
    for key, val in encoded_map.items():
        if val.startswith("b64_") and key in apply_on_keys:
            try:
                # This manual base64 decoding could be simplified with base64.urlsafe_b64decode.
                # It's kept here to match the javascript implementation.
                base64_str = val[4:].replace("-", "+").replace("_", "/")
                base64_str += "=" * ((4 - len(base64_str) % 4) % 4)
                binary_data = base64.b64decode(base64_str)
                json_str = binary_data.decode("utf-8")
                decoded_map[key] = json.loads(json_str)
            except Exception as e:
                print(f"Failed to decode URL parameter: {key}, {val} - {e}")  # noqa
    return decoded_map

# Compare outputs
def compare_outputs(expected, actual):
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
            encoded_map = inputs["encoded_map"]
            apply_on_keys = inputs["apply_on_keys"]

            try:
                expected_output = decode_url_params(encoded_map, apply_on_keys)
                actual_output = func1(encoded_map, apply_on_keys)

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
            except json.JSONDecodeError as e:
                failed_count += 1
                failures.append({
                    "case_id": i+1,
                    "type": "ExecutionError",
                    "inputs": inputs,
                    "error_type": "JSONDecodeError",
                    "error_message": str(e)
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