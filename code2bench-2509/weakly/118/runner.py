import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import smart_parse as func1
import re

# Ground truth function (func0), keep its original implementation and name
def smart_parse(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        json_match = re.search(r'{.*}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        pattern = re.findall(
            r'(\w+)=["\']([^"\']+)["\']|'  # key="value"
            r'(\w+)=([\w.]+)|'  # key=value
            r'(\w+):\s*["\']([^"\']+)["\']|'  # Key: "value"
            r'(\w+):\s*([\w.]+)',  # key: value
            text)

        if pattern:
            parsed_data = {}
            remaining_str = text

            for match in pattern:
                key = next(m for m in [match[0], match[2], match[4], match[6]] if m)
                value = next(m for m in [match[1], match[3], match[5], match[7]] if m)
                parsed_data[key.lower()] = value
                for possible_format in [f'{key}={value}', f'{key}: {value}', f'{key}="{value}"', f'{key}: "{value}"']:
                    remaining_str = remaining_str.replace(possible_format, '')

            remaining_str = remaining_str.strip().strip(',').strip()
            if remaining_str:
                parsed_data['message'] = remaining_str

            return parsed_data

        return {'message': text}

# Compare outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Diagnostic runner function
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            text = inputs["text"]

            try:
                expected_output = smart_parse(text)
                actual_output = func1(text)

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