from typing import Dict, List

def functionParams(args: Dict[str, str], vars: List[str]) -> Dict[str, str]:
    result = {}
    for i, var in enumerate(vars):
        # Try to get value using variable name
        value = args.get(var)
        if value:
            result[var] = value
        else:
            # Fall back to positional index (starting from 1)
            value = args.get(str(i + 1))
            if value:
                result[var] = value
            else:
                result[var] = ""
    return result