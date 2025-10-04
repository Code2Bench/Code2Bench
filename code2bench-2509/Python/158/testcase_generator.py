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
def similarity_score(s1: str, s2: str) -> float:
    """Fast similarity score based on common prefix and suffix.
    Returns lower score for more similar strings."""
    # Find common prefix length
    prefix_len = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            break
        prefix_len += 1

    # Find common suffix length if strings differ in middle
    if prefix_len < min(len(s1), len(s2)):
        s1_rev = s1[::-1]
        s2_rev = s2[::-1]
        suffix_len = 0
        for c1, c2 in zip(s1_rev, s2_rev):
            if c1 != c2:
                break
            suffix_len += 1
    else:
        suffix_len = 0

    # Return inverse similarity - shorter common affix means higher score
    return len(s1) + len(s2) - 2.0 * (prefix_len + suffix_len)

# Strategy for generating strings
def string_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(s1=string_strategy(), s2=string_strategy())
@example(s1="", s2="")
@example(s1="abc", s2="abc")
@example(s1="abc", s2="def")
@example(s1="abc", s2="abcd")
@example(s1="abc", s2="abx")
@example(s1="abc", s2="xbc")
@example(s1="abc", s2="ab")
@example(s1="abc", s2="bc")
def test_similarity_score(s1: str, s2: str):
    global stop_collecting
    if stop_collecting:
        return
    
    s1_copy = copy.deepcopy(s1)
    s2_copy = copy.deepcopy(s2)
    try:
        expected = similarity_score(s1_copy, s2_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to ensure meaningful test cases
    if s1 != s2 or s1 == "" or s2 == "":
        generated_cases.append({
            "Inputs": {"s1": s1, "s2": s2},
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