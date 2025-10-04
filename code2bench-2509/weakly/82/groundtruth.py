from typing import Tuple
import json
import re

def _parse_tool_call(action: str) -> Tuple[str, bool]:
    """
    Parse tool call from action text.

    Returns:
        Tuple of (parsed_action, is_valid)
    """
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