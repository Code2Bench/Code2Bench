import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import human_date as func1
from datetime import datetime

# Ground truth function (func0), keep its original implementation and name
def human_date(date_value) -> str:
    """Format a date/datetime to be more human-readable.

    Converts datetime objects or ISO strings to a format like:
    "Jan 15, 2024 at 2:30 PM"
    """
    if not date_value:
        return "—"

    # Handle string datetime values (ISO format)
    if isinstance(date_value, str):
        try:
            # Parse common ISO formats
            for fmt in [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
            ]:
                try:
                    date_value = datetime.strptime(date_value, fmt)
                    break
                except ValueError:
                    continue
            else:
                # If we can't parse it, just return the original truncated string
                return date_value[:16] if len(date_value) > 16 else date_value
        except (ValueError, AttributeError):
            return date_value[:16] if len(date_value) > 16 else date_value

    # Handle datetime objects
    if hasattr(date_value, "strftime"):
        return date_value.strftime("%b %-d, %Y at %-I:%M %p")

    # Fallback for unknown types
    return str(date_value)[:16]

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
            date_value = inputs["date_value"]

            try:
                expected_output = human_date(date_value)
                actual_output = func1(date_value)

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