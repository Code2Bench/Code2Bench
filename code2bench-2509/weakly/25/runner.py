import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import list_of_flat_dict_to_dict_of_list as func1
import collections

# Ground truth function (func0), keep its original implementation and name
def list_of_flat_dict_to_dict_of_list(list_of_dict):
    """
    Helper function to go from a list of flat dictionaries to a dictionary of lists.
    By "flat" we mean that none of the values are dictionaries, but are numpy arrays,
    floats, etc.

    Args:
        list_of_dict (list): list of flat dictionaries

    Returns:
        dict_of_list (dict): dictionary of lists
    """
    assert isinstance(list_of_dict, list)
    dic = collections.OrderedDict()
    for i in range(len(list_of_dict)):
        for k in list_of_dict[i]:
            if k not in dic:
                dic[k] = []
            dic[k].append(list_of_dict[i][k])
    return dic

# Define compare_outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Diagnostic runner structure
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            list_of_dict = inputs["list_of_dict"]

            try:
                expected_output = list_of_flat_dict_to_dict_of_list(list_of_dict)
                actual_output = func1(list_of_dict)

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