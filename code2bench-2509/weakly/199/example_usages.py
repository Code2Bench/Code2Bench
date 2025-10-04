from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import numpy as np
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def _clip(messages: list[dict[str, str]], max_tokens: int) -> list[dict[str, str]]:
    """Left clip a messages array to avoid hitting the context limit."""
    cum_tokens = np.cumsum([len(message.get("content") or "") // 3 for message in messages][::-1])
    first_message = -np.searchsorted(cum_tokens, max_tokens)
    return messages[first_message:]

# Strategies for generating inputs
def messages_strategy():
    return st.lists(
        st.dictionaries(
            keys=st.just("content"),
            values=st.text(min_size=0, max_size=100),
            min_size=1,
            max_size=1
        ),
        min_size=0,
        max_size=20
    )

def max_tokens_strategy(messages):
    if not messages:
        return st.integers(min_value=0, max_value=100)
    cum_tokens = np.cumsum([len(message.get("content") or "") // 3 for message in messages][::-1])
    return st.integers(min_value=0, max_value=int(cum_tokens[-1] * 1.5))

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(
    messages=messages_strategy(),
    max_tokens=st.builds(
        lambda m: max_tokens_strategy(m),
        messages_strategy()
    )
)
@example(messages=[], max_tokens=0)
@example(messages=[{"content": "hello"}], max_tokens=1)
@example(messages=[{"content": "hello"}, {"content": "world"}], max_tokens=2)
@example(messages=[{"content": "hello"}, {"content": "world"}, {"content": "!"}], max_tokens=3)
def test_clip(messages: list[dict[str, str]], max_tokens: int):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy inputs to avoid modification
    messages_copy = copy.deepcopy(messages)
    max_tokens_copy = max_tokens

    # Call func0 to verify input validity
    try:
        expected = _clip(messages_copy, max_tokens_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Multiple messages with sufficient tokens"
        elif case_count == 1:
            desc = "Single message with exact token count"
        else:
            desc = "Multiple messages with partial clipping"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Empty messages"
        elif case_count == 4:
            desc = "Single message with zero tokens"
        elif case_count == 5:
            desc = "Multiple messages with zero tokens"
        elif case_count == 6:
            desc = "Large number of messages"
        else:
            desc = "Messages with varying token counts"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "messages": messages_copy,
            "max_tokens": max_tokens_copy
        },
        "Expected": expected,
        "Usage": None
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)