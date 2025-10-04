from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import inspect
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
def _get_valid_kwargs(func, kwargs):
    try:
        sig = inspect.signature(func)
        param_keys = set(sig.parameters.keys())
        return {k: v for k, v in kwargs.items() if k in param_keys}
    except (ValueError, TypeError):
        return kwargs

# Strategies for generating inputs
def func_strategy():
    return st.sampled_from([len, str, int, float, dict])

def kwargs_strategy():
    return st.dictionaries(
        keys=st.text(min_size=1, max_size=10),
        values=st.one_of(
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(),
            st.lists(st.integers()),
            st.dictionaries(st.text(), st.integers())
        ),
        min_size=0, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    func=func_strategy(),
    kwargs=kwargs_strategy()
)
@example(func=len, kwargs={})
@example(func=str, kwargs={"key": "value"})
@example(func=int, kwargs={"x": 10})
@example(func=float, kwargs={"y": 3.14})
@example(func=dict, kwargs={"a": 1, "b": 2})
def test_get_valid_kwargs(func, kwargs):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    func_copy = copy.deepcopy(func)
    kwargs_copy = copy.deepcopy(kwargs)

    # Call func0 to verify input validity
    try:
        expected = _get_valid_kwargs(func_copy, kwargs_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "func": func_copy.__name__,
            "kwargs": kwargs_copy
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