REASONING_PROMPT = """
## Role: You are an expert Python developer specializing in test automation frameworks. Your task is to transform a normal test case runner into a specialized version that executes test cases and captures their outputs in JSON format.

## Input Requirements:
1. You will receive a Python file containing a normal test case runner implementation
2. The runner typically loads test cases from JSON and compares actual vs expected outputs

## Transformation Requirements:
1. Core Functionality Change:
- Convert from assertion-based testing to output-capture mode
- Remove all comparison logic (no more pass/fail checks)
- Store all actual outputs as "Expected" results in the output JSON

2. Output Specification:
- Create a global `results` dictionary with "Test cases" array
- Each executed case should append:
{
    "Inputs": original_inputs,
    "Expected": actual_output
}
- Final output should overwrite the input JSON file with enriched data

3. Ensure JSON compatibility  
- Ensure that all data types are JSON-compatible.
- Convert non-serializable types to JSON-compatible formats (`list`, `str`, `int`, etc.).
- Example: Convert `set()` to `list()`, `tuple()` to `list()`, etc.
   
## Example Transformation:
Input (Normal Runner):
```python
import json
import os
from groundtruth import fast_format_html as func1

# Configuration for loading test cases
TEST_CASE_DIR = os.path.abspath('test_cases')
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, 'test_cases.json')

# Function to load test cases from JSON
def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_FILE):
        print(f'JSON file not found: {TEST_CASE_FILE}')
        return []

    # Read the JSON file
    with open(TEST_CASE_FILE, 'r') as f:
        test_cases = json.load(f)

    return test_cases

# Function to run tests with loaded cases
def run_tests_with_loaded_cases(test_cases):
    for i, case in enumerate(test_cases):
        inputs = case['Inputs']
        expected_output = case['Expected']

        # Extract input parameter
        html_string = inputs['html_string']

        # Run the function under test
        actual_output = func1(html_string)

        # Check if the outputs match
        if actual_output != expected_output:
            print(f'Test case {i + 1} failed:')
            print(f'  Input: {html_string}')
            print(f'  Expected: {expected_output}')
            print(f'  Actual: {actual_output}')
        else:
            print(f'Test case {i + 1} passed.')

if __name__ == '__main__':
    # Load test cases from JSON
    test_cases = load_test_cases_from_json()
    run_tests_with_loaded_cases(test_cases)
```
## Output (Output Capture Runner):
```python
import json
import os
from groundtruth import target_function  # Preserve original import

# Change testcases filepath to reasoning_testcases.json
TEST_CASE_DIR = os.path.abspath('test_cases')
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, 'reasoning_testcases.json')
results = {"Test cases": []}  # New results container

def load_cases():
    with open(TEST_CASE_FILE) as f:
        return json.load(f)

def execute_cases(cases):
    for case in cases:
        actual = target_function(**case['Inputs'])
        results['Test cases'].append({
            **case,
            'Expected': actual  # Capture instead of compare
        })

if __name__ == '__main__':
    test_cases = load_cases()
    execute_cases(test_cases['Test cases'])
    
    # Overwrite with enriched data
    with open(TEST_CASE_FILE, 'w') as f:
        json.dump(results, f, indent=2)

## Note:
- Only return the generated code in JSON format with "Runner" key.
- test_cases is a dict with "Test cases" key, not a list.
- Follow the style of the exmple code provided without any extra code.
"""