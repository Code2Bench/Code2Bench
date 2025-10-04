from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from datetime import datetime
from typing import Dict, List

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def filter_periods_by_document_end_date(periods: List[Dict], document_period_end_date: str, period_type: str) -> List[Dict]:
    """Filter periods to only include those that end on or before the document period end date."""
    if not document_period_end_date:
        return periods

    try:
        doc_end_date = datetime.strptime(document_period_end_date, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        # If we can't parse the document end date, return all periods
        return periods

    filtered_periods = []
    for period in periods:
        try:
            if period_type == 'instant':
                period_date = datetime.strptime(period['date'], '%Y-%m-%d').date()
                if period_date <= doc_end_date:
                    filtered_periods.append(period)
            else:  # duration
                period_end_date = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
                if period_end_date <= doc_end_date:
                    filtered_periods.append(period)
        except (ValueError, TypeError):
            # If we can't parse the period date, include it to be safe
            filtered_periods.append(period)

    return filtered_periods

# Strategies for generating inputs
def date_strategy():
    return st.dates(min_value=datetime(1900, 1, 1).date(), max_value=datetime(2100, 12, 31).date()).map(lambda x: x.strftime('%Y-%m-%d'))

def period_strategy(period_type: str):
    if period_type == 'instant':
        return st.fixed_dictionaries({
            'date': date_strategy()
        })
    else:  # duration
        return st.fixed_dictionaries({
            'start_date': date_strategy(),
            'end_date': date_strategy()
        })

def periods_strategy(period_type: str):
    return st.lists(period_strategy(period_type), min_size=0, max_size=10)

def period_type_strategy():
    return st.sampled_from(['instant', 'duration'])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    periods=st.builds(
        lambda pt: periods_strategy(pt),
        period_type_strategy()
    ),
    document_period_end_date=st.one_of(
        date_strategy(),
        st.just(""),
        st.text(min_size=1, max_size=10)
    ),
    period_type=period_type_strategy()
)
@example(
    periods=[],
    document_period_end_date="2023-01-01",
    period_type='instant'
)
@example(
    periods=[{'date': '2023-01-01'}],
    document_period_end_date="2023-01-01",
    period_type='instant'
)
@example(
    periods=[{'start_date': '2023-01-01', 'end_date': '2023-01-31'}],
    document_period_end_date="2023-01-31",
    period_type='duration'
)
@example(
    periods=[{'date': 'invalid-date'}],
    document_period_end_date="2023-01-01",
    period_type='instant'
)
@example(
    periods=[{'start_date': 'invalid-date', 'end_date': '2023-01-31'}],
    document_period_end_date="2023-01-31",
    period_type='duration'
)
def test_filter_periods_by_document_end_date(periods: List[Dict], document_period_end_date: str, period_type: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    periods_copy = copy.deepcopy(periods)
    document_period_end_date_copy = copy.deepcopy(document_period_end_date)
    period_type_copy = copy.deepcopy(period_type)

    # Call func0 to verify input validity
    try:
        expected = filter_periods_by_document_end_date(periods_copy, document_period_end_date_copy, period_type_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "periods": periods_copy,
            "document_period_end_date": document_period_end_date_copy,
            "period_type": period_type_copy
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