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
def translation_from_matrix(matrix) -> np.ndarray:
    return np.array(matrix, copy=False)[:3, 3].copy()

# Strategy for generating 4x4 matrices
def matrix_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(4, 4),
        elements=st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(matrix=matrix_strategy())
@example(matrix=np.eye(4))
@example(matrix=np.zeros((4, 4)))
@example(matrix=np.array([[1, 0, 0, 10], [0, 1, 0, 20], [0, 0, 1, 30], [0, 0, 0, 1]]))
def test_translation_from_matrix(matrix):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    matrix_copy = copy.deepcopy(matrix)

    # Call func0 to verify input validity
    try:
        expected = translation_from_matrix(matrix_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "matrix": matrix_copy.tolist()
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