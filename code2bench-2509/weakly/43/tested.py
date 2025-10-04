from typing import Dict, List
import re

def get_chain_summary(chain: List[Dict]) -> Dict:
    if not chain:
        return {
            "length": 0,
            "total_messages": 0,
            "user_messages": 0,
            "assistant_messages": 0,
            "tools_used": [],
            "first_message": None,
            "last_message": None
        }
    
    total_messages = 0
    user_messages = 0
    assistant_messages = 0
    tools_used = set()
    first_message = chain[0]["data"]["messages"][0] if chain[0]["data"]["messages"] else None
    last_message = chain[-1]["data"]["messages"][-1] if chain[-1]["data"]["messages"] else None
    
    for node in chain:
        messages = node["data"]["messages"]
        total_messages += len(messages)
        for msg in messages:
            if msg.get("role") == "user":
                user_messages += 1
            elif msg.get("role") == "assistant":
                assistant_messages += 1
            if "tool_call" in msg:
                tool_name = msg["tool_call"].get("name")
                if tool_name:
                    tools_used.add(tool_name)
    
    return {
        "length": len(chain),
        "total_messages": total_messages,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "tools_used": list(tools_used),
        "first_message": first_message,
        "last_message": last_message
    }