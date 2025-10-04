import difflib

def suggest_similar_models(invalid_model: str, available_models: list[str]) -> list[str]:
    if not available_models:
        return []
    matches = difflib.get_close_matches(invalid_model, available_models, n=3, cutoff=0.3)
    return matches