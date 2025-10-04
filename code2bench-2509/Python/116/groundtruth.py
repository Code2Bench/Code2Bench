

def format_chat_prompt(messages):
    """
    Format multi-turn conversation into prompt string, suitable for chat models.
    Uses Qwen2 style with <|im_start|> / <|im_end|> tokens.
    """
    prompt = ""
    for msg in messages:
        role, content = msg["role"], msg["content"]
        if role == "user":
            prompt += f"<|im_start|>user\n{content}<|im_end|>\n"
        elif role == "assistant":
            prompt += f"<|im_start|>assistant\n{content}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"
    return prompt