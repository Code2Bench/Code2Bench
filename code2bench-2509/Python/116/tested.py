from typing import List, Dict

def format_chat_prompt(messages: List[Dict[str, str]]) -> str:
    prompt = ""
    for message in messages:
        role = message["role"]
        content = message["content"]
        prompt += f"{role}\n{content}\n"
    return prompt + "assistant\n"