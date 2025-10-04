import json
import copy
from typing import Tuple
from helper import deep_compare, load_test_cases_from_json
from tested import _parse_tool_call as func1
import re

# Ground truth function (func0), keep its original implementation and name
def _parse_tool_call(action: str) -> Tuple[str, bool]:
    try:
        # Extract tool call content
        tool_match = re.search(r'<tool_call>(.*?)</tool_call>', action, re.DOTALL)
        if not tool_match:
            return action, False

        tool_content = tool_match.group(1).strip()

        # Parse tool name and parameters
        tool_name = None
        params = {}

        lines = tool_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.lower().startswith('tool:'):
                tool_name = line.split(':', 1)[1].strip()
            elif line.lower().startswith('parameters:'):
                try:
                    params_str = line.split(':', 1)[1].strip()
                    # Try to parse as JSON
                    params = json.loads(params_str)
                except (json.JSONDecodeError, IndexError):
                    # Fallback to treating the whole thing as a query
                    params = {'query': params_str}
            elif ':' in line and not tool_name:
                # Handle simple key:value format
                key, value = line.split(':', 1)
                params[key.strip()] = value.strip()

        if not tool_name:
            return action, False

        # Format as structured action
        formatted_action = json.dumps({
            'type': 'tool_call',
            'tool': tool_name,
            'parameters': params,
            'original': action
        })

        return formatted_action, True

    except Exception:
        return action, False

# Compare outputs
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
            action = inputs["action"]

            try:
                expected_output, expected_valid = _parse_tool_call(action)
                actual_output, actual_valid = func1(action)

                if compare_outputs((expected_output, expected_valid), (actual_output, actual_valid)):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": (expected_output, expected_valid),
                        "actual": (actual_output, actual_valid)
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