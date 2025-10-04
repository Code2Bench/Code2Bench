from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy
from scipy import sparse

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _build_dispersed_image_of_source(x, y, flux):
    minx = int(min(x))
    maxx = int(max(x))
    miny = int(min(y))
    maxy = int(max(y))
    a = sparse.coo_matrix(
        (flux, (y - miny, x - minx)), shape=(maxy - miny + 1, maxx - minx + 1)
    ).toarray()
    bounds = [minx, maxx, miny, maxy]
    return a, bounds

# Strategies for generating inputs
def x_strategy():
    return hnp.arrays(
        dtype=np.int32,
        shape=st.integers(min_value=1, max_value=10),
        elements=st.integers(min_value=0, max_value=100)
    )

def y_strategy(x):
    return hnp.arrays(
        dtype=np.int32,
        shape=len(x),
        elements=st.integers(min_value=0, max_value=100)
    )

def flux_strategy(x):
    return hnp.arrays(
        dtype=np.float32,
        shape=len(x),
        elements=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    x=x_strategy(),
    y=st.one_of(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=10).map(np.array)),
    flux=st.one_of(st.lists(st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False), min_size=1, max_size=10).map(np.array))
)
@example(
    x=np.array([0]),
    y=np.array([0]),
    flux=np.array([1.0])
)
@example(
    x=np.array([0, 1, 2]),
    y=np.array([0, 1, 2]),
    flux=np.array([1.0, 2.0, 3.0])
)
@example(
    x=np.array([10, 20, 30]),
    y=np.array([10, 20, 30]),
    flux=np.array([10.0, 20.0, 30.0])
)
def test_build_dispersed_image_of_source(x, y, flux):
    global stop_collecting
    if stop_collecting:
        return

    # Validate input shapes
    if len(x) != len(y) or len(x) != len(flux):
        return

    # Deep copy inputs to avoid modification
    x_copy = copy.deepcopy(x)
    y_copy = copy.deepcopy(y)
    flux_copy = copy.deepcopy(flux)

    # Call func0 to verify input validity
    try:
        expected_a, expected_bounds = _build_dispersed_image_of_source(x_copy, y_copy, flux_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "x": x_copy.tolist(),
            "y": y_copy.tolist(),
            "flux": flux_copy.tolist()
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