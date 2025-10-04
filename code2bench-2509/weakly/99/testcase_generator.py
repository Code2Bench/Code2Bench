from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
def get_first_last_day(year_month_str):
    try:
        date_obj = datetime.strptime(year_month_str, "%Y-%m")
        first_day = date_obj.date().replace(day=1)
        last_day = (date_obj + relativedelta(months=1, days=-1)).date()
        return first_day, last_day
    except ValueError:
        raise ValueError("Invalid date format. Please use '%Y-%m'.")

# Strategy for generating year-month strings
def year_month_strategy():
    return st.from_regex(r"\d{4}-(0[1-9]|1[0-2])")

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(year_month_str=year_month_strategy())
@example(year_month_str="2023-01")
@example(year_month_str="2020-02")  # Leap year
@example(year_month_str="1999-12")
@example(year_month_str="2100-12")  # Edge case
@example(year_month_str="1900-01")  # Edge case
def test_get_first_last_day(year_month_str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    year_month_str_copy = copy.deepcopy(year_month_str)

    # Call func0 to verify input validity
    try:
        expected = get_first_last_day(year_month_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "year_month_str": year_month_str_copy
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