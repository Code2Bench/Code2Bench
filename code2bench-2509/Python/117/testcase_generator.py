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
def shquote(arg):
    """Quote an argument for later parsing by shlex.split()"""
    for c in '"', "'", "\\", "#":
        if c in arg:
            return repr(arg)
    if arg.split() != [arg]:
        return repr(arg)
    return arg

# Strategy for generating strings
def string_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=50
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(arg=string_strategy())
@example(arg="")
@example(arg="simple")
@example(arg="with spaces")
@example(arg="with\"quote")
@example(arg="with'quote")
@example(arg="with\\backslash")
@example(arg="with#hash")
@example(arg="with spaces and\"quote")
def test_shquote(arg):
    global stop_collecting
    if stop_collecting:
        return
    
    arg_copy = copy.deepcopy(arg)
    try:
        expected = shquote(arg_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(c in arg for c in '"\'\\#') or arg.split() != [arg]:
        generated_cases.append({
            "Inputs": {"arg": arg},
            "Expected": expected
        })
    else:
        generated_cases.append({
            "Inputs": {"arg": arg},
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