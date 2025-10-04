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
def _extract_balanced_json(text: str) -> str:
    """Extract a complete JSON object by counting balanced braces."""
    start_idx = text.find('{')
    if start_idx == -1:
        return text

    brace_count = 0
    in_string = False
    escape_next = False

    for i, char in enumerate(text[start_idx:], start_idx):
        if escape_next:
            escape_next = False
            continue

        if char == '\\':
            escape_next = True
            continue

        if char == '"' and not escape_next:
            in_string = not in_string
            continue

        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return text[start_idx:i+1]

    # If we get here, braces weren't balanced - return original text
    return text

# Strategy for generating JSON-like strings
def json_like_strategy():
    return st.one_of([
        # Valid JSON objects
        st.from_regex(r'\{[^{}]*\}'),
        # Nested JSON objects
        st.recursive(
            st.from_regex(r'\{[^{}]*\}'),
            lambda children: st.from_regex(r'\{[^{}]*' + r'[^{}]*\}'),
            max_leaves=3
        ),
        # Invalid JSON objects (unbalanced braces)
        st.from_regex(r'\{[^{}]*'),
        # Strings without JSON objects
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=json_like_strategy())
@example(text="")
@example(text="{}")
@example(text='{"key": "value"}')
@example(text='{"nested": {"key": "value"}}')
@example(text='{"unbalanced": {"key": "value"}')
@example(text='{"escaped": "\\"value\\""}')
@example(text='{"nested": {"key": "value"}}}')
@example(text='{"nested": {"key": "value"}} extra text')
def test_extract_balanced_json(text: str):
    global stop_collecting
    if stop_collecting:
        return

    text_copy = copy.deepcopy(text)
    try:
        expected = _extract_balanced_json(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Filter to prioritize meaningful cases
    if '{' in text or '}' in text:
        generated_cases.append({
            "Inputs": {"text": text},
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