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
def extract_block_content(text, start_idx):
    try:
        block_start = text.index("{", start_idx)

        brace_count = 1
        pos = block_start + 1

        while brace_count > 0 and pos < len(text):
            if text[pos] == '{':
                brace_count += 1
            elif text[pos] == '}':
                brace_count -= 1
            pos += 1

        if brace_count == 0:
            return text[block_start:pos]
    except ValueError as e:
        pass

    return ""

# Strategy for generating text with nested blocks
def nested_block_strategy():
    return st.recursive(
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        lambda children: st.tuples(
            st.just("{"),
            children,
            st.just("}")
        ).map(lambda x: "".join(x)),
        max_leaves=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    text=st.one_of([
        nested_block_strategy(),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=100)
    ]),
    start_idx=st.integers(min_value=0, max_value=100)
)
@example(text="{content}", start_idx=0)
@example(text="no block", start_idx=0)
@example(text="nested { { block } }", start_idx=0)
@example(text="multiple { blocks } { here }", start_idx=0)
@example(text="{unclosed", start_idx=0)
@example(text="start { middle } end", start_idx=6)
def test_extract_block_content(text, start_idx):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = extract_block_content(text_copy, start_idx)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "{" in text or start_idx < len(text):
        generated_cases.append({
            "Inputs": {"text": text, "start_idx": start_idx},
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