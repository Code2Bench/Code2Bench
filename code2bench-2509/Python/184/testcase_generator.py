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
def build_immediate_ancestor_map(ancestor_dict, adj_list):
    immediate_ancestor_map = {}
    for node, ancestors in ancestor_dict.items():
        if ancestors and node in adj_list:
            immediate_ancestor_map[node] = ancestors[0]
            for i in range(len(ancestors) - 1):
                if ancestors[i] not in immediate_ancestor_map:
                    immediate_ancestor_map[ancestors[i]] = ancestors[i + 1]
    return immediate_ancestor_map

# Strategy for generating ancestor_dict
def ancestor_dict_strategy():
    return st.dictionaries(
        keys=st.integers(min_value=0, max_value=100),
        values=st.lists(st.integers(min_value=0, max_value=100), min_size=0, max_size=10),
        min_size=1,
        max_size=10
    )

# Strategy for generating adj_list
def adj_list_strategy():
    return st.lists(st.integers(min_value=0, max_value=100), min_size=0, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(ancestor_dict=ancestor_dict_strategy(), adj_list=adj_list_strategy())
@example(ancestor_dict={1: [2, 3]}, adj_list=[1, 2])
@example(ancestor_dict={1: []}, adj_list=[1])
@example(ancestor_dict={1: [2], 2: [3]}, adj_list=[1, 2])
@example(ancestor_dict={1: [2, 3], 2: [3, 4]}, adj_list=[1, 2, 3])
@example(ancestor_dict={1: [2], 3: [4]}, adj_list=[1, 3])
def test_build_immediate_ancestor_map(ancestor_dict, adj_list):
    global stop_collecting
    if stop_collecting:
        return
    
    ancestor_dict_copy = copy.deepcopy(ancestor_dict)
    adj_list_copy = copy.deepcopy(adj_list)
    try:
        expected = build_immediate_ancestor_map(ancestor_dict_copy, adj_list_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(ancestors and node in adj_list for node, ancestors in ancestor_dict.items()):
        generated_cases.append({
            "Inputs": {"ancestor_dict": ancestor_dict, "adj_list": adj_list},
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