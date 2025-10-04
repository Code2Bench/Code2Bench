from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
import functools
from functools import cache

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
@cache
def format_seconds(seconds: int) -> str:
    """Convert seconds to a more readable time."""
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    parts.append(f"{s}s")
    return " ".join(parts)

# Strategy for generating seconds
def seconds_strategy():
    return st.integers(min_value=0, max_value=86400)  # 0 to 24 hours in seconds

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(seconds=seconds_strategy())
@example(seconds=0)
@example(seconds=59)
@example(seconds=60)
@example(seconds=3599)
@example(seconds=3600)
@example(seconds=3661)
def test_format_seconds(seconds: int):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    seconds_copy = copy.deepcopy(seconds)

    # Call func0 to verify input validity
    try:
        expected = format_seconds(seconds_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "seconds": seconds_copy
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