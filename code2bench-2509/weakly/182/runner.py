import json
import copy
import struct
import numpy as np
from helper import deep_compare, load_test_cases_from_json
from tested import tlv as func1

# Ground truth function (func0), keep its original implementation and name
def tlv(buf):
    n = 4
    t, l_ = struct.unpack('>HH', buf[:n])
    v = buf[n:n + l_]
    pad = (n - l_ % n) % n
    buf = buf[n + l_ + pad:]
    return t, l_, v, buf

# Define compare_outputs function
def compare_outputs(expected, actual):
    if isinstance(expected, tuple) and isinstance(actual, tuple):
        return all(compare_outputs(e, a) for e, a in zip(expected, actual))
    elif isinstance(expected, bytes) and isinstance(actual, bytes):
        return expected == actual
    else:
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
            # Convert list to bytes
            buf = bytes(inputs["buf"])

            try:
                expected_output = tlv(buf)  # Compute dynamically
                actual_output = func1(buf)

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
        print("No test cases loaded.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)