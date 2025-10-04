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
def _is_gap_high_quality(gap: str) -> bool:
    gap = gap.strip()

    # Length check
    if len(gap) < 10:
        return False

    # Generic gap check
    generic_gaps = ['general', 'overview', 'introduction', 'basics', 'fundamentals']
    if gap.lower() in generic_gaps:
        return False

    # Check for meaningful content
    if len(gap.split()) < 3:
        return False

    return True

# Strategy for generating gap strings
def gap_strategy():
    return st.one_of([
        # Short strings (length < 10)
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=9),
        # Generic gap strings
        st.sampled_from(['general', 'overview', 'introduction', 'basics', 'fundamentals']),
        # Strings with fewer than 3 words
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=10).filter(lambda x: len(x.split()) < 3),
        # Valid gap strings
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=10).filter(lambda x: len(x.split()) >= 3 and x.lower() not in ['general', 'overview', 'introduction', 'basics', 'fundamentals'])
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(gap=gap_strategy())
@example(gap="general")
@example(gap="overview")
@example(gap="introduction")
@example(gap="basics")
@example(gap="fundamentals")
@example(gap="short")
@example(gap="a b")
@example(gap="meaningful gap analysis")
def test_is_gap_high_quality(gap: str):
    global stop_collecting
    if stop_collecting:
        return
    
    gap_copy = copy.deepcopy(gap)
    try:
        expected = _is_gap_high_quality(gap_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"gap": gap},
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