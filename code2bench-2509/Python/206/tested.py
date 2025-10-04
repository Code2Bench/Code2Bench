from typing import List

def _format_models(models: List[str]) -> str:
    if not models:
        return "No models"
    if len(models) == 1:
        return models[0]
    if len(models) <= 3:
        return "\n* " + "\n* ".join(models)
    else:
        return "\n* " + "\n* ".join(models[:2]) + f"\nThere are {len(models) - 2} more models."