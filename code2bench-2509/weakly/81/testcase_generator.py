from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import copy
import bisect
import json
import os
import atexit

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _quantize(x, bins):
    bins = copy.deepcopy(bins)
    bins = sorted(bins)
    quantized = list(map(lambda y: bisect.bisect_right(bins, y), x))
    return quantized

# Strategies for generating inputs
def x_strategy():
    return st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=10)

def bins_strategy():
    return st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(x=x_strategy(), bins=bins_strategy())
@example(x=[], bins=[])
@example(x=[1.0], bins=[1.0])
@example(x=[1.0, 2.0, 3.0], bins=[1.0, 2.0, 3.0])
@example(x=[1.0, 2.0, 3.0], bins=[2.0])
@example(x=[1.0, 2.0, 3.0], bins=[4.0])
@example(x=[1.0, 2.0, 3.0], bins=[0.0, 1.0, 2.0, 3.0, 4.0])
def test_quantize(x, bins):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    x_copy = copy.deepcopy(x)
    bins_copy = copy.deepcopy(bins)

    # Call func0 to verify input validity
    try:
        expected = _quantize(x_copy, bins_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "x": x_copy,
            "bins": bins_copy
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