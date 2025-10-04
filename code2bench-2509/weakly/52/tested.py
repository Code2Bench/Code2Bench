from urllib.parse import urlparse

def check_resource_allowed(requested_resource: str, configured_resource: str) -> bool:
    parsed_requested = urlparse(requested_resource)
    parsed_configured = urlparse(configured_resource)
    
    if parsed_requested.scheme != parsed_configured.scheme:
        return False
    
    requested_netloc = parsed_requested.netloc.lower()
    configured_netloc = parsed_configured.netloc.lower()
    
    if requested_netloc != configured_netloc:
        return False
    
    if parsed_requested.port is not None and parsed_configured.port is not None:
        if parsed_requested.port != parsed_configured.port:
            return False
    
    return parsed_requested.path.startswith(parsed_configured.path)