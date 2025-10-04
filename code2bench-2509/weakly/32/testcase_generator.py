from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import string
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
def format_int_alpha(value: int) -> str:
    """Format a number as lowercase letters a-z, aa-zz, etc."""
    assert value > 0
    result: list[str] = []

    while value != 0:
        value, remainder = divmod(value - 1, len(string.ascii_lowercase))
        result.append(string.ascii_lowercase[remainder])

    result.reverse()
    return "".join(result)

# Strategy for generating valid integers
def value_strategy():
    return st.integers(min_value=1, max_value=10000)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(value=value_strategy())
@example(value=1)
@example(value=26)
@example(value=27)
@example(value=52)
@example(value=53)
@example(value=702)
@example(value=703)
def test_format_int_alpha(value: int):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    value_copy = copy.deepcopy(value)

    # Call func0 to verify input validity
    try:
        expected = format_int_alpha(value_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "value": value_copy
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