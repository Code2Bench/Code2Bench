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
def epoch_ms_to_utc_iso(ms: int) -> str:
    """Convert milliseconds since epoch to an ISO 8601 timestamp string."""
    iso_string = datetime.fromtimestamp(ms / 1000.0, tz=datetime.timezone.utc).isoformat()
    if iso_string.endswith('Z'):
        iso_string = iso_string[:-1] + '+00:00'
    return iso_string

# Strategy for generating milliseconds since epoch
def ms_strategy():
    return st.integers(min_value=0, max_value=253402300799999)  # Max value for datetime.fromtimestamp()

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(ms=ms_strategy())
@example(ms=0)
@example(ms=1609459200000)  # 2021-01-01T00:00:00Z
@example(ms=253402300799999)  # 9999-12-31T23:59:59Z
def test_epoch_ms_to_utc_iso(ms: int):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    ms_copy = copy.deepcopy(ms)

    # Call func0 to verify input validity
    try:
        expected = epoch_ms_to_utc_iso(ms_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "ms": ms_copy
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