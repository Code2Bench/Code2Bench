from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import string
import re
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
def canonicalize(text, keep_punctuation_exact_string=None):
    text = text.replace('_', ' ')
    if keep_punctuation_exact_string:
        text = keep_punctuation_exact_string.join(
            part.translate(str.maketrans('', '', string.punctuation))
            for part in text.split(keep_punctuation_exact_string))
    else:
        text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Strategies for generating inputs
def text_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=0, max_size=50
    )

def keep_punctuation_exact_string_strategy():
    return st.one_of(
        st.none(),
        st.text(
            alphabet=st.characters(whitelist_categories=('P',), min_codepoint=33, max_codepoint=126),
            min_size=1, max_size=2
        )
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    text=text_strategy(),
    keep_punctuation_exact_string=keep_punctuation_exact_string_strategy()
)
@example(text="", keep_punctuation_exact_string=None)
@example(text="Hello_World!", keep_punctuation_exact_string=None)
@example(text="Hello_World!", keep_punctuation_exact_string="!")
@example(text="This is a test.", keep_punctuation_exact_string=".")
@example(text="Multiple   spaces", keep_punctuation_exact_string=None)
@example(text="Mixed_Case_Text", keep_punctuation_exact_string="_")
def test_canonicalize(text: str, keep_punctuation_exact_string):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    text_copy = copy.deepcopy(text)
    keep_punctuation_exact_string_copy = copy.deepcopy(keep_punctuation_exact_string)

    # Call func0 to verify input validity
    try:
        expected = canonicalize(text_copy, keep_punctuation_exact_string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "text": text_copy,
            "keep_punctuation_exact_string": keep_punctuation_exact_string_copy
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