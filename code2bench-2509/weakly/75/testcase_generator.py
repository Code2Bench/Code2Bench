from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from dateutil import parser
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
def iso_to_millis(ts: str) -> int:
    """
    Convert ISO 8601 timestamp string to milliseconds since epoch.

    Args:
        ts: ISO 8601 timestamp string (handles Zulu/UTC (Z) automatically)

    Returns:
        Milliseconds since epoch as integer
    """
    dt = parser.isoparse(ts)  # handles Zulu/UTC (Z) automatically
    return int(dt.timestamp() * 1000)

# Strategy for generating ISO 8601 timestamp strings
def iso_timestamp_strategy():
    return st.datetimes(
        min_value=datetime(1970, 1, 1),  # Start from Unix epoch
        max_value=datetime(2100, 1, 1),  # Reasonable future limit
        timezones=st.just(None)  # Ensure no timezone offset
    ).map(lambda dt: dt.isoformat() + 'Z')

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(ts=iso_timestamp_strategy())
@example(ts="1970-01-01T00:00:00Z")  # Unix epoch
@example(ts="2023-01-01T00:00:00Z")  # Recent date
@example(ts="2100-01-01T00:00:00Z")  # Future date
@example(ts="2000-02-29T00:00:00Z")  # Leap year
def test_iso_to_millis(ts: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    ts_copy = copy.deepcopy(ts)

    # Call func0 to verify input validity
    try:
        expected = iso_to_millis(ts_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "ts": ts_copy
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