from typing import Optional

def parse_provider_and_model(model_str: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a model string like 'openai/gpt-4', 'text-completion-openai/gpt-3.5-turbo-instruct/', etc.
    Returns (provider, model_name), both lowercased and stripped of trailing slashes.
    """
    if not isinstance(model_str, str) or not model_str:
        return None, None
    model_str = model_str.strip().rstrip("/")
    if "/" in model_str:
        provider, model_name = model_str.split("/", 1)
        provider = provider.strip().lower()
        model_name = model_name.strip()
        # Handle cases like 'text-completion-openai' -> 'openai'
        if "-" in provider:
            provider = provider.split("-")[-1]
        return provider, model_name
    return None, model_str.strip() if model_str else None