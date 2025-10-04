from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
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
def _get_device_combinations(device_indices):
    devices = sorted(list(device_indices))
    n = len(devices)
    all_combinations = []

    if n == 0:
        return []

    for i in range(1, 1 << n):
        current_combination = []
        for j in range(n):
            if (i >> j) & 1:
                current_combination.append(devices[j])

        if 1 <= len(current_combination) <= n:
            all_combinations.append(current_combination)

    all_combinations.sort(key=lambda combo: (len(combo), combo))

    return all_combinations

# Strategy for generating device indices
device_indices_strategy = st.lists(
    st.integers(min_value=0, max_value=10),  # Restrict to reasonable range
    max_size=5  # Limit to avoid combinatorial explosion
).map(lambda x: set(x))  # Convert to set to match function input

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(device_indices=device_indices_strategy)
@example(device_indices=set())
@example(device_indices={1})
@example(device_indices={1, 2})
@example(device_indices={1, 2, 3})
def test_get_device_combinations(device_indices):
    global stop_collecting
    if stop_collecting:
        return

    device_indices_copy = copy.deepcopy(device_indices)
    try:
        expected = _get_device_combinations(device_indices_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    if len(device_indices) <= 5:  # Filter to avoid too large inputs
        generated_cases.append({
            "Inputs": {"device_indices": list(device_indices)},  # Convert set to list for JSON serialization
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