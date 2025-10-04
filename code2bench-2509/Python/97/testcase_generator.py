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
def parse_interval(interval):
    """
    Parse interval string or integer into seconds.

    Args:
        interval: Can be:
            - Integer: seconds (e.g., 3600)
            - String: number + unit (e.g., "1h", "30m", "7d")

    Returns:
        int: Total seconds

    Examples:
        parse_interval(3600) -> 3600
        parse_interval("1h") -> 3600
        parse_interval("30m") -> 1800
        parse_interval("7d") -> 604800
    """
    if interval is None:
        return None

    # If already an integer, return as-is (assuming seconds)
    if isinstance(interval, int):
        return interval

    # Parse string format
    interval = str(interval).strip().lower()

    # Extract number and unit
    if interval[-1].isdigit():
        # No unit specified, assume seconds
        return int(interval)

    unit = interval[-1]
    try:
        number = int(interval[:-1])
    except ValueError:
        raise ValueError(f"Invalid interval format: {interval}")

    # Convert to seconds
    multipliers = {
        "s": 1,  # seconds
        "m": 60,  # minutes
        "h": 3600,  # hours
        "d": 86400,  # days
        "w": 604800,  # weeks
        "y": 31536000,  # years
    }

    if unit not in multipliers:
        raise ValueError(f"Invalid time unit '{unit}'. Use: s, m, h, d, w, y")

    return number * multipliers[unit]

# Strategy for generating interval inputs
def interval_strategy():
    return st.one_of([
        st.integers(min_value=0, max_value=2147483647),  # Integer intervals
        st.tuples(
            st.integers(min_value=0, max_value=2147483647),
            st.sampled_from(["s", "m", "h", "d", "w", "y"])
        ).map(lambda x: f"{x[0]}{x[1]}"),  # String intervals with units
        st.just(None)  # None input
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(interval=interval_strategy())
@example(interval=3600)
@example(interval="1h")
@example(interval="30m")
@example(interval="7d")
@example(interval=None)
@example(interval="100")
@example(interval="1y")
@example(interval="2w")
def test_parse_interval(interval):
    global stop_collecting
    if stop_collecting:
        return

    interval_copy = copy.deepcopy(interval)
    try:
        expected = parse_interval(interval_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {"interval": interval},
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