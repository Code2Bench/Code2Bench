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
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

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
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(values=values_strategy())
@example(values=["a", "b", "a"])  # Categorical (string)
@example(values=[True, False, True])  # Categorical (boolean)
@example(values=[1, 2, 3])  # Non-categorical (integer)
@example(values=[1.0, 2.0, 3.0])  # Non-categorical (float)
def test_is_categorical(values):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy input to avoid modification
    values_copy = copy.deepcopy(values)

    # Call func0 to verify input validity
    try:
        result = _is_categorical(values_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Categorical string values"
        elif case_count == 1:
            desc = "Categorical boolean values"
        else:
            desc = "Non-categorical integer values"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Non-categorical float values"
        elif case_count == 4:
            desc = "Mixed categorical and non-categorical values"
        elif case_count == 5:
            desc = "Single categorical string value"
        elif case_count == 6:
            desc = "Single categorical boolean value"
        else:
            desc = "Single non-categorical integer value"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "values": values_copy
        },
        "Expected": result,
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