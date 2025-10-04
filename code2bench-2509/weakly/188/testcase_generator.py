from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import pandas as pd
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
def _is_categorical(values):
    dtype_name = pd.Series(values).convert_dtypes().dtype.name.lower()
    return dtype_name in ["category", "string", "boolean"]

# Strategies for generating inputs
def values_strategy():
    return st.one_of(
        st.lists(st.sampled_from(["a", "b", "c"]), min_size=1, max_size=10),  # Categorical (string)
        st.lists(st.booleans(), min_size=1, max_size=10),  # Categorical (boolean)
        st.lists(st.integers(), min_size=1, max_size=10),  # Non-categorical (integer)
        st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=10)  # Non-categorical (float)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(values=values_strategy())
@example(values=["a", "b", "a"])  # Categorical (string)
@example(values=[True, False, True])  # Categorical (boolean)
@example(values=[1, 2, 3])  # Non-categorical (integer)
@example(values=[1.0, 2.0, 3.0])  # Non-categorical (float)
def test_is_categorical(values):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    values_copy = copy.deepcopy(values)

    # Call func0 to verify input validity
    try:
        result = _is_categorical(values_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "values": values_copy
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