from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List, Dict
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
def _validate_messages(messages: List[Dict[str, str]]) -> bool:
    if not messages:
        return False

    for msg in messages:
        if not isinstance(msg, dict):
            return False
        if 'role' not in msg or 'content' not in msg:
            return False
        if msg['role'] not in ['system', 'user', 'assistant']:
            return False
        if not isinstance(msg['content'], str):
            return False

    if messages[0]['role'] != 'system':
        return False

    return True

# Strategy for generating valid messages
def message_strategy():
    return st.fixed_dictionaries({
        'role': st.sampled_from(['system', 'user', 'assistant']),
        'content': st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    })

# Strategy for generating lists of messages
def messages_strategy():
    return st.lists(message_strategy(), min_size=1, max_size=10).map(lambda msgs: [{'role': 'system', 'content': 'System message'}] + msgs[1:] if msgs else msgs)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(messages=messages_strategy())
@example(messages=[])
@example(messages=[{'role': 'user', 'content': 'Hello'}])
@example(messages=[{'role': 'system', 'content': 'System message'}, {'role': 'user', 'content': 'Hello'}])
@example(messages=[{'role': 'system', 'content': 'System message'}, {'role': 'assistant', 'content': 'Hi there!'}])
@example(messages=[{'role': 'system', 'content': 'System message'}, {'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi there!'}])
@example(messages=[{'role': 'system', 'content': 'System message'}, {'role': 'user', 'content': 123}])
@example(messages=[{'role': 'system', 'content': 'System message'}, {'role': 'invalid', 'content': 'Hello'}])
def test_validate_messages(messages: List[Dict[str, str]]):
    global stop_collecting
    if stop_collecting:
        return
    
    messages_copy = copy.deepcopy(messages)
    try:
        expected = _validate_messages(messages_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
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