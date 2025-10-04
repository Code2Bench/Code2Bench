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
def count_valid_tags(text: str, tag: str) -> int:
    """Count valid paired tags."""
    count = 0
    current_pos = 0

    while True:
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"

        start_pos = text.find(start_tag, current_pos)
        if start_pos == -1:
            break

        end_pos = text.find(end_tag, start_pos + len(start_tag))
        if end_pos == -1:
            break

        count += 1
        current_pos = end_pos + len(end_tag)

    return count

# Strategy for generating valid tags
def tag_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)

# Strategy for generating text with valid and invalid tags
def text_with_tags_strategy(tag):
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.lists(
            st.one_of([
                st.just(f"<{tag}>"),
                st.just(f"</{tag}>"),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
            ]),
            min_size=1, max_size=20
        ).map(lambda x: "".join(x))
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_with_tags_strategy(tag="tag"), tag=tag_strategy())
@example(text="<tag></tag>", tag="tag")
@example(text="<tag><tag></tag></tag>", tag="tag")
@example(text="<tag>text</tag>", tag="tag")
@example(text="<tag></tag><tag></tag>", tag="tag")
@example(text="<tag><tag>text</tag></tag>", tag="tag")
@example(text="<tag></tag><tag>text</tag>", tag="tag")
@example(text="<tag>text<tag>text</tag></tag>", tag="tag")
@example(text="<tag>text</tag><tag>text</tag>", tag="tag")
@example(text="<tag>text</tag><tag>text</tag><tag>text</tag>", tag="tag")
@example(text="<tag>text</tag><tag>text</tag><tag>text</tag><tag>text</tag>", tag="tag")
def test_count_valid_tags(text: str, tag: str):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    tag_copy = copy.deepcopy(tag)
    try:
        expected = count_valid_tags(text_copy, tag_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "<" in text or ">" in text:
        generated_cases.append({
            "Inputs": {"text": text, "tag": tag},
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