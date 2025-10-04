from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import ast
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
def safe_literal_eval(s):
    s = s.strip()
    try:
        return ast.literal_eval(s)
    except:
        pass
    if not s.startswith("{"):
        s = "{" + s
    if not s.endswith("}"):
        s = s + "}"
    s = re.sub(r'([{,]\s*)([^"\{\}\:\,\s]+)\s*:', r'\1"\2":', s)
    try:
        return ast.literal_eval(s)
    except:
        return None

# Strategy for generating strings that could be evaluated
def string_strategy():
    # Generate valid Python literals
    valid_literals = st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.booleans(),
        st.lists(st.text(min_size=1, max_size=10), min_size=0, max_size=5),
        st.dictionaries(st.text(min_size=1, max_size=10), st.text(min_size=1, max_size=10), min_size=0, max_size=5)
    ).map(lambda x: str(x))
    
    # Generate invalid strings that might be fixed by the function
    invalid_strings = st.text(min_size=1, max_size=50).filter(lambda x: not x.strip().startswith("{"))
    
    # Mix valid and invalid strings
    return st.one_of(valid_literals, invalid_strings)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(s=string_strategy())
@example(s="")
@example(s="123")
@example(s="{'a': 1}")
@example(s="a: 1")
@example(s="[1, 2, 3]")
@example(s="invalid string")
def test_safe_literal_eval(s: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    s_copy = copy.deepcopy(s)

    # Call func0 to verify input validity
    try:
        expected = safe_literal_eval(s_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "s": s_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)