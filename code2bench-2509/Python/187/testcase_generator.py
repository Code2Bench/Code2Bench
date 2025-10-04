from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Optional

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def format_media_duration(total_minutes: Optional[int]) -> str:
    """
    Converts a duration in minutes into a more human-readable format
    (e.g., "1 hour 30 minutes", "45 minutes", "2 hours").

    Args:
        total_minutes: The total duration in minutes (integer).

    Returns:
        A string representing the formatted duration.
    """
    if not total_minutes:
        return "N/A"

    if not isinstance(total_minutes, int) or total_minutes < 0:
        raise ValueError("Input must be a non-negative integer representing minutes.")

    if total_minutes == 0:
        return "0 minutes"

    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []

    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")

    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    # Join the parts with " and " if both hours and minutes are present
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    elif len(parts) == 1:
        return parts[0]
    else:
        # This case should ideally not be reached if total_minutes > 0
        return "0 minutes"  # Fallback for safety, though handled by initial check

# Strategy for generating total_minutes
def total_minutes_strategy():
    return st.one_of([
        st.none(),
        st.integers(min_value=0, max_value=2147483647),
        st.integers(min_value=-2147483648, max_value=-1)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(total_minutes=total_minutes_strategy())
@example(total_minutes=None)
@example(total_minutes=0)
@example(total_minutes=30)
@example(total_minutes=60)
@example(total_minutes=90)
@example(total_minutes=120)
@example(total_minutes=-1)
def test_format_media_duration(total_minutes: Optional[int]):
    global stop_collecting
    if stop_collecting:
        return

    try:
        expected = format_media_duration(total_minutes)
    except ValueError:
        return  # Skip invalid inputs

    generated_cases.append({
        "Inputs": {"total_minutes": total_minutes},
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