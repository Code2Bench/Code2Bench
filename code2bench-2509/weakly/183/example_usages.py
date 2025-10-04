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
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def _first_divided_difference(d, fct, fctder, atol=1e-12, rtol=1e-12):
    dif = np.repeat(d[None, :], len(d,), axis=0)
    close_ = np.isclose(dif, dif.T, atol=atol, rtol=rtol)
    dif[close_] = fctder(dif[close_])
    dif[~close_] = (fct(dif[~close_]) - fct(dif.T[~close_])) / \
                   (dif[~close_] - dif.T[~close_])
    return dif

# Strategies for generating inputs
def d_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=st.integers(min_value=1, max_value=10),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

def fct_strategy():
    return st.sampled_from([np.sin, np.cos, np.exp])

def fctder_strategy(fct):
    if fct == np.sin:
        return np.cos
    elif fct == np.cos:
        return lambda x: -np.sin(x)
    elif fct == np.exp:
        return np.exp
    else:
        return lambda x: 1.0

def atol_strategy():
    return st.floats(min_value=1e-15, max_value=1e-9)

def rtol_strategy():
    return st.floats(min_value=1e-15, max_value=1e-9)

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(
    d=d_strategy(),
    fct=fct_strategy(),
    fctder=st.builds(
        lambda f: fctder_strategy(f),
        fct_strategy()
    ),
    atol=atol_strategy(),
    rtol=rtol_strategy()
)
@example(
    d=np.array([1.0]),
    fct=np.sin,
    fctder=np.cos,
    atol=1e-12,
    rtol=1e-12
)
@example(
    d=np.array([1.0, 2.0]),
    fct=np.cos,
    fctder=lambda x: -np.sin(x),
    atol=1e-12,
    rtol=1e-12
)
@example(
    d=np.array([1.0, 1.0]),
    fct=np.exp,
    fctder=np.exp,
    atol=1e-12,
    rtol=1e-12
)
def test_first_divided_difference(d, fct, fctder, atol, rtol):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy inputs to avoid modification
    d_copy = copy.deepcopy(d)
    fct_copy = copy.deepcopy(fct)
    fctder_copy = copy.deepcopy(fctder)
    atol_copy = copy.deepcopy(atol)
    rtol_copy = copy.deepcopy(rtol)

    # Call func0 to verify input validity
    try:
        expected = _first_divided_difference(d_copy, fct_copy, fctder_copy, atol_copy, rtol_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Single element array with sin function"
        elif case_count == 1:
            desc = "Two element array with cos function"
        else:
            desc = "Multiple elements with exp function"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Single element array with exp function"
        elif case_count == 4:
            desc = "Duplicate elements with cos function"
        elif case_count == 5:
            desc = "Large array with sin function"
        elif case_count == 6:
            desc = "Small tolerance values"
        else:
            desc = "Mixed array with exp function"

    # Generate usage code
    usage = f"""import numpy as np

# Construct inputs
d = np.array({d_copy.tolist()})
fct = np.{fct_copy.__name__}
fctder = np.{fctder_copy.__name__}
atol = {atol_copy}
rtol = {rtol_copy}

# Call function
result = _first_divided_difference(d, fct, fctder, atol, rtol)
"""

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "d": d_copy.tolist(),
            "fct": fct_copy.__name__,
            "fctder": fctder_copy.__name__,
            "atol": atol_copy,
            "rtol": rtol_copy
        },
        "Expected": None,
        "Usage": usage
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