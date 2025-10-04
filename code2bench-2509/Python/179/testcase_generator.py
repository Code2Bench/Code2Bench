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
def seconds_to_time_string(seconds: int):
    """
    Converts seconds to a time string. e.g. 1 hour 2 minutes, 1 hour 2 seconds, 1 hour, 1 minute 2 seconds, etc.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        if minutes > 0:
            return f"{hours} hr{'s' if hours > 1 else ''}, {minutes} min{'s' if minutes > 1 else ''}"

        return f"{hours} hr{'s' if hours > 1 else ''}"

    if minutes > 0:
        return f"{minutes} min{'s' if minutes > 1 else ''}"

    return f"{remaining_seconds} sec"

# Strategy for generating seconds
seconds_strategy = st.integers(min_value=0, max_value=86400)  # 0 to 24 hours

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(seconds=seconds_strategy)
@example(seconds=0)
@example(seconds=1)
@example(seconds=60)
@example(seconds=3600)
@example(seconds=3660)
@example(seconds=3661)
@example(seconds=7200)
@example(seconds=7260)
@example(seconds=7261)
def test_seconds_to_time_string(seconds: int):
    global stop_collecting
    if stop_collecting:
        return

    try:
        expected = seconds_to_time_string(seconds)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {"seconds": seconds},
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