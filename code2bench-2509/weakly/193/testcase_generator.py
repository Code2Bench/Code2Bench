from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import scipy.stats
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
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t._ppf((1 + confidence) / 2.0, n - 1)
    return m, m - h, m + h

# Strategies for generating inputs
def data_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=st.integers(min_value=1, max_value=100),
        elements=st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)
    )

def confidence_strategy():
    return st.floats(min_value=0.0, max_value=1.0, exclude_min=True, exclude_max=True)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    data=data_strategy(),
    confidence=confidence_strategy()
)
@example(
    data=np.array([1.0]),
    confidence=0.95
)
@example(
    data=np.array([1.0, 2.0, 3.0]),
    confidence=0.99
)
@example(
    data=np.array([-1.0, 0.0, 1.0]),
    confidence=0.90
)
@example(
    data=np.array([0.0]),
    confidence=0.50
)
def test_mean_confidence_interval(data, confidence):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    data_copy = copy.deepcopy(data)
    confidence_copy = copy.deepcopy(confidence)

    # Call func0 to verify input validity
    try:
        expected = mean_confidence_interval(data_copy, confidence_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "data": data_copy.tolist(),
            "confidence": confidence_copy
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