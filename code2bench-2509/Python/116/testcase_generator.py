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
def format_chat_prompt(messages):
    """
    Format multi-turn conversation into prompt string, suitable for chat models.
    Uses Qwen2 style with <|im_start|> / <|im_end|> tokens.
    """
    prompt = ""
    for msg in messages:
        role, content = msg["role"], msg["content"]
        if role == "user":
            prompt += f"<|im_start|>user\n{content}<|im_end|>\n"
        elif role == "assistant":
            prompt += f"<|im_start|>assistant\n{content}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"
    return prompt

# Strategy for generating messages
def message_strategy():
    return st.fixed_dictionaries({
        "role": st.sampled_from(["user", "assistant"]),
        "content": st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(messages=st.lists(message_strategy(), min_size=1, max_size=10))
@example(messages=[{"role": "user", "content": "Hello"}])
@example(messages=[{"role": "assistant", "content": "Hi there!"}])
@example(messages=[{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}])
@example(messages=[{"role": "user", "content": ""}])
@example(messages=[{"role": "assistant", "content": ""}])
def test_format_chat_prompt(messages):
    global stop_collecting
    if stop_collecting:
        return
    
    messages_copy = copy.deepcopy(messages)
    try:
        expected = format_chat_prompt(messages_copy)
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