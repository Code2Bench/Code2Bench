from typing import List, Dict

def group_metrics_with_subprefixes(metrics: List[str]) -> Dict:
    grouped = {}
    grouped["charts"] = {
        "direct_metrics": [],
        "subgroups": {}
    }
    
    for metric in metrics:
        if '/' in metric:
            prefix, submetric = metric.split('/', 1)
            if prefix not in grouped:
                grouped[prefix] = {
                    "direct_metrics": [],
                    "subgroups": {}
                }
            
            # Add the submetric to the subgroups of the prefix
            if submetric not in grouped[prefix]["subgroups"]:
                grouped[prefix]["subgroups"][submetric] = []
            grouped[prefix]["subgroups"][submetric].append(metric)
            
            # Add the direct metric to the current level
            grouped["charts"]["direct_metrics"].append(metric)
        else:
            # Direct metric under "charts"
            grouped["charts"]["direct_metrics"].append(metric)
    
    # Remove "charts" if it has no direct metrics
    if not grouped["charts"]["direct_metrics"]:
        del grouped["charts"]
    
    # Sort the direct metrics and subgroups alphabetically
    for group in grouped.values():
        group["direct_metrics"].sort()
        group["subgroups"].values().sort()
    
    return grouped