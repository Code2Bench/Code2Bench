from typing import Dict, Optional
import inspect

def get_docstring_description_input(func) -> Dict[str, Optional[str]]:
    docstring = inspect.getdoc(func)
    if not docstring:
        return {}
    
    param_descriptions = {}
    lines = docstring.splitlines()
    in_param_section = False
    
    for line in lines:
        if line.strip().startswith("Args:"):
            in_param_section = True
            continue
        if not in_param_section:
            continue
        if line.strip().startswith("Returns:"):
            break
        if line.strip().startswith("param") or line.strip().startswith("Param"):
            parts = line.split(":")
            if len(parts) < 2:
                continue
            param_name = parts[0].strip().split()[1]
            description = ":".join(parts[1:]).strip()
            param_descriptions[param_name] = description
    
    return param_descriptions