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
def get_termination_value(item):
    if "termination" in item:
        return item["termination"]

    messages = item.get("messages", [])
    if not messages:
        return "unknown"

    last_message = messages[-1]["content"] if messages else ""

    if "max_turns_reached" in last_message.lower():
        return "max_turns_reached"
    elif "max_tokens_reached" in last_message.lower():
        return "max_tokens_reached"
    elif "<answer>" in last_message and "</answer>" in last_message:
        return "answered"
    else:
        return "unknown"

# Strategy for generating messages
def message_strategy():
    return st.dictionaries(
        keys=st.just("content"),
        values=st.text(
            st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
            min_size=1,
            max_size=100
        )
    )

# Strategy for generating items
def item_strategy():
    return st.one_of([
        st.dictionaries(
            keys=st.just("termination"),
            values=st.sampled_from(["max_turns_reached", "max_tokens_reached", "answered", "unknown"])
        ),
        st.dictionaries(
            keys=st.just("messages"),
            values=st.lists(message_strategy(), min_size=1, max_size=10)
        ),
        st.dictionaries(
            keys=st.just("messages"),
            values=st.lists(message_strategy(), max_size=0)
        )
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(item=item_strategy())
@example(item={"termination": "max_turns_reached"})
@example(item={"termination": "max_tokens_reached"})
@example(item={"termination": "answered"})
@example(item={"termination": "unknown"})
@example(item={"messages": []})
@example(item={"messages": [{"content": "max_turns_reached"}]})
@example(item={"messages": [{"content": "max_tokens_reached"}]})
@example(item={"messages": [{"content": "<answer>text</answer>"}]})
@example(item={"messages": [{"content": "random text"}]})
def test_get_termination_value(item):
    global stop_collecting
    if stop_collecting:
        return
    
    item_copy = copy.deepcopy(item)
    try:
        expected = get_termination_value(item_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "termination" in item or "messages" in item:
        generated_cases.append({
            "Inputs": {"item": item},
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