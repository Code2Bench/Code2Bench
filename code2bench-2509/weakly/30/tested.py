import re
import json

def parse_web_response(response: str) -> dict | None:
    pattern = r"<answer>(.*?)</answer>"
    match = re.search(pattern, response, re.DOTALL)
    
    if not match:
        return None
    
    content = match.group(1).strip()
    
    thought_pattern = r"Thought:\s*(.*)"
    action_pattern = r"Action:\s*(.*)"
    memory_pattern = r"Memory_Updated:\s*(.*)"
    
    thought_match = re.search(thought_pattern, content)
    action_match = re.search(action_pattern, content)
    memory_match = re.search(memory_pattern, content)
    
    if not (thought_match and action_match and memory_match):
        return None
    
    thought = thought_match.group(1).strip()
    action = action_match.group(1).strip()
    memory_str = memory_match.group(1).strip()
    
    if memory_str:
        try:
            memory = json.loads(memory_str)
        except json.JSONDecodeError:
            return None
    else:
        memory = {}
    
    return {"thought": thought, "action": action, "memory": memory}