
import json
import ast

def parse_tool_result(result):
    """Parse the tool result from agent.tool calls that may return serialized data.

    Agent calls return: {'toolUseId': ..., 'status': 'success', 'content': [{'text': '...'}]}
    Some tools may serialize complex data in the content[0]['text'] field.

    - Text message in content[0]['text']
    - Structured data in content[1]['json']

    This helper is kept for backward compatibility with other tools that may still
    serialize their results, but should not be needed for properly implemented tools.

    Example:
    - mcp_client calls: Use results directly (no parsing needed)
    - Other tools that serialize: May still need parse_tool_result()
    - Loaded MCP tools: Use results directly (no parsing needed)
    """
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