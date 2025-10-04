from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from collections.abc import Iterable
from typing import Any

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _expand_iterable(original, num_desired, default):
    if isinstance(original, Iterable) and not isinstance(original, str):
        return original + [default] * (num_desired - len(original))
    else:
        return [default] * num_desired

# Strategies for generating inputs
def original_strategy():
    return st.one_of(
        st.lists(st.integers(), min_size=0, max_size=10),
        st.text(min_size=0, max_size=10),
        st.integers(min_value=0, max_value=100),
        st.floats(min_value=0.0, max_value=100.0)
    )

def num_desired_strategy():
    return st.integers(min_value=0, max_value=10)

def default_strategy():
    return st.one_of(
        st.integers(min_value=0, max_value=100),
        st.floats(min_value=0.0, max_value=100.0)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    original=original_strategy(),
    num_desired=num_desired_strategy(),
    default=default_strategy()
)
@example(original=[1, 2, 3], num_desired=5, default=0)
@example(original="hello", num_desired=5, default=0)
@example(original=123, num_desired=5, default=0)
@example(original=[], num_desired=5, default=0)
@example(original=[1, 2, 3], num_desired=0, default=0)
def test_expand_iterable(original: Any, num_desired: int, default: Any):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    original_copy = copy.deepcopy(original)
    num_desired_copy = copy.deepcopy(num_desired)
    default_copy = copy.deepcopy(default)

    # Call func0 to verify input validity
    try:
        expected = _expand_iterable(original_copy, num_desired_copy, default_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "original": original_copy if not isinstance(original_copy, Iterable) or isinstance(original_copy, str) else list(original_copy),
            "num_desired": num_desired_copy,
            "default": default_copy
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