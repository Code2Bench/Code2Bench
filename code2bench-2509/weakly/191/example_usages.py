from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from dateutil import parser
import pytz
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def validate_and_convert_date(date_input: str) -> str:
    try:
        dt_object = parser.parse(date_input)
        if dt_object.tzinfo is not None:
            dt_object = dt_object.astimezone(pytz.utc)
        else:
            local_tz = pytz.timezone("UTC")
            dt_object = local_tz.localize(dt_object)
        formatted_date = dt_object.isoformat().replace("+00:00", "Z")
        formatted_date = formatted_date.rstrip("Z") + "Z"
        return formatted_date
    except (ValueError, OverflowError) as e:
        raise ValueError(
            f"Invalid date format: {date_input}."
            f" Date format must adhere to the RFC 3339 standard (e.g., 'YYYY-MM-DDTHH:MM:SSZ' for UTC)."
        ) from e

# Strategy for generating date strings
def date_strategy():
    # Generate valid date strings in various formats
    date_formats = [
        "%Y-%m-%dT%H:%M:%SZ",  # RFC 3339 UTC
        "%Y-%m-%dT%H:%M:%S%z",  # RFC 3339 with timezone
        "%Y-%m-%d %H:%M:%S",    # Common format without timezone
        "%d/%m/%Y %H:%M:%S",    # European format
        "%m/%d/%Y %I:%M:%S %p", # US format with AM/PM
        "%Y%m%dT%H%M%S",        # Compact format
    ]
    return st.one_of(
        [st.datetimes().map(lambda dt: dt.strftime(fmt)) for fmt in date_formats]
    )

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(date_input=date_strategy())
@example(date_input="2023-10-01T12:34:56Z")
@example(date_input="2023-10-01T12:34:56+00:00")
@example(date_input="2023-10-01 12:34:56")
@example(date_input="01/10/2023 12:34:56")
@example(date_input="10/01/2023 12:34:56 PM")
@example(date_input="20231001T123456")
def test_validate_and_convert_date(date_input: str):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy input to avoid modification
    date_input_copy = copy.deepcopy(date_input)

    # Call func0 to verify input validity
    try:
        expected = validate_and_convert_date(date_input_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "RFC 3339 UTC format"
        elif case_count == 1:
            desc = "RFC 3339 with timezone"
        else:
            desc = "Common format without timezone"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "European format"
        elif case_count == 4:
            desc = "US format with AM/PM"
        elif case_count == 5:
            desc = "Compact format"
        elif case_count == 6:
            desc = "Invalid date format"
        else:
            desc = "Edge case with minimal input"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "date_input": date_input_copy
        },
        "Expected": expected,
        "Usage": None
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)