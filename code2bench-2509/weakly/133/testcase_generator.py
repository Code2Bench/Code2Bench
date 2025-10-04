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
def k_mat(two_body_integrals):
    """
    Args:
        two_body_integrals: Numpy array of two-electron integrals with
            OpenFermion Ordering.

    Returns:
        k_matr : Numpy array of the exchange integrals K_{p,q} = (pq|qp)
            (in chemist notation).
    """
    chem_ordering = np.copy(two_body_integrals.transpose(0, 3, 1, 2), order='C')
    return np.einsum('ijji -> ij', chem_ordering)

# Strategy for generating two_body_integrals
def two_body_integrals_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=hnp.array_shapes(min_dims=4, max_dims=4, min_side=1, max_side=5),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(two_body_integrals=two_body_integrals_strategy())
@example(two_body_integrals=np.zeros((1, 1, 1, 1)))
@example(two_body_integrals=np.ones((2, 2, 2, 2)))
@example(two_body_integrals=np.random.rand(3, 3, 3, 3))
def test_k_mat(two_body_integrals):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    two_body_integrals_copy = copy.deepcopy(two_body_integrals)

    # Call func0 to verify input validity
    try:
        expected = k_mat(two_body_integrals_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "two_body_integrals": two_body_integrals_copy.tolist()
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