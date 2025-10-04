from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import re
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
def parse_mobile_response(response):
    pattern = r"Memory:(.*?)Reason:(.*?)Action:(.*)"
    match = re.search(pattern, response, re.DOTALL)
    if not match:
        return None

    memory = match.group(1).strip()
    reason = match.group(2).strip()
    action = match.group(3).strip()

    if "<|begin_of_box|>" in action:
        action = action[
            action.index("<|begin_of_box|>") + len("<|begin_of_box|>") : action.rindex(
                "<|end_of_box|>"
            )
        ]

    parsed_action = None
    if action.startswith("{"):
        parsed_action = json.loads(action)

    return {
        "memory": memory,
        "reason": reason,
        "action": action,
        "parsed_action": parsed_action,
    }

# Strategy for generating response strings
def response_strategy():
    # Generate memory, reason, and action components
    memory = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    reason = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    
    # Generate action with optional JSON content
    action_json = st.recursive(
        st.dictionaries(
            keys=st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
            values=st.one_of(
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.booleans()
            ),
            min_size=1, max_size=3
        ),
        lambda children: st.lists(children, min_size=1, max_size=3),
        max_leaves=5
    ).map(lambda x: json.dumps(x))
    
    action_text = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    action = st.one_of(
        action_json,
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50),
        st.builds(
            lambda x: f"<|begin_of_box|>{x}<|end_of_box|>",
            st.one_of(action_json, action_text)
        )
    )
    
    # Combine into response string
    return st.builds(
        lambda m, r, a: f"Memory:{m}Reason:{r}Action:{a}",
        memory, reason, action
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(response=response_strategy())
@example(response="Memory:test_memory Reason:test_reason Action:test_action")
@example(response="Memory:test_memory Reason:test_reason Action:<|begin_of_box|>test_action<|end_of_box|>")
@example(response="Memory:test_memory Reason:test_reason Action:{\"key\": \"value\"}")
@example(response="Memory:test_memory Reason:test_reason Action:<|begin_of_box|>{\"key\": \"value\"}<|end_of_box|>")
@example(response="InvalidResponse")
def test_parse_mobile_response(response: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    response_copy = copy.deepcopy(response)

    # Call func0 to verify input validity
    try:
        result = parse_mobile_response(response_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "response": response_copy
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