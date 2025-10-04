import json
import os
from groundtruth import fast_format_html as func1  # Preserve original import

# Change testcases filepath to example_usages.json
TEST_CASE_DIR = os.path.abspath('test_cases')
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, 'example_usages.json')
results = {"Normal cases": [], "Failed cases": []}  # Add a container for failed cases

def load_cases():
    with open(TEST_CASE_FILE) as f:
        return json.load(f)

def execute_cases(cases):
    # Iterate through each test case
    normal_cases = cases.get('Normal cases', [])
    if not normal_cases:
        return  # No normal cases to process
    
    for case in normal_cases:
        try:
            # Attempt to execute the function with the given inputs
            actual = func1(**case['Inputs'])
            results['Normal cases'].append({
                **case,
                'Expected': actual  # Capture the result
            })
        except Exception as e:
            # Capture the error and store the failed case
            results['Failed cases'].append({
                **case,
                'Error': str(e)  # Record the exception message
            })
    
    other_cases = cases.get('Others', [])
    if other_cases:
        results['Others'] = []
    for case in other_cases:
        try:
            # Attempt to execute the function with the given inputs
            actual = func1(**case['Inputs'])
            results['Others'].append({
                **case,
                'Expected': actual  # Capture the result
            })
        except Exception as e:
            # Capture the error and store the failed case
            results['Failed cases'].append({
                **case,
                'Error': str(e)  # Record the exception message
            })

if __name__ == '__main__':
    test_cases = load_cases()
    execute_cases(test_cases)
    
    # Overwrite with enriched data
    with open(TEST_CASE_FILE, 'w') as f:
        json.dump(results, f, indent=2)