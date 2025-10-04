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
def split_continuous_references(text: str) -> str:
    """
    Split continuous reference tags into individual reference tags.

    Converts patterns like [1:92ff35fb, 4:bfe6f044] to [1:92ff35fb] [4:bfe6f044]

    Only processes text if:
    1. '[' appears exactly once
    2. ']' appears exactly once
    3. Contains commas between '[' and ']'

    Args:
        text (str): Text containing reference tags

    Returns:
        str: Text with split reference tags, or original text if conditions not met
    """
    # Early return if text is empty
    if not text:
        return text
    # Check if '[' appears exactly once
    if text.count("[") != 1:
        return text
    # Check if ']' appears exactly once
    if text.count("]") != 1:
        return text
    # Find positions of brackets
    open_bracket_pos = text.find("[")
    close_bracket_pos = text.find("]")

    # Check if brackets are in correct order
    if open_bracket_pos >= close_bracket_pos:
        return text
    # Extract content between brackets
    content_between_brackets = text[open_bracket_pos + 1 : close_bracket_pos]
    # Check if there's a comma between brackets
    if "," not in content_between_brackets:
        return text
    text = text.replace(content_between_brackets, content_between_brackets.replace(", ", "]["))
    text = text.replace(content_between_brackets, content_between_brackets.replace(",", "]["))

    return text

# Strategy for generating text with reference tags
def reference_text_strategy():
    return st.one_of([
        # Valid reference tags with commas
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10),
            st.just("["),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.just(","),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.just("]"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10)
        ).map(lambda x: "".join(x)),
        # Invalid reference tags (no commas)
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10),
            st.just("["),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.just("]"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10)
        ).map(lambda x: "".join(x)),
        # Invalid reference tags (multiple brackets)
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10),
            st.just("["),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.just("]"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10),
            st.just("["),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.just("]"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=10)
        ).map(lambda x: "".join(x)),
        # Empty text
        st.just(""),
        # Random text without brackets
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=reference_text_strategy())
@example(text="[1:92ff35fb, 4:bfe6f044]")
@example(text="[1:92ff35fb]")
@example(text="[1:92ff35fb, 4:bfe6f044, 5:abc123]")
@example(text="[1:92ff35fb][4:bfe6f044]")
@example(text="")
@example(text="random text")
def test_split_continuous_references(text: str):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = split_continuous_references(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if (
        text.count("[") == 1 and
        text.count("]") == 1 and
        "," in text[text.find("[") + 1:text.find("]")]
    ):
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