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
def extract_content_string(content):
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Handle Anthropic's list format
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                item_type = item.get('type')  # 缓存type值
                if item_type == 'text':
                    text_parts.append(item.get('text', ''))
                elif item_type == 'tool_use':
                    tool_name = item.get('name', 'unknown')  # 缓存name值
                    text_parts.append(f"[Tool: {tool_name}]")
            else:
                text_parts.append(str(item))
        return ' '.join(text_parts)
    else:
        return str(content)

# Strategy for generating content
def content_strategy():
    return st.one_of([
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))),
        st.lists(st.one_of([
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))),
            st.dictionaries(
                keys=st.text(st.characters(whitelist_categories=('L', 'N')), max_size=10),
                values=st.one_of([
                    st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))),
                    st.text(st.characters(whitelist_categories=('L', 'N')), max_size=10)
                ]),
                max_size=5
            )
        ]), max_size=5),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.booleans()
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(content=content_strategy())
@example(content="simple string")
@example(content=[])
@example(content=[{"type": "text", "text": "hello"}])
@example(content=[{"type": "tool_use", "name": "tool1"}])
@example(content=[{"type": "text", "text": "hello"}, {"type": "tool_use", "name": "tool1"}])
@example(content=[1, 2, 3])
@example(content={"key": "value"})
def test_extract_content_string(content):
    global stop_collecting
    if stop_collecting:
        return
    
    content_copy = copy.deepcopy(content)
    try:
        expected = extract_content_string(content_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(content, (str, list)) or (isinstance(content, dict) and not isinstance(content, list)):
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