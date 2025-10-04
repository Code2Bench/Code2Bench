import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import parse_tool_result as func1

# Ground truth function (func0), keep its original implementation and name
def parse_tool_result(result):
    """Parse the tool result from agent.tool calls that may return serialized data."""
    if result.get('status') != 'success':
        return result

    try:
        text = result['content'][0]['text']
        # Try JSON parsing first
        try:
            actual_result = json.loads(text)
            return actual_result
        except json.JSONDecodeError:
            # Try evaluating as Python literal (safe eval for dict/list/etc)
            actual_result = ast.literal_eval(text)
            return actual_result
    except (KeyError, IndexError, ValueError, SyntaxError):
        return result

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
                expected_output = parse_tool_result(inputs["result"])  # Compute dynamically
                actual_output = func1(inputs["result"])

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output,  # serialize if it can be serialized
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