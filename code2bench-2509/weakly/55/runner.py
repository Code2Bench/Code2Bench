import json
import copy
from typing import Dict, Tuple
from helper import deep_compare, load_test_cases_from_json
from tested import validate_script as func1

# Ground truth function (func0), keep its original implementation and name
def validate_script(script: Dict) -> Tuple[bool, str]:
    """Validate the generated script."""
    required_sections = ['hook', 'introduction', 'showcase', 'value_proposition', 'call_to_action']

    # Check for missing sections
    for section in required_sections:
        if section not in script:
            return False, f"Missing required section: {section}"

    # Validate section content
    for section, content in script.items():
        if not content.get('text'):
            return False, f"Missing text in section: {section}"
        if not content.get('duration'):
            return False, f"Missing duration in section: {section}"

    # Validate total duration
    total_duration = sum(float(content['duration'].split()[0]) for content in script.values())
    if total_duration > 90:  # 90 seconds max
        return False, f"Total duration ({total_duration}s) exceeds maximum allowed (90s)"

    return True, ""

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

            try:
                expected_output = validate_script(inputs["script"])  # Compute dynamically
                actual_output = func1(inputs["script"])

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