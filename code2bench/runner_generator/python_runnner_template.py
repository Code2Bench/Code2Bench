import json
import os
from tested import move_y as func1
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
    for i, case in enumerate(test_cases):
        inputs = case["Inputs"]
        expected_output = case["Expected"]

        # Run function under test
        actual_output = func1(**inputs)  # Copy matrix to avoid in-place modification

        # Check if results match using deep_compare
        if not deep_compare(actual_output, expected_output, tolerance=1e-6):
            print(f"Test case {i + 1} failed:")
            print(f"  Inputs: {inputs}")
            print(f"  Expected: {expected_output}")
            print(f"  Actual: {actual_output}")
        else:
            print(f"Test case {i + 1} passed.")

if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    run_tests_with_loaded_cases(test_cases)