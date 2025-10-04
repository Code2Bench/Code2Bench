from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List, Dict
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
def _get_confidence_distribution(confidences: List[float]) -> Dict[str, int]:
    """Get distribution of confidence scores."""
    distribution = {'high': 0, 'medium': 0, 'low': 0}

    for confidence in confidences:
        if confidence >= 0.8:
            distribution['high'] += 1
        elif confidence >= 0.6:
            distribution['medium'] += 1
        else:
            distribution['low'] += 1

    return distribution

# Strategy for generating confidence scores
confidence_strategy = st.lists(
    st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    min_size=0, max_size=20
)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(confidences=confidence_strategy)
@example(confidences=[])
@example(confidences=[0.8, 0.6, 0.5])
@example(confidences=[1.0, 0.9, 0.7, 0.4])
@example(confidences=[0.8, 0.8, 0.8])
@example(confidences=[0.6, 0.6, 0.6])
@example(confidences=[0.5, 0.5, 0.5])
def test_get_confidence_distribution(confidences: List[float]):
    global stop_collecting
    if stop_collecting:
        return
    
    confidences_copy = copy.deepcopy(confidences)
    try:
        expected = _get_confidence_distribution(confidences_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to ensure meaningful test cases
    if any(confidence >= 0.8 for confidence in confidences) or \
       any(0.6 <= confidence < 0.8 for confidence in confidences) or \
       any(confidence < 0.6 for confidence in confidences):
        generated_cases.append({
            "Inputs": {"confidences": confidences},
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