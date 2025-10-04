from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from bisect import bisect_left

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def closest(value, sorted_list):
    index = bisect_left(sorted_list, value)
    if index == 0:
        return sorted_list[0]
    elif index == len(sorted_list):
        return sorted_list[-1]
    else:
        value_before = sorted_list[index - 1]
        value_after = sorted_list[index]
        if value_after - value < value - value_before:
            return value_after
        else:
            return value_before

# Strategies for generating inputs
def value_strategy():
    return st.integers(min_value=-100, max_value=100)

def sorted_list_strategy():
    return st.lists(
        st.integers(min_value=-100, max_value=100),
        min_size=1,
        max_size=20,
        unique=True
    ).map(sorted)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    value=value_strategy(),
    sorted_list=sorted_list_strategy()
)
@example(value=0, sorted_list=[0])
@example(value=5, sorted_list=[1, 2, 3, 4, 6, 7, 8])
@example(value=-10, sorted_list=[-5, 0, 5])
@example(value=10, sorted_list=[-5, 0, 5])
@example(value=3, sorted_list=[1, 2, 4, 5])
def test_closest(value, sorted_list):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    value_copy = copy.deepcopy(value)
    sorted_list_copy = copy.deepcopy(sorted_list)

    # Call func0 to verify input validity
    try:
        expected = closest(value_copy, sorted_list_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "value": value_copy,
            "sorted_list": sorted_list_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)