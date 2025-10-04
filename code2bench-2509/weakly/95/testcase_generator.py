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
def calculate_stats(times: list[float]) -> dict[str, float]:
    """Calculate timing statistics."""
    if not times:
        return {"mean": 0, "median": 0, "std_dev": 0, "min": 0, "max": 0}

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
    }

# Strategy for generating times list
def times_strategy():
    return st.lists(
        st.floats(min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
        min_size=0, max_size=20
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(times=times_strategy())
@example(times=[])
@example(times=[1.0])
@example(times=[1.0, 2.0, 3.0, 4.0, 5.0])
@example(times=[0.0, 0.0, 0.0])
@example(times=[1000.0, 500.0, 250.0])
def test_calculate_stats(times: list[float]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    times_copy = copy.deepcopy(times)

    # Call func0 to verify input validity
    try:
        expected = calculate_stats(times_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "times": times_copy
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