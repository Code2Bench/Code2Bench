from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def pretty_format_ns(value: int) -> str:
    """Pretty formats a time value in nanoseconds to human readable value."""
    if value < 1000:
        return f"{value}ns"
    elif value < 1000_000:
        return f"{value/1000:.2f}us"
    elif value < 1_000_000_000:
        return f"{value/1000_000:.2f}ms"
    else:
        return f"{value/1000_000_000:.2f}s"

# Strategy for generating nanoseconds values
def ns_value_strategy():
    return st.one_of([
        st.integers(min_value=0, max_value=999),  # ns range
        st.integers(min_value=1000, max_value=999_999),  # us range
        st.integers(min_value=1_000_000, max_value=999_999_999),  # ms range
        st.integers(min_value=1_000_000_000, max_value=2_147_483_647)  # s range
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(value=ns_value_strategy())
@example(value=0)
@example(value=999)
@example(value=1000)
@example(value=999_999)
@example(value=1_000_000)
@example(value=999_999_999)
@example(value=1_000_000_000)
def test_pretty_format_ns(value: int):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = pretty_format_ns(value)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"value": value},
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