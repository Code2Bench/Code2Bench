import json
import copy
import re
from typing import List, Dict
from helper import deep_compare, load_test_cases_from_json
from tested import get_chain_summary as func1

# Ground truth function (copied from input)
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

# Define ground truth function
ground_truth = get_chain_summary

# Define compare_outputs function
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Define diagnostic runner
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            chain = inputs["chain"]

            try:
                expected_output = ground_truth(chain)
                actual_output = func1(chain)

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
    if not test_cases:
        print("No test cases found.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)