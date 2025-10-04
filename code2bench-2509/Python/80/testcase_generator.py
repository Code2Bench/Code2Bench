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
def _extract_content_and_reasoning(parts: list) -> tuple:
    """从Gemini响应部件中提取内容和推理内容"""
    content = ""
    reasoning_content = ""

    for part in parts:
        # 处理文本内容
        if part.get("text"):
            # 检查这个部件是否包含thinking tokens
            if part.get("thought", False):
                reasoning_content += part.get("text", "")
            else:
                content += part.get("text", "")

    return content, reasoning_content

# Strategy for generating parts
def part_strategy():
    return st.fixed_dictionaries({
        "text": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        "thought": st.booleans()
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(parts=st.lists(part_strategy(), min_size=1, max_size=10))
@example(parts=[{"text": "Hello", "thought": False}])
@example(parts=[{"text": "Thinking...", "thought": True}])
@example(parts=[{"text": "Content", "thought": False}, {"text": "Reasoning", "thought": True}])
@example(parts=[{"text": "Mixed", "thought": False}, {"text": "Thought", "thought": True}, {"text": "More", "thought": False}])
def test_extract_content_and_reasoning(parts):
    global stop_collecting
    if stop_collecting:
        return
    
    parts_copy = copy.deepcopy(parts)
    try:
        expected = _extract_content_and_reasoning(parts_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(part.get("text") for part in parts):
        generated_cases.append({
            "Inputs": {"parts": parts},
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