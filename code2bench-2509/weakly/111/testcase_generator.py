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
def iso8601_to_epoch_ms(iso8601_string: str) -> int:
    """
    Convert ISO 8601 string to epoch milliseconds (matches Java iso8601StringToEpochLong).

    Args:
        iso8601_string: ISO 8601 formatted datetime string

    Returns:
        Time as epoch milliseconds
    """
    dt = datetime.fromisoformat(iso8601_string.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)

# Strategy for generating ISO 8601 datetime strings
def iso8601_strategy():
    return st.datetimes(
        min_value=datetime(1970, 1, 1),  # Unix epoch start
        max_value=datetime(2100, 1, 1)   # Reasonable future limit
    ).map(lambda dt: dt.isoformat() + "Z")

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(iso8601_string=iso8601_strategy())
@example(iso8601_string="1970-01-01T00:00:00Z")  # Unix epoch start
@example(iso8601_string="2023-01-01T00:00:00Z")  # Recent date
@example(iso8601_string="2100-01-01T00:00:00Z")  # Future date
@example(iso8601_string="2000-02-29T00:00:00Z")  # Leap year
@example(iso8601_string="1999-12-31T23:59:59Z")  # End of millennium
def test_iso8601_to_epoch_ms(iso8601_string: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    iso8601_string_copy = copy.deepcopy(iso8601_string)

    # Call func0 to verify input validity
    try:
        expected = iso8601_to_epoch_ms(iso8601_string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "iso8601_string": iso8601_string_copy
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