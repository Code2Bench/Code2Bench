from typing import Dict, Any, List

def _build_command_line_options(test_options: Dict[str, Any]) -> List[str]:
    result = []
    
    for key, value in test_options.items():
        if isinstance(value, bool):
            if value:
                result.append(f"--{key}")
            else:
                result.append(f"--no-{key}")
        elif isinstance(value, list):
            for item in value:
                result.append(f"--{key} {item}")
        else:
            result.append(f"--{key} {value}")
    
    return result