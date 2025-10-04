from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import ast
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
def parse_tool_result(result):
    """Parse the tool result from agent.tool calls that may return serialized data."""
    if result.get('status') != 'success':
        return result

    try:
        text = result['content'][0]['text']
        # Try JSON parsing first
        try:
            actual_result = json.loads(text)
            return actual_result
        except json.JSONDecodeError:
            # Try evaluating as Python literal (safe eval for dict/list/etc)
            actual_result = ast.literal_eval(text)
            return actual_result
    except (KeyError, IndexError, ValueError, SyntaxError):
        return result

# Strategies for generating inputs
def result_strategy():
    # Generate a dictionary with 'status', 'content', and other optional fields
    return st.fixed_dictionaries({
        'status': st.sampled_from(['success', 'failure', 'error']),
        'content': st.lists(
            st.fixed_dictionaries({
                'text': st.one_of(
                    st.text(),  # Random text
                    st.from_regex(r'\{.*\}'),  # JSON-like text
                    st.from_regex(r'\[.*\]')  # List-like text
                )
            }),
            min_size=1, max_size=2
        ),
        'toolUseId': st.one_of(st.none(), st.text())
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(result=result_strategy())
@example(result={'status': 'success', 'content': [{'text': '{"key": "value"}'}]})
@example(result={'status': 'success', 'content': [{'text': '[1, 2, 3]'}]})
@example(result={'status': 'success', 'content': [{'text': 'invalid_json'}]})
@example(result={'status': 'failure', 'content': [{'text': '{"key": "value"}'}]})
@example(result={'status': 'success', 'content': []})
@example(result={'status': 'success', 'content': [{'text': '{"key": "value"}'}, {'json': '{"key": "value"}'}]})
def test_parse_tool_result(result):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    result_copy = copy.deepcopy(result)

    # Call func0 to verify input validity
    try:
        expected = parse_tool_result(result_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "result": result_copy
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