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
def get_messages_summary(messages: list[dict]) -> dict:
    if not messages:
        return {"total": 0, "by_type": {}, "by_model": {}, "total_tokens": 0}

    by_type = {}
    by_model = {}
    total_tokens = 0

    for msg in messages:
        # Count by type
        msg_type = msg.get("type", "unknown")
        by_type[msg_type] = by_type.get(msg_type, 0) + 1

        # Count by model
        model = msg.get("model", "unknown")
        by_model[model] = by_model.get(model, 0) + 1

        # Sum tokens
        tokens = msg.get("tokens", {})
        if isinstance(tokens, dict):
            total_tokens += tokens.get("input", 0) + tokens.get("output", 0)

    return {"total": len(messages), "by_type": by_type, "by_model": by_model, "total_tokens": total_tokens}

# Strategy for generating messages
def message_strategy():
    return st.fixed_dictionaries({
        "type": st.one_of([st.just("user"), st.just("assistant"), st.just("system"), st.just("unknown")]),
        "model": st.one_of([st.just("gpt-3.5-turbo"), st.just("gpt-4"), st.just("unknown")]),
        "tokens": st.one_of([
            st.fixed_dictionaries({
                "input": st.integers(min_value=0, max_value=1000),
                "output": st.integers(min_value=0, max_value=1000)
            }),
            st.just({})
        ])
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(messages=st.lists(message_strategy(), max_size=20))
@example(messages=[])
@example(messages=[{"type": "user", "model": "gpt-3.5-turbo", "tokens": {"input": 10, "output": 20}}])
@example(messages=[{"type": "assistant", "model": "gpt-4", "tokens": {"input": 5, "output": 15}}])
@example(messages=[{"type": "system", "model": "unknown", "tokens": {}}])
@example(messages=[{"type": "unknown", "model": "gpt-3.5-turbo", "tokens": {"input": 0, "output": 0}}])
def test_get_messages_summary(messages: list[dict]):
    global stop_collecting
    if stop_collecting:
        return
    
    messages_copy = copy.deepcopy(messages)
    try:
        expected = get_messages_summary(messages_copy)
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