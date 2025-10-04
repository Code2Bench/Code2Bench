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
def _split_respecting_brackets(content: str) -> List[str]:
    parts = []
    current_part = ""
    bracket_count = 0
    comma_count = 0

    for i, char in enumerate(content):
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
        elif char == ',' and bracket_count == 0:
            parts.append(current_part.strip())
            current_part = ""
            comma_count += 1
            if comma_count == 2:  # After finding 2 commas, rest is tail
                remaining = content[i+1:].strip()
                if remaining:
                    parts.append(remaining)
                break
            continue
        current_part += char

    # Add final part if we haven't reached 3 parts yet
    if len(parts) < 3 and current_part.strip():
        parts.append(current_part.strip())

    return parts

# Strategy for generating content strings
def content_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.lists(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            min_size=1, max_size=3
        ).map(lambda lst: ",".join(lst)),
        st.lists(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            min_size=1, max_size=3
        ).map(lambda lst: "[" + ",".join(lst) + "]"),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda t: ",".join(t)),
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda t: "[" + ",".join(t) + "]")
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(content=content_strategy())
@example(content="a,b,c")
@example(content="a,[b,c],d")
@example(content="[a,b],c,d")
@example(content="a,b,[c,d]")
@example(content="a,b,c,d")
@example(content="a,b")
@example(content="a")
def test_split_respecting_brackets(content: str):
    global stop_collecting
    if stop_collecting:
        return
    
    content_copy = copy.deepcopy(content)
    try:
        expected = _split_respecting_brackets(content_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "," in content or "[" in content or "]" in content:
        generated_cases.append({
            "Inputs": {"content": content},
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