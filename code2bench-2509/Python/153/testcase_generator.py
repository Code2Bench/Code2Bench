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
def sanitize_streamed_message_content(text: str) -> str:
    """Remove trailing JSON delimiters that can leak into assistant text.

    Specifically handles cases where a message string is immediately followed
    by a JSON delimiter in the stream (e.g., '"', '",', '"}', '" ]').
    Internal commas inside the message are preserved.
    """
    if not text:
        return text
    t = text.rstrip()
    # strip trailing quote + delimiter
    if len(t) >= 2 and t[-2] == '"' and t[-1] in ",}]":
        return t[:-2]
    # strip lone trailing quote
    if t.endswith('"'):
        return t[:-1]
    return t

# Strategy for generating text with potential JSON delimiters
def text_with_delimiters():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1).map(lambda x: x + '"'),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1).map(lambda x: x + '",'),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1).map(lambda x: x + '"}'),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1).map(lambda x: x + '" ]'),
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_with_delimiters())
@example(text="")
@example(text='"')
@example(text='",')
@example(text='"}')
@example(text='" ]')
@example(text='Hello, world!')
@example(text='Hello, world!"')
@example(text='Hello, world!",')
@example(text='Hello, world!"}')
@example(text='Hello, world!" ]')
def test_sanitize_streamed_message_content(text: str):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = sanitize_streamed_message_content(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if text.endswith(('"', '",', '"}', '" ]')) or not text:
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