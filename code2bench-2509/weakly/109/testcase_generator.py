from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from datetime import datetime
import json
import os
import atexit
import copy
from typing import Optional

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def format_timestamp(timestamp: Optional[int]) -> Optional[str]:
    """Format Unix timestamp to ISO format string."""
    if timestamp is None:
        return None

    try:
        return datetime.fromtimestamp(timestamp / 1000).isoformat()
    except Exception as e:
        return str(f'Error: {e}, Timestamp: {timestamp}')  # Return as string if conversion fails

# Strategy for generating timestamps
def timestamp_strategy():
    return st.one_of(
        st.none(),
        st.integers(min_value=0, max_value=253402300799999),  # Max timestamp for datetime
        st.integers(min_value=-1000000000, max_value=-1),  # Negative timestamps
        st.integers(min_value=253402300800000, max_value=253402300800000 + 1000000000000)  # Timestamps beyond datetime limit
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(timestamp=timestamp_strategy())
@example(timestamp=None)
@example(timestamp=0)
@example(timestamp=1609459200000)  # 2021-01-01 00:00:00
@example(timestamp=-62167219200000)  # 0001-01-01 00:00:00
@example(timestamp=253402300799999)  # 9999-12-31 23:59:59
@example(timestamp=253402300800000)  # Beyond datetime limit
def test_format_timestamp(timestamp: Optional[int]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    timestamp_copy = copy.deepcopy(timestamp)

    # Call func0 to verify input validity
    try:
        expected = format_timestamp(timestamp_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "timestamp": timestamp_copy
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