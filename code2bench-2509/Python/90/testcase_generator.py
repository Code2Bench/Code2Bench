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
def longest_common_prefix_with_lengths(list1, list2):
    max_length = 0
    len_list1 = 0
    len_list2 = 0
    for i, sublist1 in enumerate(list1):
        for j, sublist2 in enumerate(list2):
            match_length = 0
            min_length = min(len(sublist1), len(sublist2))
            for k in range(min_length):
                if sublist1[k] == sublist2[k]:
                    match_length += 1
                else:
                    break
            if match_length > max_length:
                max_length = match_length
                len_list1 = len(sublist1)
                len_list2 = len(sublist2)
    return max_length, len_list1, len_list2

# Strategy for generating sublists
def sublist_strategy():
    return st.lists(
        st.integers(min_value=-2147483648, max_value=2147483647),
        min_size=0, max_size=10
    )

# Strategy for generating 2D lists
def list2d_strategy():
    return st.lists(sublist_strategy(), min_size=1, max_size=5)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(list1=list2d_strategy(), list2=list2d_strategy())
@example(list1=[[1, 2, 3]], list2=[[1, 2, 4]])
@example(list1=[[1, 2], [3, 4]], list2=[[1, 2], [5, 6]])
@example(list1=[[1]], list2=[[1]])
@example(list1=[[1, 2, 3]], list2=[[4, 5, 6]])
@example(list1=[[1, 2, 3], [4, 5, 6]], list2=[[1, 2, 3], [7, 8, 9]])
@example(list1=[[1, 2, 3]], list2=[[1, 2]])
@example(list1=[[1, 2]], list2=[[1, 2, 3]])
def test_longest_common_prefix_with_lengths(list1, list2):
    global stop_collecting
    if stop_collecting:
        return
    
    list1_copy = copy.deepcopy(list1)
    list2_copy = copy.deepcopy(list2)
    try:
        expected = longest_common_prefix_with_lengths(list1_copy, list2_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"list1": list1, "list2": list2},
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