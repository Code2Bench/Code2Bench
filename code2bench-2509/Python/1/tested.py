from typing import List, Dict

def collect_all_selected_models(llm_configs: List[Dict]) -> List[str]:
    selected_models = []
    for config in llm_configs:
        if 'models' in config and config['models']:
            models = config['models'].split(',')
            for model in models:
                model = model.strip()
                if model:
                    if model not in selected_models:
                        selected_models.append(model)
    return selected_models