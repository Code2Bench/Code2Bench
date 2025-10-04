import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import _timeseries_stats as func1
import statistics

# Ground truth function (func0), keep its original implementation and name
def _timeseries_stats(ts):
    """Calculate and format summary statistics for a time series.

    Args:
        ts (list): List of numeric values representing a time series

    Returns:
        str: Markdown formatted string containing summary statistics
    """
    if len(ts) == 0:
        return "No data points"

    count = len(ts)
    max_val = max(ts)
    min_val = min(ts)
    mean_val = sum(ts) / count if count > 0 else float("nan")
    median_val = statistics.median(ts)

    markdown_summary = f"""
Time Series Statistics
- Number of Data Points: {count}
- Maximum Value: {max_val}
- Minimum Value: {min_val}
- Mean Value: {mean_val:.2f}
- Median Value: {median_val}
"""
    return markdown_summary

# Define the ground truth function
ground_truth = _timeseries_stats

# Define the compare_outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Define the diagnostic runner function
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            ts = inputs["ts"]

            try:
                expected_output = ground_truth(ts)
                actual_output = func1(ts)

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
        print("No test cases loaded.")