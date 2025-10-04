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
def normalize(x):
    if not isinstance(x, str):
        x = x.decode('utf8', errors='ignore')
    # Remove diacritics
    x = ''.join(
        c for c in unicodedata.normalize('NFKD', x) if unicodedata.category(c) != 'Mn'
    )
    # Normalize quotes and dashes
    x = re.sub(r'[‘’´`]', "'", x)
    x = re.sub(r'[“”]', '"', x)
    x = re.sub(r'[‐‑‒–—−]', '-', x)
    while True:
        old_x = x
        # Remove citations
        x = re.sub(r'((?<!^)\[[^\]]*\]|\[\d+\]|[•♦†‡*#+])*$', '', x.strip())
        # Remove details in parenthesis
        x = re.sub(r'(?<!^)( \([^)]*\))*$', '', x.strip())
        # Remove outermost quotation mark
        x = re.sub(r'^"([^"]*)"$', r'\1', x.strip())
        if x == old_x:
            break
    # Remove final '.'
    if x and x[-1] == '.':
        x = x[:-1]
    # Collapse whitespaces and convert to lower case
    x = re.sub(r'\s+', ' ', x, flags=re.U).lower().strip()
    return x

# Strategy for generating text with potential diacritics, quotes, citations, etc.
def text_strategy():
    # Generate base text with diacritics, quotes, and special characters
    base_text = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'M', 'N', 'P', 'S', 'Z')),
        min_size=1, max_size=100
    )
    
    # Add citations, parenthesis, and quotation marks
    return st.builds(
        lambda t: f'"{t}" [1] (details)',
        base_text
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="Hello World")
@example(text="‘Hello’ “World”")
@example(text="Hello-World")
@example(text="Hello [1] (details)")
@example(text="Hello.")
@example(text="  Hello  World  ")
def test_normalize(text: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        expected = normalize(text_copy)
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