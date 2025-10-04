
import re
import json

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