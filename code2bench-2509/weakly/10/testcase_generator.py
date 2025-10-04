from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import string
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
def normalize_text(text: str) -> str:
    text = text.lower()
    text = ''.join(ch for ch in text if ch not in set(string.punctuation))
    text = ' '.join(text.split())
    return text

# Strategy for generating text
def text_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=0, max_size=100
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="Hello, World!")
@example(text="  Multiple   Spaces  ")
@example(text="Punctuation!@#")
@example(text="Mixed Case and Punctuation: Test 123")
def test_normalize_text(text: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        expected = normalize_text(text_copy)
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