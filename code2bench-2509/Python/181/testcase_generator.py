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
def binary_search(candidates, target):
    traj = []
    left, right = 0, len(candidates) - 1
    traj.append(candidates[left])
    traj.append(candidates[right])
    while left <= right:
        mid = (left + right) // 2
        traj.append(candidates[mid])
        if candidates[mid] < target:
            left = mid + 1
        elif candidates[mid] > target:
            right = mid - 1
        else:
            break
    return traj, candidates[left]

# Strategy for generating sorted lists of integers
def sorted_list_strategy():
    return st.lists(
        st.integers(min_value=-2147483648, max_value=2147483647),
        min_size=1,
        max_size=100
    ).map(sorted)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    candidates=sorted_list_strategy(),
    target=st.integers(min_value=-2147483648, max_value=2147483647)
)
@example(candidates=[1, 2, 3, 4, 5], target=3)
@example(candidates=[1, 2, 3, 4, 5], target=1)
@example(candidates=[1, 2, 3, 4, 5], target=5)
@example(candidates=[1, 2, 3, 4, 5], target=6)
@example(candidates=[1, 2, 3, 4, 5], target=0)
@example(candidates=[1], target=1)
@example(candidates=[1], target=2)
def test_binary_search(candidates, target):
    global stop_collecting
    if stop_collecting:
        return
    
    candidates_copy = copy.deepcopy(candidates)
    try:
        traj, result = binary_search(candidates_copy, target)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"candidates": candidates, "target": target},
        "Expected": [traj, result]
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)