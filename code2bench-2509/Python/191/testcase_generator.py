from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _recommend_timing_profile(confidence: float) -> str:
    if confidence >= 0.8:
        return "stealth"
    elif confidence >= 0.5:
        return "conservative"
    elif confidence >= 0.2:
        return "normal"
    else:
        return "aggressive"

# Strategy for generating confidence values
confidence_strategy = st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(confidence=confidence_strategy)
@example(confidence=0.8)
@example(confidence=0.5)
@example(confidence=0.2)
@example(confidence=0.0)
@example(confidence=1.0)
def test_recommend_timing_profile(confidence: float):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = _recommend_timing_profile(confidence)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"confidence": confidence},
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