from typing import Dict, Any

def display_desc_to_display_path(display_desc: Dict[str, Any]) -> str:
    path = display_desc.get('path')
    display = display_desc.get('display')
    options_str = display_desc.get('options_str')

    uri_parts = []
    if path:
        uri_parts.append(path)
    
    if path and display:
        uri_parts.append('#' + display.strip(':'))
    
    if options_str:
        uri_parts.append('?{}'.format(options_str))
    
    return ''.join(uri_parts) if uri_parts else ''