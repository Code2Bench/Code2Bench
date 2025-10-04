import json
import copy
from typing import Dict
from helper import deep_compare, load_test_cases_from_json
from tested import calculate_aggregated_metrics as func1
from collections import Counter

# Ground truth function (func0), keep its original implementation and name
def calculate_aggregated_metrics(metrics_data: Dict[str, list]) -> Dict[str, Dict]:
    """Calculate aggregated scores for metrics (numeric average or categorical frequency)."""
    agg_metrics = {}
    for metric_name, scores in metrics_data.items():
        # Remove None values
        scores = [score for score in scores if score is not None]
        if not scores:
            avg_score = 0
        elif isinstance(scores[0], (int, float)):
            # Numeric metric - calculate average
            avg_score = sum(scores) / len(scores)
        else:
            # Categorical metric - create frequency distribution
            avg_score = dict(Counter(scores))
        agg_metrics[metric_name] = {"score": avg_score}
    return agg_metrics

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
            metrics_data = inputs["metrics_data"]

            try:
                expected_output = calculate_aggregated_metrics(metrics_data)
                actual_output = func1(metrics_data)

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