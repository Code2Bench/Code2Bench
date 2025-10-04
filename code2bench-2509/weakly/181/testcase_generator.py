from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import itertools
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
def get_all_subsets(ring_list):
    all_sub_list = []
    for n_sub in range(len(ring_list)+1):
        all_sub_list.extend(itertools.combinations(ring_list, n_sub))
    return all_sub_list

# Strategy for generating ring_list
def ring_list_strategy():
    return st.lists(
        st.integers(min_value=0, max_value=100),
        min_size=0, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(ring_list=ring_list_strategy())
@example(ring_list=[])
@example(ring_list=[1])
@example(ring_list=[1, 2])
@example(ring_list=[1, 2, 3])
def test_get_all_subsets(ring_list):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    ring_list_copy = copy.deepcopy(ring_list)

    # Call func0 to verify input validity
    try:
        expected = get_all_subsets(ring_list_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "ring_list": ring_list_copy
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