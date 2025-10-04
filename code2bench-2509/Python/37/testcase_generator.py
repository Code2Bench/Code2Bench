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
def check_valid(s: str):
    cnt = 0
    for ch in s:
        if ch == "(":
            cnt += 1
        elif ch == ")":
            cnt -= 1
        else:
            return False
        if cnt < 0:
            return False
    return cnt == 0

# Strategy for generating valid and invalid parentheses strings
def parentheses_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('Ps', 'Pe')), min_size=0, max_size=20),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(s=parentheses_strategy())
@example(s="")
@example(s="()")
@example(s="(())")
@example(s="()()")
@example(s="(()))")
@example(s="((())")
@example(s="(a)")
@example(s="(1)")
def test_check_valid(s: str):
    global stop_collecting
    if stop_collecting:
        return
    
    s_copy = copy.deepcopy(s)
    try:
        expected = check_valid(s_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(ch not in "()" for ch in s) or s.count("(") != s.count(")") or "()" in s or s == "":
        generated_cases.append({
            "Inputs": {"s": s},
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