from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import re
import os
import atexit
import copy
from typing import Tuple

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _parse_tool_call(action: str) -> Tuple[str, bool]:
    try:
        # Extract tool call content
        tool_match = re.search(r'<tool_call>(.*?)</tool_call>', action, re.DOTALL)
        if not tool_match:
            return action, False

        tool_content = tool_match.group(1).strip()

        # Parse tool name and parameters
        tool_name = None
        params = {}

        lines = tool_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.lower().startswith('tool:'):
                tool_name = line.split(':', 1)[1].strip()
            elif line.lower().startswith('parameters:'):
                try:
                    params_str = line.split(':', 1)[1].strip()
                    # Try to parse as JSON
                    params = json.loads(params_str)
                except (json.JSONDecodeError, IndexError):
                    # Fallback to treating the whole thing as a query
                    params = {'query': params_str}
            elif ':' in line and not tool_name:
                # Handle simple key:value format
                key, value = line.split(':', 1)
                params[key.strip()] = value.strip()

        if not tool_name:
            return action, False

        # Format as structured action
        formatted_action = json.dumps({
            'type': 'tool_call',
            'tool': tool_name,
            'parameters': params,
            'original': action
        })

        return formatted_action, True

    except Exception:
        return action, False

# Strategy for generating action text
def action_strategy():
    # Generate tool names
    tool_name = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'),
        min_size=1, max_size=10
    )
    
    # Generate parameters as JSON or simple key:value pairs
    params = st.one_of(
        st.dictionaries(
            keys=st.text(
                alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'),
                min_size=1, max_size=10
            ),
            values=st.one_of(
                st.text(
                    alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'),
                    min_size=1, max_size=10
                ),
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False)
            ),
            min_size=0, max_size=3
        ),
        st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_-'),
            min_size=1, max_size=10
        ).map(lambda x: {'query': x})
    )
    
    # Generate tool call content
    tool_content = st.builds(
        lambda tool, params: f"tool: {tool}\nparameters: {json.dumps(params)}",
        tool_name, params
    )
    
    # Generate action text with or without tool call
    return st.one_of(
        st.builds(
            lambda content: f"<tool_call>{content}</tool_call>",
            tool_content
        ),
        st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
            min_size=0, max_size=20
        )
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(action=action_strategy())
@example(action="<tool_call>tool: search\nparameters: {'query': 'hypothesis'}</tool_call>")
@example(action="<tool_call>tool: search\nparameters: query: hypothesis</tool_call>")
@example(action="<tool_call>tool: search\nquery: hypothesis</tool_call>")
@example(action="<tool_call>tool: search\nparameters: invalid json</tool_call>")
@example(action="<tool_call>tool: search\nparameters: {'query': 'hypothesis'}</tool_call> extra text")
@example(action="no tool call here")
def test_parse_tool_call(action: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    action_copy = copy.deepcopy(action)

    # Call func0 to verify input validity
    try:
        expected_action, expected_valid = _parse_tool_call(action_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "action": action_copy
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