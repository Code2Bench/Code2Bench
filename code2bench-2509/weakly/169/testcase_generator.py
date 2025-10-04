from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import math
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
def S_inv_eulerZYX_body_deriv(euler_coordinates, omega):
    y = euler_coordinates[1]
    z = euler_coordinates[2]

    J_y = np.zeros((3, 3))
    J_z = np.zeros((3, 3))

    J_y[0, 1] = math.tan(y)/math.cos(y)*math.sin(z)
    J_y[0, 2] = math.tan(y)/math.cos(y)*math.cos(z)
    J_y[2, 1] = math.sin(z)/(math.cos(y))**2
    J_y[2, 2] = math.cos(z)/(math.cos(y))**2

    J_z[0, 1] = math.cos(z)/math.cos(y)
    J_z[0, 2] = -math.sin(z)/math.cos(y)
    J_z[1, 1] = -math.sin(z)
    J_z[1, 2] = -math.cos(z)
    J_z[2, 1] = math.cos(z)*math.tan(y)
    J_z[2, 2] = -math.sin(z)*math.tan(y)

    J = np.zeros((3, 3))
    J[:, 1] = np.dot(J_y, omega)
    J[:, 2] = np.dot(J_z, omega)

    return J

# Strategies for generating inputs
def euler_coordinates_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(3,),
        elements=st.floats(min_value=-np.pi/2 + 0.01, max_value=np.pi/2 - 0.01, allow_nan=False, allow_infinity=False)
    )

def omega_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=(3,),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    euler_coordinates=euler_coordinates_strategy(),
    omega=omega_strategy()
)
@example(
    euler_coordinates=np.array([0.0, 0.0, 0.0]),
    omega=np.array([0.0, 0.0, 0.0])
)
@example(
    euler_coordinates=np.array([0.0, np.pi/4, np.pi/4]),
    omega=np.array([1.0, 1.0, 1.0])
)
@example(
    euler_coordinates=np.array([0.0, -np.pi/4, -np.pi/4]),
    omega=np.array([-1.0, -1.0, -1.0])
)
def test_S_inv_eulerZYX_body_deriv(euler_coordinates, omega):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    euler_coordinates_copy = copy.deepcopy(euler_coordinates)
    omega_copy = copy.deepcopy(omega)

    # Call func0 to verify input validity
    try:
        expected = S_inv_eulerZYX_body_deriv(euler_coordinates_copy, omega_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "euler_coordinates": euler_coordinates_copy.tolist(),
            "omega": omega_copy.tolist()
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