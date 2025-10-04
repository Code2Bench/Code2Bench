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
def remove_consecutive_t(input_str):
    result = []
    count = 0

    for char in input_str:
        if char == "t":
            count += 1
        else:
            if count < 3:
                result.extend(["t"] * count)
            count = 0
            result.append(char)

    if count < 3:
        result.extend(["t"] * count)

    return "".join(result)

# Strategy for generating input strings
def input_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=0,
        max_size=50
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(input_str=input_strategy())
@example(input_str="")
@example(input_str="t")
@example(input_str="tt")
@example(input_str="ttt")
@example(input_str="tttt")
@example(input_str="atb")
@example(input_str="atttb")
@example(input_str="attttb")
@example(input_str="atttttb")
@example(input_str="attttttb")
def test_remove_consecutive_t(input_str):
    global stop_collecting
    if stop_collecting:
        return
    
    input_str_copy = copy.deepcopy(input_str)
    try:
        expected = remove_consecutive_t(input_str_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "t" in input_str or input_str == "":
        generated_cases.append({
            "Inputs": {"input_str": input_str},
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