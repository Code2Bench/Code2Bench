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
def _calculate_phrase_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0

    text1_lower = text1.lower()
    text2_lower = text2.lower()

    phrase_boost = 0.0

    words1 = text1_lower.split()
    words2 = text2_lower.split()

    for i in range(len(words1) - 1):
        phrase = f"{words1[i]} {words1[i+1]}"
        if phrase in text2_lower:
            phrase_boost += 0.1

    for i in range(len(words1) - 2):
        phrase = f"{words1[i]} {words1[i+1]} {words1[i+2]}"
        if phrase in text2_lower:
            phrase_boost += 0.15

    return min(0.3, phrase_boost)

# Strategy for generating text inputs
def text_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text1=text_strategy(), text2=text_strategy())
@example(text1="", text2="")
@example(text1="hello world", text2="")
@example(text1="", text2="hello world")
@example(text1="hello world", text2="hello world")
@example(text1="hello world", text2="world hello")
@example(text1="hello world", text2="hello")
@example(text1="hello world", text2="hello world!")
@example(text1="hello world", text2="hello world and universe")
@example(text1="hello world and universe", text2="hello world")
@example(text1="hello world and universe", text2="hello world and universe")
def test_calculate_phrase_similarity(text1: str, text2: str):
    global stop_collecting
    if stop_collecting:
        return

    text1_copy = copy.deepcopy(text1)
    text2_copy = copy.deepcopy(text2)
    try:
        expected = _calculate_phrase_similarity(text1_copy, text2_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {"text1": text1, "text2": text2},
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