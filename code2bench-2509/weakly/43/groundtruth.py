from typing import Dict, List
from typing import Dict, List, Any
import re

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