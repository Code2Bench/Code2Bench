from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import statistics
import json
import os
import atexit
import copy
from typing import List

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def calculate_algotune_score(speedups: List[float]) -> float:
    if not speedups:
        return 0.0

    # Filter out None and invalid values
    valid_speedups = [s for s in speedups if s is not None and s > 0]

    if not valid_speedups:
        return 0.0

    return statistics.harmonic_mean(valid_speedups)

# Strategy for generating speedups
def speedups_strategy():
    return st.lists(
        st.one_of(
            st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
            st.none()
        ),
        min_size=0, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(speedups=speedups_strategy())
@example(speedups=[])
@example(speedups=[1.0, 2.0, 3.0])
@example(speedups=[0.5, None, 1.5])
@example(speedups=[0.0, 0.0, 0.0])
@example(speedups=[None, None, None])
@example(speedups=[10.0, 20.0, 30.0])
def test_calculate_algotune_score(speedups: List[float]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    speedups_copy = copy.deepcopy(speedups)

    # Call func0 to verify input validity
    try:
        expected = calculate_algotune_score(speedups_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "speedups": speedups_copy
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