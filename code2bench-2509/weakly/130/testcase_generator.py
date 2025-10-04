from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy
from scipy.spatial.transform import Rotation as R

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def align_vector_sets(vec_set1, vec_set2):
    """
    Computes a single quaternion representing the rotation that best aligns vec_set1 to vec_set2.

    Args:
        vec_set1 (np.array): (N, 3) tensor of N 3D vectors
        vec_set2 (np.array): (N, 3) tensor of N 3D vectors

    Returns:
        np.array: (4,) Normalized quaternion representing the overall rotation
    """
    rot, _ = R.align_vectors(vec_set1, vec_set2)
    return rot.as_quat()

# Strategies for generating inputs
def vec_set_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=st.tuples(
            st.integers(min_value=1, max_value=10),  # N
            st.just(3)                               # 3D vectors
        ),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    vec_set1=vec_set_strategy(),
    vec_set2=vec_set_strategy()
)
@example(
    vec_set1=np.array([[1.0, 0.0, 0.0]]),
    vec_set2=np.array([[0.0, 1.0, 0.0]])
)
@example(
    vec_set1=np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
    vec_set2=np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
)
@example(
    vec_set1=np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    vec_set2=np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]])
)
def test_align_vector_sets(vec_set1: np.ndarray, vec_set2: np.ndarray):
    global stop_collecting
    if stop_collecting:
        return

    # Validate input shapes
    if vec_set1.shape != vec_set2.shape:
        return

    # Deep copy inputs to avoid modification
    vec_set1_copy = copy.deepcopy(vec_set1)
    vec_set2_copy = copy.deepcopy(vec_set2)

    # Call func0 to verify input validity
    try:
        quat = align_vector_sets(vec_set1_copy, vec_set2_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "vec_set1": vec_set1_copy.tolist(),
            "vec_set2": vec_set2_copy.tolist()
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