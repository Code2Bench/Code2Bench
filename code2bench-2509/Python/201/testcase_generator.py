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
def _get_quality_grade(quality_score: float) -> str:
    """Get quality grade from score."""
    if quality_score >= 0.9:
        return 'A'
    elif quality_score >= 0.8:
        return 'B'
    elif quality_score >= 0.7:
        return 'C'
    elif quality_score >= 0.6:
        return 'D'
    else:
        return 'F'

# Strategy for generating quality scores
quality_score_strategy = st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(quality_score=quality_score_strategy)
@example(quality_score=0.9)
@example(quality_score=0.8)
@example(quality_score=0.7)
@example(quality_score=0.6)
@example(quality_score=0.5)
def test_get_quality_grade(quality_score: float):
    global stop_collecting
    if stop_collecting:
        return
    
    expected = _get_quality_grade(quality_score)
    
    generated_cases.append({
        "Inputs": {"quality_score": quality_score},
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