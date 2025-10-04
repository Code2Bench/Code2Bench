import re
import json

def parse_tool_calls(content: str) -> list:
    tool_calls = []
    # Extract JSON-like objects using regex, handling both English and Chinese brackets
    matches = re.finditer(r'({.*?})', content, re.DOTALL)
    for match in matches:
        json_str = match.group(1)
        # Replace Chinese brackets with English ones
        json_str = json_str.replace('【', '{').replace('】', '}')
        # Remove trailing commas
        json_str = re.sub(r',\s*$', '', json_str)
        try:
            data = json.loads(json_str)
            if 'tool_type' in data:
                if data['tool_type'] == 'MCP':
                    tool_call = {
                        'tool_name': data.get('tool_name', ''),
                        'service_name': data.get('service_name', '')
                    }
                elif data['tool_type'] == 'Agent':
                    tool_call = {
                        'agentType': data.get('agentType', ''),
                        'agent_name': data.get('agent_name', ''),
                        'prompt': data.get('prompt', '')
                    }
                tool_calls.append(tool_call)
        except json.JSONDecodeError:
            continue
    return tool_calls