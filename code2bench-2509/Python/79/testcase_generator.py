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
def find_matching_parenthesis(expression, opening_index):
    if expression[opening_index] != "(":
        raise ValueError("The character at the provided index is not '('.")

    stack = 0

    for index in range(opening_index + 1, len(expression)):
        char = expression[index]
        if char == "(":
            stack += 1
        elif char == ")":
            if stack == 0:
                return index
            stack -= 1

    raise ValueError("No matching ')' found for '(' at index {}.".format(opening_index))

# Strategy for generating expressions with balanced parentheses
def expression_strategy():
    return st.recursive(
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
        lambda children: st.tuples(
            st.just("("),
            children,
            st.just(")")
        ).map(lambda x: "".join(x)),
        max_leaves=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    expression=expression_strategy(),
    opening_index=st.integers(min_value=0)
)
@example(expression="(a)", opening_index=0)
@example(expression="((a))", opening_index=0)
@example(expression="((a))", opening_index=1)
@example(expression="(a(b)c)", opening_index=0)
@example(expression="(a(b)c)", opening_index=3)
@example(expression="(a(b)c)", opening_index=5)
def test_find_matching_parenthesis(expression, opening_index):
    global stop_collecting
    if stop_collecting:
        return
    
    if opening_index >= len(expression):
        return  # Skip invalid indices
    
    expression_copy = copy.deepcopy(expression)
    try:
        expected = find_matching_parenthesis(expression_copy, opening_index)
    except ValueError:
        return  # Skip inputs that cause exceptions
    
    if expression[opening_index] == "(":
        generated_cases.append({
            "Inputs": {"expression": expression, "opening_index": opening_index},
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