import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import format_diff_message as func1

# Ground truth function (func0), keep its original implementation and name
def format_diff_message(optim_text: str, incr_text: str) -> str:
    """Creates a detailed diff message between two texts."""
    diff: list[str] = list(difflib.ndiff(optim_text.splitlines(), incr_text.splitlines()))

    # Collect differences
    only_in_optim: list[str] = []
    only_in_incr: list[str] = []

    for line in diff:
        if line.startswith("- "):
            only_in_optim.append(line[2:])
        elif line.startswith("+ "):
            only_in_incr.append(line[2:])

    message: list[str] = []
    if only_in_optim:
        message.append("\nOnly in optimized prompt:")
        message.extend(f"  {line}" for line in only_in_optim)

    if only_in_incr:
        message.append("\nOnly in incremental prompt:")
        message.extend(f"  {line}" for line in only_in_incr)

    return "\n".join(message)

# Compare outputs function
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
            optim_text = inputs["optim_text"]
            incr_text = inputs["incr_text"]

            try:
                expected_output = format_diff_message(optim_text, incr_text)
                actual_output = func1(optim_text, incr_text)

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