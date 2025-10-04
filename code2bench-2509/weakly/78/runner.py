import json
import copy
from typing import Optional
from helper import deep_compare, load_test_cases_from_json
from tested import decode_base_n as func1
import string

# Ground truth function (func0), keep its original implementation and name
def decode_base_n(encoded: str, n: int, table: Optional[str] = None) -> int:
    if table is None:
        table = string.digits + string.ascii_lowercase

    if not 2 <= n <= len(table):
        raise ValueError(f"Base must be between 2 and {len(table)}")

    if not encoded:
        return 0

    is_negative = encoded.startswith("-")
    if is_negative:
        encoded = encoded[1:]

    result = 0
    for i, char in enumerate(reversed(encoded.lower())):
        if char not in table:
            raise ValueError(f"Invalid character '{char}' for base {n}")

        digit_value = table.index(char)
        if digit_value >= n:
            raise ValueError(f"Invalid digit '{char}' for base {n}")

        result += digit_value * (n**i)

    return -result if is_negative else result

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
            encoded = inputs["encoded"]
            n = inputs["n"]
            table = inputs["table"]

            try:
                expected_output = decode_base_n(encoded, n, table)
                actual_output = func1(encoded, n, table)

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