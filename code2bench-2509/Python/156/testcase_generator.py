from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
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
def build_summary_request_text(retain_count: int, evicted_messages: List[str], in_context_messages: List[str]) -> str:
    parts: List[str] = []
    if retain_count == 0:
        parts.append(
            "You’re a memory-recall helper for an AI that is about to forget all prior messages. Scan the conversation history and write crisp notes that capture any important facts or insights about the conversation history."
        )
    else:
        parts.append(
            f"You’re a memory-recall helper for an AI that can only keep the last {retain_count} messages. Scan the conversation history, focusing on messages about to drop out of that window, and write crisp notes that capture any important facts or insights about the human so they aren’t lost."
        )

    if evicted_messages:
        parts.append("\n(Older) Evicted Messages:")
        for item in evicted_messages:
            parts.append(f"    {item}")

    if retain_count > 0 and in_context_messages:
        parts.append("\n(Newer) In-Context Messages:")
        for item in in_context_messages:
            parts.append(f"    {item}")

    return "\n".join(parts) + "\n"

# Strategy for generating messages
message_strategy = st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    retain_count=st.integers(min_value=0, max_value=100),
    evicted_messages=st.lists(message_strategy, max_size=5),
    in_context_messages=st.lists(message_strategy, max_size=5)
)
@example(retain_count=0, evicted_messages=[], in_context_messages=[])
@example(retain_count=1, evicted_messages=["Message 1"], in_context_messages=[])
@example(retain_count=2, evicted_messages=[], in_context_messages=["Message 2"])
@example(retain_count=3, evicted_messages=["Message 1", "Message 2"], in_context_messages=["Message 3", "Message 4"])
def test_build_summary_request_text(retain_count: int, evicted_messages: List[str], in_context_messages: List[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    evicted_messages_copy = copy.deepcopy(evicted_messages)
    in_context_messages_copy = copy.deepcopy(in_context_messages)
    try:
        expected = build_summary_request_text(retain_count, evicted_messages_copy, in_context_messages_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if retain_count == 0 or evicted_messages or (retain_count > 0 and in_context_messages):
        generated_cases.append({
            "Inputs": {
                "retain_count": retain_count,
                "evicted_messages": evicted_messages,
                "in_context_messages": in_context_messages
            },
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