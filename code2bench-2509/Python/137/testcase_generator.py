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
def _calculate_book_value_cagr(book_values: list) -> tuple[int, str]:
    """Helper function to safely calculate book value CAGR and return score + reasoning."""
    if len(book_values) < 2:
        return 0, "Insufficient data for CAGR calculation"

    oldest_bv, latest_bv = book_values[-1], book_values[0]
    years = len(book_values) - 1

    # Handle different scenarios
    if oldest_bv > 0 and latest_bv > 0:
        cagr = ((latest_bv / oldest_bv) ** (1 / years)) - 1
        if cagr > 0.15:
            return 2, f"Excellent book value CAGR: {cagr:.1%}"
        elif cagr > 0.1:
            return 1, f"Good book value CAGR: {cagr:.1%}"
        else:
            return 0, f"Book value CAGR: {cagr:.1%}"
    elif oldest_bv < 0 < latest_bv:
        return 3, "Excellent: Company improved from negative to positive book value"
    elif oldest_bv > 0 > latest_bv:
        return 0, "Warning: Company declined from positive to negative book value"
    else:
        return 0, "Unable to calculate meaningful book value CAGR due to negative values"

# Strategy for generating book values
def book_values_strategy():
    return st.lists(
        st.one_of([
            st.integers(min_value=-1000000, max_value=1000000),
            st.floats(min_value=-1000000.0, max_value=1000000.0, allow_nan=False, allow_infinity=False)
        ]),
        min_size=1, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(book_values=book_values_strategy())
@example(book_values=[100, 120])
@example(book_values=[100, 80])
@example(book_values=[-100, 120])
@example(book_values=[100, -120])
@example(book_values=[-100, -120])
@example(book_values=[100])
def test_calculate_book_value_cagr(book_values):
    global stop_collecting
    if stop_collecting:
        return
    
    book_values_copy = copy.deepcopy(book_values)
    try:
        expected = _calculate_book_value_cagr(book_values_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if len(book_values) >= 2 or any(
        (oldest_bv > 0 and latest_bv > 0) or
        (oldest_bv < 0 < latest_bv) or
        (oldest_bv > 0 > latest_bv) or
        (oldest_bv < 0 and latest_bv < 0)
        for oldest_bv, latest_bv in [(book_values[-1], book_values[0])]
    ):
        generated_cases.append({
            "Inputs": {"book_values": book_values},
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