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
def _normalize_text(s: str) -> str:
    """
    Normalize text values:
    - strip leading/trailing whitespace
    - apply Unicode NFKC normalization
    """
    return unicodedata.normalize("NFKC", s.strip())

# Strategy for generating text inputs
def text_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), blacklist_characters='\x00'),
        min_size=0, max_size=100
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(s=text_strategy())
@example(s="")
@example(s="   leading spaces")
@example(s="trailing spaces   ")
@example(s="   both spaces   ")
@example(s="\u200B\u200C\u200D\uFEFF")  # Zero-width characters
@example(s="\u00A0\u202F\u2007")  # Non-breaking spaces
@example(s="\u00C1\u0301")  # Combined and decomposed Unicode characters
def test_normalize_text(s: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    s_copy = copy.deepcopy(s)

    # Call func0 to verify input validity
    try:
        expected = _normalize_text(s_copy)
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