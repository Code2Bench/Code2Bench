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
def calculate_diff_rate(text1, text2):
    """
    Calculate the difference rate between two strings
    based on the normalized Levenshtein edit distance.
    Returns a float in [0,1], where 0 means identical.
    """
    if text1 == text2:
        return 0.0

    len1, len2 = len(text1), len(text2)
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        for j in range(len2 + 1):
            if i == 0 or j == 0:
                dp[i][j] = i + j
            elif text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    edit_distance = dp[len1][len2]
    max_len = max(len1, len2)
    return edit_distance / max_len if max_len > 0 else 0.0

# Strategy for generating text inputs
text_strategy = st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=20)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text1=text_strategy, text2=text_strategy)
@example(text1="", text2="")
@example(text1="abc", text2="abc")
@example(text1="abc", text2="def")
@example(text1="abc", text2="abcd")
@example(text1="abcd", text2="abc")
@example(text1="abc", text2="ab")
@example(text1="ab", text2="abc")
def test_calculate_diff_rate(text1, text2):
    global stop_collecting
    if stop_collecting:
        return
    
    text1_copy = copy.deepcopy(text1)
    text2_copy = copy.deepcopy(text2)
    try:
        expected = calculate_diff_rate(text1_copy, text2_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if text1 != text2 or text1 == "" or text2 == "":
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