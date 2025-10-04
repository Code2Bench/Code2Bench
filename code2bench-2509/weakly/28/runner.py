import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import extract_answer_obj as func1

# Ground truth function (func0), keep its original implementation and name
def extract_answer_obj(s: str):
    if "<|begin_of_box|>" not in s or "<|end_of_box|>" not in s:
        return None
    try:
        res = s.split("<|begin_of_box|>")[1].split("<|end_of_box|>")[0].strip()

        # Processing leading zeros if any
        ptn = r"\[\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]\]"
        m = re.search(ptn, res)
        if m:
            old_str = m.group(0)
            v1 = int(m.group(1))
            v2 = int(m.group(2))
            v3 = int(m.group(3))
            v4 = int(m.group(4))
            new_str = f"[[{v1},{v2},{v3},{v4}]]"
            res = res.replace(old_str, new_str)
        try:
            return json.loads(res)
        except:
            return eval(res, {"true": True, "false": False, "null": None})
    except:
        return None

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
            s = inputs["s"]

            try:
                expected_output = extract_answer_obj(s)
                actual_output = func1(s)

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