from typing import Tuple, Dict

def _parse_content_type_header(header: str) -> Tuple[str, Dict[str, str]]:
    # Split the header into parts
    parts = header.split(';')
    
    # The main content type is the first part
    content_type = parts[0].strip()
    
    # The parameters are the remaining parts
    parameters = {}
    for part in parts[1:]:
        # Remove any whitespace and quotes
        cleaned_part = part.strip().strip('\"\'')
        
        # Split the parameter name and value
        if cleaned_part:
            name, value = cleaned_part.split('=', 1)
            parameters[name.lower()] = value.strip()
    
    return content_type, parameters