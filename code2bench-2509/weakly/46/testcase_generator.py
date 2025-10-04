from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from datetime import date
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
def gregorian_date(jdn):
    f = jdn + 1401 + (4 * jdn + 274277) // 146097 * 3 // 4 - 38
    e = 4 * f + 3
    h = e % 1461 // 4
    h = 5 * h + 2
    d = (h % 153) // 5 + 1
    m = (h // 153 + 2) % 12 + 1
    y = e // 1461 - 4716 + (14 - m) // 12
    return date(y, m, d)

# Strategy for generating Julian Day Numbers (JDN)
def jdn_strategy():
    return st.integers(min_value=0, max_value=1000000)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(jdn=jdn_strategy())
@example(jdn=0)
@example(jdn=2451545)  # January 1, 2000
@example(jdn=2299160)  # October 15, 1582 (Gregorian calendar start)
@example(jdn=1721426)  # January 1, 1 (Gregorian calendar)
def test_gregorian_date(jdn: int):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    jdn_copy = copy.deepcopy(jdn)

    # Call func0 to verify input validity
    try:
        expected = gregorian_date(jdn_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "jdn": jdn_copy
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