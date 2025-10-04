from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from datetime import datetime
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
def format_create_date(timestamp: float) -> str:
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OSError):
        return "未知时间"

# Strategy for generating timestamps
def timestamp_strategy():
    return st.floats(
        min_value=-62167219200,  # Minimum valid timestamp (0001-01-01)
        max_value=253402300799,  # Maximum valid timestamp (9999-12-31)
        allow_nan=False,
        allow_infinity=False
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(timestamp=timestamp_strategy())
@example(timestamp=0.0)  # Unix epoch
@example(timestamp=1609459200.0)  # 2021-01-01 00:00:00
@example(timestamp=-2208988800.0)  # 1900-01-01 00:00:00
@example(timestamp=253402300799.0)  # 9999-12-31 23:59:59
@example(timestamp=-62167219200.0)  # 0001-01-01 00:00:00
def test_format_create_date(timestamp: float):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    timestamp_copy = copy.deepcopy(timestamp)

    # Call func0 to verify input validity
    try:
        expected = format_create_date(timestamp_copy)
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