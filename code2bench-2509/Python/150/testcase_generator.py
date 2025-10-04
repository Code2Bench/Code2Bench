from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
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
def format_mins_timer(mins):
    ''' mins --> 4.5 days/min/hrs '''

    try:
        if mins == 0:
            return '0 min'

        if mins >= 86400:
            time_str = f"{mins/1440:.2f} days"
        elif mins < 60:
            time_str = f"{mins:.1f} min"
        elif mins == 60:
            time_str = "1 hr"
        else:
            time_str = f"{mins/60:.1f} hrs"

        # change xx.0 min/hr --> xx min/hr
        time_str = time_str.replace('.0 ', ' ')

    except Exception as err:
        time_str = ''

    return time_str

# Strategy for generating minutes
mins_strategy = st.one_of([
    st.just(0),  # Edge case: 0 minutes
    st.just(60),  # Edge case: exactly 1 hour
    st.integers(min_value=1, max_value=59),  # Minutes less than 1 hour
    st.integers(min_value=61, max_value=86399),  # Minutes between 1 hour and 1 day
    st.integers(min_value=86400, max_value=1000000)  # Minutes greater than or equal to 1 day
])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(mins=mins_strategy)
@example(mins=0)
@example(mins=60)
@example(mins=30)
@example(mins=120)
@example(mins=86400)
def test_format_mins_timer(mins):
    global stop_collecting
    if stop_collecting:
        return
    
    mins_copy = copy.deepcopy(mins)
    try:
        expected = format_mins_timer(mins_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if expected != '':
        generated_cases.append({
            "Inputs": {"mins": mins},
            "Expected": expected
        })
        if len(generated_cases) >= 500:
            stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)