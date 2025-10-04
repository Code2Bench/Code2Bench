import json
import copy
import os
from collections import defaultdict
from helper import deep_compare, load_test_cases_from_json
from tested import get_changed_lines_from_file as func1

# Ground truth function (copied from input)
def get_changed_lines_from_file(diff_txt_path):
    """Parse diff.txt to get changed lines per file"""
    file_changes = defaultdict(set)
    current_file = None

    with open(diff_txt_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("+++ b/"):
                current_file = line[6:].strip()
            elif line.startswith("@@"):
                match = re.search(r"\+(\d+)(?:,(\d+))?", line)
                if match and current_file:
                    start_line = int(match.group(1))
                    line_count = int(match.group(2) or "1")
                    for i in range(start_line, start_line + line_count):
                        file_changes[current_file].add(i)
    return file_changes

# Define the ground truth function
ground_truth = get_changed_lines_from_file

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
            diff_txt_path = inputs["diff_txt_path"]

            try:
                expected_output = ground_truth(diff_txt_path)
                actual_output = func1(diff_txt_path)

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
        print("No test cases loaded. Exiting.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)