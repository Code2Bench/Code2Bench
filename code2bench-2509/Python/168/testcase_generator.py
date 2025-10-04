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
def get_parenthetical_substrings(text: str) -> list[str]:
    """
    Finds the all nested parenthetical substrings.

    Args:
        text: The input string to analyze.

    Returns:
        A list of parenthetical substrings.
    """
    substrings = []
    open_paren_indices = []
    for i, char in enumerate(text):
        if char == "(":
            open_paren_indices.append(i)
        elif char == ")" and open_paren_indices:
            start_index = open_paren_indices.pop()
            substrings.append(text[start_index : i + 1])
    return substrings

# Strategy for generating text with nested parentheses
def text_with_parentheses_strategy():
    return st.recursive(
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
        lambda children: st.tuples(
            st.just("("),
            children,
            st.just(")")
        ).map(lambda x: "".join(x)),
        max_leaves=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_with_parentheses_strategy())
@example(text="")
@example(text="()")
@example(text="(())")
@example(text="(a(b)c)")
@example(text="(a)(b)")
@example(text="(a(b)c(d)e)")
@example(text="(a(b)c(d)e(f)g)")
def test_get_parenthetical_substrings(text: str):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = get_parenthetical_substrings(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "(" in text or ")" in text:
        generated_cases.append({
            "Inputs": {"text": text},
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