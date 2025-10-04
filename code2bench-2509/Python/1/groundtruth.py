from typing import Dict, List

def collect_all_selected_models(llm_configs: List[Dict]) -> List[str]:
    """Collect all models from all configured providers, remove duplicates and maintain order."""
    seen = set()
    ordered_models: List[str] = []
    for conf in llm_configs or []:
        models_str = (conf.get("models") or "").strip()
        if not models_str:
            continue
        for m in models_str.split(","):
            model = m.strip()
            if model and model not in seen:
                seen.add(model)
                ordered_models.append(model)
    return ordered_models