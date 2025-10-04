from typing import List

from typing import List

def _format_models(models: List[str]) -> str:
    if not models:
        return "No models"

    if len(models) == 1:
        return models[0]
    elif len(models) <= 3:
        return "\n".join([f"• {model}" for model in models])
    else:
        first_two = models[:2]
        remaining_count = len(models) - 2
        formatted = "\n".join([f"• {model}" for model in first_two])
        formatted += f"\n• ...and {remaining_count} more"
        return formatted