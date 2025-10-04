from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
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
def normalize_name(tag_name: str) -> str:
    nfkd_form = unicodedata.normalize("NFKD", tag_name)
    nfkd_form.encode("ASCII", "ignore").decode("UTF-8")
    tag_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    tag_name = tag_name.strip().lower()
    tag_name = re.sub(r"\s+", "_", tag_name)
    tag_name = re.sub(r"[^a-zA-Z0-9_.:-]", "", tag_name)
    return tag_name

# Strategy for generating tag names
def tag_name_strategy():
    return st.text(
        alphabet=st.characters(
            whitelist_categories=('L', 'N', 'P', 'S', 'M', 'Z'),
            whitelist_characters='_.:-'
        ),
        min_size=0,
        max_size=50
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(tag_name=tag_name_strategy())
@example(tag_name="")
@example(tag_name="Hello World")
@example(tag_name="こんにちは")
@example(tag_name="123_abc")
@example(tag_name="!@#$%^&*()")
@example(tag_name="   spaces   ")
def test_normalize_name(tag_name: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    tag_name_copy = copy.deepcopy(tag_name)

    # Call func0 to verify input validity
    try:
        expected = normalize_name(tag_name_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "tag_name": tag_name_copy
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