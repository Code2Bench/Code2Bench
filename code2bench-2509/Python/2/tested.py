from typing import Union

def format_llm_error_message(model_name: str, error_str: str) -> str:
    return f"Error in {model_name}: {error_str}"