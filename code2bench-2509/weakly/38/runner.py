import json
import copy
from helper import deep_compare, load_test_cases_from_json
from tested import parse_tool_calls as func1
import re

# Ground truth function (func0), keep its original implementation and name
def parse_tool_calls(content: str) -> list:
    """解析JSON格式工具调用，支持MCP和Agent两种类型"""
    tool_calls = []
    # 支持中英文括号的正则表达式
    pattern = r'[｛{]([\s\S]*?)[｝}]'
    matches = re.finditer(pattern, content)
    for match in matches:
        try:
            # 将中文括号替换为英文括号
            json_content = "{" + match.group(1).strip() + "}"

            # 处理尾随逗号问题
            # 移除对象末尾的尾随逗号
            json_content = re.sub(r',(\s*[}\]])', r'\1', json_content)

            tool_args = json.loads(json_content)

            agent_type = tool_args.get('agentType', 'mcp').lower()
            if agent_type == 'agent':
                agent_name = tool_args.get('agent_name')
                prompt = tool_args.get('prompt')
                if agent_name and prompt:
                    tool_call = {
                        'name': 'agent_call',
                        'args': {
                            'agentType': 'agent',
                            'agent_name': agent_name,
                            'prompt': prompt
                        }
                    }
                    tool_calls.append(tool_call)
            else:
                tool_name = tool_args.get('tool_name')
                if tool_name:
                    if 'service_name' in tool_args:
                        tool_call = {
                            'name': tool_name,
                            'args': tool_args
                        }
                        tool_calls.append(tool_call)
                    else:
                        service_name = tool_name
                        tool_args['service_name'] = service_name
                        tool_args['agentType'] = 'mcp'
                        tool_call = {
                            'name': tool_name,
                            'args': tool_args
                        }
                        tool_calls.append(tool_call)
        except json.JSONDecodeError:
            continue
    return tool_calls

# Compare outputs
def compare_outputs(expected, actual):
    return deep_compare(expected, actual, tolerance=1e-6)

# Diagnostic runner
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            content = inputs["content"]

            try:
                expected_output = parse_tool_calls(content)
                actual_output = func1(content)

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
        print("No test cases loaded.")
    else:
        run_tests_with_loaded_cases_diagnostic(test_cases)