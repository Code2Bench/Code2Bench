from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import unicodedata
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
def _normalize_name(name: str):
    name = name.strip()
    name = name.lower().replace("-", " ")
    name = re.sub(" +", " ", name)
    return unicodedata.normalize("NFKD", name).lower()

# Strategy for generating names
def name_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), whitelist_characters='- '),
        min_size=0, max_size=50
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(name=name_strategy())
@example(name="")
@example(name="  ")
@example(name="John Doe")
@example(name="John-Doe")
@example(name="John   Doe")
@example(name="Jöhn Döe")
@example(name="Jöhn-Döe")
@example(name="Jöhn   Döe")
@example(name="Jöhn Döe  ")
@example(name="  Jöhn Döe")
def test_normalize_name(name: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    name_copy = copy.deepcopy(name)

    # Call func0 to verify input validity
    try:
        expected = _normalize_name(name_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "name": name_copy
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