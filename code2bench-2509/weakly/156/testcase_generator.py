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
def undistribute(iterable):
    return [
        x
        for x in itertools.chain.from_iterable(
            itertools.zip_longest(*[list(x) for x in iterable])
        )
        if x is not None
    ]

# Strategy for generating iterables
def iterable_strategy():
    return st.lists(
        st.lists(
            st.integers(min_value=0, max_value=100),
            min_size=0, max_size=10
        ),
        min_size=0, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(iterable=iterable_strategy())
@example(iterable=[])
@example(iterable=[[1, 2, 3]])
@example(iterable=[[1], [2], [3]])
@example(iterable=[[1, 2], [3, 4]])
@example(iterable=[[1, 2, 3], [4, 5], [6]])
def test_undistribute(iterable):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    iterable_copy = copy.deepcopy(iterable)

    # Call func0 to verify input validity
    try:
        expected = undistribute(iterable_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "iterable": iterable_copy
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