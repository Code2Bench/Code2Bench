
from collections import defaultdict
import re

import re
from collections import defaultdict

def sort_checkpoints(models):
    def get_checkpoint_num(model_name):
        if 'checkpoint-final' in model_name:
            return float('inf')
        # Check for checkpoint pattern
        checkpoint_match = re.search(r'checkpoint-(\d+)', model_name)
        if checkpoint_match:
            return int(checkpoint_match.group(1))
        # Check for global_step pattern
        global_step_match = re.search(r'global_step[_]?(\d+)', model_name)
        if global_step_match:
            return int(global_step_match.group(1))
        return float('inf')

    # Group models by base name (everything before checkpoint- or global_step)
    model_groups = defaultdict(list)
    for model in models:
        # Split on either checkpoint- or global_step
        base_name = re.split(r'(?:checkpoint-|global_step)', model)[0].rstrip('-')
        model_groups[base_name].append(model)

    # Sort each group's checkpoints
    sorted_models = []
    for base_name, checkpoints in model_groups.items():
        sorted_checkpoints = sorted(checkpoints, key=get_checkpoint_num)
        sorted_models.extend(sorted_checkpoints)

    return sorted_models