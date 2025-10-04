import json
import os
import copy
from dateutil import parser
import pytz
from helper import deep_compare
from tested import validate_and_convert_date as func1

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases")
TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

# Ground truth function
def validate_and_convert_date(date_input: str) -> str:
    try:
        dt_object = parser.parse(date_input)
        if dt_object.tzinfo is not None:
            dt_object = dt_object.astimezone(pytz.utc)
        else:
            local_tz = pytz.timezone("UTC")
            dt_object = local_tz.localize(dt_object)
        formatted_date = dt_object.isoformat().replace("+00:00", "Z")
        formatted_date = formatted_date.rstrip("Z") + "Z"
        return formatted_date
    except (ValueError, OverflowError) as e:
        raise ValueError(
            f"Invalid date format: {date_input}."
            f" Date format must adhere to the RFC 3339 standard (e.g., 'YYYY-MM-DDTHH:MM:SSZ' for UTC)."
        ) from e

def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)
    return test_cases

def compare_outputs(expected, actual):
    # Use deep_compare for basic types (str in this case)
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
            date_input = inputs["date_input"]

            try:
                expected_output = validate_and_convert_date(date_input)
                actual_output = func1(date_input)

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
        print("No test cases loaded.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)