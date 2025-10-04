from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def remove_duplicates(data_list):
    """
        data_list: [(67, (3386, 3406), 48, (2435, 2455)), ...]
    """
    seen = {} 
    result = []

    for item in data_list:
        if item[0] == item[2]:
            continue

        key = (item[0], item[2])

        if key not in seen.keys():
            seen[key] = True
            result.append(item)

    return result

# Strategy for generating tuples
def tuple_strategy():
    return st.tuples(
        st.integers(min_value=-2147483648, max_value=2147483647),
        st.tuples(
            st.integers(min_value=-2147483648, max_value=2147483647),
            st.integers(min_value=-2147483648, max_value=2147483647)
        ),
        st.integers(min_value=-2147483648, max_value=2147483647),
        st.tuples(
            st.integers(min_value=-2147483648, max_value=2147483647),
            st.integers(min_value=-2147483648, max_value=2147483647)
        )
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(data_list=st.lists(tuple_strategy(), min_size=0, max_size=20))
@example(data_list=[])
@example(data_list=[(67, (3386, 3406), 48, (2435, 2455))])
@example(data_list=[(67, (3386, 3406), 67, (2435, 2455))])
@example(data_list=[(67, (3386, 3406), 48, (2435, 2455)), (67, (3386, 3406), 48, (2435, 2455))])
@example(data_list=[(67, (3386, 3406), 48, (2435, 2455)), (48, (2435, 2455), 67, (3386, 3406))])
def test_remove_duplicates(data_list):
    global stop_collecting
    if stop_collecting:
        return
    
    data_list_copy = copy.deepcopy(data_list)
    try:
        expected = remove_duplicates(data_list_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(item[0] != item[2] for item in data_list):
        generated_cases.append({
            "Inputs": {"data_list": data_list},
            "Expected": expected
        })
        if len(generated_cases) >= 500:
            stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)