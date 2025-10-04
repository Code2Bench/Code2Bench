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
def _fix_a_slash_b(string):
    if len(string.split("/")) != 2:
        return string
    a = string.split("/")[0]
    b = string.split("/")[1]
    try:
        if "sqrt" not in a:
            a = int(a)
        if "sqrt" not in b:
            b = int(b)
        assert string == "{}/{}".format(a, b)
        new_string = "\\frac{" + str(a) + "}{" + str(b) + "}"
        return new_string
    except:
        return string

# Strategy for generating strings
def string_strategy():
    return st.one_of([
        # Strings with exactly one slash and integers on both sides
        st.tuples(
            st.integers(min_value=-2147483648, max_value=2147483647),
            st.integers(min_value=-2147483648, max_value=2147483647)
        ).map(lambda x: f"{x[0]}/{x[1]}"),
        # Strings with exactly one slash and "sqrt" on one or both sides
        st.tuples(
            st.one_of([
                st.just("sqrt"),
                st.integers(min_value=-2147483648, max_value=2147483647)
            ]),
            st.one_of([
                st.just("sqrt"),
                st.integers(min_value=-2147483648, max_value=2147483647)
            ])
        ).map(lambda x: f"{x[0]}/{x[1]}"),
        # Strings with more than one slash
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1).filter(lambda x: x.count("/") > 1),
        # Strings with no slash
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1).filter(lambda x: "/" not in x)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(string=string_strategy())
@example(string="1/2")
@example(string="sqrt/2")
@example(string="1/sqrt")
@example(string="sqrt/sqrt")
@example(string="1/2/3")
@example(string="no_slash")
def test_fix_a_slash_b(string):
    global stop_collecting
    if stop_collecting:
        return
    
    string_copy = copy.deepcopy(string)
    try:
        expected = _fix_a_slash_b(string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"string": string},
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