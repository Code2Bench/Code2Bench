from typing import Dict, Any, List, Optional, Tuple

def separate_lora_AB(parameters: Dict[str, Any], B_patterns: Optional[List[str]] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    # Default B patterns if not provided
    if B_patterns is None:
        B_patterns = ['.lora_B.', '__zero__']
    
    # Create two dictionaries to hold the parameters
    normal_params = {}
    b_params = {}
    
    # Iterate through the parameters dictionary
    for key, value in parameters.items():
        # Check if the key matches any of the B patterns
        if any(pattern in key for pattern in B_patterns):
            b_params[key] = value
        else:
            normal_params[key] = value
    
    return normal_params, b_params