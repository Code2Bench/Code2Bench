import json
import os
from tested import insert_lines_into_block as func1
from helper import deep_compare

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases")
TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []

    # Read JSON file
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)

    return test_cases

def run_tests_with_loaded_cases(test_cases):
    passed_count = 0
    failed_count = 0
    total_count = len(test_cases)
    failures = []

    execution_error = None
    
    try:
        for i, case in enumerate(test_cases):
            inputs = case["Inputs"]
            expected_output = case["Expected"]

            try:
                actual_output = func1(**inputs)
                
                if not deep_compare(actual_output, expected_output, tolerance=1e-6):
                    failed_count += 1
                    failure_detail = {
                        "case_id": i + 1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output,
                        "actual": actual_output
                    }
                    failures.append(failure_detail)

                    print(f"Test case {i + 1} failed:")
                    print(f"  Inputs: {inputs}")
                    print(f"  Expected: {expected_output}")
                    print(f"  Actual: {actual_output}")
                else:
                    passed_count += 1
                    print(f"Test case {i + 1} passed.")
            
            except Exception as e:
                failed_count += 1
                failure_detail = {
                    "case_id": i + 1,
                    "type": "ExecutionError",
                    "inputs": inputs,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
                failures.append(failure_detail)
                print(f"Test case {i + 1} failed with execution error:")
                print(f"  Inputs: {inputs}")
                print(f"  Error Type: {type(e).__name__}")
                print(f"  Error Message: {str(e)}")
    except Exception as e:
        execution_error = {
            "type": "CriticalExecutionError",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }

    summary = {
        "passed": passed_count,
        "failed": failed_count,
        "total": total_count,
        "failures": failures,
        "execution_error": execution_error
    }
    print("\n---DIAGNOSTIC_SUMMARY_START---")
    print(json.dumps(summary, indent=2))
    print("---DIAGNOSTIC_SUMMARY_END---")

if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    run_tests_with_loaded_cases(test_cases)