import json
import copy
import base64
from helper import deep_compare, load_test_cases_from_json
from tested import _deserialize_bytes_base64 as func1

# Ground truth function (func0), keep its original implementation and name
def _deserialize_bytes_base64(attr):
    if isinstance(attr, (bytes, bytearray)):
        return attr
    padding = "=" * (3 - (len(attr) + 3) % 4)  # type: ignore
    attr = attr + padding  # type: ignore
    encoded = attr.replace("-", "+").replace("_", "/")
    return bytes(base64.b64decode(encoded))

# Define the comparison function
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
            attr = inputs["attr"]
            # Convert list back to bytes if necessary
            if isinstance(attr, list):
                attr = bytes(attr)

            try:
                expected_output = _deserialize_bytes_base64(attr)
                actual_output = func1(attr)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": list(expected_output) if isinstance(expected_output, bytes) else expected_output,
                        "actual": list(actual_output) if isinstance(actual_output, bytes) else actual_output
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