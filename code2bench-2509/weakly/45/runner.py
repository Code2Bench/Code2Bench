import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import get_one_prot_diff_name_pairs as func1

# Ground truth function (func0), keep its original implementation and name
def get_one_prot_diff_name_pairs(names):
    """
    Get all pairs of names that have a charge difference of 1.

    Assumes that the names are in the format "name_charge_spin"
    """
    name_pairs = []
    for name0, name1 in itertools.combinations(names, 2):
        name0_charge = int(name0.split("_")[-2])
        name1_charge = int(name1.split("_")[-2])
        if abs(name0_charge - name1_charge) == 1:
            name_pairs.append((name0, name1))
    return name_pairs

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
            names = inputs["names"]

            try:
                expected_output = get_one_prot_diff_name_pairs(names)
                actual_output = func1(names)

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
        print("No test cases loaded.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)