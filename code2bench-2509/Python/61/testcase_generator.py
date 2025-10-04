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
def validate_word_constraint(text: str, N: int, quantifier: str) -> bool:
    """
    Reference implementation from: https://github.com/allenai/open-instruct/blob/main/open_instruct/if_functions.py
    """
    # 清除多余空白字符并拆分文本为单词列表
    words = text.strip().split()
    actual_count = len(words)

    # 定义 "around" 约束的容错范围（目标单词数的 ±10%，至少 1 个单词）
    tolerance = max(round(N * 0.1), 1)

    if quantifier == "at least":
        return actual_count >= N
    elif quantifier == "at most":
        return actual_count <= N
    elif quantifier == "around":
        return abs(actual_count - N) <= tolerance
    else:
        return False

# Strategy for generating text
def text_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=100)

# Strategy for generating N
def N_strategy():
    return st.integers(min_value=0, max_value=100)

# Strategy for generating quantifier
def quantifier_strategy():
    return st.sampled_from(["at least", "at most", "around"])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy(), N=N_strategy(), quantifier=quantifier_strategy())
@example(text="", N=0, quantifier="at least")
@example(text="one two three", N=3, quantifier="at least")
@example(text="one two three", N=3, quantifier="at most")
@example(text="one two three", N=3, quantifier="around")
@example(text="one two three", N=2, quantifier="around")
@example(text="one two three", N=4, quantifier="around")
@example(text="one two three", N=5, quantifier="around")
def test_validate_word_constraint(text: str, N: int, quantifier: str):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    N_copy = copy.deepcopy(N)
    quantifier_copy = copy.deepcopy(quantifier)
    try:
        expected = validate_word_constraint(text_copy, N_copy, quantifier_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"text": text, "N": N, "quantifier": quantifier},
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