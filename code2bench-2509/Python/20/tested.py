from typing import List, Dict, Optional

def compute_method_ranks(
    data: List[Dict],
    selected_models: Optional[List[str]] = None,
    selected_data: Optional[List[str]] = None
) -> Dict[str, Dict[str, int]]:
    # Filter data to include only the relevant metrics
    if selected_data is None:
        selected_data = [metric for metric in data[0].keys() if metric.endswith('_acc') and not metric == 'avg_acc']
    
    # Initialize result dictionary
    result = {}
    
    # Process each metric
    for metric in selected_data:
        metric_dict = {}
        # Process each model
        for model in data:
            model_name = model['model']
            if selected_models and model_name not in selected_models:
                continue
            # Check if the metric exists in the model's data
            if metric in model:
                accuracy = model[metric]
                # Determine rank
                rank = 1
                # Handle ties by keeping the last seen rank
                if metric_dict:
                    last_rank = metric_dict[accuracy]
                    if accuracy == last_rank:
                        rank = last_rank
                    else:
                        rank = last_rank + 1
                metric_dict[accuracy] = rank
        # Add metric to result
        result[metric] = metric_dict
    
    return result