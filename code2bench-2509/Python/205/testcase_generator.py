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
def _strip_existing_semantic_index(content: str) -> str:
    lines = content.split('\n')
    result_lines = []
    in_semantic_index = False

    for line in lines:
        if line.strip().startswith('## SEMANTIC INDEX'):
            in_semantic_index = True
            continue
        elif in_semantic_index and line.strip().startswith('##') and not line.strip().startswith('## SEMANTIC INDEX'):
            in_semantic_index = False
            result_lines.append(line)
        elif not in_semantic_index:
            result_lines.append(line)

    return '\n'.join(result_lines)

# Strategy for generating content with semantic index sections
def content_strategy():
    return st.text(
        st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), blacklist_characters='\x00'),
        min_size=1,
        max_size=1000
    ).map(lambda s: s.replace('\x00', ''))  # Ensure no null characters

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(content=content_strategy())
@example(content="## SEMANTIC INDEX\nSome content\n## Other section")
@example(content="## SEMANTIC INDEX\n## SEMANTIC INDEX\nSome content\n## Other section")
@example(content="Some content\n## SEMANTIC INDEX\n## Other section")
@example(content="## SEMANTIC INDEX\n## Other section")
@example(content="## Other section\n## SEMANTIC INDEX\nSome content")
@example(content="## SEMANTIC INDEX\nSome content\n## SEMANTIC INDEX\n## Other section")
@example(content="## SEMANTIC INDEX\n## SEMANTIC INDEX\n## Other section")
def test_strip_existing_semantic_index(content: str):
    global stop_collecting
    if stop_collecting:
        return
    
    content_copy = copy.deepcopy(content)
    try:
        expected = _strip_existing_semantic_index(content_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "## SEMANTIC INDEX" in content or "##" in content:
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