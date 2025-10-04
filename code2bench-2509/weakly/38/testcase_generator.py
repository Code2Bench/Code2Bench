from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
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

# Strategy for generating JSON-like content
def json_like_strategy():
    # Generate valid JSON-like strings with potential trailing commas
    key = st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), min_codepoint=32, max_codepoint=126), min_size=1, max_size=10)
    value = st.one_of(
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), min_codepoint=32, max_codepoint=126), min_size=1, max_size=10),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.booleans(),
        st.lists(st.text(alphabet=st.characters(whitelist_categories=('L', 'N'), min_codepoint=32, max_codepoint=126), min_size=1, max_size=10), min_size=1, max_size=3)
    )
    json_obj = st.dictionaries(keys=key, values=value, min_size=1, max_size=5)
    return json_obj.map(lambda x: json.dumps(x, ensure_ascii=False))

# Strategy for generating content with JSON-like blocks
def content_strategy():
    # Generate content with JSON-like blocks wrapped in curly braces
    json_block = json_like_strategy().map(lambda x: "{" + x + "}")
    return st.lists(
        st.one_of(
            json_block,
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), min_codepoint=32, max_codepoint=126), min_size=0, max_size=20)
        ),
        min_size=0, max_size=5
    ).map(lambda x: ' '.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(content=content_strategy())
@example(content="")
@example(content="{}")
@example(content='{"tool_name": "tool1", "service_name": "service1"}')
@example(content='{"agentType": "agent", "agent_name": "agent1", "prompt": "prompt1"}')
@example(content='{"tool_name": "tool1", "service_name": "service1", "extra": "value"}')
@example(content='{"agentType": "agent", "agent_name": "agent1", "prompt": "prompt1", "extra": "value"}')
@example(content='{"tool_name": "tool1"}')
@example(content='{"agentType": "agent", "agent_name": "agent1"}')
@example(content='{"agentType": "agent", "prompt": "prompt1"}')
@example(content='{"tool_name": "tool1", "service_name": "service1"} {"agentType": "agent", "agent_name": "agent1", "prompt": "prompt1"}')
def test_parse_tool_calls(content: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    content_copy = copy.deepcopy(content)

    # Call func0 to verify input validity
    try:
        expected = parse_tool_calls(content_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "content": content_copy
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