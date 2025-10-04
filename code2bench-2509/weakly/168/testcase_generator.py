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
def S_inv_eulerZYX_body(euler_coordinates):
    y = euler_coordinates[1]
    z = euler_coordinates[2]
    E = np.zeros((3, 3))
    E[0, 1] = np.sin(z)/np.cos(y)
    E[0, 2] = np.cos(z)/np.cos(y)
    E[1, 1] = np.cos(z)
    E[1, 2] = -np.sin(z)
    E[2, 0] = 1.0
    E[2, 1] = np.sin(z)*np.sin(y)/np.cos(y)
    E[2, 2] = np.cos(z)*np.sin(y)/np.cos(y)
    return E

# Strategies for generating inputs
def euler_coordinates_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(3,),
        elements=st.floats(min_value=-np.pi/2 + 1e-5, max_value=np.pi/2 - 1e-5, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(euler_coordinates=euler_coordinates_strategy())
@example(euler_coordinates=np.array([0.0, 0.0, 0.0]))
@example(euler_coordinates=np.array([np.pi/4, np.pi/4, np.pi/4]))
@example(euler_coordinates=np.array([-np.pi/4, -np.pi/4, -np.pi/4]))
@example(euler_coordinates=np.array([np.pi/2 - 1e-5, np.pi/2 - 1e-5, np.pi/2 - 1e-5]))
@example(euler_coordinates=np.array([-np.pi/2 + 1e-5, -np.pi/2 + 1e-5, -np.pi/2 + 1e-5]))
def test_S_inv_eulerZYX_body(euler_coordinates):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    euler_coordinates_copy = copy.deepcopy(euler_coordinates)

    # Call func0 to verify input validity
    try:
        expected = S_inv_eulerZYX_body(euler_coordinates_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "euler_coordinates": euler_coordinates_copy.tolist()
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