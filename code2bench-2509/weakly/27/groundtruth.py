from typing import Dict, Optional
import inspect

def get_docstring_description_input(func) -> Dict[str, Optional[str]]:
    """Extract parameter descriptions from function docstring.

    Parses the function's docstring to extract descriptions for each parameter.
    Looks for lines that start with parameter names followed by descriptions.

    Args:
        func: The function to extract parameter descriptions from.

    Returns:
        Dictionary mapping parameter names to their descriptions.
        Parameters without descriptions are omitted.

    Example:
        For a function with docstring containing "param1: Description of param1",
        returns {"param1": "Description of param1"}.
    """
    doc = func.__doc__
    if not doc:
        return {}
    descriptions = {}
    for line in map(str.strip, doc.splitlines()):
        for param in inspect.signature(func).parameters:
            if param == "self":
                continue
            if line.startswith(param):
                descriptions[param] = line.split(param, 1)[1].strip()
    return descriptions