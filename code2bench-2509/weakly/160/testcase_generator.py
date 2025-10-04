from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy
import math

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def orthogonalization_matrix(lengths, angles):
    """Return orthogonalization matrix for crystallographic cell coordinates.

    Angles are expected in degrees.

    The de-orthogonalization matrix is the inverse.

    >>> O = orthogonalization_matrix([10, 10, 10], [90, 90, 90])
    >>> numpy.allclose(O[:3, :3], numpy.identity(3, float) * 10)
    True
    >>> O = orthogonalization_matrix([9.8, 12.0, 15.5], [87.2, 80.7, 69.7])
    >>> numpy.allclose(numpy.sum(O), 43.063229)
    True

    """
    a, b, c = lengths
    angles = np.radians(angles)
    sina, sinb, _ = np.sin(angles)
    cosa, cosb, cosg = np.cos(angles)
    co = (cosa * cosb - cosg) / (sina * sinb)
    return np.array([[a * sinb * math.sqrt(1.0 - co * co), 0.0, 0.0, 0.0], [-a * sinb * co, b * sina, 0.0, 0.0],
                        [a * cosb, b * cosa, c, 0.0], [0.0, 0.0, 0.0, 1.0]])

# Strategies for generating inputs
def lengths_strategy():
    return st.lists(
        st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        min_size=3, max_size=3
    )

def angles_strategy():
    return st.lists(
        st.floats(min_value=0.0, max_value=180.0, allow_nan=False, allow_infinity=False),
        min_size=3, max_size=3
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    lengths=lengths_strategy(),
    angles=angles_strategy()
)
@example(
    lengths=[10.0, 10.0, 10.0],
    angles=[90.0, 90.0, 90.0]
)
@example(
    lengths=[9.8, 12.0, 15.5],
    angles=[87.2, 80.7, 69.7]
)
def test_orthogonalization_matrix(lengths, angles):
    global stop_collecting
    if stop_collecting:
        return

    # Validate input shapes
    if len(lengths) != 3 or len(angles) != 3:
        return

    # Deep copy inputs to avoid modification
    lengths_copy = copy.deepcopy(lengths)
    angles_copy = copy.deepcopy(angles)

    # Call func0 to verify input validity
    try:
        expected = orthogonalization_matrix(lengths_copy, angles_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "lengths": lengths_copy,
            "angles": angles_copy
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