
import json
import re

def parse_web_response(response):
    pattern = r"Thought:|Action:|Memory_Updated:"
    answer = re.findall(r"<answer>(.*?)</answer>", response, re.DOTALL)
    if not answer:
        return None

    response_split = re.split(pattern, answer[0])
    if len(response_split) < 4:
        return None

    thought = response_split[1].strip()
    action = response_split[2].strip()
    memory_str = response_split[3].strip()

    memory = {}
    if memory_str:
        memory = json.loads(memory_str)

    return {"thought": thought, "action": action, "memory": memory}