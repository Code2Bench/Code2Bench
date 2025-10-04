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
def compare_numerical_ans(ans_p, ans_l):
    if ans_p is None:
        return False
    ans_p = ans_p.replace(",", "").replace("$", "")
    ans_l = ans_l.replace(",", "").replace("$", "")
    try:
        if ans_p.endswith("%"):
            ans_p = float(ans_p.rstrip("%")) / 100
        if isinstance(ans_p, str):
            ans_p = float(ans_p)
        if isinstance(ans_l, str):
            ans_l = float(ans_l)
    except Exception as e:
        return False
    return abs(ans_p - float(ans_l)) < 1e-3

# Strategy for generating numerical strings
def numerical_string_strategy():
    return st.one_of([
        st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6).map(lambda x: f"{x:.3f}"),
        st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6).map(lambda x: f"${x:,.2f}"),
        st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6).map(lambda x: f"{x:.2f}%"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(ans_p=numerical_string_strategy(), ans_l=numerical_string_strategy())
@example(ans_p="100", ans_l="100")
@example(ans_p="100.001", ans_l="100")
@example(ans_p="$100", ans_l="100")
@example(ans_p="100%", ans_l="1")
@example(ans_p="1,000", ans_l="1000")
@example(ans_p="invalid", ans_l="100")
@example(ans_p=None, ans_l="100")
def test_compare_numerical_ans(ans_p, ans_l):
    global stop_collecting
    if stop_collecting:
        return
    
    ans_p_copy = copy.deepcopy(ans_p)
    ans_l_copy = copy.deepcopy(ans_l)
    try:
        expected = compare_numerical_ans(ans_p_copy, ans_l_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"ans_p": ans_p, "ans_l": ans_l},
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