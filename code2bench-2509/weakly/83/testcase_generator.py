from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from datetime import datetime

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def calculate_task_duration(start_time: str, end_time: str) -> str:
    """Calculate the duration between two times in HH:MM format"""
    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
        duration = end - start
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        return f"{hours} hours and {minutes} minutes"
    except ValueError:
        return "Invalid time format. Please use HH:MM format."

# Strategies for generating inputs
def time_strategy():
    return st.tuples(
        st.integers(min_value=0, max_value=23),
        st.integers(min_value=0, max_value=59)
    ).map(lambda t: f"{t[0]:02d}:{t[1]:02d}")

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    start_time=time_strategy(),
    end_time=time_strategy()
)
@example(start_time="00:00", end_time="00:00")
@example(start_time="12:00", end_time="12:00")
@example(start_time="23:59", end_time="00:00")
@example(start_time="00:00", end_time="23:59")
@example(start_time="12:34", end_time="13:35")
@example(start_time="invalid", end_time="12:34")
@example(start_time="12:34", end_time="invalid")
@example(start_time="invalid", end_time="invalid")
def test_calculate_task_duration(start_time: str, end_time: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    start_time_copy = copy.deepcopy(start_time)
    end_time_copy = copy.deepcopy(end_time)

    # Call func0 to verify input validity
    try:
        expected = calculate_task_duration(start_time_copy, end_time_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "start_time": start_time_copy,
            "end_time": end_time_copy
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