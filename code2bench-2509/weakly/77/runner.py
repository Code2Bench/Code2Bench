import json
import copy
from typing import Optional
from helper import deep_compare, load_test_cases_from_json
from tested import encode_base_n as func1
import string

# Ground truth function (func0), keep its original implementation and name
def encode_base_n(num: int, n: int, table: Optional[str] = None) -> str:
    """
    Encode a number in base-n representation.

    Args:
        num: The number to encode
        n: The base to use for encoding
        table: Custom character table (optional)

    Returns:
        String representation of the number in base-n

    Examples:
        >>> encode_base_n(255, 16)
        'ff'
        >>> encode_base_n(42, 36)
        '16'
    """
    if table is None:
        # Default table: 0-9, a-z
        table = string.digits + string.ascii_lowercase

    if not 2 <= n <= len(table):
        raise ValueError(f"Base must be between 2 and {len(table)}")

    if num == 0:
        return table[0]

    result = []
    is_negative = num < 0
    num = abs(num)

    while num > 0:
        result.append(table[num % n])
        num //= n

    if is_negative:
        result.append("-")

    return "".join(reversed(result))

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
            # No type conversion needed here as inputs are JSON-native

            try:
                expected_output = encode_base_n(inputs["num"], inputs["n"], inputs["table"])
                actual_output = func1(inputs["num"], inputs["n"], inputs["table"])

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
    if not test_cases:
        print("No test cases found.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)