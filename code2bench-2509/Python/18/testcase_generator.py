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
def merge_short_sentences_zh(sens):
    sens_out = []
    for s in sens:
        if len(sens_out) > 0 and len(sens_out[-1]) <= 2:
            sens_out[-1] = sens_out[-1] + " " + s
        else:
            sens_out.append(s)
    try:
        if len(sens_out[-1]) <= 2:
            sens_out[-2] = sens_out[-2] + " " + sens_out[-1]
            sens_out.pop(-1)
    except:
        pass
    return sens_out

# Strategy for generating Chinese sentences
def sentence_strategy():
    return st.text(
        st.characters(whitelist_categories=('Lo', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(sens=st.lists(sentence_strategy(), min_size=1, max_size=10))
@example(sens=["a", "b", "c"])
@example(sens=["a", "bb", "c"])
@example(sens=["a", "b", "cc"])
@example(sens=["a", "bb", "cc"])
@example(sens=["a"])
@example(sens=["a", "b"])
@example(sens=["a", "bb"])
def test_merge_short_sentences_zh(sens):
    global stop_collecting
    if stop_collecting:
        return
    
    sens_copy = copy.deepcopy(sens)
    try:
        expected = merge_short_sentences_zh(sens_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(len(s) <= 2 for s in sens):
        generated_cases.append({
            "Inputs": {"sens": sens},
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