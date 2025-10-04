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
def format_size(bytes_size):
    """Format file size in human readable format."""
    if bytes_size == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

# Strategy for generating bytes_size
bytes_size_strategy = st.one_of([
    st.integers(min_value=0, max_value=1024),  # B range
    st.integers(min_value=1024, max_value=1024**2),  # KB range
    st.integers(min_value=1024**2, max_value=1024**3),  # MB range
    st.integers(min_value=1024**3, max_value=1024**4),  # GB range
    st.integers(min_value=1024**4, max_value=1024**5),  # TB range
    st.just(0),  # Edge case for 0 bytes
])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(bytes_size=bytes_size_strategy)
@example(bytes_size=0)
@example(bytes_size=1023)
@example(bytes_size=1024)
@example(bytes_size=1024**2 - 1)
@example(bytes_size=1024**2)
@example(bytes_size=1024**3 - 1)
@example(bytes_size=1024**3)
@example(bytes_size=1024**4 - 1)
@example(bytes_size=1024**4)
@example(bytes_size=1024**5 - 1)
@example(bytes_size=1024**5)
def test_format_size(bytes_size):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = format_size(bytes_size)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"bytes_size": bytes_size},
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