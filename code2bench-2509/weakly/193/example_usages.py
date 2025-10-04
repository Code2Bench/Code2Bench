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
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

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
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
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
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy inputs to avoid modification
    data_copy = copy.deepcopy(data)
    confidence_copy = copy.deepcopy(confidence)

    # Call func0 to verify input validity
    try:
        expected = mean_confidence_interval(data_copy, confidence_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Multiple data points with default confidence"
        elif case_count == 1:
            desc = "Single data point with high confidence"
        else:
            desc = "Mixed positive and negative data points"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Single data point with low confidence"
        elif case_count == 4:
            desc = "Large dataset with high confidence"
        elif case_count == 5:
            desc = "Small dataset with low confidence"
        elif case_count == 6:
            desc = "Dataset with extreme values"
        else:
            desc = "Dataset with varying confidence levels"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "data": data_copy.tolist(),
            "confidence": confidence_copy
        },
        "Expected": expected,
        "Usage": None
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)