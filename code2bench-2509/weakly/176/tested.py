from collections import defaultdict
import re

def sort_checkpoints(models: list[str]) -> list[str]:
    grouped = defaultdict(list)
    pattern = re.compile(r'^(.*?)(checkpoint-(\d+)|global_step-(\d+)|checkpoint-final)$')
    
    for model in models:
        match = pattern.match(model)
        if not match:
            grouped[''].append(model)
            continue
        
        base_name, _, _, _ = match.groups()
        if 'checkpoint-final' in model:
            grouped['infinite'].append(model)
        else:
            grouped[base_name].append(model)
    
    sorted_models = []
    for key in sorted(grouped.keys()):
        if key == 'infinite':
            sorted_models.extend(grouped[key])
        else:
            group = grouped[key]
            sorted_group = sorted(group, key=lambda x: (
                0 if 'checkpoint-final' in x else
                int(x.split('checkpoint-')[1]) if 'checkpoint-' in x else
                int(x.split('global_step-')[1])
            ))
            sorted_models.extend(sorted_group)
    
    return sorted_models