from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from math import log, ceil

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def ratio_to_db(ratio, val2=None, using_amplitude=True):
    """
    Converts the input float to db, which represents the equivalent
    to the ratio in power represented by the multiplier passed in.
    """
    ratio = float(ratio)

    # accept 2 values and use the ratio of val1 to val2
    if val2 is not None:
        ratio = ratio / val2

    # special case for multiply-by-zero (convert to silence)
    if ratio == 0:
        return -float('inf')

    if using_amplitude:
        return 20 * log(ratio, 10)
    else:  # using power
        return 10 * log(ratio, 10)

# Strategies for generating inputs
def ratio_strategy():
    return st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)

def val2_strategy():
    return st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False, exclude_min=True)

def using_amplitude_strategy():
    return st.booleans()

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    ratio=ratio_strategy(),
    val2=st.one_of(st.none(), val2_strategy()),
    using_amplitude=using_amplitude_strategy()
)
@example(ratio=0.0, val2=None, using_amplitude=True)
@example(ratio=1.0, val2=1.0, using_amplitude=True)
@example(ratio=1.0, val2=1.0, using_amplitude=False)
@example(ratio=10.0, val2=2.0, using_amplitude=True)
@example(ratio=10.0, val2=2.0, using_amplitude=False)
@example(ratio=-1.0, val2=None, using_amplitude=True)
@example(ratio=-1.0, val2=None, using_amplitude=False)
def test_ratio_to_db(ratio, val2, using_amplitude):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    ratio_copy = copy.deepcopy(ratio)
    val2_copy = copy.deepcopy(val2)
    using_amplitude_copy = copy.deepcopy(using_amplitude)

    # Call func0 to verify input validity
    try:
        expected = ratio_to_db(ratio_copy, val2_copy, using_amplitude_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "ratio": ratio_copy,
            "val2": val2_copy,
            "using_amplitude": using_amplitude_copy
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