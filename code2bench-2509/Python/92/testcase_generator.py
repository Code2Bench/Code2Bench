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
def format_index_ranges(indices):
    """Format a list of indices into range strings like '0-1,3-6'."""
    if not indices:
        return ""

    ranges = []
    start = end = indices[0]

    for i in range(1, len(indices)):
        if indices[i] == end + 1:
            end = indices[i]
        else:
            ranges.append(str(start) if start == end else f"{start}-{end}")
            start = end = indices[i]

    # Add the last range
    ranges.append(str(start) if start == end else f"{start}-{end}")
    return ",".join(ranges)

# Strategy for generating index lists
def index_list_strategy():
    return st.lists(
        st.integers(min_value=0, max_value=2147483647),
        min_size=0,
        max_size=20,
        unique=True
    ).map(sorted)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(indices=index_list_strategy())
@example(indices=[])
@example(indices=[0])
@example(indices=[0, 1, 2, 3])
@example(indices=[0, 2, 3, 5])
@example(indices=[1, 3, 5, 7])
@example(indices=[10, 11, 12, 14, 15])
def test_format_index_ranges(indices):
    global stop_collecting
    if stop_collecting:
        return
    
    indices_copy = copy.deepcopy(indices)
    try:
        expected = format_index_ranges(indices_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to prioritize meaningful cases
    if len(indices) > 1 or not indices:
        generated_cases.append({
            "Inputs": {"indices": indices},
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