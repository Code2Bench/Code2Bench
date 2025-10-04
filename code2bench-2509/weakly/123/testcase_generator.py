from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from datetime import datetime, date
from typing import Dict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _is_annual_period(period: Dict) -> bool:
    try:
        start_date = datetime.strptime(period['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
        duration_days = (end_date - start_date).days
        return 300 < duration_days <= 400
    except (ValueError, TypeError, KeyError):
        return False

# Strategies for generating inputs
def date_strategy():
    return st.dates(min_value=date(1900, 1, 1), max_value=date(2100, 12, 31))

def period_strategy():
    return st.fixed_dictionaries({
        'start_date': date_strategy().map(lambda d: d.strftime('%Y-%m-%d')),
        'end_date': date_strategy().map(lambda d: d.strftime('%Y-%m-%d'))
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(period=period_strategy())
@example(period={'start_date': '2020-01-01', 'end_date': '2020-12-31'})  # Valid annual period
@example(period={'start_date': '2020-01-01', 'end_date': '2021-01-01'})  # Leap year
@example(period={'start_date': '2020-01-01', 'end_date': '2020-06-30'})  # Invalid (less than 300 days)
@example(period={'start_date': '2020-01-01', 'end_date': '2022-01-01'})  # Invalid (more than 400 days)
@example(period={'start_date': 'invalid', 'end_date': '2020-12-31'})  # Invalid date format
@example(period={'start_date': '2020-01-01', 'end_date': 'invalid'})  # Invalid date format
@example(period={'start_date': '2020-01-01'})  # Missing end_date
@example(period={'end_date': '2020-12-31'})  # Missing start_date
@example(period={})  # Empty dictionary
def test_is_annual_period(period: Dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    period_copy = copy.deepcopy(period)

    # Call func0 to verify input validity
    try:
        expected = _is_annual_period(period_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "period": period_copy
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