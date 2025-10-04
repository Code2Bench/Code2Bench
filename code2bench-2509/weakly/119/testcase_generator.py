from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import statistics
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
def _timeseries_stats(ts):
    """Calculate and format summary statistics for a time series.

    Args:
        ts (list): List of numeric values representing a time series

    Returns:
        str: Markdown formatted string containing summary statistics
    """
    if len(ts) == 0:
        return "No data points"

    count = len(ts)
    max_val = max(ts)
    min_val = min(ts)
    mean_val = sum(ts) / count if count > 0 else float("nan")
    median_val = statistics.median(ts)

    markdown_summary = f"""
Time Series Statistics
- Number of Data Points: {count}
- Maximum Value: {max_val}
- Minimum Value: {min_val}
- Mean Value: {mean_val:.2f}
- Median Value: {median_val}
"""
    return markdown_summary

# Strategy for generating time series
def ts_strategy():
    return st.lists(
        st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
        min_size=0, max_size=100
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(ts=ts_strategy())
@example(ts=[])
@example(ts=[0.0])
@example(ts=[1.0, 2.0, 3.0])
@example(ts=[-1.0, 0.0, 1.0])
@example(ts=[1.0, 1.0, 1.0])
@example(ts=[1.0, 2.0, 3.0, 4.0, 5.0])
def test_timeseries_stats(ts):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    ts_copy = copy.deepcopy(ts)

    # Call func0 to verify input validity
    try:
        expected = _timeseries_stats(ts_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "ts": ts_copy
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