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
def _messages_to_steps(messages: list[dict]) -> list[list[dict]]:
    """Group messages into "pages" as shown by the UI."""
    steps = []
    current_step = []
    for message in messages:
        current_step.append(message)
        if message["role"] == "user":
            steps.append(current_step)
            current_step = []
    if current_step:
        steps.append(current_step)
    return steps

# Strategy for generating messages
def message_strategy():
    return st.fixed_dictionaries({
        "role": st.sampled_from(["user", "assistant", "system"]),
        "content": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(messages=st.lists(message_strategy(), min_size=1, max_size=20))
@example(messages=[{"role": "user", "content": "Hello"}])
@example(messages=[{"role": "assistant", "content": "Hi there"}])
@example(messages=[{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there"}])
@example(messages=[{"role": "assistant", "content": "Hi there"}, {"role": "user", "content": "Hello"}])
@example(messages=[{"role": "user", "content": "Hello"}, {"role": "user", "content": "Hi there"}])
@example(messages=[{"role": "assistant", "content": "Hi there"}, {"role": "assistant", "content": "Hello"}])
def test_messages_to_steps(messages: list[dict]):
    global stop_collecting
    if stop_collecting:
        return
    
    messages_copy = copy.deepcopy(messages)
    try:
        expected = _messages_to_steps(messages_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(message["role"] == "user" for message in messages) or len(messages) > 1:
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