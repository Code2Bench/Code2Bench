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
def human_count(n: int) -> str:
    if n < 0:
        return str(n)
    if n < 1_000:
        return str(n)
    for label, scale in (("T", 1_000_000_000_000),
                         ("B", 1_000_000_000),
                         ("M", 1_000_000),
                         ("K", 1_000)):
        if n >= scale:
            return f"{n/scale:.2f}{label}"

    return str(n)

# Strategy for generating integers
def integer_strategy():
    return st.one_of([
        st.integers(min_value=-2147483648, max_value=2147483647),
        st.integers(min_value=1_000, max_value=1_000_000_000_000),
        st.integers(min_value=1_000_000, max_value=1_000_000_000),
        st.integers(min_value=1_000_000_000, max_value=1_000_000_000_000),
        st.integers(min_value=1_000_000_000_000, max_value=10_000_000_000_000)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(n=integer_strategy())
@example(n=-1)
@example(n=0)
@example(n=999)
@example(n=1_000)
@example(n=1_000_000)
@example(n=1_000_000_000)
@example(n=1_000_000_000_000)
@example(n=10_000_000_000_000)
def test_human_count(n: int):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = human_count(n)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if n < 0 or n < 1_000 or n >= 1_000_000_000_000 or any(
        n >= scale for scale in (1_000, 1_000_000, 1_000_000_000, 1_000_000_000_000)
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