from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
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
def translation_matrix(direction):
    M = np.identity(4)
    M[:3, 3] = direction[:3]
    return M

# Strategy for generating direction vectors
def direction_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(3,),
        elements=st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(direction=direction_strategy())
@example(direction=np.array([0.0, 0.0, 0.0]))
@example(direction=np.array([1.0, 2.0, 3.0]))
@example(direction=np.array([-1.0, -2.0, -3.0]))
def test_translation_matrix(direction):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    direction_copy = copy.deepcopy(direction)

    # Call func0 to verify input validity
    try:
        expected = translation_matrix(direction_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "direction": direction_copy.tolist()
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