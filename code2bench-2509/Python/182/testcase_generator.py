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
def get_displacement(before, after):
    """Calculate displacement vector for non-soldier pieces"""
    if len(before) != len(after) or not before:
        return None
    r0, c0 = next(iter(before))
    for r1, c1 in after:
        dr, dc = r1 - r0, c1 - c0
        if all((r + dr, c + dc) in after for r, c in before):
            return (dr, dc)
    return None

# Strategy for generating coordinates
def coordinate_strategy():
    return st.tuples(
        st.integers(min_value=-2147483648, max_value=2147483647),
        st.integers(min_value=-2147483648, max_value=2147483647)
    )

# Strategy for generating sets of coordinates
def coordinate_set_strategy():
    return st.sets(coordinate_strategy(), min_size=1, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(before=coordinate_set_strategy(), after=coordinate_set_strategy())
@example(before={(0, 0)}, after={(1, 1)})
@example(before={(0, 0), (1, 1)}, after={(1, 1), (2, 2)})
@example(before={(0, 0)}, after={(0, 0)})
@example(before={(0, 0)}, after={(0, 1)})
@example(before={(0, 0)}, after={(1, 0)})
@example(before={(0, 0)}, after={(0, 0), (1, 1)})
@example(before={(0, 0), (1, 1)}, after={(0, 0), (1, 1)})
@example(before={(0, 0), (1, 1)}, after={(1, 1), (2, 2)})
@example(before={(0, 0), (1, 1)}, after={(2, 2), (3, 3)})
def test_get_displacement(before, after):
    global stop_collecting
    if stop_collecting:
        return
    
    before_copy = copy.deepcopy(before)
    after_copy = copy.deepcopy(after)
    try:
        expected = get_displacement(before_copy, after_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if len(before) == len(after) and before:
        generated_cases.append({
            "Inputs": {"before": list(before), "after": list(after)},
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