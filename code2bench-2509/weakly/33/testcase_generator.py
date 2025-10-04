from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from re import match  # Corrected import
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
def validate_cses_time(time: str) -> str:
    regex = r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d)"
    if match(regex, time):
        return time
    raise ValueError({"need": repr(regex), "got": time})

# Strategy for generating valid and invalid time strings
def time_strategy():
    valid_time = st.from_regex(r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d)", fullmatch=True)
    invalid_time = st.text(min_size=1, max_size=10).filter(
        lambda x: not match(r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d)", x)
    )
    return st.one_of(valid_time, invalid_time)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(time=time_strategy())
@example(time="00:00:00")
@example(time="23:59:59")
@example(time="12:34:56")
@example(time="24:00:00")
@example(time="12:60:00")
@example(time="12:00:60")
@example(time="invalid")
def test_validate_cses_time(time: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    time_copy = copy.deepcopy(time)

    # Call func0 to verify input validity
    try:
        expected = validate_cses_time(time_copy)
    except ValueError:
        pass  # Expected for invalid inputs

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "time": time_copy
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