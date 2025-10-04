from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy
from typing import List, Dict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def get_chain_summary(chain: List[Dict]) -> Dict:
    """Get summary info about a chain"""
    total_messages = 0
    user_messages = 0
    assistant_messages = 0
    tools_used = set()

    first_message = None
    last_message = None

    for node in chain:
        messages = node.get("data", {}).get("messages", [])
        total_messages += len(messages)

        for msg in messages:
            role = msg.get("role", "")
            if role == "user":
                user_messages += 1
            elif role == "assistant":
                assistant_messages += 1

            if first_message is None:
                first_message = msg
            last_message = msg

            # extract tools
            content = str(msg.get("content", ""))
            if "tool_use" in content:
                tool_matches = re.findall(r'"name":\s*"([^"]+)"', content)
                tools_used.update(tool_matches)

    return {
        "length": len(chain),
        "total_messages": total_messages,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "tools_used": list(tools_used),
        "first_message": first_message,
        "last_message": last_message,
    }

# Strategies for generating inputs
def message_strategy():
    return st.fixed_dictionaries({
        "role": st.sampled_from(["user", "assistant"]),
        "content": st.text(min_size=0, max_size=100)
    })

def node_strategy():
    return st.fixed_dictionaries({
        "data": st.fixed_dictionaries({
            "messages": st.lists(message_strategy(), min_size=0, max_size=5)
        })
    })

def chain_strategy():
    return st.lists(node_strategy(), min_size=0, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(chain=chain_strategy())
@example(chain=[])
@example(chain=[{"data": {"messages": []}}])
@example(chain=[{"data": {"messages": [{"role": "user", "content": "Hello"}]}}])
@example(chain=[{"data": {"messages": [{"role": "assistant", "content": "Hi"}]}}])
@example(chain=[{"data": {"messages": [{"role": "user", "content": '{"tool_use": {"name": "tool1"}}'}]}}])
@example(chain=[{"data": {"messages": [{"role": "assistant", "content": '{"tool_use": {"name": "tool2"}}'}]}}])
@example(chain=[{"data": {"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]}}])
def test_get_chain_summary(chain: List[Dict]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    chain_copy = copy.deepcopy(chain)

    # Call func0 to verify input validity
    try:
        expected = get_chain_summary(chain_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "chain": chain_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)