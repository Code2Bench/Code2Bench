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
def wrap_text_for_svg(text, max_width=80):
    """Simple text wrapping for SVG - split into lines that fit within max_width characters"""
    if len(text) <= max_width:
        return [text]

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_width:
            current_line = current_line + " " + word if current_line else word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

# Strategy for generating text
def text_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=1,
        max_size=200
    )

# Strategy for generating max_width
def max_width_strategy():
    return st.integers(min_value=1, max_value=200)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy(), max_width=max_width_strategy())
@example(text="short", max_width=10)
@example(text="a b c d e f g h i j k l m n o p q r s t u v w x y z", max_width=10)
@example(text="This is a long sentence that should be wrapped.", max_width=20)
@example(text="This is a long sentence that should be wrapped.", max_width=5)
@example(text="This is a long sentence that should be wrapped.", max_width=50)
@example(text="This is a long sentence that should be wrapped.", max_width=100)
@example(text="This is a long sentence that should be wrapped.", max_width=200)
def test_wrap_text_for_svg(text, max_width):
    global stop_collecting
    if stop_collecting:
        return

    text_copy = copy.deepcopy(text)
    max_width_copy = copy.deepcopy(max_width)
    try:
        expected = wrap_text_for_svg(text_copy, max_width_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Filter to ensure meaningful test cases
    if len(text) > max_width or len(text.split()) > 1:
        generated_cases.append({
            "Inputs": {"text": text, "max_width": max_width},
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