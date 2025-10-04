from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict
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
def _extract_message_text(msg: Dict[str, Any]) -> str:
    content = msg.get("content", "")
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif item.get("type") == "image_url":
                    parts.append("[IMAGE]")
        return " ".join(parts)

    return str(content)

# Strategy for generating message dictionaries
def message_strategy():
    return st.one_of([
        # Case 1: content is a string
        st.fixed_dictionaries({
            "content": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50)
        }),
        # Case 2: content is a list of dictionaries with type "text"
        st.fixed_dictionaries({
            "content": st.lists(
                st.fixed_dictionaries({
                    "type": st.just("text"),
                    "text": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=20)
                }),
                min_size=1, max_size=5
            )
        }),
        # Case 3: content is a list of dictionaries with type "image_url"
        st.fixed_dictionaries({
            "content": st.lists(
                st.fixed_dictionaries({
                    "type": st.just("image_url")
                }),
                min_size=1, max_size=5
            )
        }),
        # Case 4: content is a list of mixed dictionaries
        st.fixed_dictionaries({
            "content": st.lists(
                st.one_of([
                    st.fixed_dictionaries({
                        "type": st.just("text"),
                        "text": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=20)
                    }),
                    st.fixed_dictionaries({
                        "type": st.just("image_url")
                    })
                ]),
                min_size=1, max_size=5
            )
        }),
        # Case 5: content is a non-string, non-list value
        st.fixed_dictionaries({
            "content": st.one_of([
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.booleans(),
                st.none()
            ])
        })
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(msg=message_strategy())
@example(msg={"content": "Hello, world!"})
@example(msg={"content": [{"type": "text", "text": "Hello"}]})
@example(msg={"content": [{"type": "image_url"}]})
@example(msg={"content": [{"type": "text", "text": "Hello"}, {"type": "image_url"}]})
@example(msg={"content": 42})
@example(msg={"content": None})
def test_extract_message_text(msg: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    msg_copy = copy.deepcopy(msg)
    try:
        expected = _extract_message_text(msg_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"msg": msg},
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