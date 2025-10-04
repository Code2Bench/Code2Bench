from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import math
from collections import Counter
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
def calculate_information_content(text):
    """计算文本的信息量（熵）"""
    char_count = Counter(text)
    total_chars = len(text)
    if total_chars == 0:
        return 0
    entropy = 0
    for count in char_count.values():
        probability = count / total_chars
        entropy -= probability * math.log2(probability)

    return entropy

# Strategy for generating text
def text_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
        min_size=0,
        max_size=100
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="a")
@example(text="aa")
@example(text="ab")
@example(text="abc")
@example(text="aabbcc")
def test_calculate_information_content(text: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        expected = calculate_information_content(text_copy)
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