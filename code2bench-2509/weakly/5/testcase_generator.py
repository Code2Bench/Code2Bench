from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import re
import os
import atexit
import copy
from typing import Any, Dict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def parse_llm_response(response: str) -> Dict[str, Any]:
    """Parse LLM response and extract trading decisions"""
    try:
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM response: {e}")
        print(f"Raw response: {response}")
        return {"error": "Failed to parse response", "raw_response": response}

# Strategy for generating LLM responses
def response_strategy():
    # Generate valid JSON strings
    valid_json = st.recursive(
        st.one_of(
            st.none(),
            st.booleans(),
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(min_size=1, max_size=10)
        ),
        lambda children: st.lists(children, min_size=1, max_size=3) | st.dictionaries(st.text(min_size=1, max_size=5), children, min_size=1, max_size=3),
        max_leaves=5
    ).map(lambda x: json.dumps(x))
    
    # Generate invalid JSON strings
    invalid_json = st.text(min_size=1, max_size=50).filter(lambda x: not is_valid_json(x))
    
    # Mix valid and invalid JSON strings with surrounding text
    return st.one_of(
        valid_json,
        invalid_json,
        st.tuples(st.text(min_size=0, max_size=20), valid_json, st.text(min_size=0, max_size=20)).map(lambda x: ''.join(x)),
        st.tuples(st.text(min_size=0, max_size=20), invalid_json, st.text(min_size=0, max_size=20)).map(lambda x: ''.join(x))
    )

def is_valid_json(s: str) -> bool:
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(response=response_strategy())
@example(response="")
@example(response="{}")
@example(response='{"key": "value"}')
@example(response="Invalid JSON")
@example(response="Some text before {\"key\": \"value\"} some text after")
@example(response="{\"key\": \"value\"} some text after")
@example(response="Some text before {\"key\": \"value\"}")
def test_parse_llm_response(response: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    response_copy = copy.deepcopy(response)

    # Call func0 to verify input validity
    try:
        expected = parse_llm_response(response_copy)
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