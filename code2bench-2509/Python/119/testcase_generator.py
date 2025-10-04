from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
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
def _human_bytes(n: float) -> str:
    if n <= 0:
        return "0B"

    for unit in ["B","KB","MB","GB","TB","PB"]:
        if n < 1024:
            return f"{n:.0f}{unit}" if unit == "B" else f"{n:.2f}{unit}"
        n /= 1024.0

    return f"{n:.2f}PB"

# Strategy for generating float values
def float_strategy():
    return st.one_of([
        st.floats(min_value=0, max_value=1024, allow_nan=False, allow_infinity=False),
        st.floats(min_value=1024, max_value=1024**2, allow_nan=False, allow_infinity=False),
        st.floats(min_value=1024**2, max_value=1024**3, allow_nan=False, allow_infinity=False),
        st.floats(min_value=1024**3, max_value=1024**4, allow_nan=False, allow_infinity=False),
        st.floats(min_value=1024**4, max_value=1024**5, allow_nan=False, allow_infinity=False),
        st.floats(min_value=1024**5, max_value=1024**6, allow_nan=False, allow_infinity=False),
        st.floats(min_value=-100, max_value=0, allow_nan=False, allow_infinity=False)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(n=float_strategy())
@example(n=0)
@example(n=1023)
@example(n=1024)
@example(n=1024**2 - 1)
@example(n=1024**2)
@example(n=1024**3)
@example(n=1024**4)
@example(n=1024**5)
@example(n=1024**6)
def test_human_bytes(n: float):
    global stop_collecting
    if stop_collecting:
        return
    
    n_copy = copy.deepcopy(n)
    try:
        expected = _human_bytes(n_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if n <= 0 or n >= 1024**6 or any(
        1024**i <= n < 1024**(i+1) for i in range(6)
    ):
        generated_cases.append({
            "Inputs": {"n": n},
            "Expected": expected
        })
        if len(generated_cases) >= 500:
            stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)