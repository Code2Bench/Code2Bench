import json
import copy
import base64
from helper import deep_compare, load_test_cases_from_json
from tested import base64_decode as func1

# Ground truth function (func0), keep its original implementation and name
def base64_decode(url_content):  # Base64 转换为 URL 链接内容
    if '-' in url_content:
        url_content = url_content.replace('-', '+')
    if '_' in url_content:
        url_content = url_content.replace('_', '/')
    missing_padding = len(url_content) % 4
    if missing_padding != 0:
        url_content += '=' * (4 - missing_padding)
    try:
        base64_content = base64.b64decode(url_content.encode('utf-8')).decode('utf-8', 'ignore')
        base64_content_format = base64_content
        return base64_content_format
    except UnicodeDecodeError:
        base64_content = base64.b64decode(url_content)
        base64_content_format = base64_content
        return str(base64_content)

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
            url_content = inputs["url_content"]

            try:
                expected_output = base64_decode(url_content)
                actual_output = func1(url_content)

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