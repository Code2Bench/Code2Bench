import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import _parsing_score as func1
import re

# Ground truth function (func0), keep its original implementation and name
def _parsing_score(grade_stdout: str) -> Optional[float]:
    for line in grade_stdout.splitlines():
        line = line.strip()
        if "score" not in line:
            continue
        m = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", line)
        if not m:
            continue
        json_str = m.group(0)
        try:
            # Priority 1: JSON parsing
            return float(json.loads(json_str)["score"])
        except:
            pass
        try:
            # Priority 2: Eval dict
            return float(eval(json_str)["score"])
        except:
            pass
        try:
            # Priority 3: Regex for the last number in the string
            return float(re.findall(r"[-+]?\d*\.\d+|\d+", json_str)[-1])
        except:
            pass
    return None

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
            grade_stdout = inputs["grade_stdout"]

            try:
                expected_output = _parsing_score(grade_stdout)
                actual_output = func1(grade_stdout)

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