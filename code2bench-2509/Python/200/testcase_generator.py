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
def _calculate_temporal_balance(recent: int, evergreen: int) -> str:
    total = recent + evergreen
    if total == 0:
        return 'unknown'

    recent_ratio = recent / total
    if recent_ratio > 0.7:
        return 'recent_heavy'
    elif recent_ratio < 0.3:
        return 'evergreen_heavy'
    else:
        return 'balanced'

# Strategy for generating integers
int_strategy = st.integers(min_value=-2147483648, max_value=2147483647)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(recent=int_strategy, evergreen=int_strategy)
@example(recent=0, evergreen=0)
@example(recent=8, evergreen=2)
@example(recent=2, evergreen=8)
@example(recent=5, evergreen=5)
@example(recent=100, evergreen=0)
@example(recent=0, evergreen=100)
def test_calculate_temporal_balance(recent, evergreen):
    global stop_collecting
    if stop_collecting:
        return
    
    recent_copy = copy.deepcopy(recent)
    evergreen_copy = copy.deepcopy(evergreen)
    try:
        expected = _calculate_temporal_balance(recent_copy, evergreen_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if recent + evergreen == 0 or recent / (recent + evergreen) > 0.7 or recent / (recent + evergreen) < 0.3 or 0.3 <= recent / (recent + evergreen) <= 0.7:
        generated_cases.append({
            "Inputs": {"recent": recent, "evergreen": evergreen},
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