import json
import copy
from typing import Dict
from helper import deep_compare, load_test_cases_from_json
from tested import parse_worldmodeling as func1
import re

# Ground truth function (func0), keep its original implementation and name
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

# Compare outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Diagnostic runner function
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])

            try:
                expected_output = parse_worldmodeling(**inputs)
                actual_output = func1(**inputs)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": expected_output,
                        "actual": actual_output
                    })
            except Exception as e:
                failed_count += 1
                failures.append({
                    "case_id": i+1,
                    "type": "ExecutionError",
                    "inputs": inputs,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })

    except Exception as e:
        execution_error = {
            "type": "CriticalExecutionError",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }

    summary = {
        "passed": passed_count,
        "failed": failed_count,
        "total": len(test_cases),
        "failures": failures[:10],
        "execution_error": execution_error
    }

    print("\n---DIAGNOSTIC_SUMMARY_START---")
    print(json.dumps(summary, indent=2))
    print("---DIAGNOSTIC_SUMMARY_END---")

# Main block
if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    if test_cases:
        run_tests_with_loaded_cases_diagnostic(test_cases)
    else:
        print("No test cases found.")