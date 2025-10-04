from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy
from typing import Dict, List

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def parse_worldmodeling(response: str, special_token_list=None, action_sep=',', max_actions=3) -> Dict:
    response = response.replace("<image>", "")
    # Pattern to check for content strictly in the expected format
    strict_pattern = r'^\s*<think>\s*<reasoning>(.*?)</reasoning>\s*<prediction>(.*?)</prediction>\s*</think>\s*<answer>(.*?)</answer>\s*$'
    strict_match = re.match(strict_pattern, response.strip(), re.DOTALL)
    format_correct = strict_match is not None

    # Pattern to extract content from tags
    extraction_pattern = r'<think>\s*<reasoning>(.*?)</reasoning>\s*<prediction>(.*?)</prediction>\s*</think>\s*<answer>(.*?)</answer>'
    match = re.search(extraction_pattern, response, re.DOTALL)

    if not match:
        reasoning_content, prediction_content, action_content, actions = "", "", "", []
        think_content = ""
    else:
        reasoning_content = match.group(1)
        prediction_content = match.group(2)
        action_content = match.group(3)
        think_content = "<reasoning>" + reasoning_content + "</reasoning><prediction>" + prediction_content + "</prediction>"

        if special_token_list is not None:
            for special_token in special_token_list:
                reasoning_content = reasoning_content.replace(special_token, "").strip()
                prediction_content = prediction_content.replace(special_token, "").strip()
                action_content = action_content.replace(special_token, "").strip()
                think_content = think_content.replace(special_token, "").strip()

        actions = [action.strip() for action in action_content.split(action_sep) if action.strip()]
        if len(actions) > max_actions:
            actions = actions[:max_actions]
            action_content = (" " + action_sep + " ").join(actions)

    # Reconstruct the cleaned llm_response
    llm_response = "<think>" + think_content.strip() + "</think>" + "<answer>" + action_content.strip() + "</answer>"

    return {
        "llm_raw_response": response,
        "llm_response": llm_response,
        "think_content": think_content,
        "reasoning_content": reasoning_content,
        "prediction_content": prediction_content,
        "action_content": action_content,
        "actions": actions,
        "format_correct": format_correct
    }

# Strategies for generating inputs
def response_strategy():
    # Generate valid content for each tag
    reasoning_content = st.text(min_size=0, max_size=100)
    prediction_content = st.text(min_size=0, max_size=100)
    action_content = st.text(min_size=0, max_size=100)
    
    # Combine into a valid response format
    return st.builds(
        lambda r, p, a: f"<think><reasoning>{r}</reasoning><prediction>{p}</prediction></think><answer>{a}</answer>",
        reasoning_content, prediction_content, action_content
    )

def special_token_list_strategy():
    return st.lists(st.text(min_size=1, max_size=5), min_size=0, max_size=3)

def action_sep_strategy():
    return st.sampled_from([',', ';', '|'])

def max_actions_strategy():
    return st.integers(min_value=1, max_value=5)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    response=response_strategy(),
    special_token_list=special_token_list_strategy(),
    action_sep=action_sep_strategy(),
    max_actions=max_actions_strategy()
)
@example(
    response="<think><reasoning>Test reasoning</reasoning><prediction>Test prediction</prediction></think><answer>Test answer</answer>",
    special_token_list=None,
    action_sep=',',
    max_actions=3
)
@example(
    response="<think><reasoning></reasoning><prediction></prediction></think><answer></answer>",
    special_token_list=[],
    action_sep=';',
    max_actions=1
)
@example(
    response="<think><reasoning>Reasoning with special token</reasoning><prediction>Prediction with special token</prediction></think><answer>Action1, Action2</answer>",
    special_token_list=["special_token"],
    action_sep=',',
    max_actions=2
)
def test_parse_worldmodeling(response: str, special_token_list, action_sep, max_actions):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    response_copy = copy.deepcopy(response)
    special_token_list_copy = copy.deepcopy(special_token_list)
    action_sep_copy = copy.deepcopy(action_sep)
    max_actions_copy = copy.deepcopy(max_actions)

    # Call func0 to verify input validity
    try:
        result = parse_worldmodeling(response_copy, special_token_list_copy, action_sep_copy, max_actions_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "response": response_copy,
            "special_token_list": special_token_list_copy,
            "action_sep": action_sep_copy,
            "max_actions": max_actions_copy
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