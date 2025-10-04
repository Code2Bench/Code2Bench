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
def format_bytes_to_human_readable(bytes: int) -> str:
    if bytes > 1000 * 1000 * 1000 * 1000:
        return f"{bytes / (1000 * 1000 * 1000 * 1000):.2f} TB"
    if bytes > 1000 * 1000 * 1000:
        return f"{bytes / (1000 * 1000 * 1000):.2f} GB"
    elif bytes > 1000 * 1000:
        return f"{bytes / (1000 * 1000):.2f} MB"
    elif bytes > 1000:
        return f"{bytes / 1000:.2f} KB"
    else:
        return f"{bytes} B"

# Strategy for generating bytes
bytes_strategy = st.one_of([
    st.integers(min_value=0, max_value=999),
    st.integers(min_value=1000, max_value=999999),
    st.integers(min_value=1000000, max_value=999999999),
    st.integers(min_value=1000000000, max_value=999999999999),
    st.integers(min_value=1000000000000, max_value=1000000000000000)
])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(bytes=bytes_strategy)
@example(bytes=0)
@example(bytes=999)
@example(bytes=1000)
@example(bytes=999999)
@example(bytes=1000000)
@example(bytes=999999999)
@example(bytes=1000000000)
@example(bytes=999999999999)
@example(bytes=1000000000000)
def test_format_bytes_to_human_readable(bytes: int):
    global stop_collecting
    if stop_collecting:
        return
    
    bytes_copy = copy.deepcopy(bytes)
    try:
        expected = format_bytes_to_human_readable(bytes_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"bytes": bytes},
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