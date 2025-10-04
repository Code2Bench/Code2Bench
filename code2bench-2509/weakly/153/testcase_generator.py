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
def safe_truncate(text: str, max_length: int) -> str:
    if max_length <= 0:
        raise ValueError("max_length must be greater than 0")
    text = unicodedata.normalize("NFC", text)
    if len(text) <= max_length:
        return text
    end_pos = max_length - 1
    if unicodedata.combining(text[end_pos + 1]):
        while unicodedata.combining(text[end_pos]):
            end_pos -= 1
        end_pos -= 1
    return text[:end_pos] + "…"

# Strategies for generating inputs
def text_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'M', 'P', 'S', 'Z'), min_codepoint=0, max_codepoint=0x10FFFF),
        min_size=0, max_size=100
    )

def max_length_strategy():
    return st.integers(min_value=1, max_value=100)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    text=text_strategy(),
    max_length=max_length_strategy()
)
@example(text="", max_length=1)
@example(text="a", max_length=1)
@example(text="a", max_length=2)
@example(text="á", max_length=1)
@example(text="á", max_length=2)
@example(text="á", max_length=1)  # Combining character
@example(text="á", max_length=2)
@example(text="áb", max_length=2)
@example(text="áb", max_length=3)
def test_safe_truncate(text: str, max_length: int):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    text_copy = copy.deepcopy(text)
    max_length_copy = copy.deepcopy(max_length)

    # Call func0 to verify input validity
    try:
        expected = safe_truncate(text_copy, max_length_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "text": text_copy,
            "max_length": max_length_copy
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