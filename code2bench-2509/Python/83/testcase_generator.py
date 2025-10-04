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
def is_properly_closed(text):
    quote_count = 0
    bracket_stack = []
    i = 0
    while i < len(text):
        char = text[i]
        if char == "'":
            if i > 0 and text[i - 1] == "\\":
                i += 1
                continue
            quote_count += 1
        elif char == "[":
            bracket_stack.append("[")
        elif char == "]":
            if not bracket_stack or bracket_stack[-1] != "[":
                return False
            bracket_stack.pop()
        i += 1
    return quote_count % 2 == 0 and len(bracket_stack) == 0

# Strategy for generating text with quotes and brackets
def text_strategy():
    return st.text(
        st.characters(
            whitelist_categories=('L', 'N', 'P', 'S', 'Z'),
            whitelist_characters=["'", "[", "]"]
        ),
        min_size=0,
        max_size=50
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="'")
@example(text="''")
@example(text="'\\'")
@example(text="[]")
@example(text="[[]]")
@example(text="[']")
@example(text="['']")
@example(text="[['']]")
@example(text="[[']']")
@example(text="[['\\']']")
@example(text="[['\\'']]")
@example(text="[['\\'\\']]")
@example(text="[['\\'\\'']]")
@example(text="[['\\'\\'\\']]")
@example(text="[['\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\']]")
@example(text="[['\\'\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\'\\']]")
@example(text="[['\\'\\'\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\'\\'\\']]")
@example(text="[['\\'\\'\\'\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'\\']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'\\'\\']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'\\']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'\\']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'']]")
@example(text="[['\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'\\'\\']]")
def test_is_properly_closed(text):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = is_properly_closed(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
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