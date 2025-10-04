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
def fullwidth_to_halfwidth(s):
    result = []
    for char in s:
        code = ord(char)
        # Convert full-width space to half-width space
        if code == 0x3000:
            code = 0x0020
        # Convert other full-width characters to half-width
        elif 0xFF01 <= code <= 0xFF5E:
            code -= 0xFEE0
        result.append(chr(code))
    return ''.join(result)

# Strategy for generating full-width and half-width characters
def char_strategy():
    return st.one_of([
        st.just(chr(0x3000)),  # Full-width space
        st.characters(min_codepoint=0xFF01, max_codepoint=0xFF5E),  # Full-width characters
        st.characters(min_codepoint=0x0020, max_codepoint=0x007E),  # Half-width characters
        st.characters(min_codepoint=0x4E00, max_codepoint=0x9FFF),  # CJK Unified Ideographs
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(s=st.text(char_strategy(), min_size=1, max_size=50))
@example(s=chr(0x3000))  # Full-width space
@example(s=chr(0xFF01))  # Full-width exclamation mark
@example(s=chr(0x0020))  # Half-width space
@example(s=chr(0x0041))  # Half-width 'A'
@example(s="ＡＢＣ")  # Full-width 'ABC'
@example(s="ABC")  # Half-width 'ABC'
@example(s="ＡＢＣ123")  # Mixed full-width and half-width
def test_fullwidth_to_halfwidth(s):
    global stop_collecting
    if stop_collecting:
        return
    
    s_copy = copy.deepcopy(s)
    try:
        expected = fullwidth_to_halfwidth(s_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(ord(char) == 0x3000 or 0xFF01 <= ord(char) <= 0xFF5E for char in s):
        generated_cases.append({
            "Inputs": {"s": s},
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