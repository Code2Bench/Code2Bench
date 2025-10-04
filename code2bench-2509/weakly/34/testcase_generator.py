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
def remove_control_characters(text: str) -> str:
    """Remove control characters from text.
    Control characters are non-printable characters in the Unicode standard that control how text is displayed or processed.
    """
    return "".join(i for i in text if unicodedata.category(i)[0] != "C")

# Strategy for generating text with control characters
def text_strategy():
    # Generate a mix of printable and control characters
    printable_chars = st.characters(
        whitelist_categories=('L', 'N', 'P', 'S', 'Z'),
        min_codepoint=32,  # Start from space character
        max_codepoint=0x10FFFF  # Maximum Unicode code point
    )
    control_chars = st.characters(
        whitelist_categories=('C',),
        min_codepoint=0,  # Start from null character
        max_codepoint=0x10FFFF  # Maximum Unicode code point
    )
    return st.lists(
        st.one_of(printable_chars, control_chars),
        min_size=0, max_size=100
    ).map(lambda x: ''.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="Hello, World!")
@example(text="\x00\x01\x02\x03")  # Control characters
@example(text="Hello\x07World\x1B")  # Mixed printable and control characters
@example(text="\u2028\u2029")  # Unicode line and paragraph separators
def test_remove_control_characters(text: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        expected = remove_control_characters(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "text": text_copy
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