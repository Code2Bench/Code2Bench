from typing import Optional, Tuple

def parse_provider_and_model(model_str: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    if model_str is None or not model_str:
        return (None, None)
    
    # Split the model string by '/' to get provider and model name
    parts = model_str.split('/')
    if len(parts) < 2:
        return (None, model_str)
    
    provider = parts[0].lower()
    model_name = parts[1].rstrip('/').lower()
    
    return (provider, model_name)