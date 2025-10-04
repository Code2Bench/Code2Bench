from typing import Dict, Any

def format_improvement_safe(parent_metrics: Dict[str, Any], child_metrics: Dict[str, Any]) -> str:
    result = []
    if not parent_metrics or not child_metrics:
        return ""
    
    for metric in parent_metrics:
        if metric in child_metrics:
            parent_value = parent_metrics[metric]
            child_value = child_metrics[metric]
            
            if isinstance(parent_value, (int, float)) and isinstance(child_value, (int, float)):
                diff = child_value - parent_value
                if diff > 0:
                    result.append(f"{metric}=+{diff:.4f}")
                elif diff < 0:
                    result.append(f"{metric}=-{abs(diff):.4f}")
    
    return ",".join(result) if result else ""