from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
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
def _apply_stops(text: str, stop: List[str]) -> str:
    if not text:
        return ""
    for s in stop or []:
        if s and s in text:
            return text.split(s, 1)[0].strip()
    return text.strip()

# Strategy for generating text
def text_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

# Strategy for generating stop lists
def stop_strategy():
    return st.lists(text_strategy(), max_size=5)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy(), stop=stop_strategy())
@example(text="", stop=[])
@example(text="hello world", stop=[])
@example(text="hello world", stop=["world"])
@example(text="hello world", stop=["hello"])
@example(text="hello world", stop=["hello", "world"])
@example(text="hello world", stop=["world", "hello"])
@example(text="hello world", stop=["lo", "wor"])
@example(text="hello world", stop=["xyz"])
def test_apply_stops(text: str, stop: List[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    stop_copy = copy.deepcopy(stop)
    try:
        expected = _apply_stops(text_copy, stop_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(s in text for s in stop) or not text or not stop:
        generated_cases.append({
            "Inputs": {"text": text, "stop": stop},
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