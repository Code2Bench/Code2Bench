from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import unicodedata
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
def find_special_unicode(s):
    special_chars = {}
    for char in s:
        if ord(char) > 127:  # Non-ASCII characters
            unicode_name = unicodedata.category(char)
            special_chars[char] = f'U+{ord(char):04X} ({unicode_name})'
    return special_chars

# Strategy for generating strings with special Unicode characters
def special_unicode_strategy():
    # Generate non-ASCII characters
    non_ascii_chars = st.characters(min_codepoint=128, max_codepoint=0x10FFFF)
    
    # Generate strings with a mix of ASCII and non-ASCII characters
    return st.lists(
        st.one_of(
            st.characters(max_codepoint=127),  # ASCII characters
            non_ascii_chars
        ),
        min_size=0, max_size=20
    ).map(lambda x: ''.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(s=special_unicode_strategy())
@example(s="")
@example(s="Hello, world!")
@example(s="こんにちは")
@example(s="Привет")
@example(s="😊🌟")
@example(s="a😊b🌟c")
def test_find_special_unicode(s: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    s_copy = copy.deepcopy(s)

    # Call func0 to verify input validity
    try:
        expected = find_special_unicode(s_copy)
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