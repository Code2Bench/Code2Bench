from typing import Dict, Any

def _format_product_context_md(data: Dict[str, Any]) -> str:
    result = "# Product Context\n\n"
    
    for key, value in data.items():
        # Convert key to title case with underscores replaced by spaces
        key_title = key.replace("_", " ").title()
        
        # Handle different value types
        if isinstance(value, str):
            result += f"## {key_title}\n{value}\n\n"
        elif isinstance(value, list):
            result += f"## {key_title}\n*   {value}\n\n"
        else:
            result += f"## {key_title}\n{value}\n\n"
    
    return result