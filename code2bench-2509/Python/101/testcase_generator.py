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
def _round_up_to_multiple_of_128_within_limit(x: int, limit: int) -> int:
    assert limit >= 128 and limit % 128 == 0
    if x <= 128:
        return 128
    if x < limit:
        return (x + 127) // 128 * 128
    for candidate in range(limit, 511, -128):
        if x % candidate == 0:
            return candidate
    return limit

# Strategy for generating valid limits
def limit_strategy():
    return st.integers(min_value=128, max_value=1024).filter(lambda x: x % 128 == 0)

# Strategy for generating x values
def x_strategy(limit):
    return st.one_of([
        st.integers(min_value=-2147483648, max_value=128),  # x <= 128
        st.integers(min_value=129, max_value=limit - 1),   # x < limit
        st.integers(min_value=limit, max_value=2147483647) # x >= limit
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(limit=limit_strategy(), x=st.integers(min_value=-2147483648, max_value=2147483647))
@example(x=128, limit=128)
@example(x=129, limit=256)
@example(x=256, limit=256)
@example(x=512, limit=512)
@example(x=1024, limit=1024)
@example(x=1025, limit=1024)
@example(x=100, limit=256)
@example(x=200, limit=256)
@example(x=300, limit=256)
@example(x=400, limit=256)
def test_round_up_to_multiple_of_128_within_limit(x, limit):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = _round_up_to_multiple_of_128_within_limit(x, limit)
    except AssertionError:
        return  # Skip invalid limits
    
    generated_cases.append({
        "Inputs": {"x": x, "limit": limit},
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