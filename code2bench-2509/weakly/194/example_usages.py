from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from collections import Counter

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def calculate_ngram_repetition(text, n):
    words = text.split()
    ngrams = [tuple(words[i : i + n]) for i in range(len(words) - n + 1)]
    ngram_counts = Counter(ngrams)
    total_ngrams = len(ngrams)
    repeated_ngrams = sum(1 for count in ngram_counts.values() if count > 1)
    return repeated_ngrams / total_ngrams if total_ngrams > 0 else 0

# Strategies for generating inputs
def text_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=0, max_size=100
    )

def n_strategy():
    return st.integers(min_value=1, max_value=5)

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy(), n=n_strategy())
@example(text="", n=1)
@example(text="a", n=1)
@example(text="a b c", n=2)
@example(text="a a b b c c", n=2)
@example(text="a b c d e f", n=3)
@example(text="a a a a a a", n=3)
def test_calculate_ngram_repetition(text, n):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy inputs to avoid modification
    text_copy = copy.deepcopy(text)
    n_copy = copy.deepcopy(n)

    # Call func0 to verify input validity
    try:
        expected = calculate_ngram_repetition(text_copy, n_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Multiple unique n-grams"
        elif case_count == 1:
            desc = "Single n-gram"
        else:
            desc = "Mixed text with repeated n-grams"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Empty string"
        elif case_count == 4:
            desc = "Single character"
        elif case_count == 5:
            desc = "Repeated n-grams"
        elif case_count == 6:
            desc = "Long text with no repetition"
        else:
            desc = "Large n value"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "text": text_copy,
            "n": n_copy
        },
        "Expected": expected,
        "Usage": None
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)