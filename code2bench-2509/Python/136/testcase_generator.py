from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict, List
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
def _reformat_messages(
    messages: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    for message in messages:
        content = message.get("content", [])

        is_all_text = True
        texts = []
        for item in content:
            if not isinstance(item, dict) or "text" not in item:
                is_all_text = False
                break
            if "type" in item and item["type"] != "text":
                is_all_text = False
                break
            if item["text"]:
                texts.append(item["text"])

        if is_all_text and texts:
            message["content"] = "\n".join(texts)

    return messages

# Strategy for generating message content items
def content_item_strategy():
    return st.one_of([
        st.fixed_dictionaries({
            "text": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
            "type": st.just("text")
        }),
        st.fixed_dictionaries({
            "text": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
        }),
        st.fixed_dictionaries({
            "image_url": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
            "type": st.just("image")
        }),
        st.fixed_dictionaries({
            "text": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
            "type": st.just("other")
        })
    ])

# Strategy for generating messages
def message_strategy():
    return st.fixed_dictionaries({
        "role": st.sampled_from(["user", "assistant", "system"]),
        "content": st.one_of([
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
            st.lists(content_item_strategy(), min_size=1, max_size=5)
        ])
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(messages=st.lists(message_strategy(), min_size=1, max_size=5))
@example(messages=[{"role": "user", "content": "Hello"}])
@example(messages=[{"role": "user", "content": [{"text": "Hello", "type": "text"}]}])
@example(messages=[{"role": "user", "content": [{"text": "Hello", "type": "text"}, {"text": "World", "type": "text"}]}])
@example(messages=[{"role": "user", "content": [{"text": "Hello", "type": "text"}, {"image_url": "example.com/image.png", "type": "image"}]}])
@example(messages=[{"role": "user", "content": [{"text": "Hello"}, {"text": "World"}]}])
@example(messages=[{"role": "user", "content": [{"text": "Hello", "type": "other"}]}])
def test_reformat_messages(messages: List[Dict[str, Any]]):
    global stop_collecting
    if stop_collecting:
        return
    
    messages_copy = copy.deepcopy(messages)
    try:
        expected = _reformat_messages(messages_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to prioritize cases that exercise meaningful branches
    if any(isinstance(message.get("content"), list) for message in messages):
        generated_cases.append({
            "Inputs": {"messages": messages},
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