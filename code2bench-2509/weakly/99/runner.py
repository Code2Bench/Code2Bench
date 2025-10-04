import json
import copy
from datetime import datetime
from dateutil.relativedelta import relativedelta
from helper import deep_compare, load_test_cases_from_json
from tested import get_first_last_day as func1

# Ground truth function (func0), keep its original implementation and name
def get_first_last_day(year_month_str):
    try:
        date_obj = datetime.strptime(year_month_str, "%Y-%m")
        first_day = date_obj.date().replace(day=1)
        last_day = (date_obj + relativedelta(months=1, days=-1)).date()
        return first_day, last_day
    except ValueError:
        raise ValueError("Invalid date format. Please use '%Y-%m'.")

# Define compare_outputs function
def compare_outputs(expected, actual):
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
            year_month_str = inputs["year_month_str"]

            try:
                expected_output = get_first_last_day(year_month_str)
                actual_output = func1(year_month_str)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": [expected_output[0].isoformat(), expected_output[1].isoformat()],
                        "actual": [actual_output[0].isoformat(), actual_output[1].isoformat()]
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