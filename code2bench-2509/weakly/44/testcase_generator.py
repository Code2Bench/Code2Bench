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
def calculate_fcf_volatility(fcf_history: list[float]) -> float:
    """Calculate FCF volatility as coefficient of variation."""
    if len(fcf_history) < 3:
        return 0.5  # Default moderate volatility

    # Filter out zeros and negatives for volatility calc
    positive_fcf = [fcf for fcf in fcf_history if fcf > 0]
    if len(positive_fcf) < 2:
        return 0.8  # High volatility if mostly negative FCF

    try:
        mean_fcf = statistics.mean(positive_fcf)
        std_fcf = statistics.stdev(positive_fcf)
        return min(std_fcf / mean_fcf, 1.0) if mean_fcf > 0 else 0.8
    except:
        return 0.5

# Strategy for generating fcf_history
def fcf_history_strategy():
    return st.lists(
        st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False),
        min_size=0, max_size=20
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(fcf_history=fcf_history_strategy())
@example(fcf_history=[])
@example(fcf_history=[0.0, 0.0, 0.0])
@example(fcf_history=[1.0, 2.0, 3.0])
@example(fcf_history=[-1.0, -2.0, -3.0])
@example(fcf_history=[1.0, -1.0, 2.0, -2.0])
@example(fcf_history=[1.0, 0.0, 0.0])
def test_calculate_fcf_volatility(fcf_history: list[float]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    fcf_history_copy = copy.deepcopy(fcf_history)

    # Call func0 to verify input validity
    try:
        expected = calculate_fcf_volatility(fcf_history_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "fcf_history": fcf_history_copy
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