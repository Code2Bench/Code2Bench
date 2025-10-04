import json
import copy
from datetime import datetime
from typing import Dict, List
from helper import deep_compare, load_test_cases_from_json
from tested import filter_periods_by_document_end_date as func1

# Ground truth function (func0), keep its original implementation and name
def filter_periods_by_document_end_date(periods: List[Dict], document_period_end_date: str, period_type: str) -> List[Dict]:
    """Filter periods to only include those that end on or before the document period end date."""
    if not document_period_end_date:
        return periods

    try:
        doc_end_date = datetime.strptime(document_period_end_date, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        # If we can't parse the document end date, return all periods
        return periods

    filtered_periods = []
    for period in periods:
        try:
            if period_type == 'instant':
                period_date = datetime.strptime(period['date'], '%Y-%m-%d').date()
                if period_date <= doc_end_date:
                    filtered_periods.append(period)
            else:  # duration
                period_end_date = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
                if period_end_date <= doc_end_date:
                    filtered_periods.append(period)
        except (ValueError, TypeError):
            # If we can't parse the period date, include it to be safe
            filtered_periods.append(period)

    return filtered_periods

# Define compare_outputs function
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
            periods = inputs["periods"]
            document_period_end_date = inputs["document_period_end_date"]
            period_type = inputs["period_type"]

            try:
                expected_output = filter_periods_by_document_end_date(periods, document_period_end_date, period_type)
                actual_output = func1(periods, document_period_end_date, period_type)

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
    try:
        test_cases = load_test_cases_from_json()
        if test_cases:
            run_tests_with_loaded_cases_diagnostic(test_cases)
        else:
            print("No test cases found in the JSON file.")
    except json.JSONDecodeError:
        print("Error: The test cases file contains invalid JSON.")
    except FileNotFoundError:
        print("Error: The test cases file was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")